---
name: requirements-gatherer
description: >-
  Systematically elicit software project requirements through structured questions, 
  ensuring alignment with roadmap and necessities. Use when starting a new project,
  when requirements are vague, or before creating MASTER_IMPLEMENTATION.md.
license: MIT
compatibility: ["opencode"]
metadata:
  version: 1.0
  author: AI Assistant
  created: 2026-03-25
---

# Requirements Gatherer

This skill helps you (the user) or the AI to collect complete, actionable requirements for a software project. It ensures that nothing critical is missed and that the resulting plan aligns with the project's true needs.

## When to Use
- Starting a new project or major feature.
- When requirements are vague or missing.
- Before creating the `MASTER_IMPLEMENTATION.md` file.
- When the user says "I need a new feature" without details.

## Instructions for the Agent

1. **Read the current project state** if any: check `MASTER_IMPLEMENTATION.md`, `MASTER_TASK.md`, and existing code. This avoids re‑asking answered questions.

2. **Greet and set context**:
   - Explain that you'll ask a series of questions to understand the project.
   - Assure the user they can skip or defer any question.
   - Let them know the answers will be saved as an artifact in `docs/dev/artifacts/requirements-<timestamp>.md`.

3. **Ask questions in categories**. Use the template below, but adapt to the project type (web, API, mobile, etc.) based on initial user input.

4. **For each answer, record it** in a structured format (Markdown). After finishing, save the artifact.

5. **After gathering answers**, propose a high‑level plan (phases) based on the requirements, and update `MASTER_IMPLEMENTATION.md` accordingly.

6. **If the user already has a roadmap**, use the questions to validate and refine it.

---

## Question Categories

### 1. Project Overview
- What is the main goal of this project? (One sentence.)
- Who are the target users?
- What problem does it solve?

### 2. Functional Requirements
- List the core features (top 3–5).
- What are the user roles (if any)?
- What are the most important user workflows?

### 3. Non‑Functional Requirements
- Performance: expected users, response times?
- Security: authentication, authorization, data protection?
- Scalability: expected growth?
- Reliability: uptime, backup needs?
- Accessibility: any compliance (e.g., WCAG)?

### 4. Technical Constraints
- Preferred technologies (languages, frameworks, database)?
- Platform (web, mobile, desktop)?
- Integration with existing systems?
- Budget or hosting limitations?

### 5. Development Process
- Who will be involved (team size, roles)?
- Timeline: when is the MVP needed?
- How will it be deployed (CI/CD, manual)?

### 6. Risks & Uncertainties
- What are the biggest unknowns?
- What parts are most likely to change?

### 7. Success Criteria
- How will we know the project is successful?
- What metrics matter (e.g., user adoption, speed, cost)?

---

## Output Format

After gathering answers, produce a summary like:

```markdown
# Requirements Summary – <Project Name>

## Overview
[Goal, users, problem]

## Core Features
1. ...
2. ...

## Non‑functional Priorities
- Security: [high/medium/low] – details
- Performance: ...

## Technical Stack
- Frontend: ...
- Backend: ...

## Phases (Proposed)
1. Foundation: setup, auth, …
2. Core Features: …
3. Polish & Deploy

## Next Steps
- Create detailed tasks for Phase 1.
- Begin work after approval.
```

---

## Example Interaction

**User:** "I want to build a task management app for teams."

**Agent (using skill):**
"Great! Let's gather requirements. I'll ask a few questions to make sure we build the right thing.

1. **Core features** – what are the top 3 things the app must do?"
   *User: "Create projects, assign tasks, see progress."*
"Got it. 2. **Who are the users?**"
   *User: "Team leads and members."*
…

After collecting all answers, the agent saves the artifact and suggests a phased plan.

---

## Handling Project‑Specific Nuances

If the user mentions a specific domain (e.g., e‑commerce, healthcare, fintech), ask domain‑specific follow‑ups:
- **E‑commerce**: payment gateways, inventory management, shipping.
- **Healthcare**: compliance (HIPAA), patient data privacy.
- **Fintech**: regulatory requirements, transaction security.

Use the general categories as a base, then probe deeper based on the user's context.

---

## Integration with Master Files

After requirements are clear, create or update:
- `MASTER_IMPLEMENTATION.md` with phases and references to the requirements artifact.
- `MASTER_TASK.md` with initial tasks derived from the first phase.
- The agent then uses the plan/task management rules to execute.

---

## Notes
- If the user already has a document, you can read it and only ask for missing pieces.
- Always ask permission before saving anything.
- Keep the conversation interactive; don't dump all questions at once.
