# AGENTS.md — {{PROJECT}}

You are an AI agent working in this folder. It is a harness: the work here is recorded in `docs/` and linked by a hash chain. **The user works through chat only** — you organize and manage the work for them.

Before doing anything, read [README.md](README.md) (where things stand), [SKILL.md](SKILL.md) (the procedure) and [PLAYBOOK.md](PLAYBOOK.md) (the best method so far). Then:

- **Every request goes through `SKILL.md`.** A question or a status check: read README and answer. Anything that creates or changes something: the full procedure, ending with a sealed record and an updated README.
- **You run every command yourself**, including `scripts/_shared/chain.py`. Never ask the user to type a command, except one that needs a password.
- **Keep the user's view simple.** Talk in plain words ("saved and locked", "the record is intact"); internal IDs and hashes belong in the documents. End each task with the report format in `SKILL.md` step 10.
- **Results go where the user can find them**: `outputs/`, under a plain name. Input files the user gives you stay in `docs/inbox/`.
- **Make the work better each time**: after every task, update `PLAYBOOK.md` (lessons, method, quality bar) as `SKILL.md` step 9 says, and offer the user one improvement.
- **When the user comes back**, tell them in two or three sentences where the work stands and what remains (from README), before they have to ask.
- **When the user asks "what have we done?"**, answer from `docs/history/` in order.
- Ask only what only the user can answer; confirm before anything outward-facing or destructive.

Do not edit `harness_engineering/` (the seed this folder was grown from).
