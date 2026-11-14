---
name: build-skill
description: The procedure for turning a chat into a harness (the docs/ backbone (req, plan, instruction, logs, history) + README.md + SKILL.md + scripts/ + a hash chain) once the work done in chat shows repetition and continuity. Run from harness_engineering/ cloned inside a project folder. Use it for requests like "build a harness", "build_skill", "systematize this work".
---

# build_skill — turning a conversation into a harness

The agent reads this document and executes it as written. The result is created in **the parent folder of this folder (the project root)**.

(Korean version: `build_skill.ko.md`)

## What this procedure does

At first the user asks the agent all sorts of things in chat. Then a **purpose and a repetition** become visible, and once the user decides the work will have to continue, they create a project folder, clone this repository into it and ask for this procedure.

The procedure does not throw the conversation away. It records it as the first work item (000) and plants a structure that makes every later task take the same road.

**What is planted centers on `docs/`.** `docs/` is the link between tasks and the record itself; README is its entrance, SKILL is the rule for writing into it, and chain.py is the tool that checks it is connected. The document system is described in `template/en/docs/README.md` — read it before starting.

```
chat (one-off) ──repetition and continuity noticed──▶ project folder + git clone harness_engineering
                                         │
                                         ▼  build_skill.md (this document)
                       docs/{req,plan,instruction,logs,history} · README.md · SKILL.md · scripts/_shared/chain.py
                                         │
                                         ▼  from now on every request goes through SKILL.md
                       REQ → PLAN → INS → scripts(MANIFEST) → LOG → HISTORY → next REQ … (hash chain)
```

## Assumptions

- Location: `<project>/harness_engineering/build_skill.md`. Project root = the parent of this folder
- Run every command **from the project root**
- The conversation so far (everything said before this procedure was requested) is the raw material. If it happened in another session, ask the user to paste a summary or the original text

## Procedure

### 0. Check the ground

```bash
ls -la; ls harness_engineering
```

- If the project root already has a `SKILL.md` or `docs/`, **stop and ask**: is this an upgrade of an existing harness, or should a new one be planted in another folder? `seed.py init` never overwrites existing files, but mixing two would tangle the chain
- If the project root looks wrong (home folder, desktop, a place where several things are mixed), stop and ask which folder is the project
- Do not move files that were already in the project root (code, material). Just list them in step 0 and leave them in the "existing assets" part of the step 4 HISTORY

### 1. Extract the genetic information from the conversation — harvest

Re-read the conversation from the beginning and fill in the table below. Leave blank what is not in the conversation; do not make anything up. The table is shown to the user in step 2 and becomes the material for the REQ, LOG and HISTORY of work item 000 in step 4.

| Item | What to look for | Where it is used |
|---|---|---|
| Purpose | why this work is done (the reason the user kept repeating) | README section 2 "Purpose", SKILL "What this folder is for" |
| Goal now | what, once achieved, ends the current stage | README "Stage now", remaining work no. 1 |
| Repeated work | lookups, commands or judgments done twice or more in the conversation | SKILL "Reality check", README section 6, automation candidates |
| Targets | systems, devices, data, repositories being handled; access paths | README section 2 state table |
| Deployment targets | is there code that ships to another device, a customer, the web or an app? is there earlier developers' code or an SDK? | README section 3 "`vendor/` status", SKILL "Targets and permissions" |
| People and roles | who owns what, who decides, who receives reports | README section 2, SKILL "Targets and permissions" |
| Things not to do | what the user blocked, near-accidents, things that belong to others | SKILL "Targets and permissions" |
| Settings and secrets | addresses, accounts, keys mentioned in the conversation — **key names only** | `.env.example` |
| Work already done | what was actually done in the conversation, with results (✅/❌/⏳) | work item 000 HISTORY |
| Existing code | code created or brought in during the conversation, its logic and how it changed | work item 000 LOG |
| Remaining work | what was still open when the conversation ended | README "Remaining work", work item 000 HISTORY |
| The user's own words | the user's sentences stating purpose and rules, verbatim | work item 000 REQ "Original request" |
| Address and prefix | how to address the user, one word to put in front of document titles | `seed.py init --user-call --prefix` |

Secrets are not written as values in this table either. Write key names only, as in "there is a database password → `DB_PASSWORD`".

### 2. Align with the user

Based on the table, show the user the following in one go and get confirmation. Do not go to step 3 without it.

1. "The purpose of this folder is … and the goal now is …" (one or two sentences)
2. What you saw as repeated work (three at most)
3. The rules you will put in SKILL as things not to do
4. Values to decide: title prefix (e.g. `ACME`), a one-line README title, how to address the user (e.g. `Alex`), document language (`en`/`ko`)
5. What is blank in the table and cannot be known from the conversation alone (as questions, only what is really needed)

What the user corrects is the truth. Update the table accordingly.

### 3. Plant the seed and fill the blanks

