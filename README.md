# PawPal+

A Python and Streamlit pet care planner for multiple pets. Track feeding, walks,
medication, and appointments; filter daily schedules; complete recurring tasks;
and plan care within an available time budget.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
python -m streamlit run app.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.
The UI stores its Owner object in Streamlit session state. Data survives UI
reruns, but is not saved to disk and may be lost when the session ends.

## Features

- Add multiple pets and schedule feeding, walks, medication, or appointments.
- Edit a pending task's description, date, time, frequency, duration, and priority.
- View schedules by date, pet, and completion status.
- Complete tasks and automatically create the next daily or weekly occurrence.
- See conflict warnings and prioritize care within a total time budget.

## Implementation summary

`pawpal_system.py` contains four classes independent of the UI. `Task` and `Pet`
are dataclasses; `Owner` manages pets and exposes every `(pet, task)` pair through
`get_all_tasks()`. `Scheduler` uses that aggregate interface for every operation,
so all pets participate in scheduling. `main.py` verifies the backend without
Streamlit. `app.py` calls the same methods from forms and completion buttons.

See `diagrams/uml_draft.mmd` for the initial design and
`diagrams/uml_final.mmd` for the implemented architecture.

## Smarter Scheduling

| Feature | Method | Behavior |
| --- | --- | --- |
| Chronological sorting | `Scheduler.sort_by_time()` | Date then normalized HH:MM; stable for ties |
| Filtering | `Scheduler.filter_tasks()` | Optional pet name, completion status, and date |
| Conflict warnings | `Scheduler.detect_conflicts()` | Groups pending tasks at the same date and time across all pets |
| Editing | `Scheduler.update_task()` | Validates changes before replacing a pending occurrence; preserves its ID |
| Recurrence | `Scheduler.mark_task_complete()` | Creates a distinct pending task 1 or 7 days after the original due date |
| Priority and time budget | `Scheduler.build_plan()` | Greedily selects high, medium, then low priority tasks that fit; returns chosen and skipped tasks |

Completing an already completed occurrence creates no additional tasks. Use the
Scheduler completion method to generate recurrence; `Task.mark_complete()` alone
only changes the status. Recurrence advances from the scheduled date, including
for overdue tasks, and creates one occurrence at a time.

Conflict detection compares exact start times, not overlapping durations. The
budget is total care time, not a calendar availability window. Plans preserve
entered start times and display warnings rather than automatically moving tasks.
The greedy budget algorithm favors priority and simplicity over maximizing task
count. Sorting costs O(n log n); filtering and recurrence lookup cost O(n).

## Demo Walkthrough

1. Enter the owner's name, then add Mochi and Luna using **Add pet**.
2. Schedule breakfast for Mochi at 08:00 with daily frequency. Schedule medication
   for Luna at 08:00 and a later walk for Mochi.
3. View that date's chronologically sorted schedule. A warning names both
   conflicting 08:00 tasks. Filter by pet or completion status.
4. Click **Complete** beside breakfast. The occurrence becomes complete; change
   the view date to tomorrow to see its pending replacement.
5. Open **Edit a pending task**, choose the task, change its duration or priority,
   and click **Save changes**. The schedule and budget plan reflect the saved edits.
   Completed occurrences stay locked to preserve their history.
6. Set available care minutes to see which pending tasks fit. High priority tasks
   are considered first; skipped tasks are named below the plan.

### Sample Output

`python main.py` uses a fixed demonstration date for reproducible output:

```text
Today's Schedule (2026-11-08)
08:00 | Mochi | Breakfast (10 min, medium)
08:00 | Luna  | Medication (5 min, high)
12:00 | Luna  | Grooming (20 min, low)
18:00 | Mochi | Evening walk (20 min, high)
WARNING: Conflict on 2026-11-08 at 08:00: Mochi: Breakfast; Luna: Medication
Pending Mochi tasks: 2
Breakfast completed; next occurrence: 2026-11-09 at 08:00
10-minute plan: Luna: Medication
Skipped for time budget: 2
```

## Testing PawPal+

```bash
python -m pytest
```

Tests cover completion, adding tasks, multi-pet chronological sorting, filters,
empty schedules, daily/weekly recurrence across year boundaries, repeat
completion, one-time tasks, conflicts, priority budgets, editing, and invalid inputs.

Verification results are recorded below after running the checks.

Successful run (Python 3.14.3; pytest 9.2.0):

```text
collected 20 items

tests/test_app.py ..                                                     [ 10%]
tests/test_pawpal.py ..................                                  [100%]

============================== 20 passed in 3.55s ==============================
```

The Streamlit AppTest adds two pets, submits a daily task, completes it, and
checks the next occurrence and retained session data. A second UI test edits a
task, submits another invalid edit, and checks that the valid data remains intact. In the Codex macOS sandbox,
Streamlit's table renderer timed out; the full suite passed outside the sandbox.
No real browser or manual usability test was performed.

Engineering confidence: **4/5 stars** for the implemented scope, supported by
these automated checks. Disk persistence, interval conflict detection, and
browser verification remain future improvements. Add your own confidence
assessment to the reflection after reviewing the app.

## Requirement audit and design review

See [REQUIREMENTS.md](REQUIREMENTS.md) for phase-by-phase evidence, design and
algorithm review, the test plan, and outstanding submission steps. The repository
was confirmed to be a public fork of the CodePath starter through the connected
GitHub account. Optional extensions are separate from the required six phases.
