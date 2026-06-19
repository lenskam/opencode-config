---
name: router-skill-template
description: Template for creating router skills that dispatch to domain sub-skills. Use when designing a new router skill or reviewing an existing one. Not for direct invocation — copy and adapt.
metadata:
  category: router
---

# Router Skill Template

## What is a Router Skill?

A router skill accepts broad inputs, classifies the work, then invokes the appropriate domain sub-skills via the `skill` tool. It does **not** implement logic directly — it dispatches.

### When to Create a Router Skill

- You have 5+ domain skills in a related area (e.g., WordPress, cloud services, e-commerce)
- Users often give vague intents that could map to multiple skills
- You need a single entry point that triages and dispatches

## Structure

```
skills/<domain>-router/
  SKILL.md              # This file — router logic
  references/
    decision-tree.md    # Optional: detailed routing decision tree
```

## Frontmatter

```yaml
---
name: <domain>-router
description: "One sentence: what inputs this accepts and which sub-skills it dispatches to."
metadata:
  category: router
---
```

The `metadata.category: router` marker is critical — it distinguishes this from process and domain skills.

## SKILL.md Sections

### 1. When to use

Describe what kinds of inputs trigger this router. Be explicit.

### 2. Inputs required

What the agent needs from the user (repo, intent, constraints).

### 3. Procedure

Three mandatory sub-steps:

#### 3a. Triage

Run a detection/classification step to identify what we're working with. Example: `detect_wp_project.mjs`, `package.json` inspection, directory scanning.

#### 3b. Classify

Map triage output + user intent to the sub-skills that should be invoked. Use a table:

| User says / mentions | Primary skill | When to invoke |
|---|---|---|

#### 3c. Invoke sub-skills

For each classified work area, invoke the skill:

```typescript
await skill({ name: "<sub-skill-name>" })
```

For multi-skill tasks, invoke ALL relevant skills before starting implementation.

### 4. Intent-to-Skill Mapping

A comprehensive keyword → skill(s) reference table. Front-load the most common keywords.

### 5. Verification

Steps to run after dispatching (re-run triage, run lint/tests).

### 6. Failure modes / Escalation

What to do when triage fails or routing is ambiguous. Include a fallback question.

## Example

See `wordpress-router` for a working implementation that dispatches to 15+ WordPress sub-skills.

## Checklist for Creating a Router Skill

- [ ] Frontmatter has `metadata.category: router`
- [ ] Includes a triage step (script or manual inspection)
- [ ] Has a classification table mapping intent → skills
- [ ] Shows `skill({ name: "..." })` invocation examples
- [ ] Handles multi-skill dispatch (load all relevant skills)
- [ ] Has a verification step
- [ ] Has an escalation path for ambiguous inputs
- [ ] Has a comprehensive keyword → skill mapping table
