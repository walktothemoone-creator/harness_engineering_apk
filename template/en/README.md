# {{PROJECT}} — {{TITLE}}

<!-- FILL: what this folder is for, in one or two sentences (whose what, and why it keeps going) -->
**Whatever the task, read this document first.** The work procedure is in [SKILL.md](SKILL.md); the best way we currently know to do the work is in [PLAYBOOK.md](PLAYBOOK.md).
**If you are an AI agent** (Claude, ChatGPT/Codex, Cursor, Gemini or any other): you operate this harness and the user only chats. Read this file, then `SKILL.md` and `PLAYBOOK.md`, before doing anything.
The procedure of this folder exists to keep context and to let the agent and the user sharpen the goal together until the purpose and goal are met.

Legend: ✅ confirmed · ❌ problem · ⏳ unconfirmed / in progress

---

## 1. History — what to read

| Order | Document | What you learn |
|---|---|---|
<!-- FILL: one row per work item. | 1 | [docs/history/FILE](docs/history/FILE) | what this record tells | -->

- Reading the work history (`docs/history/`) in work order gives the flow of the work; reading the code change log (`docs/logs/`) in work order gives how the code evolved. Only when you need more, read the file with the same name in `docs/req/` (what was wanted) → `docs/plan/` (how it was to be done) → `docs/instruction/` (what exactly was done) → `scripts/{work id}_…/MANIFEST.md` (what code remains).
- The role of the six document types and how they connect: [docs/README.md](docs/README.md)
- Work list and document status: `python3 scripts/_shared/chain.py status` / list in work order: `python3 scripts/_shared/chain.py list history` (`list logs`)

## 2. Current state (as of: <!-- FILL: yyyy-mm-dd HH:MM, and how it was confirmed -->)

**Purpose:** <!-- FILL: what this project ultimately wants to achieve, one sentence -->
**Stage now:** <!-- FILL: how far it has come and what is next -->

| Item | State | Evidence |
|---|---|---|
<!-- FILL: people and roles, state of the targets (systems / devices / data), access paths, what is decided and what is open. Evidence = file name, command, work id -->

Remaining work (the next task starts with number 1)

<!-- FILL: 1. ... 2. ... -->

> This section is updated at the end of every work item. Reality may have changed since the reference time, so do the "reality check" of SKILL step 1 first. Past states remain in each work history (`docs/history/`).

## 3. Folder layout

```
{{PROJECT}}/
├── README.md            this document (entry point, current state)
├── SKILL.md             the common work procedure for agents
├── PLAYBOOK.md          the best current method, quality bar, lessons — updated after every task
├── AGENTS.md, CLAUDE.md what an agent reads automatically when it opens this folder
├── outputs/             finished results for the user to open (copies; the sealed originals are in scripts/)
├── .env                 real settings — never share or commit
├── .env.example         list of setting keys, explanations, key ↔ script map
├── harness_engineering/ the seed that planted this structure (separate repository) — outside the chain, not committed
├── docs/                the backbone of the work — the link and the record (explained in docs/README.md)
│   ├── README.md        explanation of the document system
│   ├── _templates/      document templates (read by chain.py new)
│   ├── LEDGER.md        seal ledger — written by the tool, never by hand (appears at the first seal)
│   ├── inbox/           drop request documents and input files here — outside the chain, not committed (may hold personal data)
│   ├── req/             Requirements    (REQ)     what is wanted
│   ├── plan/            Plan            (PLAN)    how it will be done
│   ├── instruction/     Instructions    (INS)     what exactly is executed
│   ├── logs/            Code Change Log (LOG)     how the code's concept and logic started and changed
│   └── history/         Work History    (HISTORY) what was achieved and what remains — in work order
├── scripts/             code I work with — tests, analysis, drafts, tools
│   ├── _shared/                  modules shared by several work items (chain.py, envload.py)
│   └── {yyyymmdd}_{seq}_{slug}/  code per work item + MANIFEST.md (TASK)
└── vendor/              code of what gets deployed (the application) — appears only when deployment is required
    └── {app}/                    folder created by the user: SDK, earlier developers' code, the code to deploy + README.md
```

`vendor/` status: <!-- FILL: one line per app folder (what it is, where it is deployed, where the original came from). If none: "none — the user creates the folder when a deployment requirement appears" -->

| Work id | Content | State | Code folder |
|---|---|---|---|
<!-- FILL: | {yyyymmdd}_000 | harness setup | done | `scripts/{yyyymmdd}_000_harness_genesis/` | -->

## 4. Work procedure (summary — details in SKILL.md)

1. Read this `README.md` and check whether reality changed since the reference time
2. Understand the request from chat or `docs/inbox/` and record it as a **REQ** (write the purpose and goal, align with the user)
3. Write the **PLAN** in `docs/plan/` (each item answers a REQ)
4. Write the **INS** in `docs/instruction/` (each item answers a PLAN item)
5. Create code in `scripts/{work id}_{slug}/` and list it in **MANIFEST.md** (each item answers an INS item)
6. Write the **LOG** in `docs/logs/` (how the code's concept and logic changed, before → after, each item answers an INS item)
7. Write the **HISTORY** in `docs/history/` (with the REQ → PLAN → INS → deliverable → LOG traceability table)
8. Link documents and code into the chain: check with `chain.py seal --dry-run` → `chain.py seal` → "chain OK". **Sealing is final** (there is no re-seal)
9. Finish by updating sections 1, 2 and 3 of this `README.md`
10. Report to the user, starting with whether the goal was met. If a request conflicts with the purpose and goal, ask before proceeding (SKILL "When context blurs")

## 5. Rules

- **Names**: documents are `{yyyymmdd}_{3-digit seq}_{title}.md` (name order = work order); the documents of one work item have the same file name in the five folders (`req` `plan` `instruction` `logs` `history`). Titles start with `{{PREFIX}}`. Code folders are `{yyyymmdd}_{seq}_{slug}`
- **Chain**: each document's `prev_hash` points to the `hash` of the document before it (REQ → PLAN → INS → TASK → LOG → HISTORY → next work item's REQ). Sealed documents and code are never edited; corrections become a new work item. `docs/` works like a blockchain, idempotent and immutable — determinism, deduplication, integrity, consistency, finality (SKILL "docs/ works like a blockchain")
- **Secrets**: never copy values from `.env` into documents or output
- **Code location**: code I work with goes in `scripts/`, code of what gets deployed goes in `vendor/{app}/`. Only what was verified in scripts is applied to vendor, and vendor changes are recorded in `docs/logs/`
- **Facts**: separate what was confirmed (✅), what was not (⏳) and assumptions, and leave the evidence file name
<!-- FILL: rules specific to this project (a summary of SKILL "Targets and permissions") -->

## 6. Frequent commands (from `{{PROJECT}}/`)

Verify the chain

```bash
python3 scripts/_shared/chain.py verify
```

Check the harness (blanks, required files, chain)

```bash
python3 harness_engineering/tools/seed.py check
```

<!-- FILL: commands used repeatedly, such as the reality-check commands. Delete this line if there are none -->
