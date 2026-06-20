"""Structural enforcement tests for the human-in-the-loop (HITL) framework.

These lock in Constitution Principle VI so the refactor cannot silently regress:
- every core command embeds a Human-in-the-Loop Contract,
- the consequential commands keep their named decision/approval gates,
- the bundled SDD workflow pauses at a gate after every phase and requires an
  explicit authorization gate before any code is written,
- the policy file is shipped (bundled) and seeded into a project's memory.

They read the source-of-truth assets directly (no network, offline-safe) per the
project's testing conventions.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
WORKFLOW_FILE = REPO_ROOT / "workflows" / "speckit" / "workflow.yml"
POLICY_TEMPLATE = REPO_ROOT / "templates" / "human-in-the-loop.md"
CONSTITUTION = REPO_ROOT / ".specify" / "memory" / "constitution.md"
PYPROJECT = REPO_ROOT / "pyproject.toml"

# The ten core commands (skills/agent personas) the refactor governs.
CORE_COMMANDS = [
    "analyze",
    "checklist",
    "clarify",
    "constitution",
    "converge",
    "implement",
    "plan",
    "specify",
    "tasks",
    "taskstoissues",
]


@pytest.mark.parametrize("command", CORE_COMMANDS)
def test_every_core_command_embeds_hitl_contract(command: str) -> None:
    """Each command must carry the self-sufficient HITL Contract block."""
    text = (COMMANDS_DIR / f"{command}.md").read_text(encoding="utf-8")
    assert "Human-in-the-Loop Contract" in text, (
        f"{command}.md is missing its 'Human-in-the-Loop Contract' block "
        "(Constitution Principle VI)."
    )
    # It must point at the single source of truth (or be explicitly self-sufficient).
    assert "human-in-the-loop.md" in text, (
        f"{command}.md should reference /memory/human-in-the-loop.md."
    )


def test_critical_commands_keep_named_gates() -> None:
    """The highest-stakes commands keep their specific decision/approval gates."""
    plan = (COMMANDS_DIR / "plan.md").read_text(encoding="utf-8")
    assert "Architecture Decision Gate" in plan

    implement = (COMMANDS_DIR / "implement.md").read_text(encoding="utf-8")
    assert "Implementation Approval Gate" in implement

    # Outward-facing / destructive writes must each gate before acting.
    for command in ("specify", "taskstoissues", "constitution", "converge"):
        text = (COMMANDS_DIR / f"{command}.md").read_text(encoding="utf-8").lower()
        assert "gate" in text and (
            "approval" in text or "confirmation" in text
        ), f"{command}.md lost its approval/confirmation gate."


def _load_workflow_steps() -> list[dict]:
    data = yaml.safe_load(WORKFLOW_FILE.read_text(encoding="utf-8"))
    return data["steps"]


def test_workflow_has_authorization_gate_before_implement() -> None:
    """`implement` (which writes code) must be immediately preceded by a gate."""
    steps = _load_workflow_steps()
    ids = [s.get("id") for s in steps]
    assert "implement" in ids, "workflow is missing the implement step"
    impl_index = ids.index("implement")
    assert impl_index > 0, "implement must not be the first step"
    preceding = steps[impl_index - 1]
    assert preceding.get("type") == "gate", (
        "the step before implement must be an approval gate"
    )
    assert preceding.get("id") == "confirm-implementation", (
        "expected a 'confirm-implementation' authorization gate before implement"
    )


def test_workflow_gates_every_phase_and_aborts_on_reject() -> None:
    """Every command phase is followed by a gate, and gates abort on reject."""
    steps = _load_workflow_steps()
    gates = [s for s in steps if s.get("type") == "gate"]
    assert gates, "workflow defines no gates"
    for gate in gates:
        assert gate.get("on_reject") == "abort", (
            f"gate {gate.get('id')} must abort on reject (non-skippable)"
        )

    # Each command step (except the final one) must be immediately followed by a gate.
    for i, step in enumerate(steps[:-1]):
        if "command" in step:
            nxt = steps[i + 1]
            assert nxt.get("type") == "gate", (
                f"command step {step.get('id')} must be followed by a review gate"
            )


def test_policy_template_is_shipped_and_bundled() -> None:
    """The policy file exists and is wired into the wheel bundle."""
    assert POLICY_TEMPLATE.exists(), "templates/human-in-the-loop.md is missing"
    body = POLICY_TEMPLATE.read_text(encoding="utf-8")
    # Sanity: it carries the core HITL vocabulary.
    for token in ("Decision Point", "Assumption Ledger", "approval gate", "advisor"):
        assert token.lower() in body.lower(), f"policy missing '{token}'"

    pyproject = PYPROJECT.read_text(encoding="utf-8")
    assert (
        "templates/human-in-the-loop.md" in pyproject
        and "core_pack/templates/human-in-the-loop.md" in pyproject
    ), "policy template is not force-included in the wheel build"


def test_init_seeds_policy_into_memory(tmp_path: Path) -> None:
    """`specify init` copies the policy into .specify/memory."""
    from typer.testing import CliRunner

    from specify_cli import app

    import os

    project = tmp_path / "hitl-seed"
    project.mkdir()
    old_cwd = os.getcwd()
    try:
        os.chdir(project)
        result = CliRunner().invoke(
            app,
            [
                "init",
                "--here",
                "--integration",
                "claude",
                "--script",
                "sh",
                "--ignore-agent-tools",
            ],
            catch_exceptions=False,
        )
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0, f"init failed: {result.output}"
    seeded = project / ".specify" / "memory" / "human-in-the-loop.md"
    assert seeded.exists(), "init did not seed .specify/memory/human-in-the-loop.md"


def test_constitution_has_hitl_principle() -> None:
    text = CONSTITUTION.read_text(encoding="utf-8")
    assert "Human-in-the-Loop Authority" in text, (
        "constitution is missing Principle VI"
    )
