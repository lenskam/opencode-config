# Agent Skills Reference for Phase Execution

This document describes the AI agent skills referenced in phase files, how they work, and when to use them.

---

## Skills Reference

### /full-stack-orchestration-full-stack-feature

**Purpose**: Implement end-to-end full-stack features (database → API → UI → tests).

**When to use**: Every phase that builds a user-facing feature.

**How it applies**:
- Scaffolds the database migration for the feature's data model
- Creates API endpoints (REST or GraphQL)
- Builds UI components with proper state management
- Writes integration tests for the full flow
- Ensures the feature is complete and working from front to back

**Example**: Implementing signup means:
1. Create user model and migration
2. Create register endpoint with validation
3. Build signup form with error handling
4. Write test: user fills form → submits → sees dashboard

---

### /using-superpowers

**Purpose**: Leverage advanced agent capabilities for code generation, refactoring, and debugging.

**When to use**: All phases, especially for repetitive patterns.

**How it applies**:
- Generate boilerplate code (CRUD endpoints, form components, test stubs)
- Apply automated refactoring (extract functions, rename variables, restructure components)
- Use debugging tools to identify and fix issues
- Speed up routine coding tasks without manual repetition

**Example**: Creating 5 CRUD endpoints → use superpowers to generate the pattern from one example, then customize.

---

### /workflow-orchestration-patterns

**Purpose**: Apply structured patterns for multi-step asynchronous workflows.

**When to use**: Phases involving email sending, payment processing, notifications, queue processing, or any multi-step process.

**How it applies**:
- Saga pattern for distributed transactions (e.g., order → payment → fulfillment)
- Step functions for long-running workflows
- Retry with exponential backoff for unreliable operations
- Compensation actions for failed workflows

**Example**: User signup triggers:
1. Create user record
2. Send verification email (async)
3. Create default workspace
4. If email fails → retry up to 3 times
5. If all retries fail → log and notify admin (compensation: user is created but unverified)

---

### /workflow-patterns

**Purpose**: Structure task execution as pipelines with clear stages and error handling.

**When to use**: All phases for organizing the implementation flow.

**How it applies**:
- Pipeline pattern: Task A → Task B → Task C (sequential)
- Branching pattern: Tasks A and B in parallel → Task C after both complete
- Fan-out pattern: Task A → Tasks B1, B2, B3 in parallel → Task C
- Error handling: Each stage has defined failure behavior (stop, skip, fallback)

**Example**: Implementing a form:
1. Create the form component (pipeline start)
2. Add validation logic (depends on 1)
3. Connect to API endpoint (depends on 1)
4. Add error display (depends on 2, 3)
5. Write tests (depends on 1-4)

---

## When NOT to Use Each Skill

| Skill | Don't use when |
|-------|----------------|
| full-stack-orchestration | Phase is purely infrastructure (database design, CI/CD config) — no user-facing feature |
| using-superpowers | Code is already optimized and further automation would introduce risk |
| workflow-orchestration-patterns | All tasks are synchronous and single-step |
| workflow-patterns | There's only one task in the phase |

---

## Combining Skills in a Phase

Most phases benefit from **/full-stack-orchestration** + **/using-superpowers** + **/workflow-patterns**. The orchestration skill gives the structure, superpowers give the speed, and workflow patterns provide the organization.

Add **/workflow-orchestration-patterns** only when the feature has async multi-step processes (emails, payments, notifications).

### Example: Phase — User Onboarding

| Task | Skills Used |
|------|-------------|
| Create user model + migration | orchestration, superpowers |
| Build signup API endpoint | orchestration, superpowers |
| Build signup form UI | orchestration, superpowers |
| Email verification | orchestration, superpowers, orchestration-patterns |
| Write tests | superpowers, workflow-patterns |
| Structure as pipeline | workflow-patterns |
