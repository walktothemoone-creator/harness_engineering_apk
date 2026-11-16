# ENVIRONMENT — what this work needs on a machine

The agent checks this before working (SKILL step 1) and keeps it current. It is outside the chain. Nothing personal goes here: no user name, host name or absolute path.

## 1. This machine (written by the tool)

`python3 scripts/_shared/envcheck.py --write` rewrites the table below. Run it again on another machine or after an update.

<!-- auto:begin -->
<!-- auto:end -->

## 2. Base requirements (every harness)

| Need | Why | If missing |
|---|---|---|
| Python 3.8+ | runs `chain.py`, `envcheck.py` and the work scripts (standard library only) | macOS: `xcode-select --install` or `brew install python` · Windows: `winget install Python.Python.3.12` · Linux: `sudo apt install python3` |
| git | fetches the seed; keeps history if the folder becomes a repository | macOS: `xcode-select --install` · Windows: `winget install Git.Git` · Linux: `sudo apt install git` |
| UTF-8 file names and content | document names may be in any language | Windows: use a UTF-8 terminal (Windows Terminal; `chcp 65001`) |

Installing system software changes the user's computer: say in plain words what will be installed and why, and install only after the user agrees. Commands that ask for a password are run by the user.

## 3. What this project needs (kept by the agent)

Packages go in a virtual environment in this folder, never into the system Python. Create it once: `python3 -m venv .venv`; install with `.venv/bin/pip install -r requirements.txt` (Windows: `.venv\Scripts\pip`). Every package is pinned in `requirements.txt` with the work history (HIST ID) that introduced it.

| Tool or package | Version | Used by | Since (HIST ID) |
|---|---|---|---|

Other tools (a CLI, a browser, an account, access to a system):

| Tool | What for | How to check it works | Since (HIST ID) |
|---|---|---|---|
