# docs/ — the backbone of the work

This folder is the core of the harness. It is the link between one task and the next, and the record of what was wanted and what was done. `SKILL.md` is the rule for what to write here and in what order; `scripts/_shared/chain.py` is the tool that checks this record is connected and unchanged.

Every document is Markdown. Each folder is flat, and file names are `{yyyymmdd}_{seq}_{title}.md`, so **listing a folder by name gives the work order**. (`python3 scripts/_shared/chain.py list history` shows the same order.)

## Six documents

One work item leaves six documents. Five live in this folder, one (the MANIFEST) lives next to the code.

| Order | Folder | Document (ID) | Question it answers | What it takes from the previous one | What it hands on |
|---|---|---|---|---|---|
| 1 | `req/` | Requirements (REQ) | What is wanted? | "Remaining work" of the previous HISTORY, the user's original request | requirements R1, R2 … with acceptance criteria |
| 2 | `plan/` | Plan (PLAN) | How will it be done? | R IDs | tasks P1, P2 … (each answers an R) |
| 3 | `instruction/` | Instructions (INS) | What exactly is executed? | P IDs | instructions I1, I2 … (each answers a P) |
| 4 | `../scripts/{work id}_{slug}/` | Deliverables (TASK, `MANIFEST.md`) | What code remains? | I IDs | file list with verification state, hash of the whole folder |
| 5 | `logs/` | Code Change Log (LOG) | How did the code's concept and logic start and change? | I IDs, the previous LOG | changes L1, L2 …, the logic now, lineage |
| 6 | `history/` | Work History (HISTORY) | What was achieved and what remains? | all of R, P, I, L | traceability table, **remaining work → the next work item's REQ** |

```
work N:    REQ ─▶ PLAN ─▶ INS ─▶ TASK(code) ─▶ LOG ─▶ HISTORY
            R1 ◀── P1 ◀── I1 ◀──── files ◀───── L1 ◀── traceability      (tracing backwards)
                                                          │ remaining work
work N+1:  REQ ◀──────────────────────────────────────────┘
```

## Two timelines

The same work order is recorded from two points of view.

- **`history/` — the timeline of the work.** In work order it accumulates "was the goal met, what remains". Reading this folder alone tells how the project has moved. A new person or agent starts here.
- **`logs/` — the timeline of the code.** In work order it accumulates "with what concept and logic the code in `scripts/` (code I work with) and `vendor/` (code of what gets deployed) started, and what changed this time and why". Without following git branches or commits, reading this folder alone tells how the code evolved.

MANIFEST versus LOG: the MANIFEST is **what is in this folder now** (file list, verification state); the LOG is **how we got here** (before → after, reasons, lineage).

## Code lives in two places — scripts/ and vendor/

| | `scripts/{work id}_{slug}/` | `vendor/{app}/` |
|---|---|---|
| What | code I work with: tests, investigation and analysis, drafts, tools | code of what gets deployed (the application): what ships to another device, a customer, the web or an app; SDKs; earlier developers' code |
| When | every work item | only when the request or REQ names a deployment target (otherwise the folder does not even exist) |
| Who creates it | the agent, a new folder per work item | the user creates the app folder and puts SDKs etc. in it |
| Tracking | MANIFEST + sealed `tree_hash`, LOG | not sealed — **the LOG is the only record** |

Flow: build and verify in `scripts/` → once the structure is reasonably complete, apply it to `vendor/{app}/` based on that → write a "vendor application" row in the LOG (the scripts it was based on, what differs from the originals, whether it was deployed). Each app folder has a `README.md` (template: `_templates/vendor_app.md`).

## What goes in a LOG

