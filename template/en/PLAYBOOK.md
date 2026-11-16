# PLAYBOOK — how this work is done, and how it gets better

`docs/` records what happened. This file records **the best way we currently know** to do the work here. The agent reads it before every task (SKILL step 1) and updates it after every task (SKILL step 9). It is outside the chain, so it is edited freely; every change names the work history (HIST ID) it came from, so the reason is always traceable.

## 1. Recurring work — the current method

| Work | Method now (steps, in plain words) | Tool | Level | Since |
|---|---|---|---|---|

Level — raise it one step at a time, only on evidence from a finished work item:

| Level | Meaning |
|---|---|
| 1 Recorded | done by hand each time, but recorded |
| 2 Repeatable | the method is written here and the next run followed it |
| 3 Tooled | a shared script in `scripts/_shared/` does the main part |
| 4 Checked | automatic checks (tests, validations) guard the result |
| 5 Self-running | the agent runs it alone and reports (loop stage) |

## 2. Quality bar — what "done well" means here

Checks made before reporting a task as done. Add a check when a mistake slipped through; never remove one silently.

| Check | Why (the work history it came from) |
|---|---|

## 3. Lessons

| Date | From | What happened | What we changed |
|---|---|---|---|

## 4. Improvement candidates

What is still done by hand, slow or error-prone. The user chooses which becomes a work item.

| Candidate | Seen in | Expected gain |
|---|---|---|
