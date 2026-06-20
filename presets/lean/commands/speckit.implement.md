---
description: Execute the implementation plan by processing all tasks in tasks.md.
---

## User Input

```text
$ARGUMENTS
```

## Outline

1. Read `.specify/feature.json` to get the feature directory path.

2. **Load context**: `.specify/memory/constitution.md` and `<feature_directory>/spec.md` and `<feature_directory>/plan.md` and `<feature_directory>/tasks.md`.

3. **Authorization gate (before writing any code)**: summarize what will change and get the
   user's explicit go-ahead. Halt and ask if a task is ambiguous — don't improvise
   (human-in-the-loop: `/memory/human-in-the-loop.md`).

4. **Execute tasks** in order (only after authorization):
   - Complete each task before moving to the next
   - Mark completed tasks by changing `- [ ]` to `- [x]` in `<feature_directory>/tasks.md`
   - Halt on failure and report the issue

5. **Validate**: Verify all tasks are completed and the implementation matches the spec.
