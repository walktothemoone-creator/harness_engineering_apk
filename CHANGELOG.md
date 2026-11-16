# CHANGELOG

Recorded whenever the common body changes (the docs/ system, the SKILL body, chain.py, the report format, the build_skill procedure). A project planted from this seed knows its version from the `seed:` line in its SKILL.md front matter.

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
