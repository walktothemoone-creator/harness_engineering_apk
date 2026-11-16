# harness_engineering — a seed for harness engineering

**English** · [한국어](README.ko.md) · [Intro page](https://walktothemoone-creator.github.io/harness_engineering_apk/)

Most work with an AI agent starts as a chat: you ask, it answers, you ask again. At some point you notice that the work has a **purpose** and that it **repeats** — and that it will have to continue next week, with a new conversation, maybe with a different agent. Chat prompts do not survive that. A harness does.

This repository is a **seed**. Clone it into any project folder, ask your agent to run `build_skill.md`, and the conversation you have had so far grows into a harness: a document backbone (`docs/`), a work procedure (`SKILL.md`), an entry point (`README.md`) and a small tool that links every document and every piece of code into a hash chain.

It is a personal project, published to offer a working system to anyone who wants to practice harness engineering — and to be evaluated. Criticism, issues and pull requests are very welcome.

## Why

- An agent forgets everything when the conversation ends. The only thing the next session, or the next agent, can pick up is what is left in files.
- So the core of a harness is not the prompt but the **record**: what was wanted → how it was to be done → what was executed → how the code changed → what remains.
- That record must be trustworthy. Here it behaves like a blockchain ledger: append-only, tamper-evident, and reproducible from the first document.

## The backbone is docs/

Everything else exists for `docs/`.

| What | Role |
|---|---|
| **`docs/`** | the link between tasks and the record itself |
| `README.md` | the entrance to `docs/`: current state and remaining work |
| `SKILL.md` | the rule for what to write into `docs/`, in what order |
| `scripts/_shared/chain.py` | the tool that proves `docs/` is connected and unchanged |

```
docs/
├── README.md        the document system explained
├── _templates/      templates for the six documents (edit these to change the forms)
├── LEDGER.md        seal ledger, written by the tool
├── req/             REQ      what is wanted
├── plan/            PLAN     how it will be done                    (each item answers a REQ)
├── instruction/     INS      what exactly is executed               (each item answers a PLAN item)
├── logs/            LOG      how the code's concept and logic changed (each item answers an INS item)
└── history/         HISTORY  what was achieved and what remains      (remaining work → the next REQ)
scripts/{work id}_{slug}/MANIFEST.md   TASK  what code remains
```

```
work N:    REQ ─▶ PLAN ─▶ INS ─▶ TASK(code) ─▶ LOG ─▶ HISTORY
                                                          │ remaining work
work N+1:  REQ ◀──────────────────────────────────────────┘         … linked by hashes
```

- Every document is Markdown; every folder is flat. File names are `{yyyymmdd}_{seq}_{title}.md`, so name order is work order.
- **`history/` is the timeline of the work**: read it in order and you know how the project moved.
- **`logs/` is the timeline of the code**: read it in order and you know with what concept and logic the code started and how it changed — without digging through git branches.

### Two places for code

| Folder | What | When |
|---|---|---|
| `scripts/` | code *I work with* — tests, analysis, drafts, tools. One folder per work item, sealed | every work item |
| `vendor/{app}/` | code of *what gets deployed* — to another device, a customer, the web or an app. SDKs and earlier developers' code live here too. The user creates the app folder | only when a request names a deployment target |

Only what has been verified in `scripts/` is applied to `vendor/`. `vendor/` is not sealed, so `docs/logs/` is its record.

### Like a blockchain: idempotent and immutable

| Property | How the harness keeps it |
|---|---|
| Determinism | a hash depends only on content — not on time, person, location or file name |
| Deduplication | the work sequence number is the nonce; a duplicate `new` is refused; `seal` run twice changes nothing |
| Integrity | tampering, deletion (via the seal ledger), stray files and ledger edits are all detected |
| Consistency | `verify` replays from GENESIS and prints one head hash; same `docs/`, same head, for everyone |
| Finality | sealing is final, there is no re-seal; a mistake is corrected by a new work item, never by editing |

These are not just rules in a document. `tests/property_test.sh` tries to break each of them and checks that the tool refuses or reports it.

## Quick start

> In a hurry: [QUICKSTART.md](QUICKSTART.md) (5 minutes) · a finished example: [examples/ko_demo/](examples/ko_demo/) · more than one person: [TEAM.md](TEAM.md)


1. You have been working in chat and decide "this is going to continue". Create a project folder.
2. Clone this repository inside it.

   ```bash
   git clone https://github.com/walktothemoone-creator/harness_engineering_apk.git harness_engineering
   ```

3. In the same chat (where the context still is), tell your agent:

   > Read harness_engineering/build_skill.md and build a harness in this folder from what we have discussed so far.

4. The agent harvests the conversation, shows you the purpose, goal and rules it found, and after your confirmation plants `docs/`, `README.md`, `SKILL.md` and `scripts/`, then seals the conversation as work item 000.
5. From then on, whatever you ask in that folder goes through `SKILL.md`: REQ → PLAN → INS → scripts → LOG → HISTORY.

Korean documents and tool messages: add `--lang ko` (the agent follows `build_skill.ko.md`).

You can also try the tools by hand, without an agent:

```bash
python3 harness_engineering/tools/seed.py init --prefix DEMO --title "Demo workspace"
```

```bash
python3 scripts/_shared/chain.py new first_task "DEMO first task"
```

```bash
python3 scripts/_shared/chain.py seal --dry-run
```

Requirements: Python 3.8+ (standard library only) and git. Written and used with Claude Code, but nothing in it depends on a particular agent — any agent that can read Markdown and run commands can follow it.

## What is in this repository

```
harness_engineering/
├── README.md / README.ko.md            this document
├── QUICKSTART.md / QUICKSTART.ko.md    5-minute start (incl. Windows notes)
├── TEAM.md / TEAM.ko.md                rules for using it with more than one person
├── examples/ko_demo/                   a finished harness: planted with the tools, two sealed work items, a tested script
├── build_skill.md / build_skill.ko.md  the procedure the agent runs: conversation → harness
├── template/
│   ├── common/        language-independent: .gitignore, scripts/_shared/chain.py, envload.py
│   ├── en/            README.md, SKILL.md, .env.example, docs/README.md, docs/_templates/
│   └── ko/            the same in Korean
├── tools/seed.py      init (plant the seed) / check (blanks, required files, chain)
├── tests/property_test.sh   tries to violate the five properties and checks they hold
├── LICENSE (MIT), VERSION, CHANGELOG.md
```

### Common body and project slots

Every harness grown from this seed shares the same body; only the slots are filled from your conversation.

| Common (same in every harness) | Project slots (filled from the conversation) |
|---|---|
| the `docs/` system — six documents, ID tracing (R→P→I→L), two timelines | what the folder is for (purpose) |
| the five blockchain properties — sealing is final | how the agent addresses you, the title prefix |
| code location — `scripts/` first, then `vendor/{app}/` after verification | reality-check commands |
| the intent — keep context, sharpen the goal together, reach the goal | rules about targets and permissions |
| asking back when context blurs ("something seems off") | current state, remaining work, `.env.example` keys |
| the fixed report format | `vendor/` status |

## Roadmap

Automation here means **the agent works on its own and reports to a manager.** All three stages use `docs/` as their common interface.

| Stage | Name | What becomes automatic | Status |
|---|---|---|---|
| 1 | Harness engineering | one task, done by a person and an agent through the same procedure; context survives in documents and the chain | **this repository** |
| 2 | Loop engineering | one task, run by the agent on its own: reality check → REQ → … → HISTORY → `verify` passes → report | planned |
| 3 | Graph engineering | many tasks (and many harnesses) connected into a whole development process: HISTORY "remaining work" → the next REQ | planned |

## Feedback

This is an attempt to turn a way of working into something others can pick up and judge. If the structure is too heavy, if a property does not actually hold, if a step is unclear — please open an issue. That is the reason this is public.