- For a work item that created or changed code: the change table (target, kind, before → after, why, INS ID), the logic now, lineage
- Kinds: new / changed / copied then changed (code from a sealed earlier work folder copied into a new folder and changed — say where it came from) / deleted / vendor application (a change in `vendor/{app}/` — say which scripts work item and files it was based on, what differs from the originals the user provided, the base commit or version, whether it was deployed)
- "The logic now" is written so the flow is clear without opening the code: input → processing order → output, assumptions
- "Lineage" names the previous LOG's ID so the change of one piece of code can be followed backwards from LOG to LOG
- A work item without code changes still leaves a LOG: one line "no code change" in the summary. The timeline must not have holes
- Raw material such as run output and test logs does not go here but in that work item's `scripts/{work id}_{slug}/`. The LOG only says what it shows

## Naming

- Documents: `{yyyymmdd}_{3-digit seq}_{title}.md` (date and sequence first — name order = work order). The documents of one work item have **the same file name** in `req/` `plan/` `instruction/` `logs/` `history/`
- Code folders: `scripts/{yyyymmdd}_{seq}_{slug}/`
- Document IDs: `REQ-`, `PLAN-`, `INS-`, `TASK-`, `LOG-`, `HIST-` + `{yyyymmdd}-{seq}`. Item IDs: R1, P1, I1, L1 …
- Never create the skeleton by hand: `python3 scripts/_shared/chain.py new <slug> "<title>"`

## Templates — `_templates/`

`chain.py new` reads `_templates/{req,plan,instruction,task,log,history}.md` to create the body of each document. The front matter and the title line are added by the tool. `_templates/vendor_app.md` is the template for `vendor/{app}/README.md` (not used by the tool; copy it when an app folder appears). To change table columns or add sections, edit these files; documents that already exist are not affected. `_templates/` and this `README.md` are outside the chain.

## The chain — like a blockchain, idempotent and immutable

```
REQ → PLAN → INS → TASK → LOG → HISTORY → next work item's REQ → …
```

- `prev_hash` in each document's front matter = `hash` of the document right before it. `hash` = SHA-256 of that document's content
- The `tree_hash` of a TASK (MANIFEST) binds all the code in that folder. Changing a single line of code makes verification fail
- `LEDGER.md` is the seal ledger: the ids and hashes of sealed documents in chain order. The tool only appends to it

The record in this folder keeps the same five properties as a blockchain ledger.

| Property | In a blockchain | Here | When violated |
|---|---|---|---|
| 1. Determinism | the same input always yields the same result, whoever runs it, whenever, however often | `hash` depends only on document content, `tree_hash` only on file contents. Time, person, location and file name are not part of it | — (the computation is built that way) |
| 2. Deduplication | nonces and UTXOs prevent the same transaction from being processed twice | the work sequence is the nonce: contiguous from 0, no gaps, no duplicates. `new` refuses an unsealed duplicate title or slug. `seal` never touches sealed documents, so running it again changes nothing | `new` refuses; `verify` reports "sequence is not contiguous" |
| 3. Integrity | duplicates and tampering are impossible, so the whole ledger can be trusted | tampered content → hash mismatch. Deleted document → still in the ledger, so it shows. Stray file → folder check | `verify` prints ❌, exit code 1 |
| 4. Consistency | every node that replays from the beginning reaches the same final state | `verify` trusts no stored value; it recomputes from GENESIS and prints the **head** (hash of the last document). Anyone with the same `docs/` gets the same head | a head that differs from the reported one means something changed in between |
| 5. Finality | a finalized result is recorded permanently and never changes | sealing is final. There is no re-seal. Draft documents and work items with missing documents are not sealed. Corrections are appended as a new work item | `seal --work` is refused; nothing is sealed on top of a broken chain |

Order of use: when everything is written, run `python3 scripts/_shared/chain.py seal --dry-run` to see what will be finalized → `seal` → "chain OK — N documents, head …". Put that document count and head in the report. Until sealing you may edit freely; after sealing not even a typo is fixed.

Only documents created by `chain.py new` live in these five folders. Notes, drafts and run output go in that work item's `scripts/` folder.

One limit to know: the ledger is a file inside `docs/`, so someone who rewrites documents *and* the ledger together cannot be detected from this folder alone. That is why the head is reported outside (in the report to the user, or in a git commit) — a rewritten past no longer matches the head that was reported.
