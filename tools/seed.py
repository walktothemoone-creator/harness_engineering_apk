#!/usr/bin/env python3
"""harness_engineering seed tool — plant the harness structure in a project folder (init) and check that it has grown (check).

Usage (from the project root; harness_engineering/ is cloned right under the project root):
  python3 harness_engineering/tools/seed.py init --prefix ACME --title "ACME data pipeline workspace" \\
          [--lang en|ko] [--user-call "Alex"] [--root <project root>]
  python3 harness_engineering/tools/seed.py check [--root <project root>]

init
- copies template/common/ and template/<lang>/ into the project root and fills the {{...}} slots.
  Files that already exist are skipped, never overwritten.
- creates the docs/ backbone (README.md, _templates/, req, plan, instruction, logs, history) and scripts/_shared.
- what is left blank is marked `FILL:`; the agent fills it by following build_skill.md.

check (exit code 0 = the harness is complete)
- required files exist; no FILL blanks left in README, SKILL, .env.example
- .gitignore contains .env; at least one work item exists and `chain.py verify` passes
"""
import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SEED = Path(__file__).resolve().parent.parent          # harness_engineering/
TEMPLATE = SEED / "template"
RENAME = {"gitignore": ".gitignore", "env.example": ".env.example"}
REQUIRED = ["README.md", "SKILL.md", ".env.example", ".gitignore", "docs/README.md",
            "scripts/_shared/chain.py", "scripts/_shared/envload.py"]
REQUIRED += [f"docs/_templates/{t}.md" for t in ("req", "plan", "instruction", "task", "log", "history")]
FILL_CHECKED = ["README.md", "SKILL.md", ".env.example"]
DOC_DIRS = ["docs/req", "docs/plan", "docs/instruction", "docs/logs", "docs/history"]
DEFAULTS = {"en": {"user_call": "Hi", "language": "English"}, "ko": {"user_call": "사용자님", "language": "한국어"}}
MSG = {
    "en": {"self": "the project root is harness_engineering itself. Clone it inside a project folder.",
           "prefix": "--prefix must be one word without spaces or symbols (e.g. ACME)",
           "project": "project: {root}  (seed {v}, lang {lang})", "created": "  created", "skipped": "  skipped (exists)",
           "next": "next: build_skill.md step 3 — fill the FILL blanks, then step 4 — record work item 000",
           "absent": "  — missing", "blanks": "blanks", "none": "none", "left": "  — lines left {x}",
           "gitignore": ".gitignore contains .env",
           "nowork": "no work item — record work item 000 (build_skill.md step 4)",
           "done": "harness complete", "notdone": "incomplete: {n}"},
    "ko": {"self": "프로젝트 루트가 harness_engineering 자신입니다. 프로젝트 폴더 안에 clone 해서 쓰세요.",
           "prefix": "--prefix 는 공백·기호 없는 한 단어 (예: ACME)",
           "project": "프로젝트: {root}  (씨앗 {v}, 언어 {lang})", "created": "  생성", "skipped": "  건너뜀(이미 있음)",
           "next": "다음: build_skill.ko.md 3단계 — FILL 빈칸 채우기, 이어서 4단계 작업 000 기록",
           "absent": "  — 없음", "blanks": "빈칸", "none": "없음", "left": "  — 남은 줄 {x}",
           "gitignore": ".gitignore 에 .env",
           "nowork": "작업 없음 — 작업 000을 기록하세요 (build_skill.ko.md 4단계)",
           "done": "하네스 완성", "notdone": "미완성 {n}건"},
}


