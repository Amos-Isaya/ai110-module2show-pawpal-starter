# AI Interactions Log

## Agent Workflow

The user provided the complete PawPal+ assignment in Codex while the repository
contained only the starter UI and documentation. Codex implemented
`pawpal_system.py`, `main.py`, `app.py`, `tests/test_pawpal.py`, draft/final Mermaid
diagrams, and documentation.

The additional budget planner selects by priority within total available minutes.
It returns skipped tasks explicitly rather than silently removing them.
Verification includes the CLI demo, pytest, and Streamlit's AppTest. The final
suite contains 20 passing tests.
See README for actual results and limitations.

Human review remains necessary for personal reflection answers and final
submission. No multi-model comparison or separate phase chats occurred.

## Final requirement review

The user requested a complete check against the assignment. Codex added
`Scheduler.update_task()`, a Streamlit editing form, backend and UI editing tests,
a same-pet conflict test, and a fourth CLI task so the demo has three distinct
times plus an intentional conflict. It updated the final UML, README, reflection,
and requirement audit. The UI test exposed a widget-state problem during repeated
edits; stable widget keys fixed it. No user-performed manual code correction has
been recorded.

## Algorithm review

The final review considered indexing tasks by ID to speed up completion/edit
lookup. The implementation retains a linear scan through Owner.get_all_tasks()
for readability and to avoid keeping a second index synchronized with pet task
lists. Sorting uses Python's sorted() with a (date, HH:MM) lambda key. Conflict
detection groups tasks once by (date, time), avoiding pairwise comparisons.
Neither decision implies that the user manually rejected an AI code suggestion.
