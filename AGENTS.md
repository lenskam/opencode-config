Below is a production-grade `AGENTS.md` file for OpenCode.

# AGENTS.md – OpenCode Development Rules

This file defines how the AI agent should behave when working on this project. Follow these rules strictly for every request.

---

## Implementation Best Practices

### 0 — Purpose  
These rules ensure maintainability, safety, and developer velocity.  
**MUST** rules are enforced by CI; **SHOULD** rules are strongly recommended.

When writing rules or reviewing agent behavior, ensure these six areas are explicitly addressed:

| Area | What to Specify | Example |
|------|-----------------|---------|
| **Commands** | Full executable commands with parameters | `npm test`, `pytest -v`, `npm run build -- --watch` |
| **Testing** | Framework, location, coverage expectations | Jest in `tests/unit/`, 80% coverage required |
| **Project Structure** | Where code, tests, docs live | `src/` for code, `tests/` for tests, `docs/` for documentation |
| **Code Style** | Real code snippet showing formatting | Include a sample of properly formatted code |
| **Git Workflow** | Branch naming, commit format, PR requirements | `feature/xxx` branches, Conventional Commits |
| **Boundaries** | What the agent must never touch | `node_modules/`, `.env`, production configs |

**Rule**: If any of these six areas are ambiguous in the current project, ask the user for clarification before proceeding.

---

### 1 — Before Coding

- **BP-1 (MUST)** Ask the user clarifying questions.  
- **BP-2 (SHOULD)** Draft and confirm an approach for complex work.  
- **BP-3 (SHOULD)** If ≥ 2 approaches exist, list clear pros and cons.

---

### 2 — While Coding

- **C-1 (MUST)** Follow TDD: scaffold stub -> write failing test -> implement.  
- **C-2 (MUST)** Name functions with existing domain vocabulary for consistency.  
- **C-3 (SHOULD NOT)** Introduce classes when small testable functions suffice.  
- **C-4 (SHOULD)** Prefer simple, composable, testable functions.  
- **C-5 (MUST)** Prefer branded `type`s for IDs  
  ```ts
  type UserId = Brand<string, 'UserId'>   // ✅ Good
  type UserId = string                    // ❌ Bad
  ```  
- **C-6 (MUST)** Use `import type { … }` for type-only imports.  
- **C-7 (SHOULD NOT)** Add comments except for critical caveats; rely on self‑explanatory code.  
- **C-8 (SHOULD)** Default to `type`; use `interface` only when more readable or interface merging is required.  
- **C-9 (SHOULD NOT)** Extract a new function unless it will be reused elsewhere, is the only way to unit-test otherwise untestable logic, or drastically improves readability of an opaque block.

---

### 3 — Testing

- **T-1 (MUST)** For a simple function, colocate unit tests in `*.spec.ts` in same directory as source file.  
- **T-2 (MUST)** For any API change, add/extend integration tests in `packages/api/test/*.spec.ts`.  
- **T-3 (MUST)** ALWAYS separate pure-logic unit tests from DB-touching integration tests.  
- **T-4 (SHOULD)** Prefer integration tests over heavy mocking.  
- **T-5 (SHOULD)** Unit-test complex algorithms thoroughly.  
- **T-6 (SHOULD)** Test the entire structure in one assertion if possible  
  ```ts
  expect(result).toBe([value]) // Good

  expect(result).toHaveLength(1); // Bad
  expect(result[0]).toBe(value); // Bad
  ```
### 3.1 — Verification Loops

- **VL-1 (MUST)** After every significant code change (new function, modified API, refactor), run the relevant test suite before marking the task as complete.

- **VL-2 (SHOULD)** Use "red-green TDD" for new features:
  - Write a failing test (red)
  - Confirm the test fails
  - Implement the feature (green)
  - Confirm the test passes
  - Refactor if needed

- **VL-3 (SHOULD)** Before committing any change, run:
  - Linter/formatter checks
  - Unit tests for changed modules
  - Any integration tests that cover the changed area

- **VL-4 (SHOULD)** When a test fails, do not proceed to the next task until the failure is resolved. If resolution requires more than 3 attempts, pause and ask the user for guidance.
---

### 4 — Security & Privacy

- **S-1 (MUST)** Never log or save secrets, API keys, or credentials. If command output might contain them, sanitize or redact before storing as an artifact.
- **S-2 (MUST)** Use environment variables for all secrets. Do not hardcode them.
- **S-3 (SHOULD)** When asking the user for sensitive input (passwords, tokens), use masked prompts if supported.
- **S-4 (SHOULD)** Before saving command output or artifacts, scan for common secret patterns and warn the user if found.
- - **S-5 (MUST)** Run agents with minimal file permissions. Start in read-only mode (`Read`, `Grep`) and only grant write access after verification.

- **S-6 (SHOULD)** Never grant write access to production configuration files, secrets, or CI/CD pipelines without explicit human approval.

- **S-7 (SHOULD)** Log all tool calls, prompts, and outputs for any automated change. Store logs with the PR for post-incident analysis.

- **S-8 (MUST)** Before any destructive operation (deleting files, database migrations, deployment commands), the agent MUST:
  1. Display the exact command to be executed
  2. List the potential impact
  3. Wait for explicit user approval (not just a generic "yes")
 
#### 4.1 Boundaries and Constraints

##### Explicit "Do Not Touch" Zones

The following areas are **strictly off-limits** unless explicitly authorized:

- 🚫 **Never modify**: `node_modules/`, `vendor/`, `dist/`, `build/`, `.env` files, production configuration files
- 🚫 **Never commit**: API keys, passwords, tokens, or any secrets (even if commented out)
- 🚫 **Never delete**: User data, database records, or files outside the current workspace without confirmation
- 🚫 **Never run**: Commands that modify global system state (`sudo`, `rm -rf /`, `chmod 777`) without explicit approval

##### Ask-First Zones

The following operations require user approval before execution:

- ⚠️ **Database schema changes** (including migrations)
- ⚠️ **Adding new dependencies** (npm packages, pip packages, etc.)
- ⠀⚠️ **Modifying CI/CD configuration** (GitHub Actions, Jenkins, etc.)
- ⚠️ **Changes to authentication or security code**
- ⚠️ **Any operation that affects production or staging environments**

##### Always-Allowed Zones

The agent may freely operate in these areas without approval:

- ✅ Reading source code and documentation
- ✅ Running tests and linters
- ✅ Making code changes within `src/`, `app/`, `lib/` (subject to tests passing)
- ✅ Creating or modifying documentation in `docs/`
- ✅ Running development servers (local only)

### 5 — Database

- **D-1 (MUST)** Type DB helpers as `KyselyDatabase | Transaction<Database>`, so it works for both transactions and DB instances.  
- **D-2 (SHOULD)** Override incorrect generated types in `packages/shared/src/db-types.override.ts`. e.g. autogenerated types show incorrect BigInt value – so we override to `string` manually.

---

### 6 — Code Organization

- **O-1 (MUST)** Place code in `packages/shared` only if used by ≥ 2 packages.
- - **O-2 (SHOULD)** Use reference imports to reuse common guidelines:
  - Create `docs/dev/COMMON_RULES.md` for shared rules across multiple projects
  - Import them with `@docs/dev/COMMON_RULES.md` in your AGENTS.md
  - This reduces duplication and ensures consistency

