# PLAYBOOK — how this work is done, and how it gets better

`docs/` records what happened. This file records **the best way we currently know** to do the work here. The agent reads it before every task (SKILL step 1) and updates it after every task (SKILL step 9). It is outside the chain, so it is edited freely; every change names the work history (HIST ID) it came from, so the reason is always traceable.

## 1. Recurring work — the current method

| Work | Method now (steps, in plain words) | Tool | Level (with the HIST ID that proved it) | History of levels (HIST IDs) |
|---|---|---|---|---|

Level — raise it only on evidence from a finished work item, and at most one level per work item. A level counts only after a **real run** of the work used it (building a tool is not yet level 3; the first real run with it is). Next to the level, say what it still does not cover.

| Level | Meaning |
|---|---|
| 1 Recorded | done once and recorded; the method is not yet proven to repeat |
| 2 Repeatable | the method is written here and the next run followed it |
| 3 Tooled | a shared script in `scripts/_shared/` does the main part |
| 4 Checked | automatic checks (tests, validations) guard the result |
| 5 Self-running | the agent runs it alone and reports (loop stage) |

## 2. Quality bar — what "done well" means here

Every check made before reporting a task as done belongs here — the standing checks from the first run on, not only those added after a mistake. Add a check when a mistake slipped through; never remove one silently.

| Check | Why (the work history it came from) |
|---|---|

## 3. Lessons

Describe the change in words; do not point at step numbers of the method, which change.

| Date | From | What happened | What we changed |
|---|---|---|---|

## 4. Improvement candidates

What is still done by hand, slow or error-prone. The user chooses which becomes a work item. Offer first the ones that could make a result wrong. When one is done, move it to the "Done" list with its HIST ID instead of deleting it.

| Candidate | Seen in | Expected gain |
|---|---|---|

Done:
