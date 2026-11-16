#!/usr/bin/env python3
"""Document/code chain tool — links REQ → PLAN → INS → TASK(scripts) → LOG → HISTORY with hashes.

Usage (from the project root; shared tool planted by the harness_engineering seed — outside the chain):
  python3 scripts/_shared/chain.py new <slug> "<title>"    create the six documents of a new work item
  python3 scripts/_shared/chain.py seal --dry-run          show what sealing would finalize + pre-seal checks
  python3 scripts/_shared/chain.py seal                    seal unsealed documents in order (final — cannot be undone)
  python3 scripts/_shared/chain.py verify                  recompute everything from GENESIS (exit code 1 on mismatch)
  python3 scripts/_shared/chain.py status                  documents per work item
  python3 scripts/_shared/chain.py list <history|logs|…>   list documents of one kind in work order

Document system (details: docs/README.md)
  docs/req/          REQ      what is wanted
  docs/plan/         PLAN     how it will be done
  docs/instruction/  INS      what exactly is executed
  scripts/{work}/    TASK     MANIFEST.md + the code in that folder (tree_hash)
  docs/logs/         LOG      how the code's concept and logic started and changed
  docs/history/      HISTORY  what was achieved and what remains (flat, in work order)
  docs/LEDGER.md     seal ledger — id and hash of every sealed document, in order (written by this tool)

Like a blockchain — the five properties this tool enforces
  1. Determinism     hash depends only on document content, tree_hash only on file contents.
  2. Deduplication   the work sequence number is the nonce: contiguous from 0, no gaps, no duplicates.
                     `new` refuses a second unsealed work item with the same title or slug.
                     `seal` never touches sealed documents, so running it again changes nothing.
  3. Integrity       changed content breaks the hash, a deleted document shows up against the ledger,
                     a stray file in a document folder is reported.
  4. Consistency     `verify` trusts no stored value: it replays from GENESIS and prints the head
                     (hash of the last document). Anyone with the same docs/ gets the same head.
  5. Finality        sealing is final. There is no re-seal. The ledger is append-only.
                     Corrections are made by adding a new work item.

Rules
- work id = {yyyymmdd}_{3-digit seq}. Document file name = {work id}_{title}.md, so name order = work order.
- prev_hash in a document's front matter = hash of the document right before it. A work item's REQ follows
  the previous work item's HISTORY (the very first one follows GENESIS).
- hash = SHA-256 of the whole document except its own `hash:` line.
- The chain is linked by front matter (work, type) and content hashes, never by file names or paths.
- Backward compatibility: a document with `type: brief` is read as history. LOG is mandatory only from
  the first work item that has one.
- Outside the chain (free to edit): README.md, SKILL.md, docs/README.md, docs/_templates/.
  docs/LEDGER.md is written by this tool only.
"""
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

LANG = "ko"  # "en" or "ko" — set by harness_engineering/tools/seed.py init --lang

ROOT = Path(__file__).resolve().parent.parent.parent
ORDER = ["req", "plan", "instruction", "task", "log", "history"]
ALIAS = {"brief": "history"}
DIRS = {"req": "req", "plan": "plan", "instruction": "instruction", "log": "logs", "history": "history"}
PREFIX = {"req": "REQ", "plan": "PLAN", "instruction": "INS", "task": "TASK", "log": "LOG", "history": "HIST"}
SKIP = {"__pycache__", ".DS_Store", "MANIFEST.md"}
TEMPLATES = ROOT / "docs" / "_templates"
LEDGER = ROOT / "docs" / "LEDGER.md"
DRAFTS = {"draft", "작성 중"}