- **O-3 (SHOULD)** Keep project-specific rules in this file, and shared rules in imported files.

---

### 7 — Tooling Gates

- **G-1 (MUST)** `prettier --check` passes.  
- **G-2 (MUST)** `turbo typecheck lint` passes.

#### 7.1 Model Selection Guidance

Different models excel at different tasks. The agent may suggest switching models when appropriate.

##### When to Suggest a Different Model

- **Planning & Architecture**: Use reasoning-focused models (e.g., Gemini, Claude Opus) for spec generation and complex planning
- **Code Generation**: Use code-specialized models (e.g., DeepSeek Coder, Claude Sonnet) for implementation
- **Debugging**: Use models with strong reasoning for error analysis
- **Simple Edits**: Any capable model works; speed may be prioritized

##### Cross-Checking Pattern

If a model struggles with a task:
1. Attempt a second time with clearer guidance
2. If still stuck, suggest trying a different model
3. Document which model worked best for each task type in `docs/dev/model-notes.md`

##### Model-Agnostic Rules

- Write rules and prompts that work across models when possible
- Avoid model-specific quirks or assumptions
- When a model hallucinates, explicitly note the correct information in the specification

---

### 8 — Git

- **GH-1 (MUST)** Use Conventional Commits format when writing commit messages: https://www.conventionalcommits.org/en/v1.0.0  
- **GH-2 (SHOULD NOT)** Refer to Claude or Anthropic in commit messages.
- - **GH-3 (SHOULD)** Before committing, ensure `prettier --check` and `turbo typecheck lint` pass. If tests are defined, run them as well.
- **GH-4 (SHOULD)** If a commit introduces changes that break tests, fix the tests before committing (do not commit broken tests).
- **GH-5 (SHOULD)** When merging, resolve conflicts locally and re‑run all relevant checks before pushing.

---

### 9 — Tool Usage

- **TU-1 (SHOULD)** Prefer built‑in OpenCode tools (`read_file`, `write_file`, `bash`) over custom ones unless they lack required functionality.
- **TU-2 (SHOULD)** When a tool fails, attempt a fallback (e.g., if `read_file` fails, check permissions and retry).
- **TU-3 (SHOULD)** After using `write_file`, immediately read the file back to confirm content was written correctly.
- **TU-4 (SHOULD)** Use `bash` with `--no-permission-ask` only when you are certain the command is safe; otherwise, rely on the permission system.

### 10 — MCP Integration (if applicable)
- If your project uses MCP servers, prefer using them over direct shell commands for supported operations (e.g., file system, GitHub, browser).
- When an MCP tool is available, use it; it often provides better error handling and security.

### 11 — Specification-First Development

- **SFD-1 (SHOULD)** Before implementing any significant feature, create a detailed specification document in `docs/dev/specs/` following this structure:
  - **Objective**: What problem does this solve? Who are the users?
  - **Requirements**: Bullet-point list of functional and non-functional requirements
  - **Constraints**: Technical limitations, dependencies, or boundaries
  - **Success Criteria**: How to verify completion (tests, metrics, acceptance criteria)

- **SFD-2 (SHOULD)** Use the specification as the "single source of truth" throughout development. When the spec changes, update it before changing code.

- **SFD-3 (SHOULD)** For complex features, use the following workflow:
  1. Generate spec with AI (in `plan` mode)
  2. Review and refine spec with user approval
  3. Generate technical plan from spec
  4. Break plan into tasks (update `MASTER_TASK.md`)
  5. Execute tasks incrementally

- **SFD-4 (SHOULD)** Save all specifications as artifacts in `docs/dev/specs/` with naming convention: `YYYY-MM-DD-feature-name-spec.md`

## Writing Functions Best Practices

When evaluating whether a function you implemented is good or not, use this checklist:

1. Can you read the function and HONESTLY easily follow what it's doing? If yes, then stop here.  
2. Does the function have very high cyclomatic complexity? (number of independent paths, or, in a lot of cases, number of nesting if if-else as a proxy). If it does, then it's probably sketchy.  
3. Are there any common data structures and algorithms that would make this function much easier to follow and more robust? Parsers, trees, stacks / queues, etc.  
4. Are there any unused parameters in the function?  
5. Are there any unnecessary type casts that can be moved to function arguments?  
6. Is the function easily testable without mocking core features (e.g. sql queries, redis, etc.)? If not, can this function be tested as part of an integration test?  
7. Does it have any hidden untested dependencies or any values that can be factored out into the arguments instead? Only care about non-trivial dependencies that can actually change or affect the function.  
8. Brainstorm 3 better function names and see if the current name is the best, consistent with rest of codebase.

**IMPORTANT**: you SHOULD NOT refactor out a separate function unless there is a compelling need, such as:
- the refactored function is used in more than one place
- the refactored function is easily unit testable while the original function is not AND you can't test it any other way
- the original function is extremely hard to follow and you resort to putting comments everywhere just to explain it

---

## Writing Tests Best Practices

When evaluating whether a test you've implemented is good or not, use this checklist:

1. SHOULD parameterize inputs; never embed unexplained literals such as 42 or "foo" directly in the test.  
2. SHOULD NOT add a test unless it can fail for a real defect. Trivial asserts (e.g., expect(2).toBe(2)) are forbidden.  
3. SHOULD ensure the test description states exactly what the final expect verifies. If the wording and assert don’t align, rename or rewrite.  
4. SHOULD compare results to independent, pre-computed expectations or to properties of the domain, never to the function’s output re-used as the oracle.  
5. SHOULD follow the same lint, type-safety, and style rules as prod code (prettier, ESLint, strict types).  
6. SHOULD express invariants or axioms (e.g., commutativity, idempotence, round-trip) rather than single hard-coded cases whenever practical. Use `fast-check` library e.g.  
   ```ts
   import fc from 'fast-check';
   import { describe, expect, test } from 'vitest';
   import { getCharacterCount } from './string';

   describe('properties', () => {
     test('concatenation functoriality', () => {
       fc.assert(
         fc.property(
           fc.string(),
           fc.string(),
           (a, b) =>
             getCharacterCount(a + b) ===
             getCharacterCount(a) + getCharacterCount(b)
         )
       );
     });
   });
   ```  
7. Unit tests for a function should be grouped under `describe(functionName, () => ...`.  
8. Use `expect.any(...)` when testing for parameters that can be anything (e.g. variable ids).  
9. ALWAYS use strong assertions over weaker ones e.g. `expect(x).toEqual(1)` instead of `expect(x).toBeGreaterThanOrEqual(1)`.  
10. SHOULD test edge cases, realistic input, unexpected input, and value boundaries.  
11. SHOULD NOT test conditions that are caught by the type checker.

---

## Code Organization (Specific to this Project)

- `packages/api` - Fastify API server  
  - `packages/api/src/publisher/*.ts` - Specific implementations of publishing to social media platforms  
- `packages/web` - Next.js 15 app with App Router  
- `packages/shared` - Shared types and utilities  
  - `packages/shared/social.ts` - Character size and media validations for social media platforms  
- `packages/api-schema` - API contract schemas using TypeBox

---


## Planning, Task Management, and Artifacts

### 0. Master Implementation Plan (`docs/dev/tasks/MASTER_IMPLEMENTATION.md`)

