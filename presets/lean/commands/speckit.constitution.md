---
description: Create or update the project constitution.
---

## User Input

```text
$ARGUMENTS
```

## Outline

1. Create or update the project constitution and store it in `.specify/memory/constitution.md`.
   - Project name, guiding principles, non-negotiable rules
   - Derive from user input and existing repo context (README, docs)
   - Confirm the version bump and any values inferred from repo context **before writing**
     (human-in-the-loop: `/memory/human-in-the-loop.md`).
