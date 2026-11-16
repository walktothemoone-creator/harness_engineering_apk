# CHANGELOG

Recorded whenever the common body changes (the docs/ system, the SKILL body, chain.py, the report format, the build_skill procedure). A project planted from this seed knows its version from the `seed:` line in its SKILL.md front matter.

## 1.4.0 — 2026-11-17

Environment setup is part of building and of every task.

- `scripts/_shared/envcheck.py` (planted): checks Python 3.8+, the Python command to use (`python3`/`python`/`py`), git, UTF-8 file names, write permission, project packages; `--write` records the result in `ENVIRONMENT.md`; without it, compares and reports a changed machine. Records nothing personal
- `ENVIRONMENT.md` (planted, outside the chain): this machine, base requirements with install commands per OS, and the project's own packages and tools (`.venv` + pinned `requirements.txt`)
- `seed.py init` runs the check and writes `ENVIRONMENT.md`; `seed.py check` requires it to pass
- AGENTS.md "Check the environment first" and build_skill step 0: verify Python and git before cloning or planting; install only with the user's agreement
- SKILL step 1 runs `envcheck.py`; step 5 has the rule for packages and tools

## 1.3.1 — 2026-11-16

From a five-work-item test of the PLAYBOOK mechanism (setup, three weekly runs, one improvement).

- build_skill step 4 seeds `PLAYBOOK.md` from the conversation, so the first task does not start from an empty playbook
- PLAYBOOK levels: at most one level per work item, a level counts only after a real run used it, and the level says what it does not cover yet; standing checks belong in the quality bar from the first run; lessons do not cite step numbers; finished candidates move to a "Done" list
- One rule for promoting recurring work: offer on second use, build as its own work item when the user agrees
- Shared scripts (outside the chain): keep a sealed copy of each version in the work folder, record its SHA-256, compare at the start of a run
- Report format: the last line is now "Record: intact — N documents, check value …" (was "Chain: … head …"), plus a "Next improvement" line
- Rules for customer text in results and for keeping input files

## 1.3.0 — 2026-11-16

Any agent, README first, and work that improves with use. Driven by an end-to-end test (a fresh agent, a bare URL, a non-developer's weekly report task).

- `PLAYBOOK.md` (planted, outside the chain): the current best method per recurring work with a five-step level, the quality bar, lessons, improvement candidates. SKILL step 1 reads it, step 9 updates it with three questions; every row names its HIST ID
- README (seed and planted) opens with a note to the AI agent, whichever it is; AGENTS.md explains which agents can operate a harness and that switching agents continues from the same record
- `outputs/`: results for the user are sealed in the work folder and copied to `outputs/` under a plain name; the report tells the user that path in one plain sentence
- Inputs: `docs/inbox/` is now in `.gitignore`; raw input with personal data is never copied into sealed folders; the INS records the input's SHA-256
- Recurring work: promote the script to `scripts/_shared/` on second use instead of copying it every time
- Fix: REQ template said `docs/req` for the request source (now `docs/inbox`); AGENTS.md names the clone folder and the empty-folder case

## 1.2.0 — 2026-11-16

The user works through chat only; the agent sets up and manages the harness.

- `AGENTS.md` (+ `CLAUDE.md` pointing to it) at the seed root: what an agent does when a user only gives it this repository's URL — where to plant, how to run build_skill, rules for a chat-only user (run every command, plain words, ask only what only the user can answer)
- Planted harnesses now get `AGENTS.md` and `CLAUDE.md`, so any agent opening the folder later follows `SKILL.md` without being told. `seed.py check` requires them
- SKILL: new common section "The user works through chat" — the agent runs and fixes everything, talks in plain words, and tells the returning user where things stand
- build_skill step 0: start from a bare URL; step 6 no longer suggests adding `CLAUDE.md` by hand
- README / QUICKSTART: "Just talk to your agent" as the first way in

## 1.1.0 — 2026-11-16

For using the seed in a team.

- `TEAM.md` / `TEAM.ko.md`: one harness folder = one writer at a time, split harnesses when the work splits, handover by head hash, recovery when two branches create the same sequence
- `QUICKSTART.md` / `QUICKSTART.ko.md`: 5-minute start, Windows notes (`py`/`python`, Git Bash or WSL for the tests; not tested on Windows yet)
- `examples/ko_demo/`: a finished harness built with the tools (two sealed work items, a tested script)
- `LICENSE`: MIT
- Fix: request documents go to `docs/inbox/` (outside the chain). The SKILL said to put them in `docs/req/`, which made `verify` fail with a stray-file error. `seed.py init` creates `docs/inbox/`
- Fix: SKILL templates no longer write the absolute local path of the project (`{{PROJECT_PATH}}`) — it leaked the user name of the machine into public repositories
- `chain.py`: the duplicated-sequence error now explains the cause and points to TEAM.md

## 1.0.1 — 2026-11-14

- Fix: the front matter of `template/en/SKILL.md` and `template/ko/SKILL.md` was not valid YAML (a value starting with `{{…}}` is read as a flow mapping), so GitHub showed "Error in user YAML". The three values are now quoted. Planted projects are unaffected in behaviour; their `SKILL.md` front matter now carries quoted strings.

## 1.0.0 — 2026-11-14

First public release.

- `docs/` backbone: `req` `plan` `instruction` `logs` `history`, document templates in `docs/_templates/`, file names `{yyyymmdd}_{seq}_{title}.md` (name order = work order)
- Six documents per work item, linked by a hash chain: REQ → PLAN → INS → TASK (MANIFEST + code) → LOG → HISTORY → next REQ
- `logs/`: the timeline of the code — concept and logic changes per work item, with lineage from LOG to LOG
- Code location rule: `scripts/` (code I work with) first, `vendor/{app}/` (code of what gets deployed) only on a deployment requirement and only after verification
- Blockchain properties enforced by `chain.py`: determinism, deduplication (nonce, duplicate `new` refused), integrity (seal ledger `docs/LEDGER.md`, stray-file check), consistency (replay from GENESIS, head hash), finality (no re-seal, `seal --dry-run`, drafts are not sealed)
- `build_skill.md`: harvest the conversation → align with the user → `seed.py init` → fill the blanks → seal the conversation as work item 000 → `seed.py check`
- English and Korean: documents in `template/en` and `template/ko`, tool messages follow `--lang`
- `tests/property_test.sh`: tries to violate each property and checks the tool refuses or reports it