This file is the **high‑level roadmap** for the entire project. It outlines the major phases, milestones, and architectural decisions, and it links to detailed artifacts stored in `docs/dev/artifacts/`.

**Purpose**:
- Provide a single source of truth for the project’s overall structure and progress.
- Serve as a navigational index: each phase or significant step references the corresponding detailed plan, technical specification, or walkthrough saved as an artifact.

**Format** (Markdown):

```markdown
# Master Implementation Plan

## Project Overview
[Brief description of the project]

## Phases

### Phase 1: Foundation
- **Goal**: Set up the project skeleton and core infrastructure.
- **Detailed Plan**: [docs/dev/artifacts/2026-03-20_phase1-plan.json](artifacts/2026-03-20_phase1-plan.json)
- **Technical Spec**: [docs/dev/artifacts/architecture.md](artifacts/architecture.md)
- **Status**: Completed
- **Completion Date**: 2026-03-22

### Phase 2: Authentication
- **Goal**: Implement user authentication and session management.
- **Detailed Plan**: [docs/dev/artifacts/2026-03-23_auth-plan.json](artifacts/2026-03-23_auth-plan.json)
- **Technical Def**: [docs/dev/artifacts/auth-technical-spec.md](artifacts/auth-technical-spec.md)
- **Status**: In Progress
- **Notes**: [docs/dev/artifacts/auth-progress-walkthrough.md](artifacts/auth-progress-walkthrough.md)

### Phase 3: ...
```

**Rules**:
- The file **must** be created at the start of the project and updated whenever a new phase, major feature, or significant architectural change is introduced.
- Every phase should link to at least one artifact (plan, spec, walkthrough) stored in `docs/dev/artifacts/`.
- When a phase is completed, update its status and add a completion date.
- When a new task or fix is added that does not belong to an existing phase, create a new section (e.g., "Ad‑hoc Tasks") or update the relevant phase to include it.

---

### 1. Directories
- All task‑related files **MUST** be placed under `docs/dev/tasks/`.
- All artifact files **MUST** be placed under `docs/dev/artifacts/`.
- Create these directories if they don’t exist.

### 2. Master Task File (`docs/dev/tasks/MASTER_TASK.md`)

This file is the **single source of truth** for every task ever executed in the project. It tracks:
- Tasks from **planned work** (generated by the planning process).
- Tasks from **direct, unplanned changes** (e.g., quick fixes, refactors not derived from a plan).

**Format** (Markdown with YAML frontmatter for machine‑readable fields):

```markdown
---
# YAML frontmatter for easy parsing
tasks:
  - id: 1
    description: "Create authentication branch"
    status: completed
    created_at: 2026-03-20T10:00:00Z
    completed_at: 2026-03-20T10:05:00Z
    plan_id: auth-feature
    artifact: docs/dev/artifacts/2026-03-20_100500_auth-branch.log
  - id: 2
    description: "Fix login button styling"
    status: completed
    created_at: 2026-03-20T11:00:00Z
    completed_at: 2026-03-20T11:15:00Z
    plan_id: (direct)
    artifact: docs/dev/artifacts/2026-03-20_111500_styling-fix.png
---
```

**Rules**:
- Every task **must** be appended to `MASTER_TASK.md` when it is created.
- For planned tasks, include the `plan_id` (the name of the plan file, e.g., `auth-feature`).
- For direct tasks, set `plan_id: (direct)`.
- Update the task status and `completed_at` when it finishes.
- Optionally add an `artifact` field pointing to any generated output.
- Keep the file in **reverse chronological order** (newest tasks last, or newest first – pick one and be consistent). I recommend newest last so that reading sequentially shows the project history.

### 3. Planning

#### 3.1 Before Starting Any Task
For any request that requires more than one step (or is complex), you **MUST** first create a detailed plan.

- Create a plan file in `docs/dev/tasks/` with a descriptive name, e.g., `auth-feature-plan.json`.
- The plan must be a JSON object with the following structure:
  ```json
  {
    "goal": "User's original request",
    "created_at": "ISO timestamp",
    "tasks": [
      {
        "id": 1,
        "description": "Step description",
        "status": "pending",
        "depends_on": [],   // ids of tasks that must be completed first
        "retries": 0
      }
    ]
  }
  ```
- Use the `plan_task` mental tool: think step by step, break down the goal into logical, sequential tasks.
- **Also, immediately append each task to `MASTER_TASK.md`** with status `pending` and the `plan_id` set to the plan file name (without extension). This ensures that all tasks are recorded centrally.
- If this plan represents a new phase or a major feature, **update `MASTER_IMPLEMENTATION.md`** to include a reference to it (add a phase entry or update an existing one).

#### 3.2 Presenting the Plan
After creating the plan, show it to the user and ask for approval before proceeding. Example:
```
I've created a plan:
1. [task 1]
2. [task 2] (depends on 1)
...
Do you approve? (yes/no)
```
Wait for user confirmation.

#### 3.3 Memory Across Sessions
- At the start of a session, **always** read `docs/dev/tasks/MASTER_TASK.md` and `docs/dev/tasks/MASTER_IMPLEMENTATION.md` to restore context.
- Keep a lightweight session log in `docs/dev/sessions/YYYY-MM-DD_HHMMSS.md` summarizing key actions, decisions, and artifacts created.
- Use the living document approach to capture important decisions so they are available to future sessions.

### 4. Task Management

#### 4.1 Task States
Each task can be in one of the following states:
- `pending` – not started yet  
- `running` – currently being executed  
- `completed` – finished successfully  
- `failed` – execution failed  
- `blocked` – waiting for dependencies  
- `retrying` – failed but will be retried

#### 4.2 Executing Tasks
- Always check the current plan file (e.g., `auth-feature-plan.json`) for the next actionable task (status `pending` and all dependencies completed).
- Before starting a task, update its status to `running` in both the plan file and in `MASTER_TASK.md`.
- After completing a task successfully, update its status to `completed` in both places, and set `completed_at` in `MASTER_TASK.md`.
- If a task fails:
  - Increment `retries` count in the plan file.
  - If retries < 3, set status to `retrying` and attempt again after a short wait.
  - If retries >= 3, set status to `failed` and stop the plan (notify user). Also update `MASTER_TASK.md` accordingly.

#### 4.3 Dependencies
- A task with `depends_on` cannot start until all those tasks are `completed`.
- When a task fails, any tasks that depend on it become `blocked` automatically (update them in the plan file and in `MASTER_TASK.md` if they are already listed there).

#### 4.4 Persistent State
- After every task status change, **immediately** write the updated plan JSON back to the plan file and update `MASTER_TASK.md`.
- At the start of a session, read `docs/dev/tasks/MASTER_TASK.md` to understand the project history and any incomplete tasks.

### 4.5 — Session Hygiene

- **SH-1 (SHOULD)** Keep sessions focused on a single objective. When the goal changes, explicitly state the new goal or start a fresh session.

- **SH-2 (SHOULD)** Every 30-60 minutes of active work, summarize what has been learned and what remains. Add this summary to `docs/dev/sessions/` for future reference.

- **SH-3 (SHOULD)** Use the "routefinding" pattern: before making changes, first locate the relevant files using `grep` or similar. Open only the 3-5 most relevant files rather than scanning entire directories.

