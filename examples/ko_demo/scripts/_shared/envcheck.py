#!/usr/bin/env python3
"""Environment check for this harness — is this machine ready to work here?

Usage (from the project root):
  python3 scripts/_shared/envcheck.py            check and compare with ENVIRONMENT.md
  python3 scripts/_shared/envcheck.py --write    check and record the result in ENVIRONMENT.md

Checks: Python 3.8+, git, UTF-8 file names and content, write permission, and the project's own
packages (.venv / requirements.txt) if it has any. Standard library only.
Nothing personal is recorded: no user name, no host name, no absolute path.
Exit code 0 = ready, 1 = something required is missing.
"""
import locale
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

LANG = "ko"
ROOT = Path(__file__).resolve().parent.parent.parent
ENVFILE = ROOT / "ENVIRONMENT.md"
BEGIN, END = "<!-- auto:begin -->", "<!-- auto:end -->"
MIN_PY = (3, 8)

T = {
    "en": {"py": "Python {v} (needs {m}+)", "cmd": "Python command to use: `{c}`", "nocmd": "no python command found on PATH",
           "git": "git {v}", "nogit": "git not found — needed to fetch the seed and to keep history",
           "utf8": "UTF-8 file names and content", "noutf8": "cannot write UTF-8 file names here: {e}",
           "write": "can write in the project folder", "nowrite": "cannot write in the project folder: {e}",
           "venv": "project packages: .venv present", "novenv": "project packages: requirements.txt exists but .venv does not — create it (see ENVIRONMENT.md)",
           "nopkg": "project packages: none needed so far", "os": "OS: {v}",
           "ready": "environment ready", "notready": "environment not ready: {n} problem(s)",
           "same": "matches ENVIRONMENT.md", "diff": "differs from ENVIRONMENT.md (another machine or an update) — run with --write and tell the user what changed",
           "norec": "ENVIRONMENT.md has no record yet — run with --write", "wrote": "recorded in ENVIRONMENT.md",
           "h": "| Item | This machine |\n|---|---|", "stdout": "terminal output encoding: {v}"},
    "ko": {"py": "Python {v} ({m} 이상 필요)", "cmd": "쓸 파이썬 명령: `{c}`", "nocmd": "PATH에서 파이썬 명령을 찾지 못함",
           "git": "git {v}", "nogit": "git 없음 — 씨앗을 받고 이력을 남기는 데 필요",
           "utf8": "UTF-8 파일명과 내용", "noutf8": "여기에 UTF-8 파일명을 쓸 수 없음: {e}",
           "write": "프로젝트 폴더에 쓸 수 있음", "nowrite": "프로젝트 폴더에 쓸 수 없음: {e}",
           "venv": "프로젝트 패키지: .venv 있음", "novenv": "프로젝트 패키지: requirements.txt는 있는데 .venv가 없음 — 만든다 (ENVIRONMENT.md 참고)",
           "nopkg": "프로젝트 패키지: 아직 필요 없음", "os": "운영체제: {v}",
           "ready": "환경 준비됨", "notready": "환경 준비 안 됨: 문제 {n}건",
           "same": "ENVIRONMENT.md와 같음", "diff": "ENVIRONMENT.md와 다름 (다른 컴퓨터이거나 업데이트됨) — --write 로 다시 기록하고 무엇이 바뀌었는지 사용자에게 알린다",
           "norec": "ENVIRONMENT.md에 아직 기록 없음 — --write 로 실행", "wrote": "ENVIRONMENT.md에 기록함",
           "h": "| 항목 | 이 컴퓨터 |\n|---|---|", "stdout": "터미널 출력 인코딩: {v}"},
}
M = T.get(LANG, T["en"])


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return (r.stdout or r.stderr).strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def python_command():
    """The first command name on PATH that runs Python 3.8+ (python3, python, py)."""
    for name in ("python3", "python", "py"):
        if not shutil.which(name):
            continue
        out = run([name, "-c", "import sys;print('%d.%d'%sys.version_info[:2])"])
        m = re.fullmatch(r"(\d+)\.(\d+)", out)
        if m and (int(m.group(1)), int(m.group(2))) >= MIN_PY:
            return name
    return ""


def checks():
    """-> list of (ok, required, label, text). `required` failures make the exit code 1."""
    out = []
    v = sys.version_info
    out.append((v[:2] >= MIN_PY, True, "python", M["py"].format(v="%d.%d.%d" % v[:3], m="%d.%d" % MIN_PY)))
    cmd = python_command()
    out.append((bool(cmd), True, "python_cmd", M["cmd"].format(c=cmd) if cmd else M["nocmd"]))
    g = re.search(r"\d+(\.\d+)+", run(["git", "--version"]) if shutil.which("git") else "")
    out.append((bool(g), True, "git", M["git"].format(v=g.group(0)) if g else M["nogit"]))
    probe = ROOT / "_envcheck_한글_probe.tmp"
    try:
        probe.write_text("확인 ✓", encoding="utf-8")
        ok = probe.read_text(encoding="utf-8") == "확인 ✓"
        out.append((True, True, "write", M["write"]))
        out.append((ok, True, "utf8", M["utf8"] if ok else M["noutf8"].format(e="read back differs")))
    except UnicodeError as e:
        out.append((True, True, "write", M["write"]))
        out.append((False, True, "utf8", M["noutf8"].format(e=type(e).__name__)))
    except OSError as e:
        out.append((False, True, "write", M["nowrite"].format(e=type(e).__name__)))
    finally:
        try:
            probe.unlink()
        except OSError:
            pass
    enc = (getattr(sys.stdout, "encoding", None) or locale.getpreferredencoding(False) or "?").lower()
    out.append(("utf" in enc, False, "stdout", M["stdout"].format(v=enc)))
    has_req, has_venv = (ROOT / "requirements.txt").exists(), (ROOT / ".venv").exists()
    if has_venv:
        out.append((True, False, "packages", M["venv"]))
    elif has_req:
        out.append((False, False, "packages", M["novenv"]))
    else:
        out.append((True, False, "packages", M["nopkg"]))
    osname = {"Darwin": "macOS", "Windows": "Windows", "Linux": "Linux"}.get(platform.system(), platform.system())
    rel = platform.mac_ver()[0] if osname == "macOS" else platform.release()
    out.append((True, False, "os", M["os"].format(v=f"{osname} {rel}".strip())))
    return out


def auto_block(results):
    rows = "\n".join(f"| {label} | {'✅' if ok else '❌'} {text} |" for ok, _req, label, text in results)
    return f"{BEGIN}\n{M['h']}\n{rows}\n{END}"


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    results = checks()
    for ok, req, _label, text in results:
        print(f"{'✅' if ok else ('❌' if req else '⚠️ ')} {text}")
    block = auto_block(results)
    old = ENVFILE.read_text(encoding="utf-8") if ENVFILE.exists() else ""
    m = re.search(re.escape(BEGIN) + r".*?" + re.escape(END), old, flags=re.S)
    if "--write" in sys.argv[1:]:
        new = old.replace(m.group(0), block) if m else (old.rstrip() + "\n\n" + block + "\n" if old else block + "\n")
        if new != old:
            ENVFILE.write_text(new, encoding="utf-8")
        print(M["wrote"])
    elif not m or M["h"] not in m.group(0) or m.group(0).count("\n") < 4:
        print(M["norec"])
    else:
        print(M["same"] if m.group(0) == block else M["diff"])
    bad = sum(1 for ok, req, _l, _t in results if req and not ok)
    print(M["ready"] if not bad else M["notready"].format(n=bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
