---
name: "{{SKILL_NAME}}"
description: "The common procedure for all work in the {{PROJECT}} folder. It exists to keep context and to let the agent and the user sharpen the goal together until the purpose and goal are met. The order is request (REQ) → plan (PLAN) → instructions (INS) → code (scripts) → code change log (LOG) → work history (HISTORY) → seal the chain → update README. Read this before creating or changing any file in this folder."
seed: "harness_engineering {{SEED_VERSION}} ({{DATE}})"
---

# {{PROJECT}} work procedure

Every agent working in this folder follows this.

**What this folder is for:** <!-- FILL: the purpose of this project in one or two sentences. What work kept repeating in chat, and why it has to continue -->

## Why this procedure exists

This procedure exists to **keep context, let the agent and the user sharpen the goal together, and reach the purpose and the goal.** Filling in documents is not the point.

- **Keep context**: even when a conversation ends or another agent takes over, "what was wanted → how it was to be done → what was actually done → what remains" continues through the documents and the chain. That is why every task starts by reading README and ends by updating README.
- **Sharpen the goal together**: the agent does not set the goal alone. On every request, write down the purpose (why) and the goal (what makes it done), align with the user, and re-align whenever things drift.
- **Reach the purpose and goal**: every item in the plan, instructions, code and report must trace back to that goal. The report is not "what I did" but "was the goal met".

Whenever you are unsure what to write at a step, choose what serves these three.

**The backbone is `docs/`.** It is the link between one task and the next, and it is where the record accumulates. This document is the rule for what to write into `docs/` and in what order. The role of each of the six document types and how they connect is in [docs/README.md](docs/README.md).

## When context blurs — ask the user

Guarding the goal is also the agent's job. If what the user says does not connect to the purpose and goal so far, contradicts them, or you cannot tell what it is for, **do not just follow it; give feedback first.** Following silently breaks the context and blurs the goal.

Ask when:
- the request is unrelated to, or goes against, the goal of the work in progress
- it contradicts something already decided (scope, target, things agreed not to do)
- you cannot tell what would make it done
- you can no longer explain what you yourself are working toward

The feedback has three parts.
1. A signal that something is off — "{{USER_CALL}}, something seems off."
2. The purpose and goal so far — "So far the purpose is … and the goal is …" (one or two sentences, based on README and the REQ in progress)
3. A question — "What is the goal of this request? The context is getting unclear." Offer choices where you can: is this changing the existing goal, a separate new task, or a short side trip?

Handle the answer accordingly: if the goal changes, update the REQ (before sealing); if it is a new task, start again from step 2. Do not ask back on light questions or status checks that do not conflict with the goal — just answer.

Working location: the folder this file is in (`{{PROJECT}}/`) — run every command below from here

## When to use this procedure

- Creating or changing code, investigating or acting on a target, producing a new document → **the full procedure**
- Answering a question or only checking status → step 1 (read README) only, then answer. Do not create documents
- If it is unclear whether a request is a small follow-up or a new task, treat it as a new task (sealed documents cannot be changed)

## Where code lives — scripts/ and vendor/

Code lives in two places. Do not mix them.

| Folder | What | Who creates it | Chain |
|---|---|---|---|
| `scripts/{work id}_{slug}/` | **Code I work with** — tests, investigation and analysis, drafts, tools | the agent, per work item | sealed by the MANIFEST `tree_hash` |
| `vendor/{app}/` | **Code of what gets deployed (the application)** — what ships to another device, a customer, the web or an app. SDKs and code from earlier developers also live here | **the user** creates the folder and puts SDKs etc. in it | not sealed (it keeps growing). Its changes are tracked only through LOG |