- **SH-4 (SHOULD)** When working on large codebases (>100 files), use sub-agents or separate worktrees for different subsystems to avoid context overflow.

- **SH-5 (SHOULD)** At the start of each session, read the last session summary from `docs/dev/sessions/` to restore context.

### 5. Artifacts

#### 5.1 What to Save as Artifacts
Save any important output generated during your work, such as:
- Implementation plans (already in `docs/dev/tasks/`)
- Code snippets or generated files
- Analysis results, research summaries
- Walkthroughs or explanations
- Logs of command outputs
- Screenshots (for UI work)
- Technical definitions, specifications, or architecture diagrams

#### 5.2 Where and How to Save
- Save artifacts in `docs/dev/artifacts/`.
- Use the following naming convention:  
  `YYYY-MM-DD_HHMMSS_<description>.<ext>`  
  Example: `docs/dev/artifacts/2025-03-11_143022_authentication-plan.json`
- For artifacts related to a specific task, include the task ID in the description:  
  `docs/dev/artifacts/task-5_test-output.log`

#### 5.3 Creating an Artifact
When you have content to save:
1. Choose a descriptive filename.
2. Write the content to the file.
3. Optionally, append an entry to `docs/dev/artifacts/index.json` (if you want a catalog):
   ```json
   {
     "timestamp": "ISO",
     "filename": "docs/dev/artifacts/...",
     "description": "Brief description",
     "task_id": 5
   }
   ```
4. Inform the user: `"Saved artifact: docs/dev/artifacts/filename"`
5. If the artifact is the result of a task, link it in `MASTER_TASK.md` by adding the `artifact` field to that task.
6. If the artifact corresponds to a phase or major step in `MASTER_IMPLEMENTATION.md`, update that file with a reference.

#### 5.4 Retrieving Artifacts
If the user asks to see a past artifact, you can list the `docs/dev/artifacts/` folder or read `index.json` and display the content.

We'll add a new section **Reading Terminal Output** right after **Artifacts** (or before the retry section). This will guide the agent on how to handle command output, capture errors, and use it for decision‑making.

Insert this before **6. Retry and Recovery** (renumber subsequent sections accordingly).

---

### 6. Reading Terminal Output

When the agent runs a command (via `run_command`, `bash`, or any shell tool), it **must** treat the output as a critical part of the feedback loop.

#### 6.1 Capture Both stdout and stderr
- Always capture **stdout** and **stderr** separately.  
- If the tool does not provide separate streams, capture the combined output and note that both are included.

#### 6.2 Analyze Exit Codes
- Check the exit code (0 = success, non‑zero = failure).  
- If the exit code is non‑zero, treat the command as failed unless the user explicitly said failures can be ignored.  
- Log the exit code and any error messages for debugging.

#### 6.3 Handling Long Output
- If the output is very long (> 10,000 characters), **do not** embed it directly in the conversation context (it may be truncated or cause performance issues).  
- Instead:
  - Save the full output as an artifact in `docs/dev/artifacts/` (e.g., `command-output-YYYYMMDD_HHMMSS.log`).  
  - Summarise the key parts (first/last few lines, error messages, important data) in the conversation.  
  - Provide the artifact path for the user to inspect if needed.

#### 6.4 Extracting Information
- Parse the output to extract relevant information:  
  - Build errors: look for lines containing `error:`, `failed:`, `cannot find`, etc.  
  - Test results: identify passed/failed tests, stack traces.  
  - Data from commands: use grep, jq, or regex (in your reasoning) to extract specific values.  
- If the output contains structured data (JSON, XML, YAML), attempt to parse it and use the structured fields in subsequent steps.

#### 6.5 Using Output in Decision‑Making
- After reading the output, determine the next action:
  - If the command succeeded, proceed to the next task.  
  - If it failed, diagnose based on the error output.  
    - For known transient errors (e.g., network timeouts), retry (see **Retry and Recovery**).  
    - For permanent errors, ask the user for help or suggest a fix.  
- When proposing a fix, reference the specific error message to justify the change.

#### 6.6 Logging and Artifacts
- For every significant command (build, test, deployment), **automatically save the output** as an artifact.  
- Use the artifact naming convention: `docs/dev/artifacts/YYYY-MM-DD_HHMMSS_command-description.log`  
- Link the artifact in `MASTER_TASK.md` under the corresponding task, and if it relates to a phase, reference it in `MASTER_IMPLEMENTATION.md`.

#### 6.7 Example
```
> run_command: npm test
[stderr] FAIL test/auth.test.js
[stdout] 1 test failed, 3 passed

Agent reasoning:
- Exit code: 1 → failure.
- Error: "auth.test.js" failed.
- Save full output as artifact `docs/dev/artifacts/2025-03-24_143022_npm-test-failure.log`.
- Update task status to `failed`, increment retries.
- Propose fix based on the specific test failure.
```

This ensures that the agent remains fully aware of command results and can take appropriate action while keeping the conversation concise.


### 7. Retry and Recovery

- If a command fails due to transient issues (network, timeout), retry up to 3 times with exponential backoff.
- If a task fails permanently, update its status to `failed` in both the plan file and `MASTER_TASK.md`, and ask the user how to proceed (abort, skip, or retry manually).
- When resuming a session, always read `docs/dev/tasks/MASTER_TASK.md` to see the state of the project.
#### Error Handling & Escalation
- For a command failure, classify the error:
  - **Transient** (network timeouts, rate limits) → retry up to 3 times with exponential backoff.
  - **Recurring** (same error after retries) → stop and ask the user for guidance.
  - **Critical** (missing dependencies, invalid configuration) → stop immediately and explain how to fix.
- Always save the full error output as an artifact (see Artifacts section) and reference it when asking for help.
#### Failure Recovery Patterns

| Symptom | Likely Cause | Recovery Action |
|---------|--------------|-----------------|
| Agent "forgets" constraints mid-session | Context drift | Re-summarize constraints. Ask agent to repeat key rules. |
| Edits touch unrelated files | Scope creep | Reduce batch size to 5-10 files. Enable checkpoints. |
| Flaky tests block progress | Test instability | Stabilize tests first. Ask agent to fix only the test if needed. |
| Agent repeats same error | Misunderstanding | Provide explicit counter-example. Save correct pattern to rules. |
| Changes break existing functionality | Missing regression tests | Ask agent to run all tests before proceeding. Add tests for the broken case. |

When any failure pattern occurs:
1. **Stop** current execution
2. **Log** the failure with artifact
3. **Diagnose** using the table above
4. **Propose** a specific recovery action
5. **Ask** user for confirmation before proceeding

### 8. Pattern Recognition and Skill Creation

When the same issue recurs or the user frequently asks for similar actions, the agent **should** propose creating a new skill to automate or streamline the process.

#### 8.1 When to Propose a Skill
- **Repeated failures**: If the same command fails with the same error more than twice (after retries), it may indicate a recurring environmental problem that a skill could fix (e.g., a skill that sets up the environment correctly).  
- **Recurring user requests**: If the user gives similar instructions across different sessions (e.g., “run linter and fix issues”, “create a PR”), the agent should suggest packaging that sequence as a skill.  
- **Complex multi‑step tasks**: Any sequence of actions that the user performs frequently or that the agent itself executes repeatedly should be considered for a skill.