TEXT = {
    "en": {
        "labels": {"req": "Requirements", "plan": "Plan", "instruction": "Instructions",
                   "task": "Deliverables", "log": "Code Change Log", "history": "Work History"},
        "draft": "draft",
        "sealed": "sealed", "written": "written", "missing": "missing",
        "created": "created", "seal": "sealed ", "to_seal": "to seal",
        "ok": "chain OK — {n} documents, head {head}",
        "problems": "{n} problem(s)",
        "e_unsealed": "not sealed",
        "e_changed": "content changed after sealing",
        "e_link": "does not link to the previous document ({prev})",
        "e_tree": "code in the folder changed after sealing",
        "e_missing": "{w}: missing documents {x}",
        "e_dup_kind": "{w}: more than one document of the same kind {x}",
        "e_seq_shared": "sequence {s} is used by several work items {x} — two branches created the same number. One harness folder takes one writer at a time; see TEAM.md in the seed",
        "e_seq_gap": "work sequence is not contiguous from 0 {x}",
        "e_dup_id": "more than one document with id {x}",
        "e_order": "work dates and sequence numbers are out of order",
        "e_stray": "{f}: file outside the chain in a document folder (no work/type in front matter)",
        "e_no_ledger": "docs/LEDGER.md is missing although sealed documents exist",
        "e_ledger_gone": "ledger (docs/LEDGER.md) and documents differ — in the ledger only (deleted): {x}",
        "e_ledger_diff": "ledger (docs/LEDGER.md) and documents differ — order or hash mismatch",
        "s_broken": "the sealed part has problems; nothing is sealed on top of it. Run `chain.py verify` first",
        "s_none": "nothing to seal (everything is already sealed)",
        "s_insert": "{a}: a later document ({b}) is already sealed — cannot insert (a finalized chain does not change)",
        "s_draft": "{id}: status is '{st}' — finish the document, change its status, then seal",
        "s_refused": "not sealed — {n} check(s) failed",
        "s_dry": "checks passed — sealing will finalize {n} document(s) (cannot be undone)",
        "s_ledger_past": "the ledger's past rows differ from the documents — the ledger is not rewritten",
        "s_no_reseal": "there is no re-seal. Sealing is final — record corrections as a new work item",
        "n_templates": "document templates are missing: {x}",
        "n_slug": "slug must be lowercase letters, digits and underscores only",
        "n_dup": "an unsealed work item with the same title or slug already exists: {w} ({t}) — continue that one instead of creating a new one",
        "l_kind": "kind must be one of {x}",
        "ledger": ["# LEDGER — seal ledger", "",
                   "Every sealed document in chain order. `chain.py seal` only appends to it. **Do not edit by hand.**",
                   "`chain.py verify` compares this list with the actual documents: a deleted document or a rewritten past shows up here.", ""],
    },
    "ko": {
        "labels": {"req": "요구사항 정의서", "plan": "작업계획서", "instruction": "작업지시서",
                   "task": "작업 결과물 목록", "log": "코드 변경 기록", "history": "작업 기록"},
        "draft": "작성 중",
        "sealed": "봉인", "written": "작성", "missing": "없음",
        "created": "생성", "seal": "봉인 ", "to_seal": "봉인 예정",
        "ok": "체인 정상 — 문서 {n}개, head {head}",
        "problems": "문제 {n}건",
        "e_unsealed": "봉인 안 됨",
        "e_changed": "내용이 봉인 후 바뀜",
        "e_link": "앞 문서({prev})와 연결 불일치",
        "e_tree": "폴더 안 코드가 봉인 후 바뀜",
        "e_missing": "{w}: 빠진 문서 {x}",
        "e_dup_kind": "{w}: 같은 종류 문서가 둘 이상 {x}",
        "e_seq_shared": "순번 {s} 을 여러 작업이 씀 {x} — 두 브랜치가 같은 번호를 만들었다. 하네스 폴더 하나는 한 번에 한 사람이 쓴다 (씨앗의 TEAM.ko.md)",
        "e_seq_gap": "작업 순번이 0부터 이어지지 않음 {x}",
        "e_dup_id": "같은 id 의 문서가 둘 이상 {x}",
        "e_order": "작업 날짜와 순번의 순서가 어긋남",
        "e_stray": "{f}: 문서 폴더에 체인 밖 파일 (머리말에 work·type 없음)",
        "e_no_ledger": "docs/LEDGER.md 없음 — 봉인된 문서가 있는데 원장이 없다",
        "e_ledger_gone": "원장(docs/LEDGER.md)과 문서가 다르다 — 원장에만 있는(지워진) 문서 {x}",
        "e_ledger_diff": "원장(docs/LEDGER.md)과 문서가 다르다 — 순서나 hash 가 다름",
        "s_broken": "이미 봉인된 부분에 문제가 있어 그 위에 봉인하지 않는다. 먼저 `chain.py verify`로 확인",
        "s_none": "봉인할 문서 없음 (이미 모두 봉인됨)",
        "s_insert": "{a}: 뒤 문서({b})가 이미 봉인돼 있어 끼워 넣을 수 없음 (확정된 체인은 바뀌지 않는다)",
        "s_draft": "{id}: status 가 '{st}' — 다 쓴 뒤 status 를 바꾸고 봉인",
        "s_refused": "봉인하지 않음 — 점검 {n}건",
        "s_dry": "점검 통과 — 봉인하면 {n}개 문서가 확정된다 (되돌릴 수 없다)",
        "s_ledger_past": "원장의 과거 기록이 지금 문서와 다르다 — 원장을 고쳐 쓰지 않는다",
        "s_no_reseal": "다시 봉인하는 기능은 없다. 봉인은 확정이다 — 고칠 일은 새 작업으로 남긴다",
        "n_templates": "문서 양식이 없습니다: {x}",
        "n_slug": "slug 는 영문 소문자·숫자·밑줄만",
        "n_dup": "같은 제목·slug 의 미봉인 작업이 이미 있다: {w} ({t}) — 새로 만들지 말고 그 작업을 이어서 쓴다",
        "l_kind": "종류는 {x} 중 하나",
        "ledger": ["# LEDGER — 봉인 원장", "",
                   "봉인된 문서를 체인 순서대로 적은 목록이다. `chain.py seal`이 뒤에 덧붙이기만 한다. **손으로 고치지 않는다.**",
                   "`chain.py verify`는 이 목록과 실제 문서를 대조한다. 문서가 지워지거나 과거 기록이 바뀌면 여기서 드러난다.", ""],
    },
}
T = TEXT.get(LANG, TEXT["en"])


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_meta(p: Path) -> dict:
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---\n"):
        return {}
    meta = {}
    for line in t.split("\n---\n", 1)[0].splitlines()[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def set_meta(p: Path, key: str, val: str) -> None:
    t = p.read_text(encoding="utf-8")
    head, body = t.split("\n---\n", 1)
    if re.search(rf"^{key}:.*$", head, flags=re.M):
        head = re.sub(rf"^{key}:.*$", f"{key}: {val}", head, flags=re.M)
    else:
        head += f"\n{key}: {val}"
    p.write_text(head + "\n---\n" + body, encoding="utf-8")


def doc_hash(p: Path) -> str:
    t = p.read_text(encoding="utf-8")
    return sha(re.sub(r"^hash:.*\n", "", t, count=1, flags=re.M).encode("utf-8"))


def tree_hash(folder: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(x for x in folder.rglob("*") if x.is_file() and not (set(x.parts) & SKIP)):
        h.update(f.relative_to(folder).as_posix().encode() + b"\0" + sha(f.read_bytes()).encode() + b"\n")
    return h.hexdigest()


def links() -> list:
    """(meta, path, kind) in chain order. kind is a value of ORDER (brief is read as history)."""
    found = []
    paths = [p for d in DIRS.values() for p in (ROOT / "docs" / d).glob("*.md")]
    paths += list((ROOT / "scripts").glob("*/MANIFEST.md"))
    for p in paths:
        m = read_meta(p)
        kind = ALIAS.get(m.get("type", ""), m.get("type", ""))
        if m.get("work") and kind in ORDER:
            found.append((m, p, kind))
    found.sort(key=lambda x: (x[0]["work"], ORDER.index(x[2])))
    return found


def log_since(items: list) -> str:
    """Work id of the first LOG. LOG is mandatory from that work item on. Empty if none yet."""
    logs = [m["work"] for m, _, kind in items if kind == "log"]
    return min(logs) if logs else ""


def required(work: str, since: str) -> list:
    return [t for t in ORDER if t != "log" or (since and work >= since)]


def strays() -> list:
    """md files inside document folders that are not chain documents."""
    out = []
    for d in DIRS.values():
        for p in sorted((ROOT / "docs" / d).glob("*.md")):
            m = read_meta(p)
            if not (m.get("work") and ALIAS.get(m.get("type", ""), m.get("type", "")) in ORDER):
                out.append(p.relative_to(ROOT).as_posix())
    return out


def ledger_rows(items: list) -> list:
    """Sealed documents in chain order as (id, work, kind, hash, prev_hash)."""
    return [(m["id"], m["work"], kind, m["hash"], m.get("prev_hash", "")) for m, _, kind in items if m.get("hash")]


def read_ledger():
    if not LEDGER.exists():
        return None
    rows = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 6 and c[0].isdigit():
            rows.append(tuple(c[1:]))
    return rows


def write_ledger(rows: list) -> None:
    out = list(T["ledger"]) + ["| n | id | work | type | hash | prev_hash |", "|---|---|---|---|---|---|"]
    out += [f"| {n} | {' | '.join(r)} |" for n, r in enumerate(rows)]
    out += ["", f"count: {len(rows)}", f"head: {rows[-1][3] if rows else 'GENESIS'}", ""]
    LEDGER.write_text("\n".join(out), encoding="utf-8")


def seq_errors(items: list) -> list:
    """The work sequence (nonce) is contiguous from 0 without duplicates; document ids are unique."""
    errs = []
    by_seq = {}
    for m, _, _ in items:
        by_seq.setdefault(m["work"].split("_")[1], set()).add(m["work"])
    for s, ws in sorted(by_seq.items()):
        if len(ws) > 1:
            errs.append(T["e_seq_shared"].format(s=s, x=sorted(ws)))
    seqs = sorted(int(s) for s in by_seq)
    if seqs and seqs != list(range(len(seqs))):
        errs.append(T["e_seq_gap"].format(x=[f"{s:03d}" for s in seqs]))
    ids = [m["id"] for m, _, _ in items]
    for i in sorted({x for x in ids if ids.count(x) > 1}):
        errs.append(T["e_dup_id"].format(x=i))
    order = [m["work"] for m, _, _ in items]
    if order != sorted(order, key=lambda w: int(w.split("_")[1])):
        errs.append(T["e_order"])
    return errs


def cmd_status() -> int:
    items = links()
    since = log_since(items)
    works = {}
    for m, p, kind in items:
        works.setdefault(m["work"], {})[kind] = m
    for w, d in works.items():
        title = next(iter(d.values())).get("title", "")
        marks = []
        for t in ORDER:
            if t in d:
                marks.append(f"{t}:{T['sealed'] if d[t].get('hash') else T['written']}")
            else:
                marks.append(f"{t}:{T['missing'] if t in required(w, since) else '—'}")
        print(f"{w}  {title}\n    {' '.join(marks)}")
    return 0


def cmd_list(folder: str) -> int:
    kind = {v: k for k, v in DIRS.items()}.get(folder, folder if folder in ORDER else "")
    if not kind:
        print("❌", T["l_kind"].format(x=sorted(DIRS.values()) + ["task"]))
        return 2
    for m, p, k in links():
        if k == kind:
            print(f"{m['work']}  {p.relative_to(ROOT)}")
    return 0


def cmd_seal(dry: bool = False) -> int:
    """Sealing is final. Check everything first; if anything fails, write nothing. Sealed documents are never touched."""
    if cmd_verify(quiet=True, sealed_only=True):
        print("❌", T["s_broken"])
        return 1
    items = links()
    since = log_since(items)
    todo = [(m, p, kind) for m, p, kind in items if not m.get("hash")]
    if not todo:
        print(T["s_none"])
        return 0 if dry else cmd_verify()
    errs = []
    open_seen = ""
    for m, _, _ in items:
        if not m.get("hash"):
            open_seen = open_seen or m["id"]
        elif open_seen:
            errs.append(T["s_insert"].format(a=open_seen, b=m["id"]))
            break
    for m, p, _ in todo:
        st = m.get("status", T["draft"])
        if st in DRAFTS:
            errs.append(T["s_draft"].format(id=m["id"], st=st))
    have = {}
    for m, _, kind in items:
        have.setdefault(m["work"], []).append(kind)
    for w in sorted({m["work"] for m, _, _ in todo}):
        missing = [k for k in required(w, since) if k not in have[w]]
        if missing:
            errs.append(T["e_missing"].format(w=w, x=missing))
    if errs:
        for e in errs:
            print("❌", e)
        print(T["s_refused"].format(n=len(errs)))
        return 1
    if dry:
        for m, p, _ in todo:
            print(f"{T['to_seal']}  {m['id']:22} {p.relative_to(ROOT)}")
        print(T["s_dry"].format(n=len(todo)))
        return 0
    old = read_ledger()
    prev_id, prev_hash = "GENESIS", "GENESIS"
    for m, p, kind in items:
        if m.get("hash"):
            prev_id, prev_hash = m["id"], m["hash"]
            continue
        if kind == "task":
            set_meta(p, "tree_hash", tree_hash(p.parent))
        set_meta(p, "prev", prev_id)
        set_meta(p, "prev_hash", prev_hash)
        h = doc_hash(p)
        set_meta(p, "hash", h)
        print(f"{T['seal']} {m['id']:22} {h[:12]}  ← {prev_id}")
        prev_id, prev_hash = m["id"], h
    rows = ledger_rows(links())
    if old is not None and rows[:len(old)] != old:
        print("❌", T["s_ledger_past"])
        return 1
    write_ledger(rows)
    return cmd_verify()


def cmd_verify(quiet: bool = False, sealed_only: bool = False) -> int:
    """Replay from GENESIS. sealed_only: look at the sealed part only (used right before sealing)."""
    say = (lambda *a: None) if quiet else print
    items = links()
    since = log_since(items)
    bad, prev_id, prev_hash, seen = 0, "GENESIS", "GENESIS", {}
    for m, p, kind in items:
        if sealed_only and not m.get("hash"):
            continue
        rel = p.relative_to(ROOT)
        seen.setdefault(m["work"], []).append(kind)
        errs = []
        if not m.get("hash"):
            errs.append(T["e_unsealed"])
        else:
            if m["hash"] != doc_hash(p):
                errs.append(T["e_changed"])
            if m.get("prev") != prev_id or m.get("prev_hash") != prev_hash:
                errs.append(T["e_link"].format(prev=prev_id))
            if kind == "task" and m.get("tree_hash") != tree_hash(p.parent):
                errs.append(T["e_tree"])
        say(f"{'❌' if errs else '✅'} {m['id']:22} {rel}" + (f"  — {', '.join(errs)}" if errs else ""))
        bad += bool(errs)
        prev_id, prev_hash = m["id"], m.get("hash", "")
    for w, types in seen.items():
        missing = [t for t in required(w, since) if t not in types]
        dup = sorted({t for t in types if types.count(t) > 1})
        if missing and not sealed_only:
            say("❌", T["e_missing"].format(w=w, x=missing))
            bad += 1
        if dup:
            say("❌", T["e_dup_kind"].format(w=w, x=dup))
            bad += 1
    for e in seq_errors(items):
        say("❌", e)
        bad += 1
    for s in strays():
        say("❌", T["e_stray"].format(f=s))
        bad += 1
    rows, led = ledger_rows(items), read_ledger()
    if led is None:
        if rows and not sealed_only:
            say("❌", T["e_no_ledger"])
            bad += 1
    elif led != rows:
        gone = [r[0] for r in led if r[0] not in {x[0] for x in rows}]
        say("❌", T["e_ledger_gone"].format(x=gone) if gone else T["e_ledger_diff"])
        bad += 1
    if bad:
        say(T["problems"].format(n=bad))
    else:
        say(T["ok"].format(n=len(rows), head=rows[-1][3][:12] if rows else "GENESIS"))
    return 1 if bad else 0


HEAD = """---
id: {pid}-{ymd}-{seq}
work: {work}
type: {typ}
title: {title}
date: {iso}
status: {draft}
prev:
prev_hash:
hash:
---

# {title} — {label} ({pid}-{ymd}-{seq})

"""


def cmd_new(slug: str, title: str) -> int:
    missing = [t for t in ORDER if not (TEMPLATES / f"{t}.md").exists()]
    if missing:
        print("❌", T["n_templates"].format(x=[f"docs/_templates/{t}.md" for t in missing]))
        return 2
    if not re.fullmatch(r"[a-z0-9_]+", slug):
        print("❌", T["n_slug"])
        return 2
    for m, p, kind in links():
        if not m.get("hash") and (m.get("title") == title or p.parent.name.endswith("_" + slug)):
            print("❌", T["n_dup"].format(w=m["work"], t=m.get("title", "")))
            return 2
    today = date.today()
    ymd, iso = today.strftime("%Y%m%d"), today.isoformat()
    used = [int(m["work"].split("_")[1]) for m, _, _ in links()]
    seq = f"{(max(used) + 1 if used else 0):03d}"
    work = f"{ymd}_{seq}"
    fname = f"{ymd}_{seq}_{title.replace(' ', '_')}.md"
    targets = {t: ROOT / "docs" / d / fname for t, d in DIRS.items()}
    targets["task"] = ROOT / "scripts" / f"{work}_{slug}" / "MANIFEST.md"
    for typ in ORDER:
        p = targets[typ]
        p.parent.mkdir(parents=True, exist_ok=True)
        head = HEAD.format(pid=PREFIX[typ], ymd=ymd, seq=seq, work=work, typ=typ, title=title, iso=iso,
                           label=T["labels"][typ], draft=T["draft"])
        p.write_text(head + (TEMPLATES / f"{typ}.md").read_text(encoding="utf-8").strip() + "\n", encoding="utf-8")
        print(T["created"], p.relative_to(ROOT))
    return 0


def main() -> int:
    a = sys.argv[1:]
    if a[:1] == ["verify"]:
        return cmd_verify()
    if a[:1] == ["status"]:
        return cmd_status()
    if a == ["seal"]:
        return cmd_seal()
    if a == ["seal", "--dry-run"]:
        return cmd_seal(dry=True)
    if a[:2] == ["seal", "--work"]:
        print("❌", T["s_no_reseal"])
        return 2
    if a[:1] == ["list"] and len(a) == 2:
        return cmd_list(a[1])
    if a[:1] == ["new"] and len(a) == 3:
        return cmd_new(a[1], a[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
