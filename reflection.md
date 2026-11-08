# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

---

## Implementation evidence for reviewing the prompts

These notes describe the AI-assisted implementation in this session. They are
not personal reflection answers; review the code and add your own experience
under the prompts above before submission.

- **1a — Core actions and design:** Add multiple pets, schedule care tasks, and
  view/complete daily care. Owner aggregates pets, Pet stores tasks, Task holds
  occurrence data, and Scheduler owns cross-pet scheduling algorithms.
- **1b — Design change:** The final model adds due dates and unique occurrence
  IDs to support recurrence safely. Completion through Scheduler creates the
  replacement on the original pet. The draft and final diagrams show the change.
- **2a — Constraints:** The planner considers date, completion status, task
  priority, and total available care minutes. Schedule views additionally filter
  by pet. No owner preference engine was implemented.
- **2b — Tradeoffs:** Exact-start conflict checks are easy to explain but miss
  partially overlapping activities. A greedy priority budget is readable but
  does not guarantee the maximum possible number of tasks.
- **3a — AI use:** Codex read the assignment and starter files, implemented the
  backend and Streamlit integration, created diagrams, and drafted tests and
  documentation in this conversation. Separate phase chats were not used.
- **3b — Judgment:** No user rejection of an AI suggestion has been recorded.
  Add an actual example after reviewing the implementation. Do not claim the
  generated code was manually verified until you have reviewed it yourself.
- **4a — Verification:** Tests exercise sorting across pets, recurrence,
  idempotent completion, conflicts, filters, budgets, and validation. The CLI
  provides visible examples of the same backend operations.
- **4b — Confidence:** Set your own 1–5 star rating after reviewing the test
  results in README. Next checks could include real browser interaction,
  overlapping durations, persistence, and timezone-aware scheduling.
- **5 — Personal reflection:** Explain what you learned and what you would
  improve after running the app. These answers should reflect your experience.
