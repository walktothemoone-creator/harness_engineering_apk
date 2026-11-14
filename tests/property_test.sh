#!/usr/bin/env bash
# Tries to violate each of the five blockchain properties and checks that chain.py refuses or reports it.
#
# Usage:  bash tests/property_test.sh [en|ko]
# Creates a throwaway project in a temp folder, plants the seed there and runs the checks.
# Touches nothing outside that temp folder. Exit code 0 = all checks passed.
set -u
LANG_CODE="${1:-en}"
SEED="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
P="$WORK/demo_project"
mkdir -p "$P" && cp -R "$SEED" "$P/harness_engineering" && rm -rf "$P/harness_engineering/.git"
cd "$P" || exit 2

pass=0; fail=0
C() { python3 scripts/_shared/chain.py "$@"; }
ok()   { pass=$((pass+1)); echo "  PASS  $1"; }
bad()  { fail=$((fail+1)); echo "  FAIL  $1"; }
# expect <description> <expected exit code> <command...>
expect() { local d="$1" want="$2"; shift 2; "$@" >/dev/null 2>&1; local got=$?; [ "$got" -eq "$want" ] && ok "$d" || bad "$d (exit $got, wanted $want)"; }
finish() { sed -i.bak -E 's/^status: (draft|작성 중)$/status: done/' docs/*/2*.md scripts/2*/MANIFEST.md && rm -f docs/*/*.bak scripts/*/*.bak; }
head_of() { C verify | tail -1 | sed -E 's/.*head ([0-9a-fGENSI]+).*/\1/'; }

python3 harness_engineering/tools/seed.py init --lang "$LANG_CODE" --prefix DEMO --title "Demo" >/dev/null || exit 2

echo "[4 Consistency] empty chain"
expect "verify passes on an empty chain" 0 C verify

C new first "DEMO first task" >/dev/null
echo "[2 Deduplication] new"
expect "new with the same slug is refused" 2 C new first "DEMO another title"
expect "new with the same title is refused" 2 C new other "DEMO first task"

echo "[5 Finality] pre-seal checks"
expect "sealing draft documents is refused" 1 C seal
finish
expect "seal --dry-run passes" 0 C seal --dry-run
grep -q '^hash:$' docs/req/*.md && ok "dry-run wrote nothing" || bad "dry-run wrote a hash"
expect "seal succeeds" 0 C seal
[ -f docs/LEDGER.md ] && ok "seal ledger was created" || bad "no ledger"

echo "[2 Deduplication] seal again"
before="$(cat docs/*/2*.md docs/LEDGER.md scripts/2*/MANIFEST.md | shasum)"
expect "second seal succeeds" 0 C seal
after="$(cat docs/*/2*.md docs/LEDGER.md scripts/2*/MANIFEST.md | shasum)"
[ "$before" = "$after" ] && ok "second seal changed no file (idempotent)" || bad "second seal changed files"

echo "[5 Finality] re-seal"
expect "seal --work (re-seal) is refused" 2 C seal --work x

C new second "DEMO second task" >/dev/null; finish; C seal >/dev/null
H="$(head_of)"

echo "[3 Integrity]"
last="$(ls docs/history/*second_task.md)"
mv "$last" "$WORK/gone.md"
expect "deleting the last document is detected" 1 C verify
mv "$WORK/gone.md" "$last"
expect "chain is OK again after restoring it" 0 C verify

f="$(ls docs/plan/*first_task.md)"; cp "$f" "$WORK/keep"
echo "tampered" >> "$f"
expect "tampering with a sealed document is detected" 1 C verify
cp "$WORK/keep" "$f"

echo "print('x')" >> "$(ls -d scripts/*_first)/extra.py"
expect "adding code to a sealed work folder is detected" 1 C verify
rm "$(ls -d scripts/*_first)/extra.py"

echo "# memo" > docs/history/memo.md
expect "a stray file in a document folder is detected" 1 C verify
rm docs/history/memo.md

cp docs/LEDGER.md "$WORK/ledger"
sed -i.bak 's/| 3 | TASK/| 3 | TASX/' docs/LEDGER.md && rm -f docs/LEDGER.md.bak
expect "editing the ledger is detected" 1 C verify
cp "$WORK/ledger" docs/LEDGER.md
expect "chain is OK again" 0 C verify

echo "[5 Finality] broken chain / insertion"
C new third "DEMO third task" >/dev/null; finish
echo "tampered" >> "$f"
expect "nothing is sealed on top of a broken chain" 1 C seal
cp "$WORK/keep" "$f"
expect "seal succeeds once the chain is intact" 0 C seal
g="$(ls docs/logs/*second_task.md)"; cp "$g" "$WORK/keep2"
python3 - "$g" <<'PY'
import re, sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(re.sub(r"^hash:.*$", "hash:", t, count=1, flags=re.M))
PY
expect "re-sealing a document in the middle of the chain is refused" 1 C seal
cp "$WORK/keep2" "$g"

echo "[2 Deduplication] sequence (nonce)"
G="$WORK/gap"; cp -R "$P" "$G"
( cd "$G" && rm -f docs/*/*_001_* && rm -rf scripts/*_001_* )
( cd "$G" && python3 scripts/_shared/chain.py verify >/dev/null 2>&1 ); [ $? -eq 1 ] && ok "a gap in the work sequence is detected" || bad "gap not detected"
expect "the real project is still intact" 0 C verify

echo "[1 Determinism / 4 Consistency] same docs, same head"
# rebuild a clean project deterministically and compare heads between two locations
Q="$WORK/replay"; mkdir -p "$Q" && cp -R "$SEED" "$Q/harness_engineering" && rm -rf "$Q/harness_engineering/.git"
( cd "$Q" && python3 harness_engineering/tools/seed.py init --lang "$LANG_CODE" --prefix DEMO --title "Demo" >/dev/null \
  && python3 scripts/_shared/chain.py new first "DEMO first task" >/dev/null \
  && sed -i.bak -E 's/^status: (draft|작성 중)$/status: done/' docs/*/2*.md scripts/2*/MANIFEST.md && rm -f docs/*/*.bak scripts/*/*.bak \
  && python3 scripts/_shared/chain.py seal >/dev/null )
R="$WORK/replay_copy"; cp -R "$Q" "$R"
h1="$(cd "$Q" && python3 scripts/_shared/chain.py verify | tail -1)"
h2="$(cd "$R" && python3 scripts/_shared/chain.py verify | tail -1)"
[ -n "$h1" ] && [ "$h1" = "$h2" ] && ok "a copy in another location yields the same head" || bad "heads differ: '$h1' vs '$h2'"
( cd "$R" && mv docs/req/*first_task.md docs/req/renamed.md )
h3="$(cd "$R" && python3 scripts/_shared/chain.py verify | tail -1)"
[ "$h1" = "$h3" ] && ok "renaming a file does not change the head (hash depends on content only)" || bad "rename changed the result"

echo
echo "passed $pass, failed $fail   (lang: $LANG_CODE, head line: $h1)"
rm -rf "$WORK"
[ "$fail" -eq 0 ]
