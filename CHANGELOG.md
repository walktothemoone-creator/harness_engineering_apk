# CHANGELOG

Recorded whenever the common body changes (the docs/ system, the SKILL body, chain.py, the report format, the build_skill procedure). A project planted from this seed knows its version from the `seed:` line in its SKILL.md front matter.

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
