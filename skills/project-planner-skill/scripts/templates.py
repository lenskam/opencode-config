#!/usr/bin/env python3
"""
Template helpers for the project-planner-skill.

Provides reusable template strings and formatting functions for generating
features.md, user-journeys.md, phase files, and README_PHASES.md.

Usage:
    from scripts.templates import (
        render_features_doc,
        render_journeys_doc,
        render_phase_file,
        render_phases_index,
    )

    doc = render_features_doc(project_data, features, personas, constraints)
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def render_features_doc(
    project_name: str,
    project_description: str,
    project_type: str,
    personas: List[Dict[str, str]],
    mvp_features: List[Dict[str, Any]],
    secondary_features: List[Dict[str, Any]],
    constraints: Dict[str, str],
) -> str:
    """
    Generate the content for docs/dev/features.md.

    Args:
        project_name: Name of the project.
        project_description: 2-3 sentence description of the project.
        project_type: SaaS, mobile, landing page, API, e-commerce, full-stack.
        personas: List of dicts with keys 'name' and 'description'.
        mvp_features: List of dicts with keys 'name', 'description',
            'acceptance_criteria' (list of str), 'journey_name' (str).
        secondary_features: List of dicts with keys 'name', 'description', 'notes'.
        constraints: Dict with keys 'performance', 'security', 'infrastructure'.

    Returns:
        The complete markdown content for features.md.
    """
    lines: List[str] = [
        "# Features",
        "",
        f"## Project Overview",
        f"**{project_name}** — {project_type}",
        "",
        project_description,
        "",
        "## User Personas",
        "",
    ]

    for persona in personas:
        lines.append(f"- **{persona['name']}**: {persona['description']}")

    lines.extend(["", "## MVP Features (P0)", ""])

    for idx, feature in enumerate(mvp_features, 1):
        lines.append(f"### Feature {idx}: {feature['name']}")
        lines.append("")
        lines.append(f"- **Priority**: P0 (MVP)")
        lines.append(f"- **Description**: {feature['description']}")
        lines.append(f"- **Acceptance Criteria**:")
        for criterion in feature.get("acceptance_criteria", []):
            lines.append(f"  - {criterion}")
        if feature.get("journey_name"):
            lines.append(f"- **User Journey**: [Journey: {feature['journey_name']}](user-journeys.md)")
        lines.append("")

    if secondary_features:
        lines.append("## Secondary Features (P1)")
        lines.append("")
        for idx, feature in enumerate(secondary_features, 1):
            lines.append(f"### Feature {idx}: {feature['name']}")
            lines.append("")
            lines.append(f"- **Priority**: P1")
            lines.append(f"- **Description**: {feature['description']}")
            if feature.get("notes"):
                lines.append(f"- **Notes**: {feature['notes']}")
            lines.append("")

    lines.append("## Technical Constraints")
    lines.append("")
    lines.append(f"- **Performance**: {constraints.get('performance', 'TBD')}")
    lines.append(f"- **Security**: {constraints.get('security', 'TBD')}")
    lines.append(f"- **Infrastructure**: {constraints.get('infrastructure', 'TBD')}")
    lines.append("")

    return "\n".join(lines)


def render_journeys_doc(
    journeys: List[Dict[str, Any]],
) -> str:
    """
    Generate the content for docs/dev/user-journeys.md.

    Args:
        journeys: List of dicts with keys:
            - name (str): Journey name
            - feature (str): Feature name this journey maps to
            - persona (str): Persona name
            - trigger (str): What starts this journey
            - steps (list of dicts with 'action' and 'response')
            - success_criteria (list of str)

    Returns:
        The complete markdown content for user-journeys.md.
    """
    lines: List[str] = [
        "# User Journeys",
        "",
    ]

    for journey in journeys:
        lines.append(f"## Journey: {journey['name']}")
        lines.append("")
        lines.append(f"- **Feature**: {journey.get('feature', 'N/A')}")
        lines.append(f"- **Persona**: {journey.get('persona', 'N/A')}")
        lines.append(f"- **Trigger**: {journey.get('trigger', 'N/A')}")
        lines.append("")
        lines.append("### Steps")
        lines.append("")

        for step_idx, step in enumerate(journey.get("steps", []), 1):
            action = step.get("action", "")
            response = step.get("response", "")
            lines.append(f"{step_idx}. **{action}** — User does {{action}}. System responds with {{response}}.")

        lines.append("")
        lines.append("### Success Criteria")
        lines.append("")
        for criterion in journey.get("success_criteria", []):
            lines.append(f"- {criterion}")
        lines.append("")

    return "\n".join(lines)


def render_phase_file(
    phase_number: int,
    phase_name: str,
    goal: str,
    prerequisites: List[str],
    style: str,
    tasks: List[str],
    dependencies: Optional[List[str]],
    ai_skills: Optional[List[str]],
    checklist_items: List[str],
    expected_outputs: List[str],
    success_criteria: str,
    estimated_time: Optional[str] = None,
) -> str:
    """
    Generate a single PHASE_N.md file.

    Args:
        phase_number: The phase number (1-indexed).
        phase_name: Short name for the phase.
        goal: What the app will do after this phase.
        prerequisites: List of previous phases required.
        style: "incremental", "chronological", or "mixed".
        tasks: List of task descriptions.
        dependencies: List of dependency descriptions (e.g., "Task 2 requires Task 1").
        ai_skills: List of AI skills to apply. Defaults to standard set if None.
        checklist_items: List of checklist items.
        expected_outputs: List of expected output file paths.
        success_criteria: One sentence describing "done".
        estimated_time: Optional estimated time string.

    Returns:
        The complete markdown content for the phase file.
    """
    default_skills = [
        "/full-stack-orchestration-full-stack-feature",
        "/using-superpowers",
        "/workflow-orchestration-patterns",
        "/workflow-patterns",
    ]
    skills = ai_skills if ai_skills is not None else default_skills

    lines: List[str] = [
        f"# PHASE_{phase_number}: {phase_name}",
        "",
        f"**Goal**: {goal}",
        "",
    ]

    if estimated_time:
        lines.append(f"**Estimated time**: {estimated_time}")
        lines.append("")

    if prerequisites:
        prereq_names = ", ".join(prerequisites)
        lines.append(f"**Prerequisites**: {prereq_names}")
        lines.append("")

    lines.append(f"**Style**: {style}")
    lines.append("")
    lines.append("## Tasks")
    lines.append("")

    for task in tasks:
        lines.append(f"- [ ] {task}")

    lines.append("")
    lines.append("## Dependencies")
    lines.append("")
    if dependencies:
        for dep in dependencies:
            lines.append(f"- {dep}")
    else:
        lines.append("- None (tasks are independent)")

    lines.append("")
    lines.append("## AI-Specific Instructions")
    lines.append("")
    lines.append("When implementing this phase, the agent **must** apply the following skills:")
    lines.append("")

    for skill in skills:
        skill_name = skill.lstrip("/")
        if "full-stack-orchestration" in skill:
            desc = "Implement the full‑stack feature end‑to‑end (database → API → UI)."
        elif "using-superpowers" in skill:
            desc = "Use code generation for repetitive boilerplate and automated refactoring where safe."
        elif "workflow-orchestration-patterns" in skill:
            desc = "If any task involves multiple asynchronous steps, use a saga pattern."
        elif "workflow-patterns" in skill:
            desc = "Structure task execution as a pipeline (task A → B → C) with clear error handling."
        else:
            desc = "Apply this skill for specialized domain guidance."
        lines.append(f"- **{skill}** — {desc}")

    lines.append("")
    lines.append("## Completeness Checklist")
    lines.append("")

    for item in checklist_items:
        lines.append(f"- [ ] {item}")

    lines.append("")
    lines.append("## Expected Outputs")
    lines.append("")

    for output in expected_outputs:
        lines.append(f"- `{output}`")

    lines.append("")
    lines.append("## Success Criteria")
    lines.append("")
    lines.append(success_criteria)
    lines.append("")

    return "\n".join(lines)


def render_phases_index(
    project_name: str,
    phases: List[Dict[str, str]],
) -> str:
    """
    Generate README_PHASES.md index file.

    Args:
        project_name: Name of the project.
        phases: List of dicts with keys 'number', 'name', 'goal', 'style'.

    Returns:
        The complete markdown content for README_PHASES.md.
    """
    lines: List[str] = [
        "# Implementation Phases",
        "",
        f"## Overview",
        f"**{project_name}** — {len(phases)} phase(s)",
        "",
        "| Phase | Name | Goal | Style |",
        "|-------|------|------|-------|",
    ]

    for phase in phases:
        lines.append(
            f"| {phase['number']} | {phase['name']} | {phase['goal']} | {phase['style']} |"
        )

    lines.append("")

    return "\n".join(lines)


def format_date() -> str:
    """Return today's date as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")