```bash
python3 harness_engineering/tools/seed.py init --prefix <prefix> --title "<README title>" --user-call "<address>"
```

(`--lang ko` plants the Korean documents and tool messages.)

What appears: `README.md`, `SKILL.md`, `.env.example`, `.gitignore`, `scripts/_shared/chain.py`, `scripts/_shared/envload.py`, and the backbone `docs/` — `README.md` (the document system), `_templates/` (the document templates), `req/` `plan/` `instruction/` `logs/` `history/`.

Then fill the `FILL:` blanks in `README.md`, `SKILL.md` and `.env.example` from the step 1 table. Remove the `FILL` comment wherever you fill one.

- **Do not change** the common parts of SKILL.md (intent, asking back, where code lives, procedure 1–10, blockchain properties, chain, recording and secret rules, done checklist). They are the body every harness shares. Project-specific content goes only into three places: "What this folder is for", "Reality check" and "Targets and permissions"
- If the project-specific rules grow long, split "Targets and permissions" with sub-headings (e.g. **Devices**, **Deployment**)
- Do not create `vendor/`. If the conversation had a deployment target, write it in README section 3 "`vendor/` status" and ask the user to create `vendor/{app}/` and put the SDK or existing code in it. All code created during the conversation goes to `scripts/` (the work item 000 folder) — only what is verified is applied to vendor later
- `.env.example` gets example values only. Just tell the user to create the real `.env` with `cp .env.example .env`
- The README section 1 history table and section 3 work list are filled after step 4

### 4. Record the conversation so far as work item 000

```bash
python3 scripts/_shared/chain.py new harness_genesis "<prefix> harness setup"
```

Fill in the six documents. Their content is "the work done in chat + the building of the harness".

| Document | What to write |
|---|---|
| REQ | Background: what was being done in chat and why it is being systematized (purpose), what is true once this work item ends (goal: the harness stands and the conversation's context is recorded). Original request: the "user's own words" from step 1 and the words that asked for this procedure. Requirements: R1 record the conversation's context, R2 create the harness structure, R3 reflect the project rules (+ any requirement that came up in the conversation) |
| PLAN | P1 harvest the conversation (step 1) / P2 align with the user (step 2) / P3 plant the seed and fill the blanks (step 3) / P4 record work item 000 (step 4) — each with the REQ it answers |
| INS | the commands actually run (`seed.py init …`, `chain.py new …`) and how they were checked (`seed.py check`) |
| MANIFEST | if code was created during the conversation, move it into this folder (`scripts/{work id}_harness_genesis/`) and list it. Otherwise "no code" |
| LOG | the starting point of the code created or brought in during the conversation: what it was for, with what logic it was built, how it changed during the conversation. This is where the lineage of every later LOG begins. If there is no code, "no code change" |
| HISTORY | summary (starting with whether the goal was met) / what was done in the conversation and the results (✅/❌/⏳, with evidence) / the "existing assets" list from step 0 / traceability table / remaining work (same as README remaining work) / automation candidates (the "repeated work" of step 1) |

Change the `status` of the six documents to `done`. **Sealing is final and cannot be repeated**, so check first.

```bash
python3 scripts/_shared/chain.py seal --dry-run
```

Read the six documents one last time (did the step 1 table and the user's corrections from step 2 go in correctly?) and seal. The first seal creates `docs/LEDGER.md` (the seal ledger).

```bash
python3 scripts/_shared/chain.py seal
```

Then add work item 000 to the README section 1 history table and section 3 work list.

### 5. Check that it has grown

```bash
python3 harness_engineering/tools/seed.py check
```

You are done only when it prints "harness complete". If there is a ❌, fix it and run again. If you find a mistake in a sealed document of work item 000, do not edit it; tell the user and correct it in the next work item.

### 6. Report and hand over

Report in the format of SKILL.md step 10. Add the following at the end.

- From now on, any request in this folder goes through the `SKILL.md` procedure
- When the project becomes a git repository, `harness_engineering/` is already in `.gitignore` (the seed is a separate repository; the version that built this harness is recorded in the `seed:` line of SKILL.md's front matter)
- To make an agent find this folder automatically: with Claude Code, put a `CLAUDE.md` in the project root with one line "read README.md and SKILL.md before working", or link `SKILL.md` as `.claude/skills/<name>/SKILL.md` — only if the user wants it

## What not to do

- Do not invent a purpose, a rule or a state that was not in the conversation. If unknown, leave it as ⏳ and ask in step 2
- Do not delete or move files that were already in the project (moving them into the work item 000 code folder also needs the user's confirmation)
- Do not copy secrets into documents, output or commits
- Do not adapt the common body of SKILL.md to the project. If you want to change the body, that is a change to the seed (the harness_engineering repository) → record it in `CHANGELOG.md` and raise the version
- After this procedure is finished, do not edit anything inside `harness_engineering/`
