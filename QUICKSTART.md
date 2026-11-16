# 5-minute quick start

**English** · [한국어](QUICKSTART.ko.md) · details in [README.md](README.md)

You need Python 3.8+, git, and an AI agent that can run commands (e.g. Claude Code). Nothing to install.

## 0. The shortest way

Open an empty folder in your agent and say: "Set up a harness for my work from https://github.com/walktothemoone-creator/harness_engineering_apk". The agent does everything below for you. The steps below are for doing it by hand.

## 1. Put the seed in your project folder (1 min)

```bash
mkdir my-project && cd my-project
git clone https://github.com/walktothemoone-creator/harness_engineering_apk.git harness_engineering
```

## 2. Let the agent build the harness (3 min)

If you have been chatting with the agent about this work, say this **in the same chat**:

> Read harness_engineering/build_skill.md and build a harness in this folder from what we have discussed so far.

Confirm or correct the purpose, goal and rules it shows you. It then creates `README.md`, `SKILL.md`, `docs/` and `scripts/`, and seals the conversation as work item 000.

Starting from nothing? Describe the purpose of the work in two or three sentences first, then send the line above.

## 3. Check (30 s)

```bash
python3 harness_engineering/tools/seed.py check
```

Done when it prints "harness complete".

## 4. From then on

Whatever you ask in this folder, the agent follows `SKILL.md`: request (REQ) → plan → instructions → code → code change log (LOG) → work history (HISTORY) → seal.

- Current state: `README.md` section 2
- The work so far: `python3 scripts/_shared/chain.py list history`
- Is the record intact: `python3 scripts/_shared/chain.py verify`

To see a finished example, open [examples/ko_demo/](examples/ko_demo/) (Korean). For more than one person, read [TEAM.md](TEAM.md) first.

## Windows

- Use `py` or `python` instead of `python3` (e.g. `py harness_engineering\tools\seed.py check`).
- `tests/property_test.sh` is a bash script: run it in Git Bash or WSL.
- Not tested on Windows yet. Please report problems as Issues.
