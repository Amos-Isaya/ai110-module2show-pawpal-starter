# PawPal+ Project Reflection

This reflection is based on the AI-assisted work and requirement review in this
session. Codex implemented the code and ran the automated checks. I still need
to review the application myself before final submission.

## 1. System Design

**a. Initial design**

The three main actions for PawPal+ are adding a pet, scheduling a care task, and
viewing or completing today's tasks. The design uses four classes: Owner, Pet,
Task, and Scheduler. Owner manages multiple pets and provides access to all their
tasks. Pet stores a pet's name, species, and tasks. Task represents one activity,
including its time, date, duration, priority, frequency, and completion status.
Scheduler organizes tasks across the owner's pets.

The UML shows an Owner connected to multiple Pets, each Pet connected to its
Tasks, and Scheduler connected to Owner. Keeping scheduling in a separate class
allows the same logic to work in both the CLI demo and Streamlit UI.

**b. Design changes**

The final design includes a due date and unique ID for each task occurrence.
Time alone would not distinguish today's breakfast from tomorrow's breakfast.
The ID also lets a completion button identify the correct task.

Recurring task completion is handled by Scheduler.mark_task_complete(). It marks
the original occurrence complete and adds a new pending occurrence to the same
pet. Repeated completion does not create more copies. The final UML includes
these methods and attributes. A later requirements audit also added
Scheduler.update_task() so the UI can edit pending occurrences. It validates a
replacement before changing the stored task, preserving the original data when
an edit is invalid.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers task dates, times, completion status, priorities, and
the owner's available care minutes. Users can filter the schedule by pet and
status. The budget planner considers high priority tasks first, followed by
medium and low priority tasks, and selects tasks whose durations fit the
remaining budget. It displays the chosen tasks chronologically.

These constraints support the main goal of organizing daily pet care. A general
owner preference system was not implemented. The available minutes represent a
total care-time budget rather than specific free periods on a calendar.

**b. Tradeoffs**

Conflict detection checks for identical dates and start times. This keeps the
algorithm understandable and provides useful warnings, but it misses tasks that
start at different times and overlap because of their durations. For example,
a 30-minute walk at 08:00 and feeding at 08:15 are not flagged.

The budget planner also uses a greedy algorithm. It favors priority and
readability, but does not guarantee the largest number of completed tasks. Both
choices are reasonable for a small first version, provided the limitations are
clearly documented.

## 3. AI Collaboration

**a. How I used AI**

I provided the assignment to Codex in the project workspace. Codex inspected the
starter files, implemented the Python classes and Streamlit integration,
generated Mermaid UML diagrams, created tests, and updated the documentation.
File editing and terminal execution were useful because the implementation
could be checked against actual CLI output and test results.

My follow-up request, "show me the requirements," was especially useful. It
shifted the conversation from a general completion claim to a specific checklist
of completed and remaining work. Separate chat sessions were not used for the
individual phases, so I cannot claim that workflow helped organize this build.
A future attempt could separate design, implementation, and verification more
clearly while keeping the requirements available in each phase.

**b. Judgment and verification**

I did not accept the AI's statement that everything was done without asking for
more detail. I asked whether everything had really been included and requested
the requirements. The resulting checklist identified unfinished personal
reflection, missing task editing, and pending repository and submission steps.
This showed why I need evidence for a completion claim.

Codex verified the implementation through the CLI demo and automated pytest
suite. The Streamlit test exercises adding pets, scheduling a daily task, and
completing it. These checks are useful evidence, but they do not mean I have
personally reviewed every method or tested the app in a real browser.

## 4. Testing and Verification

**a. What was tested**

The automated suite covers task completion and addition, chronological sorting
across pets and dates, filtering, empty schedules, daily and weekly recurrence,
year boundaries, repeated completion, one-time tasks, conflict detection,
priority budgets, and invalid inputs. The UI integration tests check session state, recurring task completion, editing,
and invalid edit handling through Streamlit forms and buttons.

These behaviors matter because a scheduler can appear correct for one pet while
losing tasks from another pet, creating duplicate recurring tasks, or showing
completed tasks as pending. The CLI demo also provides readable evidence of
sorting, conflicts, filtering, recurrence, and budget planning.

**b. Confidence**

My provisional confidence rating is 4 out of 5 stars for the implemented scope,
based on the 20 passing automated tests reported in this session. The Streamlit
test initially timed out under the macOS sandbox; it and the full suite passed
when run outside that restriction.

Before increasing that rating, I would test the app in a real browser. Further
checks should cover overlapping durations, overdue recurring tasks, longer
sequences of user actions, and data persistence. Passing the current tests does
not establish that those additional capabilities exist.

## 5. Reflection

**a. What went well**

A strong part of the result is that the CLI and UI share one backend. The
multi-pet task interface keeps Scheduler from relying on a single pet, and the
tests provide concrete evidence for the main scheduling behaviors. The final
requirements checklist also made the remaining work visible.

**b. What I would improve**

In another iteration, I would save pets and tasks between sessions, add calendar exports, and detect
overlapping time intervals. Task editing was added during the final audit. I would also review
the code and use the browser interface myself before treating the assignment
as ready for submission. The current session state is useful during interaction,
but it is not permanent storage.

**c. Key takeaway**

The main takeaway from this project is that an AI-generated implementation still
needs human direction and verification. Being the lead architect includes
checking relationships in the UML, understanding algorithm tradeoffs, and asking
for evidence that each requirement is satisfied. Context engineering matters:
providing the assignment and project files gave the assistant a clear starting
point, while asking for a requirements checklist exposed gaps that a general
claim of completion missed.
