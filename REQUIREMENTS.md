# PawPal+ requirement audit

This audit covers the required six phases of the supplied assignment. It
separates final artifacts from instructional workflow steps that cannot be
claimed retroactively.

## Phase-by-phase evidence

| Phase | Required deliverables | Evidence |
| --- | --- | --- |
| 1 — Design | Three actions; class responsibilities; draft Mermaid; dataclass-based architecture | `reflection.md` section 1; `diagrams/uml_draft.mmd`; `pawpal_system.py` |
| 2 — Core | Four working classes; owner-wide tasks; two pets and three differently timed tasks; CLI output; initial tests; docstrings | `Owner.get_all_tasks()` feeds Scheduler; `main.py` has two pets, four tasks, three distinct times and a deliberate conflict; README sample output; `tests/test_pawpal.py` |
| 3 — Integration | Backend imports; Owner in session state; pet/task forms call backend | `app.py`; `tests/test_app.py` |
| 4 — Algorithms | Sorting; filtering by pet/status; daily/weekly recurrence; conflicts; tradeoffs | `Scheduler.sort_by_time`, `filter_tasks`, `mark_task_complete`, `detect_conflicts`; CLI demo; README Smarter Scheduling; reflection section 2 |
| 5 — Verification | Completion/addition/sorting/recurrence/conflict tests; passing run; testing instructions and output; confidence rating | 20 tests; README Testing PawPal+; reflection section 4 |
| 6 — Final package | Scheduler-driven UI; warnings; final Mermaid; features; walkthrough; CLI output; completed reflection | `app.py`; `diagrams/uml_final.mmd`; README; `reflection.md` |

The starter README's additional task-editing requirement is implemented through
Scheduler.update_task() and the **Edit a pending task** form. Duration and
priority can be changed along with description, date, time, and frequency.

## Building blocks and design review

| Class | Information held | Responsibilities |
| --- | --- | --- |
| Task | Description, time, due date, frequency, duration, priority, completion, ID | Validate occurrence data and record completion |
| Pet | Name, species, task list | Store and add care tasks |
| Owner | Name, pets | Add pets and expose all `(pet, task)` pairs |
| Scheduler | Owner reference | Filter, sort, edit, complete with recurrence, warn about conflicts, build budget plans |

Design review identified the importance of a single owner-wide task interface.
Scheduler uses that interface for every lookup and algorithm. Pet task lists are
the source of truth; there is no duplicate global task list to keep synchronized.
Dates distinguish occurrences; IDs distinguish completion and editing targets.

Algorithm review retained readable linear task lookups rather than adding a
second ID index. For small household schedules, avoiding synchronization bugs is
more useful than optimizing that lookup. Time sorting is O(n log n), and conflict
grouping uses a dictionary rather than comparing every pair. Existing methods
are documented in README, including their limitations.

## Test plan and interpretation

1. **Entity changes:** Completing a task changes its status; adding a task stores
   it on its pet; blank descriptions, invalid times, and invalid options fail.
2. **Multi-pet schedules:** Tasks sort by date and normalized time; filters retain
   the correct pet/status/date combinations; empty owners return empty lists.
3. **Recurrence:** Daily/weekly completion creates a distinct pending occurrence
   on the same pet; year boundaries work; repeated completion creates no extra
   copies; one-time tasks do not recur.
4. **Conflicts and budgets:** Same-pet and cross-pet duplicate start times warn;
   different dates and completed tasks do not collide; high priorities receive
   budget first; a zero-minute budget selects nothing.
5. **UI and edits:** Forms retain pets in session state, create and complete tasks,
   and save valid edits. Invalid edits preserve the previous task. Completed
   occurrences cannot be edited, preserving completion history.

Assertions compare observable behavior (dates, statuses, task counts, chosen
items), rather than simply checking that a method ran. AppTest executes Streamlit
forms and reruns without requiring a real browser. It is not a manual visual
usability test. The full suite passed with macOS access outside the sandbox;
README records the actual output.

## Workflow transparency

The final implementation was generated directly rather than first committing a
stub-only version. The original local history has separate backend, UI, and
testing/documentation commits, but no initial skeleton-only commit. Rewriting
history to suggest otherwise would misrepresent the workflow.

Separate phase chats and a Source Control-tab commit generator were not used.
Design review, implementation, algorithm review, tests, and documentation were
handled in this conversation. Reflection describes that accurately. Personal
understanding and practicing the vocabulary aloud require the student's own
participation.

## Submission checklist

- Public fork: confirmed through connected GitHub metadata for
  `Amos-Isaya/ai110-module2show-pawpal-starter`, forked from CodePath's starter.
- Required code, diagrams, tests, README, reflection: present.
- Multiple meaningful commits: present, including the final implementation audit.
- Push: pending destination-specific user approval. Automatic approval review
  rejected publishing to the remote without that confirmation. After publishing,
  verify the final local HEAD matches remote main.
- Deadline: none was supplied, so on-time submission cannot be verified here.
- Course submission: the student must use the course's Submit button. No course
  submission session or button is available in this workspace.

Optional extensions are not prerequisites for the six phases. Priority budgeting
and readable CLI tables are included. JSON persistence and a multi-model prompt
comparison are not claimed.
