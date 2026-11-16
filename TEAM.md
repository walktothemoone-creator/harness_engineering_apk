# Using it in a team — TEAM.md

**English** · [한국어](TEAM.ko.md)

A harness is a **single line of records**. Work numbers (`{date}_{seq}`) must run from 0 without gaps or duplicates, and every document points to the hash of the one before it. When several people are involved, keep these rules.

## 1. One harness folder = one writer at a time

- Only **one person (or agent) at a time** creates (`chain.py new`) and seals work items in a given harness folder.
- If two people run `new` on separate branches, both get the same number; after a merge `verify` fails with "sequence is used by several work items", and `docs/LEDGER.md` conflicts.
- Everyone else contributes **requests**: tell the writer in chat, drop a request document in `docs/inbox/`, or open an Issue.

## 2. Split the harness when the work splits

If two streams of work run at the same time, do not mix them in one harness: give **each stream its own harness folder**.

```
team-repo/
├── payments/          ← harness A (one owner)
│   ├── harness_engineering/  (the seed, not committed)
│   ├── README.md  SKILL.md  docs/  scripts/
└── reporting/         ← harness B (another owner)
    ├── harness_engineering/
    ├── README.md  SKILL.md  docs/  scripts/
```

Run `seed.py init` and `chain.py` inside each folder. Folders can read each other's `docs/history/` for context.

## 3. Handing over ownership

1. The current owner finishes and seals the work in progress (`seal --dry-run` → `seal` → "chain OK").
2. Update README "Current state" and "Remaining work".
3. Give the new owner the head hash (last line of `chain.py verify`).
4. The new owner runs `verify`, gets the same head, then starts.

## 4. With git

- A harness folder can live in git. `harness_engineering/` (the seed) and `.env` are already in `.gitignore`.
- Commit right after sealing: the commit becomes an outside reference for the head (the seal ledger itself lives inside `docs/`).
- Do not keep work branches open for long, and never open two branches on the same harness at once.

## 5. When numbers collide (recovery)

If a merge makes `verify` report a duplicated sequence:

1. Keep the work item that landed first.
2. Re-create the later one as a new work item: `chain.py new` → copy its request and results → note in its HISTORY "re-recorded after a branch merge, original work id …" → seal.
3. Leave the colliding files of the later branch out of the merge.

Never renumber a sealed document by hand — its hash breaks.

## 6. Recommended rollout

- Start with one or two people, each on **a multi-week piece of work they run alone**.
- Do not use it for one-day fixes (six documents per work item).
- Report friction as Issues.