#### 8.2 How to Propose
When the agent detects a pattern, it should:
1. **Explain the pattern** to the user.  
   Example: *“I’ve noticed you often ask me to fix linting errors manually. This could be automated with a skill.”*
2. **Ask** if the user wants to create a skill.  
   Example: *“Would you like me to create a `fix-lint-errors` skill?”*
3. If the user agrees, **create the skill** in `.opencode/skills/<skill-name>/SKILL.md` with proper frontmatter:
   ```yaml
   ---
   name: fix-lint-errors
   description: Automatically run linter and fix common issues
   ---
   # Instructions for the agent when this skill is invoked
   Run `npm run lint` and automatically apply fixes where possible.
   If manual intervention is needed, explain the changes.
   ```
4. **Update `MASTER_IMPLEMENTATION.md`** to note that this skill was added (if it’s a project‑level enhancement).

#### 8.3 Skill Content Guidelines
- Use a clear, actionable description in the frontmatter.  
- Include step‑by‑step instructions that the agent can follow when the skill is loaded.  
- If the skill requires specific tools (e.g., `eslint`), mention them.  
- Keep the skill focused on a single, well‑defined task.

#### 8.4 Example
```
> run_command: npm run lint
[error] 15 linting errors found

Agent reasoning:
- This is the third time today the user has asked me to fix linting errors.
- The errors are similar each time.
- I’ll propose creating a skill.

Agent output:
“I see you’ve asked me to fix linting errors several times. I could create a `fix-lint-errors` skill that automatically runs the linter and applies safe fixes. Would you like me to do that?”
```

This proactive approach reduces repetitive work and builds a library of reusable skills over time.

### 9. Example Workflow

**User**: "Add user authentication to the Flask app."

**Agent**:
1. Check `MASTER_IMPLEMENTATION.md`. If a "Authentication" phase does not exist, add one with a reference to the detailed plan that will be created.
2. Create `docs/dev/tasks/auth-feature-plan.json` with tasks:
   - 1: Create branch (depends_on: [])
   - 2: Add login route (depends_on: [1])
   - 3: Add registration route (depends_on: [1])
   - 4: Write tests (depends_on: [2,3])
3. Append each task to `MASTER_TASK.md` with `plan_id: auth-feature` and status `pending`.
4. Show plan, ask approval.
5. After approval, execute task 1 (update to running → completed in both files).
6. Execute task 2 (running → if fail, retry → if still fail, mark failed and notify).
7. Save test output as artifact `docs/dev/artifacts/2025-03-11_..._test-output.log` and link it in `MASTER_TASK.md`.
8. If the authentication phase is completed, update `MASTER_IMPLEMENTATION.md` with its status and completion date.
9. Continue until all tasks done.
10. Report completion and list artifacts created.


Now the master implementation plan is integrated, and all tasks and artifacts are centralized under `docs/dev/`.

## Coding Assistant Guidelines (Claude‑inspired)

- **CA-1 (SHOULD)** After every significant code change, run the relevant tests or checks before marking the task as completed.
- **CA-2 (SHOULD)** Before finalising a plan, compare it with existing codebase patterns; if inconsistent, flag the inconsistency to the user.
- **CA-3 (SHOULD)** Split large tasks into smaller, independently verifiable steps. Deliver and verify each step before moving to the next.
- **CA-4 (SHOULD)** In your responses, show your reasoning explicitly, especially when diagnosing errors or planning complex changes. This helps the user follow your thought process.
- **CA-5 (SHOULD)** Use self‑consistency checks: after writing code, ask yourself “Does this make sense given the rest of the project?” If not, revise.

Add the following section to your `AGENTS.md` file. I recommend placing it **after the “Planning, Task Management, and Artifacts” section** (just before the “Living Document & Revision History” section) because it deals with the initial and final phases of a project.

---

## Requirements Gathering & Post‑Implementation Assessment

### When to Use the `requirements-gatherer` Skill

The skill `requirements-gatherer` (located in `.opencode/skills/requirements-gatherer/` or globally in `~/.config/opencode/skills/`) is the official way to systematically collect project requirements. It must be invoked in the following situations:

- **Before starting a new project** – to establish a clear understanding of goals, constraints, and priorities.
- **Before beginning a major new feature** – to ensure alignment with the overall roadmap.
- **When requirements are vague or missing** – the skill will ask targeted questions to fill gaps.
- **After completing a significant implementation** – to verify that the delivered work meets the success criteria defined earlier.

### How to Invoke the Skill

Use the `skill` tool with the skill name and (optionally) a context prompt. For example:

```typescript
await skill({
  name: "requirements-gatherer",
  parameters: {
    context: "New e‑commerce platform for a small business"
  }
});
```

If the skill is not available, fall back to the manual question list described in its `SKILL.md` file.

### What to Do with the Output

1. **Save the gathered requirements** as an artifact in `docs/dev/artifacts/requirements-<timestamp>.md`.
2. **Update the Master Implementation Plan** (`docs/dev/tasks/MASTER_IMPLEMENTATION.md`) with the newly defined phases and high‑level goals.
3. **Create initial tasks** in `docs/dev/tasks/MASTER_TASK.md` for the first phase.
4. **If used after implementation**:
   - Compare the delivered work against the success criteria captured during requirements gathering.
   - Note any gaps or misalignments.
   - Suggest corrective actions or open tasks.

### Example Use Cases

- **New project**: User says “I want to build a task management app.” Agent invokes the skill, collects requirements, then proposes a phased plan.
- **After deployment**: User says “We finished the MVP.” Agent runs the skill in assessment mode, compares outcomes to the original requirements, and reports success or missing pieces.
- **Vague request**: User says “Add chat to the app.” Agent invokes the skill to clarify scope, integration needs, and user expectations before coding.

### Integration with Planning

The requirements gathering process must happen **before** any detailed planning (i.e., before the `plan_task` tool is used). The plan itself should reference the requirements artifact, and tasks should be derived from the approved requirements.

By consistently using this skill, we ensure every project starts with a solid foundation and every implementation is measured against its intended goals.


## Living Document & Revision History

### Active File Maintenance
This file (`AGENTS.md` or `GEMINI.md`) is a **living document**. It must be updated whenever:
- The **master plan** (e.g., task list, dependencies, goals) changes significantly.  
- **Unplanned code changes** are made – any deviation from the original plan that affects architecture, features, or implementation details.  
- New decisions, rules, or workflows are established.

### How to Update
- **Plan Changes**: When tasks are added, removed, reordered, or dependencies change, update the relevant sections (e.g., the task list in `tasks/current.json` should also be reflected here in a human‑readable summary).  
- **Unplanned Code Changes**: After making a code change that was not in the original plan, add a brief note under a **"Unplanned Changes"** section, describing what was changed and why.  
- **Major Decisions**: Document any architectural decisions, tool choices, or workflow adjustments.


## Cognitive Debt Management

### What Is Cognitive Debt?
Cognitive debt occurs when code works, but you (or the team) don't fully understand how or why. Unlike technical debt (poor code quality), cognitive debt represents gaps in understanding that will hinder future development.

### How to Prevent Cognitive Debt

- **CD-1 (SHOULD)** After generating complex code, use the "linear演练" pattern: ask the agent to generate a structured explanation of what was built, why, and how it works. Save this as an artifact.

