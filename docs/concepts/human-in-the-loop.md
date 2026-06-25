# Human-in-the-Loop (HITL) Framework

This document is the deliverable for the human-in-the-loop refactor of Spec Kit. It records
what changed and why, inventories every component, and explains how to verify and use the
new framework.

The operating contract itself lives in enforced places:

- **Policy (single source of truth):** [`.specify/memory/human-in-the-loop.md`](../../.specify/memory/human-in-the-loop.md)
  (this repo's active, self-governing copy), seeded from the distributable source
  [`templates/human-in-the-loop.md`](../../templates/human-in-the-loop.md).
- **Governance (binding gate):** Principle VI of [`.specify/memory/constitution.md`](../../.specify/memory/constitution.md).
- **Per-command enforcement:** a self-sufficient *Human-in-the-Loop Contract* block at the top
  of every command in [`templates/commands/`](../../templates/commands/), so the policy holds
  even if the standalone file is absent.

> **One sentence:** across every command, agent persona, and workflow, the AI is an analyst,
> advisor, and facilitator — it generates options, surfaces assumptions, and recommends; the
> **human chooses, validates, and decides**, and can override or redirect at any gate.

---

## Phase 1 — Discovery & Analysis

Spec Kit's "skills, agents, and workflows" map to three concrete asset types:

- **Commands (skills + agent personas):** the prompt templates in
  [`templates/commands/`](../../templates/commands/). Each is invoked as a slash command and,
  in handoffs/workflows, as an agent (`agent: speckit.plan`). These are where the AI makes
  choices.
- **Workflow:** [`workflows/speckit/workflow.yml`](../../workflows/speckit/workflow.yml) — the
  orchestrated specify → plan → tasks → implement cycle with review gates.
- **Templates & governance:** [`templates/*.md`](../../templates/) (spec/plan/tasks/checklist/
  constitution) and the constitution in `.specify/memory/`.

### Decision-sensitivity classification (the roadmap)

Components were categorized by the impact of the decisions they make, which set the
refactoring priority:

| Tier | Component | Why | Priority |
|------|-----------|-----|----------|
| **CRITICAL** | `plan` | Chooses architecture, tech stack, storage, structure — silently resolved every `NEEDS CLARIFICATION` with no human checkpoint | 1 |
| **CRITICAL** | `implement` | Writes code and creates files; only one conditional gate existed | 1 |
| **CRITICAL** | `specify` | "Make informed guesses", capped clarifications, and a "don't ask about these" list that silently decided auth/security/retention | 1 |
| **CRITICAL** | `taskstoissues` | Outward-facing: creates GitHub issues in a real repo with no preview/approval | 2 |
| **CRITICAL** | `constitution` | Infers governance values and overwrites the constitution | 2 |
| **HIGH** | `tasks` | Silently defaulted test strategy and MVP scope | 2 |
| **HIGH** | `converge` | Appends remediation tasks (a write) — previewed but not gated | 2 |
| **HIGH/strong already** | `clarify` | Already an interview; risk was treating recommendations as auto-applied | 3 |
| **MEDIUM/strong already** | `checklist` | Already asks clarifying questions; risk was silent fallback defaults | 3 |
| **LOW/strong already** | `analyze` | Already strictly read-only and advisory | 3 |

**Autonomous behaviors that bypassed confirmation (the gaps we closed):**

1. `specify` filled scope, auth, data-retention, and success-criteria gaps with unsurfaced
   "reasonable defaults".
2. `plan` self-resolved all architecture/tech decisions inside Phase 0 research.
3. `tasks` decided test strategy and MVP scope without asking.
4. `implement` created ignore files and wrote code with only a checklist-conditional pause.
5. `taskstoissues` created external issues without a preview/approval gate.
6. `constitution` inferred and wrote governance values without confirmation.
7. `converge` appended tasks after previewing, but with no explicit approval gate.

---

## Phase 5 — Refactoring Summary

| # | Component changed | Change |
|---|-------------------|--------|
| 0 | **`templates/human-in-the-loop.md`** (new) | Distributable source of the policy; bundled with templates and installed to `.specify/templates/` on `init`. |
| 1 | **`.specify/memory/human-in-the-loop.md`** (new) | Active single source of truth for this repo: roles, decision tiers, Decision Point format, Assumption Ledger, default handling, approval gates, authority. |
| 2 | **`constitution.md`** | Added Principle VI *Human-in-the-Loop Authority (NON-NEGOTIABLE)* (1.0.0 → 1.1.0); later expanded VI to encourage scanning code/docs/specs and web search before presenting options (1.1.0 → 1.2.0); updated Sync Impact Report + governance authority. |
| 3 | **`constitution-template.md`** | Added a recommended-baseline HITL principle for new projects. |
| 4 | **`commands/specify.md`** | HITL Contract; reframed "informed guesses/defaults" into a surfaced `[ASSUMED — confirm]` ledger; CRITICAL gaps become decisions; added a non-skippable approval gate before "ready". |
| 5 | **`commands/plan.md`** | HITL Contract; added an **Architecture Decision Gate** (options + pros/cons/risks + labeled recommendation) before any artifact is generated; research records human-approved decisions only. |
| 6 | **`commands/implement.md`** | HITL Contract; added a non-skippable **Implementation Approval Gate** before any file write; per-phase pause option; "I need more information" is a valid stop. |
| 7 | **`commands/tasks.md`** | HITL Contract; test strategy + MVP scope surfaced as labeled recommendations, not silent defaults. |
| 8 | **`commands/taskstoissues.md`** | HITL Contract; preview + explicit approval gate before creating any GitHub issue. |
| 9 | **`commands/constitution.md`** | HITL Contract; confirmation gate (version bump + diff + inferred values) before overwriting the constitution. |
| 10 | **`commands/converge.md`** | HITL Contract; explicit approval gate before appending convergence tasks. |
| 11 | **`commands/clarify.md` / `analyze.md` / `checklist.md`** | HITL Contract blocks reinforcing their already-advisory stance (recommendations are labeled, not auto-applied; fallbacks are surfaced). |
| 12 | **`spec-template.md`** | "Assumptions" upgraded to an **Assumptions & Decision Ledger** with `[STATED]` / `[ASSUMED — confirm]` / `[PENDING DECISION]` provenance tags. |
| 13 | **`plan-template.md`** | Added **Decision Points & Alternatives** table (auditable record of human-chosen architecture) + an Assumptions-pending-validation section. |
| 14 | **`workflow.yml`** | Non-skippable approval gate after **every** phase (`review-spec`, `review-plan`, `review-tasks`), a dedicated **`confirm-implementation`** authorization gate before code is written, and a final `accept-implementation` gate; `edit` option provides the reconsider/revise path. |
| 15 | **`pyproject.toml`** | Force-includes `templates/human-in-the-loop.md` into the bundled `core_pack` so the policy ships with the package. |
| 16 | **`init.py`** | `ensure_hitl_policy_from_template()` seeds `.specify/templates/human-in-the-loop.md` → `.specify/memory/human-in-the-loop.md` on `specify init` (idempotent; skips if present), with a `("hitl-policy", …)` tracker step. |
| 17 | **`integrations/base.py` + `agent-context` ext scripts** | The agent-context block (and the `update-agent-context` bash/PowerShell scripts) inject a *HITL Policy Enforcement* reminder pointing at `/memory/human-in-the-loop.md` (Principle VI), so every agent loads the policy. |
| 18 | **`presets/lean/commands/*`** | Propagated concise HITL lines into the bundled lean preset's `specify`, `plan`, `implement`, `tasks`, and `constitution` commands. |
| 19 | **`tests/test_human_in_the_loop.py`** (new) | 26 structural-enforcement tests locking in the invariants (every command embeds the contract; decision commands present a recommendation + custom path; named gates exist; the CRITICAL `confirm-implementation` gate is not a bare yes/no; workflow gates every phase and aborts on reject; policy is shipped + bundled; `init` seeds it; constitution carries Principle VI). |
| 20 | **`docs/concepts/differences-from-upstream.md`** (new) | Side-by-side comparison of this fork vs. upstream `github/spec-kit`. |

---

## Phase 5 — Component Inventory

Each entry lists: **Input required** · **Decision points (human approval)** · **Assumption
validation** · **Approval gates / bypass conditions**.

### `specify` (CRITICAL)
- **Input required:** problem/users/value, scope boundaries (in/out), hard constraints.
- **Decision points:** scope & boundaries, target users/permissions, security/privacy/auth,
  success criteria — raised as `[NEEDS CLARIFICATION]`/Decision Points.
- **Assumption validation:** every default written to the spec's ledger as `[ASSUMED — confirm]`.
- **Gate:** Approval Gate before the spec is declared "ready" (STATED vs. ASSUMED vs. PENDING
  shown). *Bypass:* none for CRITICAL; MEDIUM/LOW phrasing defaults proceed.

### `clarify` (advisory — interview)
- **Input required:** answers to ≤5 targeted questions, one at a time.
- **Decision points:** each question; recommendation is labeled, applied only on explicit "yes".
- **Assumption validation:** answers written back into the spec verbatim.
- **Gate:** inherent — every question pauses for the human. *Bypass:* early-termination signals.

### `plan` (CRITICAL)
- **Input required:** language/runtime, platform, hosting, data store, performance/scale,
  compliance constraints.
- **Decision points:** language & dependencies, storage, architecture/structure, testing
  approach, external deps — the **Architecture Decision Gate**.
- **Assumption validation:** Technical Context fields tagged; unresolved items `[ASSUMED — confirm]`.
- **Gate:** Architecture Decision Gate before Phase 0/1. *Bypass:* a field the human/spec
  already fixed (`[STATED]`).

### `tasks` (HIGH)
- **Input required:** approved spec + plan; optional test/scope preferences.
- **Decision points:** test strategy (TDD?), MVP scope — surfaced as recommendations.
- **Assumption validation:** ordering/dependency assumptions noted `[ASSUMED — confirm]`.
- **Gate:** workflow `review-tasks` gate; tasks.md is editable. *Bypass:* none silent.

### `analyze` (advisory — read-only)
- **Input required:** spec + plan + tasks present.
- **Decision points:** none auto-applied; severities are assessments; remediation is opt-in.
- **Assumption validation:** reports findings without modifying files.
- **Gate:** explicit approval required before any remediation edit. *Bypass:* n/a (read-only).

### `implement` (CRITICAL)
- **Input required:** authorization to write code; run-through vs. pause-per-phase preference.
- **Decision points:** none re-opened here; ambiguous tasks trigger "I need more information".
- **Assumption validation:** no new assumptions — follows approved artifacts.
- **Gate:** Implementation Approval Gate before any write; checklist gate; per-phase pause;
  confirm before destructive/outward actions. *Bypass:* none for the pre-write gate.

### `converge` (HIGH)
- **Input required:** spec + plan + tasks present; post-implement.
- **Decision points:** which findings become tasks (human selects a subset).
- **Assumption validation:** gap-type/severity shown as assessment.
- **Gate:** approval before appending to tasks.md. *Bypass:* if human declines all, writes
  nothing (advisory-only).

### `taskstoissues` (CRITICAL — outward-facing)
- **Input required:** confirmation of target repo + the issue set.
- **Decision points:** which issues to create / titles.
- **Assumption validation:** dedup preview (create vs. skip) shown first.
- **Gate:** approval before any issue is created; GitHub-remote-only guardrails remain.
  *Bypass:* none — outward action always gated.

### `constitution` (CRITICAL — governance)
- **Input required:** principle content; confirmation of inferred values + version bump.
- **Decision points:** principle wording, version bump level, ratification date.
- **Assumption validation:** inferred values shown `[ASSUMED — confirm]`.
- **Gate:** confirmation gate before overwriting the constitution. *Bypass:* none.

### `checklist` (advisory)
- **Input required:** answers to up to 3 (optionally 5) clarifying questions.
- **Decision points:** depth/audience/focus — asked, or fallback defaults surfaced.
- **Assumption validation:** "do not hallucinate scope"; fallbacks stated.
- **Gate:** inherent interview. *Bypass:* fallback defaults when interaction impossible (stated).

### Workflow `speckit` (orchestration)
- **Input required:** spec description, integration, scope (input form at entry).
- **Decision points:** every phase boundary.
- **Gates:** `review-spec`, `review-plan`, `review-tasks`, `confirm-implementation`, and
  `accept-implementation` — all offer **approve / edit / reject** (no CRITICAL gate is a bare
  yes/no). All `on_reject: abort`. `edit` pauses for the human to revise/step back, then
  `specify workflow resume`.

### Agent context (cross-cutting enforcement)
- **What:** the agent-context block emitted by
  [`integrations/base.py`](../../src/specify_cli/integrations/base.py) and the
  `agent-context` extension's `update-agent-context` scripts now append a *HITL Policy
  Enforcement* reminder.
- **Effect:** every agent that loads its context file is pointed at
  `/memory/human-in-the-loop.md` (Constitution Principle VI) for all decisions and user
  interactions — so the contract reaches even agents invoked outside the bundled workflow.

---

## Phase 4 — Testing Plan (verifying HITL enforcement)

The validation criteria and how to check each:

| Criterion | How to verify |
|-----------|---------------|
| No AI finalizes a CRITICAL decision without human input | Run `/speckit.plan` on a spec with an unspecified data store; confirm it **stops** at the Architecture Decision Gate with options + a labeled recommendation, and does **not** generate `research.md` until you answer. |
| All assumptions stated & require confirmation | Run `/speckit.specify "build a todo app"`; confirm the spec's Assumptions & Decision Ledger lists `[ASSUMED — confirm]` items and that auth/security appears as `[PENDING DECISION]`, not a silent default. |
| Outputs separate human choices from AI recommendations | Inspect any generated spec/plan: every material line is tagged `[STATED]`/`[ASSUMED — confirm]`/`[PENDING DECISION]`/`[RECOMMENDATION]`. |
| Workflows pause at approval gates | `specify workflow run speckit`; confirm it pauses at `review-spec`, `review-plan`, `review-tasks`, and `confirm-implementation`, and that **no files are written** before `confirm-implementation` is approved. |
| Gates are non-skippable | Confirm each gate's `on_reject: abort` halts the run; confirm `confirm-implementation` exists between `tasks` and `implement`. |
| User can override/redirect at any point | At any gate choose `edit`, modify the artifact, `specify workflow resume`; confirm downstream steps consume the edited file. |
| Outward actions gated | Run `/speckit.taskstoissues` against a GitHub remote; confirm a preview + approval prompt appears before any issue is created. |
| Governance binds it | Run `/speckit.analyze`; confirm a Principle VI violation (e.g., a plan that auto-selected a stack with no decision record) is flagged CRITICAL. |
| Invariants are regression-locked | Run `pytest tests/test_human_in_the_loop.py` — 26 structural tests assert every command embeds the contract, decision commands present a recommendation + custom path, named gates exist (and the CRITICAL `confirm-implementation` gate is not a bare yes/no), the workflow gates every phase and aborts on reject, the policy is shipped + bundled, and `init` seeds it. |

**Automated coverage (implemented):** [`tests/test_human_in_the_loop.py`](../../tests/test_human_in_the_loop.py)
asserts the `speckit` workflow contains a `confirm-implementation` gate immediately before
`implement` and a gate after each command step, that each `templates/commands/*.md` contains a
"Human-in-the-Loop Contract" heading, that the policy template is shipped and force-included in
`pyproject.toml`, and that `specify init` seeds the policy into `.specify/memory/`. These run
alongside the existing `tests/test_workflows.py` suite.

---

## Phase 4 — Usage Guide

### Mental model
You drive; the AI navigates. At every consequential fork it hands you a labeled map (options +
tradeoffs + its recommendation) and waits. Nothing CRITICAL happens without your "go".

### Running the full cycle
```bash
specify workflow run speckit
```
You will be prompted for the build description, then **paused at each gate**:
- **`review-spec`** — validate the Assumptions & Decision Ledger; optionally run `/speckit.clarify`.
- **`review-plan`** — confirm the "Decision Points & Alternatives" table reflects *your* choices.
- **`review-tasks`** — adjust MVP scope / test strategy.
- **`confirm-implementation`** — explicit authorization; **no code is written before this**.
- **`accept-implementation`** — accept or reject the result.

At any gate: `approve` to continue, `edit` to pause and revise the artifact then
`specify workflow resume <run_id>`, or `reject` to abort.

### Running commands individually
Each command embeds a **Human-in-the-Loop Contract** at the top stating its input
requirements, decision points, and gates. Expect to be asked, not assumed-for. Reading the
four provenance tags:

| Tag | Meaning | Your action |
|-----|---------|-------------|
| `[STATED]` | You said it | Nothing — it's grounded in your input |
| `[ASSUMED — confirm]` | AI filled a gap | Confirm or correct it |
| `[PENDING DECISION]` | CRITICAL choice awaiting you | Answer it (blocks dependent work) |
| `[RECOMMENDATION]` | AI advice, not applied | Accept, modify, or decline |

### Opting out / tuning
- Projects that want lighter ceremony can keep or relax Principle VI in their own
  constitution (the constitution template marks the HITL principle as an adaptable baseline).
- Every artifact is a plain editable file — edit it directly and it becomes the source of truth.

---

## Scope

This refactor covers the **canonical core** — `templates/commands/*.md`, `templates/*.md`,
`workflows/speckit/workflow.yml`, the constitution + new policy file — plus the distribution
and enforcement wiring around it.

**Completed (initially scoped as follow-ups):**

1. ✅ **Auto-seed the policy on `init`.** `ensure_hitl_policy_from_template()` in
   [`src/specify_cli/commands/init.py`](../../src/specify_cli/commands/init.py) mirrors
   `ensure_constitution_from_template` (copy `.specify/templates/human-in-the-loop.md` →
   `.specify/memory/human-in-the-loop.md`, skip if present, warn if template missing), with a
   `("hitl-policy", …)` tracker step.
2. ✅ **Propagate HITL into the bundled lean preset.** `presets/lean/commands/` carries concise
   HITL lines on `specify`, `plan`, `implement`, `tasks`, and `constitution`. All presets and
   extensions also inherit Principle VI via the constitution.
3. ✅ **Structural tests.** [`tests/test_human_in_the_loop.py`](../../tests/test_human_in_the_loop.py)
   asserts the `speckit` workflow has a `confirm-implementation` gate immediately before
   `implement`, that each core command file contains a "Human-in-the-Loop Contract" heading,
   that the policy is shipped + bundled, and that `init` seeds it.

**Preset coverage (final state):**

- **`lean`** — the only *bundled/distributed* preset (force-included in `pyproject.toml`). Its
  `specify`, `plan`, `implement`, `tasks`, and `constitution` commands carry concise HITL lines.
- **`scaffold`** — an in-repo authoring example, not distributed. Its functional
  `speckit.specify.md` carries the same concise HITL line so the example models the project's
  own NON-NEGOTIABLE Principle VI. Its `speckit.myext.myextcmd.md` is a "replace-with-your-own"
  placeholder and is intentionally left uninstrumented.
- **`self-test`** — test fixtures (content asserted by `tests/test_presets.py`), not a real
  workflow; intentionally left as-is.

All presets and extensions additionally inherit Principle VI at runtime via the constitution and
the agent-context HITL-enforcement injection, so the policy reaches them even where a command
file does not embed the contract verbatim.
