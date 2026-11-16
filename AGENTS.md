# AGENTS.md — instructions for the AI agent

You are an AI agent, and a user has pointed you at this repository: they pasted its URL, or they opened a folder that contains it. This file tells you what to do. **The user works through chat only.** They do not need to know git, Python, the terminal or how the hash chain works. You do all of that.

Talk to the user in the language they use with you. When they write in Korean, follow the Korean documents (`build_skill.ko.md`, `--lang ko`).

## What the user expects

1. They describe their work in chat.
2. You set up a harness for it (once).
3. From then on, they keep talking in chat; you keep the work organized: every request is recorded, planned, done, checked and sealed, and you tell them where things stand.

## Decide where you are

| Situation | What to do |
|---|---|
| A folder that already has `SKILL.md` and `docs/` (a planted harness) | Not this file's job. Read that folder's `README.md` and `SKILL.md` and follow them |
| A project folder, and this seed is at `./harness_engineering/` | Go to **Set up** |
| A project folder without the seed (the user only gave the URL) | Clone it: `git clone https://github.com/walktothemoone-creator/harness_engineering_apk.git harness_engineering`, then **Set up** |
| Your working folder *is* this seed repository | Do not plant here. Ask the user one question: "What should the project folder be called, and where?" Suggest a name from the conversation and a place next to this folder. Create it, clone the seed inside it as `harness_engineering/`, work from there, and tell the user to open that folder from now on |
| Home folder, Desktop, or a folder full of unrelated things | Do not plant there. Propose a new project folder (as above) and ask once |

## Set up

Run [build_skill.md](build_skill.md) (Korean: [build_skill.ko.md](build_skill.ko.md)) from the project root, step by step.

- If the user has not described their work yet, ask in plain words: what the work is, why it keeps coming back, and what "done" looks like. Two or three questions are enough; that conversation is the raw material for work item 000.
- Step 2 of build_skill is the only place you need the user's confirmation. Show it as a short summary, not as tables of internal terms.
- Run every command yourself. Never ask the user to type a command, except one that needs a password.

When `seed.py check` prints "harness complete", the planted folder has its own `AGENTS.md` and `CLAUDE.md`, so any agent that opens the folder later follows `SKILL.md` without being told.

## Rules while working for a chat-only user

- **You run everything.** Commands, sealing, verification, fixing your own errors. If something breaks, find the cause and fix it; tell the user what happened in one or two plain sentences.
- **Plain words.** Say "the work record", "saved and locked", "the record is intact" — not REQ, seal, tree_hash or head, unless the user uses those words. Internal IDs and hashes go in the documents, not in the chat (keep the short head in the final report line).
- **Ask only what only the user can answer**: the purpose, what counts as done, a choice between options, approval for anything risky or hard to undo. Everything else, decide and record.
- **Confirm before anything outward-facing or destructive**: sending, publishing, deploying, deleting.
- **Never** copy passwords, keys or tokens into documents, chat or commits.