- **CD-2 (SHOULD)** For any code you don't fully understand, request an "interactive explanation" that includes visualizations (diagrams, animations) where helpful.

- **CD-3 (SHOULD)** Before merging any AI-generated code, ensure you can explain:
  - What problem it solves
  - How it works (at a high level)
  - What edge cases are handled
  - What assumptions were made

- **CD-4 (SHOULD)** Treat "it works" as insufficient justification. If you can't explain why it works, you haven't finished reviewing.

### Reducing Cognitive Debt After the Fact

- **CD-5 (SHOULD)** When revisiting old code, use the agent to generate a "walkthrough" document explaining the code's purpose and structure.

- **CD-6 (SHOULD)** Maintain a "TIL" (Today I Learned) file in `docs/dev/` where you capture insights gained during AI-assisted development. This becomes a searchable knowledge base for future sessions.

### Revision History
At the **end of this file**, maintain a revision history table. Every time you modify this file (per the rules above), append a new row with:

| Date       | Change Description | Reason |
|------------|--------------------|--------|
| YYYY-MM-DD | What was updated   | Why it was necessary |

Use ISO dates (e.g., 2026-03-11). Keep the history in reverse chronological order (newest first) for easy scanning.

### Example
```markdown
## Revision History
| Date       | Change Description | Reason |
|------------|--------------------|--------|
| 2026-03-11 | Added rule for living document and revision history | To keep AGENTS.md in sync with evolving plans and code changes. |
| 2026-03-10 | Updated task list for authentication feature | User requested additional OAuth support. |
```

---

## Communication & Presentation

- **C&P-1 (SHOULD)** When presenting a plan, use a numbered list or table.
- **C&P-2 (SHOULD)** When executing multiple tasks, show a progress indicator (e.g., “Task 3/5: Running tests...”).
- **C&P-3 (SHOULD)** After completing a phase, provide a brief summary: what was done, any artifacts created, and what remains.
- **C&P-4 (SHOULD)** When asking for approval, clearly state the action, its impact, and any risks.

## Shortcuts

The user may invoke these shortcuts during a conversation:

- **QNEW** – “Understand all BEST PRACTICES listed in AGENTS.md. Your code SHOULD ALWAYS follow these best practices.”  
- **QPLAN** – “Analyze similar parts of the codebase and determine whether your plan: is consistent with rest of codebase, introduces minimal changes, reuses existing code.”  
- **QCODE** – “Implement your plan and make sure your new tests pass. Always run tests to make sure you didn't break anything else. Always run `prettier` on the newly created files to ensure standard formatting. Always run `turbo typecheck lint` to make sure type checking and linting passes.”  
- **QCHECK** – “You are a SKEPTICAL senior software engineer. Perform this analysis for every MAJOR code change you introduced (skip minor changes): 1. AGENTS.md checklist Writing Functions Best Practices. 2. AGENTS.md checklist Writing Tests Best Practices. 3. AGENTS.md checklist Implementation Best Practices.”  
- **QCHECKF** – “You are a SKEPTICAL senior software engineer. Perform this analysis for every MAJOR function you added or edited (skip minor changes): 1. AGENTS.md checklist Writing Functions Best Practices.”  
- **QCHECKT** – “You are a SKEPTICAL senior software engineer. Perform this analysis for every MAJOR test you added or edited (skip minor changes): 1. AGENTS.md checklist Writing Tests Best Practices.”  
- **QUX** – “Imagine you are a human UX tester of the feature you implemented. Output a comprehensive list of scenarios you would test, sorted by highest priority.”  
- **QGIT** – “Add all changes to staging, create a commit, and push to remote. Follow the Conventional Commits format; do not refer to Claude or Anthropic in the commit message.”

---

## Skills – Invocation, Usage, and Creation

Skills are reusable, documented behaviors that extend the agent’s capabilities. They are stored as Markdown files in `.config/opencode/skills/<skill-name>/SKILL.md`. This section defines how to invoke, use, and create skills effectively.

---

### 1. Skill Invocation

The agent can invoke a skill in two ways:

- **Via tool call**: Use the `skill` tool with the skill name and any required parameters.
- **Via conversation**: If the skill is documented with a clear description, the agent may suggest using it when appropriate.

#### 1.1 When to Invoke a Skill
- When the user explicitly asks for it (e.g., “run the `fix-lint-errors` skill”).
- When the task matches the skill’s description and the skill can handle it more efficiently than writing ad‑hoc code.
- When the skill is part of a workflow (e.g., after writing code, invoke `run-tests` to verify).

#### 1.2 How to Invoke
```typescript
// Example: calling a skill via tool
const result = await skill({
  name: "fix-lint-errors",
  parameters: {
    files: ["src/**/*.ts"]
  }
});
```

If the skill does not require parameters, simply call it with an empty object.

---

### 2. Skill Usage Best Practices

- **Check availability**: Before invoking a skill, list available skills via `skill.list()` or by scanning `.opencode/skills/` to ensure it exists.
- **Understand the skill**: Read its frontmatter (name, description) and the instructions inside `SKILL.md` to know what it does and any prerequisites.
- **Pass minimal parameters**: Only provide parameters the skill expects; avoid over‑specifying.
- **Handle results**: After a skill runs, check its output. If the skill returns structured data (e.g., JSON), parse it and use it for further steps.
- **Fallback**: If a skill fails or is not available, fall back to manual steps (e.g., running the equivalent shell commands) and consider proposing to fix or update the skill.

---

### 3. Creating a New Skill

Create a skill when you notice a repeatable pattern or when the user requests it. Follow this process:

#### 3.1 Skill Structure
- Directory: `.config/opencode/skills/<skill-name>/`
- File: `SKILL.md` with YAML frontmatter and instructions.

#### 3.2 Frontmatter Requirements
```yaml
---
name: fix-lint-errors           # required, lowercase+hyphens, 1‑64 chars
description: Automatically run linter and fix common issues   # required, 1‑1024 chars
license: MIT                     # optional
compatibility: ["node>=18", "npm"]  # optional
metadata:                         # optional key‑value pairs
  requires: eslint
---
```

#### 3.3 Writing Instructions
After the frontmatter, write the instructions in plain Markdown. Be explicit and step‑by‑step:

```markdown
# Steps
1. Run `npm run lint` to detect issues.
2. For each error:
   - If auto‑fixable, run `npm run lint:fix`.
   - If manual intervention is needed, output the file and line number.
3. After fixing, run `npm run lint` again to verify.
4. If any issues remain, list them for the user.
```

#### 3.4 Skill Creation Workflow
1. **Propose** – When you detect a pattern (see Pattern Recognition section), suggest creating a skill.
2. **Create** – If user agrees, create the directory and file with proper frontmatter and instructions.
3. **Test** – Immediately invoke the skill (in a dry run) to ensure it works as expected.
4. **Document** – Update `MASTER_IMPLEMENTATION.md` under a “Skills” section to note the new skill and its purpose.
5. **Iterate** – If the user asks to modify the skill, update the file and test again.

#### 3.5 Skill Naming Conventions
- Use lowercase letters, digits, and hyphens only.
- Keep names descriptive but concise (e.g., `run-tests`, `create-pr`, `fix-formatting`).
- Avoid generic names like `script` or `helper`.

---

### 4. Managing Skills

