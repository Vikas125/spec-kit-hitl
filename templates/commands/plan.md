---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Human-in-the-Loop Contract

**This command makes the most consequential technical choices in the workflow. You are an
architect-advisor, not the decider.** Full protocol: `/memory/human-in-the-loop.md` (load IF
EXISTS; if absent, this block is self-sufficient).

- **Input you need from the human**: known constraints (language/runtime, platforms, hosting,
  data store, performance/scale targets, compliance). The `__SPECKIT_COMMAND_PLAN__` invocation
  message usually carries some ("I am building with…"); treat what's missing as input to
  request or to raise as a decision — not to invent.
- **Decision points (CRITICAL — present, recommend, do NOT auto-select)**: language &
  primary dependencies, storage/persistence, architecture & project structure, testing
  approach, and any third-party/external dependency. Each is resolved via the **Architecture
  Decision Gate** below before any design artifact is generated.
- **Assumptions**: anything you must assume to proceed goes into the plan's "Assumptions
  (pending validation)" section marked `[ASSUMED — confirm]`.
- **Approval gate**: the human approves the decision set **before** Phase 0/Phase 1 generate
  research, data model, and contracts. Do not generate design artifacts on top of unapproved
  CRITICAL decisions.

## Pre-Execution Checks

**Check for extension hooks (before planning)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_plan` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied). IF EXISTS, also load `/memory/human-in-the-loop.md`.

3. **Fill Technical Context**: Populate the Technical Context fields. For each field, mark its
   provenance: `[STATED]` if the human/spec gave it, or `[ASSUMED — confirm]` / `NEEDS
   CLARIFICATION` if you would otherwise be guessing. Do not paper over unknowns with
   plausible-sounding defaults.

4. **Architecture Decision Gate (CRITICAL — human approval required)**: Before any research or
   design artifact is produced, surface the consequential technical choices as Decision Points
   and **pause for the human's answers**. For each open CRITICAL field (language & primary
   dependencies, storage, architecture/project structure, testing approach, notable external
   dependencies), present:

   ```markdown
   ## Decision [N]: [e.g., Persistence layer]   ·   Sensitivity: CRITICAL

   **What's being decided**: [one sentence]   **Downstream impact**: [what Phase 0/1 + tasks depend on it]

   | Option | Description | Pros | Cons / Tradeoffs | Risks & Dependencies |
   |--------|-------------|------|------------------|----------------------|
   | A | ... | ... | ... | ... |
   | B | ... | ... | ... | ... |
   | C (Custom) | Provide your own | — | — | — |

   **Recommendation**: Option [X] — [rationale]. *(Recommendation only; nothing is chosen until you confirm.)*
   ```

    - Before presenting options, you SHOULD perform relevant research to ensure they are accurate, feasible, and contextual: scan the current codebase (configs, structure, existing code), read documentation and specs, and, when appropriate (e.g. comparing third-party libraries, checking package versions, or assessing security advisories), perform web searches. Record key findings (pros, cons, risks) in the option descriptions.
    - Skip a decision only when the human or spec already fixed it (record it as `[STATED]`).
   - Batch the decisions so the human can answer them together, but keep each individually
     answerable and editable. Wait for answers; do not self-resolve to keep moving.
   - Record every confirmed answer in the plan; record anything still unsettled but
     non-blocking as `[ASSUMED — confirm]`.

5. **Execute plan workflow** (only after the Architecture Decision Gate is resolved): Follow
   the structure in IMPL_PLAN template to:
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md — record the **human-approved** decisions and the
     alternatives that were considered (do not silently re-decide them)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_plan`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_plan` key.
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue to the Completion Report.
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Mandatory hook** (`optional: false`) — **You MUST emit `EXECUTE_COMMAND:` for each mandatory hook**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

## Completion Report

Command ends after Phase 2 planning. Report:
- Branch, IMPL_PLAN path, and generated artifacts
- The **decision set** the human approved at the Architecture Decision Gate (so it is on the
  record), plus any `[ASSUMED — confirm]` items still carried in the plan
- A reminder that the plan and its artifacts are editable, and that `__SPECKIT_COMMAND_TASKS__`
  should run only once the human is satisfied with the plan (the workflow's review-plan gate)

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen] — note whether `[STATED]` by the human or `[APPROVED]` at the
     Architecture Decision Gate; research MUST NOT overturn an approved decision without
     re-surfacing it to the human
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated, including the options shown at the gate]

**Output**: research.md in which every decision traces to a human-stated or human-approved
choice (no NEEDS CLARIFICATION silently self-resolved)

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Define interface contracts** (if project has external interfaces) → `/contracts/`:
   - Identify what interfaces the project exposes to users or other systems
   - Document the contract format appropriate for the project type
   - Examples: public APIs for libraries, command schemas for CLI tools, endpoints for web services, grammars for parsers, UI contracts for applications
   - Skip if project is purely internal (build scripts, one-off tools, etc.)

3. **Create quickstart validation guide** → `quickstart.md`:
   - Document runnable validation scenarios that prove the feature works end-to-end
   - Include prerequisites, setup commands, test/run commands, and expected outcomes
   - Use links or references to contracts and data model details instead of duplicating them
   - Do not include full implementation code, model/service/controller bodies, migrations, or complete test suites
   - Keep this artifact as a validation/run guide; implementation details belong in `tasks.md` and the implementation phase

4. **Agent context update**:
   - Update the plan reference between the `<!-- SPECKIT START -->` and `<!-- SPECKIT END -->` markers in `__CONTEXT_FILE__` to point to the plan file created in step 1 (the IMPL_PLAN path)

**Output**: data-model.md, /contracts/*, quickstart.md, updated agent context file

## Key rules

- Use absolute paths for filesystem operations; use project-relative paths for references in documentation and agent context files
- ERROR on gate failures or unresolved clarifications

## Done When

- [ ] Architecture Decision Gate completed — CRITICAL technical choices presented and approved by the human (not auto-selected)
- [ ] Plan workflow executed and design artifacts generated on top of approved decisions
- [ ] Assumptions surfaced as `[ASSUMED — confirm]`; no NEEDS CLARIFICATION silently self-resolved
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with branch, plan path, generated artifacts, and the approved decision set
