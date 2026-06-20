---
description: Create a plan and store it in plan.md.
---

## User Input

```text
$ARGUMENTS
```

## Outline

1. Read `.specify/feature.json` to get the feature directory path.

2. **Load context**: `.specify/memory/constitution.md` and `<feature_directory>/spec.md`.

3. **Before deciding the architecture**, present the key technical choices (tech stack,
   storage, structure) as options with a labeled recommendation and let the user choose —
   don't auto-decide. Before presenting, perform relevant research: scan codebase/docs/specs and search the web (human-in-the-loop: `/memory/human-in-the-loop.md`).

4. Create an implementation plan from the user's chosen decisions and store it in
   `<feature_directory>/plan.md`.
   - Technical context: tech stack, dependencies, project structure
   - Design decisions, architecture, file structure (recording what the user chose)