#### 4.1 Listing Available Skills
Use `skill.list()` or scan `.config/opencode/skills/` to see what’s available. Present the list to the user when relevant.

#### 4.2 Updating a Skill
- To modify an existing skill, edit its `SKILL.md` file.
- After editing, test it again to ensure changes work.
- Update the revision history in `MASTER_IMPLEMENTATION.md` if the change is significant.

#### 4.3 Removing a Skill
- If a skill is no longer needed, ask the user before deleting the directory.
- Remove any references in `MASTER_IMPLEMENTATION.md`.

#### 4.4 Permissions for Skills
- Skills are subject to the same permission system as other tools. Set permissions in `opencode.json` if a skill should always ask for approval.
- For skills that run dangerous commands (e.g., deployment), ensure they are marked `ask` in permissions.

---

### 5. Example: Creating a Skill for “Run Tests”

**User**: “I always run `npm test && npm run coverage` after changes. Can you make that a skill?”

**Agent**:
1. Create directory `.config/opencode/skills/run-tests/`
2. Create `SKILL.md`:
   ```yaml
   ---
   name: run-tests
   description: Run the test suite and generate coverage report
   ---
   # Instructions
   1. Run `npm test`
   2. If tests pass, run `npm run coverage`
   3. Save the coverage report as an artifact in `docs/dev/artifacts/`
   4. Report the number of passing/failing tests and coverage percentage.
   ```
3. Test by invoking the skill.
4. Update `MASTER_IMPLEMENTATION.md` under “Skills” with a link to the skill.
5. Inform the user: “Skill `run-tests` is ready. You can invoke it by typing `@run-tests` or when I detect you need to run tests.”

---

### 6. Skill Interoperability

Skills can call other skills. For example, a “deploy” skill might first invoke “build” and then “push”. Use the same `skill` tool inside the instructions to compose them.

---

### 7. Troubleshooting Skills

If a skill does not appear:
- Check that the directory name matches the `name` in frontmatter.
- Ensure the frontmatter is valid YAML and contains both `name` and `description`.
- Verify the skill is in `.config/opencode/skills/` (not a sub‑subdirectory).
- Run `skill.list()` to see if OpenCode loads it; if not, restart the session.

If a skill fails during execution:
- Log the error.
- Provide the user with a fallback manual command.
- Suggest editing the skill to improve robustness.

---

### 8. Skills and the Master Implementation Plan

Maintain a “Skills” section in `MASTER_IMPLEMENTATION.md` to track all custom skills:

```markdown
## Skills
- **fix-lint-errors**: Auto‑fixes ESLint errors. [Location](.config/opencode/skills/fix-lint-errors/SKILL.md)
- **run-tests**: Runs test suite and coverage. [Location](.config/opencode/skills/run-tests/SKILL.md)
```

---

This section gives the agent a clear framework for discovering, using, creating, and maintaining skills—essential for building a self‑improving assistant. Insert it after the “Custom Commands” or “MCP Integration” section, or as a new top‑level section before “Living Document & Revision History”.

## Proactive Reminders & Project Orientation

Users often lose track of the current task list, the overall roadmap, or what comes next. This section defines how the agent should **proactively remind** the user about the project state, next steps, and any overlooked items—before, during, and after scoping actions.

---

### 1. Why Reminders Matter

- **Maintain momentum** – the user stays focused on the next logical step.
- **Prevent scope creep** – reminders ground the conversation in the agreed plan.
- **Catch omissions** – if a task or phase is missed, reminders surface it early.
- **Build trust** – consistent, clear communication shows the agent is on top of the project.

---

### 2. What to Remind

| When | What to Include |
|------|-----------------|
| **Before starting any work** | Current active phase, immediate next task, and any prerequisites. |
| **After completing a task** | What was just done, next pending task(s), and estimated remaining tasks. |
| **When the user asks a new or vague question** | Summarise the current state (completed vs remaining) and ask how the new request fits. |
| **When the user seems stuck or idle** | Suggest the next logical action based on the plan. |
| **After a session break** | Recap the last completed task and the next step (read from `MASTER_TASK.md`). |

---

### 3. Reminder Format

Use a consistent, scannable format. For example:

```markdown
📋 **Project Status**
- **Phase**: Authentication (Phase 2)
- **Completed**: 3/5 tasks
- **Next task**: Add login route (depends on: branch creation)
- **Blocked**: None
- **Remaining**: Registration route, tests, PR creation

💡 **Suggested next action**: Implement login route. Would you like me to proceed?
```

If the user asks a new request that is unrelated, acknowledge the existing plan:

```markdown
I see you’re asking about database optimization. Currently we’re in the middle of the authentication phase.  
Do you want to:
1. Finish authentication first, then tackle database?  
2. Pause authentication and switch to this new task?  
3. Explore how database fits into the current plan?
```

---

### 4. When to Remind

#### 4.1 Before Starting
- **When the user says “let’s start”** or gives a new high‑level goal.
- **At the beginning of a session**, after reading `MASTER_IMPLEMENTATION.md` and `MASTER_TASK.md`.
- **Before any major decision** (e.g., choosing between two approaches) – show the impact on the remaining plan.

#### 4.2 During Execution
- **After each completed task** – show the updated list and the next step.
- **When a task fails** – remind what’s blocked and what alternatives exist.
- **When the user introduces an unplanned change** – flag it and ask if it should replace, augment, or postpone existing tasks.
- **When the user asks a question unrelated to the current task** – gently steer back or offer to adjust the plan.

#### 4.3 After Scoping/Completion
- **After a phase is complete** – summarise what was delivered and list the next phase’s tasks.
- **When the user thinks everything is done** – double‑check that all tasks are marked completed and that all artifacts are saved.
- **If the user says “that’s all for now”** – offer to create a session summary and remind about the next steps for the next session.

#### 4.4 Periodic Checks
- **Every ~5 tasks** – pause and ask if the user wants a status recap.
- **When the conversation goes silent for >2 minutes** – offer a quick status or ask if they need clarification.

---

### 5. Reminders from the Master Files

Always base reminders on the authoritative sources:
- `docs/dev/tasks/MASTER_TASK.md` – for task‑level status.
- `docs/dev/tasks/MASTER_IMPLEMENTATION.md` – for phase‑level progress.

At the start of each session, read both files to restore context. If the files are missing or incomplete, ask the user to clarify or help create them.

---

### 6. Example Reminder Flow

**User**: “Let’s start the authentication feature.”

**Agent** (before starting):
```
📋 **Current Plan**: Authentication Phase
- **Tasks**:
  1. Create feature branch (pending)
  2. Add login route (pending)
  3. Add registration route (pending)
  4. Write tests (pending)
- **Next**: Create feature branch. I’ll do that now, okay?
```

After finishing branch creation:
```
✅ **Task completed**: Create feature branch.
📋 **Remaining tasks**:
  1. Add login route (pending)
  2. Add registration route (pending)
  3. Write tests (pending)
Next: Add login route. Shall I proceed?
```

When user asks a new request: “Can we also add OAuth later?”
```
I’ve noted the request to add OAuth. This would expand the authentication phase.  
Currently the plan includes only login/registration.  
Would you like me to:
- Add OAuth as a new task after registration?
- Replace one of the existing tasks?
- Create a separate phase for OAuth?
```

---

### 7. Handling Missed Items