- **Touch vendor only when there is a special requirement.** That is when the chat or the REQ names a deployment target: "apply to another device", "deploy to the web/app", "deliver to a customer". Work without such a requirement ends in `scripts/`. The `vendor/` folder itself does not exist until such a requirement appears.
- **scripts first, vendor second.** Only what has been sufficiently verified in `scripts/` by testing and analysis (MANIFEST verification state ✅) and has a reasonably complete structure is applied to `vendor/{app}/`. Never write an unverified draft straight into vendor.
- **Work on vendor with scripts as the reference.** Record in the LOG which work item and which files it was based on.
- The agent does not create app folders directly under `vendor/` on its own. If one is needed and missing, ask the user for the folder name and what goes in it (SDK, existing code). Create it only when the user says so.
- SDKs and earlier developers' code that the user put there are originals. Before changing them, record what the original is and where it came from (repository, commit, version) in that app folder's `README.md` and in the LOG (template: `docs/_templates/vendor_app.md`).
- Applying to vendor and actually deploying are different things. Deploying (installing on a device, publishing to the web/app, pushing to someone else's repository) needs the user's confirmation at the planning stage.

## Procedure

### 1. Read README.md

Check "Current state" and "Remaining work" in `README.md`. If you need more background, read `docs/history/` in work order (`python3 scripts/_shared/chain.py list history`). To see how the code evolved, read `docs/logs/` in the same order (`list logs`). Then check that the chain is intact.

```bash
python3 scripts/_shared/chain.py verify
```

If it fails, tell the user before starting. It means someone changed a sealed document or sealed code.

**Reality check:** README "Current state" carries a reference time. The outside world (someone else's deployment, a settings change) may have changed since. If the work involves an external target, query the following before starting, look for differences from README, and tell the user first if there are any.
- <!-- FILL: reality-check commands. E.g. server/device status, latest commit of someone else's repository, listing of external storage. If none: "no external target — skip" -->
- Files changed in this folder: `find . -newer docs/history/<latest HISTORY> -type f -not -path './.venv/*' -not -path './vendor/*' -not -path './harness_engineering/*'`

### 2. Understand the request — REQ

Requests come from chat or from a document placed in `docs/inbox/` beforehand (`docs/req/` holds only REQs created by the tool — any other file there makes `verify` fail). First check whether a work item already covers this request (`python3 scripts/_shared/chain.py status`). If an unsealed work item exists, continue it; if a sealed one already finished the same request, do not create a new one — point to its HISTORY. Only when there is none, create the skeleton of a new work item (the sequence number is automatic; the tool refuses if an unsealed work item with the same title or slug exists).

```bash
python3 scripts/_shared/chain.py new <slug> "<title>"
```

- `<slug>`: a short name of lowercase letters, digits and underscores. `<title>`: the document title, starting with `{{PREFIX}} ` (e.g. `"{{PREFIX}} what this task does"`)
- Six files are created: `docs/req|plan|instruction|logs|history/{yyyymmdd}_{seq}_{title}.md` and `scripts/{yyyymmdd}_{seq}_{slug}/MANIFEST.md`. Their bodies come from `docs/_templates/`
- If the user left a request document in `docs/inbox/`, copy its content into the REQ's "Original request" and name the source file. Inbox files are outside the chain; keep or delete them as you like

What goes in a REQ: background (**purpose**: why, **goal**: what makes it done, **deployment target**: none or `vendor/{app}/`) / **the original request (quoted verbatim)** / a requirements table (R1, R2 … with acceptance criteria) / out of scope and constraints.

If the request involves applying to another device, deploying to the web/app or delivering to a customer, write the deployment target as `vendor/{app}/`; otherwise write "none (ends in scripts)". Ask if it is unclear which.

This is where you align the goal with the user. State the purpose and goal you understood in one or two sentences, then start. If the request can be read two ways, or there is no criterion to judge whether the goal is met, ask before planning. Also write in the background how this request continues the previous HISTORY's "Remaining work".

### 3. Plan — PLAN (`docs/plan/`)

Goal / scope (included, excluded) / work breakdown table / risks and responses / completion criteria.
Each item in the breakdown (P1, P2 …) names the **REQ ID it answers** and how it will be verified. No task without a REQ, no REQ without a PLAN item.

### 4. Instructions — INS (`docs/instruction/`)

Preconditions / procedure table / prohibitions and cautions / stop and recovery criteria.
Each item (I1, I2 …) names the **PLAN ID it answers**, the actual command or target, and how to check it. Someone else must be able to do the same work from this document alone.

### 5. Do the work — scripts (`scripts/{yyyymmdd}_{seq}_{slug}/`), and vendor (`vendor/{app}/`) if required

- Create code only in that work item's folder. Only what several work items share goes in `scripts/_shared/`
- If code from an earlier work item must change, do not touch that folder; copy it into the new work folder and change it there (the earlier folder is sealed)
- Make scripts **give the same result when run again** (idempotent): skip what is already done, never create or send the same thing twice. Where that is impossible (commands that change the state of a target), write "re-run caution" in the MANIFEST together with what to check before running again
- Do not hard-code settings; read them from `.env` (`scripts/_shared/envload.py`). When a new key appears, add it to `.env.example` with an explanation
- In `MANIFEST.md`, record for each file what it does, the **INS ID it answers**, and its verification state (was it actually run?). For a work item without code, write "no code"
- Only work items whose REQ names `vendor/{app}/` as the deployment target change vendor. The order is: build and verify in scripts → verification state ✅ in the MANIFEST → apply to `vendor/{app}/` based on it. Leave a "vendor application" entry in the MANIFEST (which file went where in vendor)
- If things go differently from the plan, fix PLAN and INS first, then continue (they are not sealed yet)
- If you find that the REQ's goal itself is wrong or unreachable, stop and re-align the goal with the user. Reflect the agreement in the REQ. Never quietly change or shrink the goal to finish

### 6. Code change log — LOG (`docs/logs/`)

Summary / change table / the logic now / lineage.
Record **from what concept and logic the code in `scripts/` and `vendor/` changed to what** in this work item. Without following git branches, reading `docs/logs/` in work order alone must be enough to trace how the code evolved.

- Each row of the change table (L1, L2 …) has the target (path, function), the kind (new / changed / copied then changed / deleted / vendor application), before → after, why, and the **INS ID it answers**
- For "copied then changed", say which file of which work item it came from
- If you changed `vendor/{app}/`, use the kind "vendor application" and record the scripts work item and files it was based on, what differs from the originals the user provided (SDK, existing code), and whether it was deployed (when, where). vendor is not sealed, so **the LOG is the only way to trace it**. If the app folder is a git repository, record the commit hash too
- Write "the logic now" so the flow is clear without opening the code (input → processing order → output, assumptions)
- In "lineage", name the previous LOG's ID so the change of one piece of code can be followed backwards
- If there was no code change, write only "no code change" in the summary. The LOG document is still kept
- MANIFEST is "what is here now"; LOG is "how we got here". Raw material such as run output stays in the work folder; the LOG only states the gist

### 7. Work history — HISTORY (`docs/history/`)

Summary / results / **traceability table (REQ → PLAN → INS → deliverable → LOG → state)** / remaining work.
`docs/history/` is the history of this project, accumulated in work order. Write it so that this document alone tells what happened in the work item.
The first sentence of the summary says whether the REQ's goal was met. Every REQ ID must appear in the traceability table. Leave what was not done as ❌ or ⏳ with the reason. "Remaining work" is the context the next work item inherits, so write it so that it is clear what to start with.

### 8. Link into the chain

Change the `status` of the six documents to `done`. **Sealing is final**, so check first.

```bash
python3 scripts/_shared/chain.py seal --dry-run
```

Look at what will be finalized and at the check results (draft documents, missing documents), read the six documents one last time, then seal.

```bash
python3 scripts/_shared/chain.py seal
```

You are done only when it prints "chain OK — N documents, head …". **There is no re-seal.** If you find something missing or wrong after sealing, do not edit the sealed document; correct it with a new work item (and write in that HISTORY which document it corrects and what).

### 9. Finish README.md

Update the "Current state" table (with its reference time), "Remaining work", the work list table and the history table in `README.md`. README is outside the chain and can be edited freely, and **it must always tell the current state.**

### 10. Report to the user

Report in the format below. This format is reused as the report to the manager in the later loop (automatic repetition) and graph (connecting many tasks) stages, so do not change it.

```
Goal: ✅ met / ⏳ partly / ❌ not met — <the goal in one sentence>
Done: <key results, 1–3 lines>
Not verified: <⏳ items and why, or "none">
Remaining / next goal candidates: <1–3, so the user can choose>
Evidence: <link to the HISTORY file>
Chain: OK / problem — <N> documents, head <first 12 characters>
```

## docs/ works like a blockchain — idempotent and immutable

The record in `docs/` is treated like a blockchain ledger. **Doing the same thing any number of times must give the same result (idempotent), and a record once finalized must never change (immutable).** Part of this is enforced by the tool (`chain.py`), part must be kept by the agent.

| Property | Meaning | Enforced by the tool | Kept by the agent |
|---|---|---|---|
| 1. Determinism | the same input gives the same result no matter who runs it, when, or how often | `hash` is computed from document content only, `tree_hash` from file contents only | Never write `prev`, `prev_hash`, `hash`, `tree_hash` by hand. Cite evidence that can be re-checked (command, file, time) |
| 2. Deduplication | the same thing is never processed twice | the work sequence is the nonce — contiguous from 0 with no gaps or duplicates. `new` refuses when an unsealed work item with the same title or slug exists. `seal` never touches sealed documents | Before `new`, check whether a work item already covers the request (`chain.py status`). Continue an unsealed one instead of creating another. If a finished request comes again, point to its HISTORY |
| 3. Integrity | no tampering or loss, so the whole record can be trusted | changed content or code breaks the hash, a deleted document shows up against the ledger (`docs/LEDGER.md`), a stray file is caught by the folder check | Keep only documents created by `chain.py new` in `docs/req`, `plan`, `instruction`, `logs`, `history`. Notes, drafts and raw output go in the work item's `scripts/` folder. Never edit `docs/LEDGER.md` by hand |
| 4. Consistency | replaying from the beginning reaches the same final state | `verify` trusts no stored value; it recomputes everything from GENESIS and prints the head (hash of the last document) | Run `verify` at the start and at the end of work. Put the document count and head in the report — whoever comes next knows they are in the same state if they get the same head |
| 5. Finality | what is finalized never changes | sealing is final. There is no re-seal. The ledger is append-only. Draft documents and work items with missing documents are not sealed | Never edit a sealed document or sealed code (not even a typo). When something is wrong, **correct it with a new work item** and say in its HISTORY which document it corrects. That is why you check with `seal --dry-run` before sealing |

Until sealing, edit freely. Sealing is the "finalize" button.

## What the chain does

```
REQ → PLAN → INS → TASK(MANIFEST + code in the folder) → LOG → HISTORY → next work item's REQ → …
```

- The `prev_hash` in each document's front matter equals the `hash` of the document before it. `hash` is the SHA-256 of that document's content
- The MANIFEST's `tree_hash` binds every code file in the same folder. Changing a single line of code makes verification fail
- In the front matter (`id`, `work`, `type`, `title`, `date`, `status`, `prev`, `prev_hash`, `hash`), the tool fills `prev`, `prev_hash`, `hash` and `tree_hash`. Do not write them by hand
- `docs/LEDGER.md` is the seal ledger: the ids and hashes of sealed documents in order, written by the tool only
- Outside the chain: `README.md`, `SKILL.md`, `docs/README.md`, `docs/_templates/`, `.env`, `.env.example`, `.gitignore`, `scripts/_shared/`, `.venv/`, `vendor/`, `harness_engineering/`

## When you notice repetition

If you did the same lookup, command or judgment by hand in two or more work items, write it under HISTORY "Remaining work" as an "automation candidate". If the user wants, build a script for it as a new work item, and move it to `scripts/_shared/` when several work items use it. This is the raw material for the next stage (loop engineering).

## Rules to keep

**Recording**
- Mark what was confirmed ✅, what could not be confirmed ⏳, problems ❌, and write "(assumed)" for assumptions. Leave the file name or command that is the evidence. Never write "works" for code that was not run
- Write answers and documents in {{LANGUAGE}}. Keep code names and commands as they are

**Secrets**
- Never copy values from `.env` (passwords, keys, tokens) into documents, output or commits. Use key names only
- Runs that need a password typed in are done by the user

**Targets and permissions** (rules specific to this project)
<!-- FILL: prohibitions and confirmation rules that came up in chat. Format: "- do not X / do X only after user confirmation — reason". E.g. no direct deployment of code owned by someone else, no deletion of production data, commands that change a device need confirmation at planning. Name owners and roles if any -->

## Done checklist

- [ ] The REQ states the purpose and goal, matching what was aligned with the user
- [ ] The HISTORY summary starts with whether that goal was met
- [ ] The LOG has every code change of this work item (or "no code change"), each with its INS ID and before → after
- [ ] If vendor was changed: the REQ names the deployment target, it was verified in scripts first, and the LOG has a "vendor application" row with the scripts it was based on
- [ ] All six documents exist and `chain.py status` shows them all as sealed
- [ ] `seal --dry-run` was checked before sealing
- [ ] `chain.py verify` prints "chain OK", and the document count and head are in the report
- [ ] No sealed document or code was edited. No stray file was left in the five `docs/` folders
- [ ] Every HISTORY traceability row covers all REQ IDs
- [ ] New `.env` keys are in `.env.example`
- [ ] `README.md` current state (reference time), remaining work and work list reflect the work just done and the reality check