def seed_version() -> str:
    v = (SEED / "VERSION").read_text(encoding="utf-8").strip()
    try:
        c = subprocess.run(["git", "-C", str(SEED), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=5)
        if c.returncode == 0 and c.stdout.strip():
            v += f"@{c.stdout.strip()}"
    except (OSError, subprocess.SubprocessError):
        pass
    return v


def project_lang(root: Path) -> str:
    chain = root / "scripts/_shared/chain.py"
    if chain.exists():
        m = re.search(r'^LANG = "(\w+)"', chain.read_text(encoding="utf-8"), flags=re.M)
        if m and m.group(1) in MSG:
            return m.group(1)
    return "en"


def cmd_init(a) -> int:
    M = MSG[a.lang]
    root = Path(a.root).resolve() if a.root else SEED.parent
    if root == SEED:
        print("❌", M["self"])
        return 2
    if not re.fullmatch(r"[A-Za-z0-9가-힣]+", a.prefix):
        print("❌", M["prefix"])
        return 2
    project = root.name
    values = {
        "PROJECT": project,
        "PROJECT_PATH": str(root),
        "TITLE": a.title,
        "PREFIX": a.prefix,
        "SKILL_NAME": re.sub(r"[^a-z0-9]+", "-", project.lower()).strip("-") + "-workflow",
        "USER_CALL": a.user_call or DEFAULTS[a.lang]["user_call"],
        "LANGUAGE": a.language or DEFAULTS[a.lang]["language"],
        "DATE": date.today().isoformat(),
        "SEED_VERSION": seed_version(),
    }
    created, skipped = [], []
    for base in (TEMPLATE / "common", TEMPLATE / a.lang):
        for src in sorted(p for p in base.rglob("*") if p.is_file() and p.name not in (".DS_Store", ".gitkeep")):
            rel = src.relative_to(base)
            dst = root / rel.parent / RENAME.get(rel.name, rel.name)
            if dst.exists():
                skipped.append(dst.relative_to(root).as_posix())
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            text = src.read_text(encoding="utf-8")
            for k, v in values.items():
                text = text.replace("{{" + k + "}}", v)
            if rel.name == "chain.py":
                text = re.sub(r'^LANG = "\w+"', f'LANG = "{a.lang}"', text, count=1, flags=re.M)
            dst.write_text(text, encoding="utf-8")
            created.append(dst.relative_to(root).as_posix())
    for d in DOC_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    print(M["project"].format(root=root, v=values["SEED_VERSION"], lang=a.lang))
    for f in created:
        print(M["created"], f)
    for f in skipped:
        print(M["skipped"], f)
    print(M["next"])
    return 0


def cmd_check(a) -> int:
    root = Path(a.root).resolve() if a.root else SEED.parent
    M = MSG[project_lang(root)]
    bad = 0
    for f in REQUIRED + DOC_DIRS:
        ok = (root / f).exists()
        bad += not ok
        print(f"{'✅' if ok else '❌'} {f}" + ("" if ok else M["absent"]))
    for f in FILL_CHECKED:
        p = root / f
        if not p.exists():
            continue
        left = [i + 1 for i, line in enumerate(p.read_text(encoding="utf-8").splitlines())
                if "FILL:" in line or "{{" in line]
        bad += bool(left)
        print(f"{'✅' if not left else '❌'} {f} {M['blanks']}" + (M["left"].format(x=left) if left else f" {M['none']}"))
    gi = root / ".gitignore"
    if gi.exists():
        ok = ".env" in gi.read_text(encoding="utf-8").split()
        bad += not ok
        print(f"{'✅' if ok else '❌'} {M['gitignore']}")
    chain = root / "scripts/_shared/chain.py"
    if chain.exists():
        works = list((root / "docs/req").glob("*.md")) if (root / "docs/req").exists() else []
        if not works:
            bad += 1
            print("❌", M["nowork"])
        r = subprocess.run([sys.executable, str(chain), "verify"], cwd=root, capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
        bad += r.returncode != 0
        print(f"{'✅' if r.returncode == 0 else '❌'} chain.py verify — {last}")
    print(M["done"] if not bad else M["notdone"].format(n=bad))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--prefix", required=True, help="one-word prefix for document titles (e.g. ACME)")
    i.add_argument("--title", required=True, help="one-line project description (README title)")
    i.add_argument("--lang", choices=["en", "ko"], default="en", help="language of the planted documents and tool messages")
    i.add_argument("--user-call", default="", help='how the agent addresses the user (e.g. "Alex")')
    i.add_argument("--language", default="", help="language the agent writes answers and documents in (default follows --lang)")
    i.add_argument("--root", help="project root (default: the parent folder of harness_engineering)")
    c = sub.add_parser("check")
    c.add_argument("--root", help="project root (default: the parent folder of harness_engineering)")
    a = ap.parse_args()
    return cmd_init(a) if a.cmd == "init" else cmd_check(a)


if __name__ == "__main__":
    sys.exit(main())