If the agent realises a task or phase was overlooked:
- **Admit it** – “I noticed we haven’t added error handling for the login form. This was not in the original plan.”
- **Offer options** – “Should we add it as a new task now, after the current tasks, or create a separate follow‑up issue?”
- **Update the plan** – after user approval, update `MASTER_TASK.md` and `MASTER_IMPLEMENTATION.md` accordingly.

---

### 8. Session Summaries

At the end of a session, or when the user says “goodbye” or “stop”, create a summary in `docs/dev/sessions/YYYY-MM-DD_HHMMSS-summary.md` that includes:
- What was accomplished.
- Remaining tasks.
- Next steps for the next session.
- Any unresolved questions or blockers.

This summary helps both the user and the agent resume seamlessly.

---

### 9. Proactive Reminders Checklist

| Action | Reminder Trigger |
|--------|------------------|
| New task added | Show updated task list, ask for priority. |
| Task completed | Show next task, ask to continue. |
| User asks vague question | Recap current plan, ask how to integrate. |
| User appears idle | Offer a status update or suggest next step. |
| Session starts | Restore context, show current phase and next task. |
| Phase finishes | Summarise, list next phase tasks. |
| Before any destructive command | Remind what will be changed and what’s at stake. |

---

### 10. Tone and Communication

- Be concise but informative.
- Use friendly, encouraging language.
- Never assume the user remembers the plan; always refresh context before proceeding.
- When reminding, present options rather than dictating the next step.

By following these guidelines, the agent becomes a reliable co‑pilot that helps the user stay on track, prevents surprises, and ensures nothing is forgotten.

## MVP Development Strategy

### 1. Objective
Launch a usable version of the SaaS platform as quickly as possible to gather real‑user feedback, validate the core value proposition, and iterate. This MVP focuses on the **essential business logic** while deferring non‑critical features to later phases.

### 2. Core Principles
- **Ship early, iterate fast** – aim for a working release within 4‑6 weeks.
- **Focus on the user journey** – prioritize the steps a new user takes from signup to first value.
- **One tenant, one user** initially – postpone advanced multi‑tenancy complexity.
- **Use built‑in tools** – leverage the design system files as guides, but implement only the necessary subset.
- **Measure feedback** – integrate basic analytics and user surveys from day one.

### 3. Feature Prioritisation (P0 = Must have for MVP)

| Priority | Feature Area | Rationale |
|----------|--------------|-----------|
| **P0** | **Authentication** (`AUTH.md`) | Signup, login, logout, email verification, password reset. |
| **P0** | **User Management** (`USER_ACCESS_MANAGEMENT.md`) | Simple user profile, role assignment (basic user/admin). |
| **P0** | **Core Business Logic** | The main value‑delivering feature (e.g., project creation, task management, reporting). This is application‑specific. |
| **P0** | **Basic UI & Onboarding** (`ONBOARDING.md`) | A clean, responsive interface with a guided first‑time user flow (e.g., welcome screen, first action). |
| **P1** | **Simple Billing** (`BILLING_SUBSCRIPTION.md`) | One payment method (Stripe), one plan (free trial + paid). Manual upgrade/downgrade handling via Stripe Dashboard initially. |
| **P1** | **Background Jobs** (`BACKGROUND_JOBS_QUEUES.md`) | Essential async tasks (e.g., sending welcome email, processing file uploads). |
| **P1** | **Basic Notifications** (`NOTIFICATION.md`) | In‑app notifications and one transactional email (e.g., welcome email). |
| **P2** | **Feature Flags** (`FEATURE_FLAGS.md`) | Can be introduced later to gradually roll out new features. |
| **P2** | **Webhooks** (`WEBHOOKS.md`) | Not needed for MVP unless external integrations are core. |
| **P2** | **Audit Logging** (`AUDIT_LOGGING.md`) | Start with basic database‑backed audit; advanced immutability later. |
| **P2** | **Rate Limiting** (`RATE_LIMITING.md`) | Basic per‑IP limits; advanced per‑plan limits later. |
| **P2** | **Advanced Multi‑tenancy** (`MULTITENANCY.md`) | Use shared‑schema with tenant_id column; postpone full isolation. |
| **P3** | **Full I18n** (`INTERNATIONALIZATION.md`) | Support only one language initially; add more as market expands. |
| **P3** | **A/B Testing** (`AB_TESTING.md`) | Not needed at launch. |
| **P3** | **Custom Themes** (`THEMING_WHITE_LABEL.md`) | Single brand theme; white‑label later. |

### 4. Phased Implementation Plan

#### Phase 0: Foundation (Week 1)
- Set up project structure (backend + frontend) with environment configuration.
- Implement authentication (signup, login, logout) using JWT.
- Create basic user model with roles (user/admin).
- Establish database schema (PostgreSQL) with migrations.
- Deploy to a staging environment.

#### Phase 1: Core Business Logic (Week 2‑3)
- Develop the main feature that delivers user value (e.g., project management, document processing, etc.).
- Build a simple, responsive UI using the component library (from `FRONTEND_DESIGN_SYSTEM.md`).
- Implement onboarding: welcome screen, guided tour for the main feature.
- Add in‑app notifications for important events.

#### Phase 2: Payment & Production Readiness (Week 4‑5)
- Integrate Stripe for one‑time payments or subscriptions.
- Set up background jobs (e.g., email sending).
- Add basic monitoring: health checks, error tracking (Sentry).
- Run security checks (OWASP Top 10, dependency scanning).
- Prepare deployment pipeline (CI/CD, Docker, Kubernetes minimal).

#### Phase 3: Launch & Feedback Loop (Week 6)
- Release to a small group of beta users.
- Collect feedback via integrated surveys and analytics.
- Fix critical bugs.
- Prepare for public launch.

### 5. Tools & Techniques
- **Conductor** – Use `conductor-setup` to initialize the project structure and maintain context.
- **TDD Orchestrator** – Apply test‑driven development for all core modules.
- **Feature Flags** – Even if not fully implemented, use environment variables as simple flags to toggle unfinished features.
- **Analytics** – Add lightweight tracking (e.g., PostHog, Mixpanel) to measure user actions.
- **Feedback channels** – Include a “Feedback” button and a short NPS survey after onboarding.

### 6. How to Proceed
1. Create a new branch `mvp/plan` and add this document.
2. Create a project board (GitHub Projects) with tasks for each phase.
3. Invoke the `conductor-setup` skill to initialize the repository with the chosen tech stack.
4. Start with authentication and the core business logic using the design system files as reference, but only implement the necessary subset.
5. Regularly demo progress to stakeholders and adjust priorities based on feedback.

### 7. After MVP
- Collect and analyse user feedback.
- Prioritise the next set of features (from P1 and P2).
- Gradually add remaining design system components.
- Scale infrastructure as needed.

--- 

*This MVP plan ensures we deliver value quickly while leaving room for iterative improvement. All design system files are blueprints for the final system; we implement only what’s essential for launch.*

## Revision History
| Date       | Change Description | Reason |
|------------|--------------------|--------|
| 2026-03-20 | Merged best practices with planning/task/artifact rules; added living document section | Created production‑grade AGENTS.md for OpenCode |
```

This single file now contains all the rules, best practices, shortcuts, and the new planning/task/artifact/living‑document sections.