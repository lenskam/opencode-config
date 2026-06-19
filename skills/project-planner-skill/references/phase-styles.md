# Phase Styles Reference

## Overview

Two primary phase styles exist for structuring software implementation plans. The user chooses one based on their project's needs.

---

## Incremental Style

### Concept
Each phase delivers **one complete user story or feature** from end to end. After each phase, the application has a new working capability that can be demonstrated.

### When to Use
- Product-focused teams that need early demos
- MVPs where rapid feedback is critical
- Projects where feature priority is clear
- Stakeholders want to see progress every sprint
- Startup environments needing to validate assumptions

### Example
```
Phase 1: User can sign up and log in
Phase 2: User can create a project
Phase 3: User can invite team members
Phase 4: User can assign tasks to team members
Phase 5: User can generate reports
```

### Advantages
- **Demo‑ready after every phase** — stakeholders see working features
- **Early user feedback** — real users can test and provide input
- **Clear scope boundaries** — each phase is a self-contained feature
- **Natural prioritization** — most valuable features first
- **Lower integration risk** — each feature is integrated as it's built

### Disadvantages
- **May require refactoring** — early architectural decisions might not scale
- **Backend may be fragile** — built incrementally alongside frontend
- **Integration complexity grows** — each new feature must integrate with existing ones

### Typical Phase Structure
```
1. Implement feature X backend (database models, API endpoints)
2. Implement feature X frontend (UI components, state management)
3. Write tests for feature X
4. Verify end-to-end flow
```

---

## Chronological Style

### Concept
Each phase builds a **technical layer** of the system. Multiple layers may be needed before any user-facing feature is complete.

### When to Use
- API-first or infrastructure-heavy projects
- Complex backend systems with multiple services
- Projects where architecture quality is critical
- Teams that need a solid foundation before building UI
- Projects with strict performance or security requirements

### Example
```
Phase 1: Database schema and data models
Phase 2: Core API endpoints and service layer
Phase 3: Authentication and authorization
Phase 4: Frontend scaffolding and design system
Phase 5: User signup and login UI
Phase 6: Project creation UI
```

### Advantages
- **Solid architectural foundation** — infrastructure is designed before features are built
- **Easier to maintain** — well-layered code is easier to extend
- **Better testability** — each layer can be tested independently
- **Clear separation of concerns** — database, API, auth, UI are distinct phases
- **Scales better** — architectural decisions are made upfront

### Disadvantages
- **No user‑facing output until later** — demos are impossible in early phases
- **Late validation** — you might build infrastructure for features users don't want
- **Harder to estimate** — infrastructure phases often take longer than expected
- **Risk of over-engineering** — building the perfect foundation for features that may change

### Typical Phase Structure
```
1. Database schema design and migration scripts
2. API endpoint scaffolding with basic CRUD
3. Authentication middleware and session management
4. Frontend project setup with routing and state management
5. Feature implementations on top of the foundation
```

---

## Mixed Style

### Concept
Start with **chronological** phases for infrastructure and core architecture, then switch to **incremental** phases for feature delivery.

### When to Use
- Complex projects where infrastructure is non-trivial
- Teams that need both solid foundations AND visible progress
- Projects where architectural mistakes are expensive to fix later
- Enterprise applications with multiple services

### Example
```
Phase 1: Database schema and migrations (chronological)
Phase 2: API skeleton with core endpoints (chronological)
Phase 3: Authentication and authorization (chronological)
Phase 4: User signup feature (incremental)
Phase 5: Project creation feature (incremental)
Phase 6: Team invitations feature (incremental)
```

### Advantages
- **Best of both worlds** — solid foundation + visible progress
- **Balanced risk** — architecture is stable before features are built
- **Clear transition point** — teams know when to switch from infra to features

### Disadvantages
- **More complex to plan** — requires deciding when to switch styles
- **May delay first feature** — infrastructure phases still come first

---

## Decision Matrix

| Factor | Incremental | Chronological | Mixed |
|--------|-------------|---------------|-------|
| Need early demos? | ✅ Best | ❌ No | ⚠️ After infra |
| Infrastructure heavy? | ❌ Risky | ✅ Best | ✅ Best |
| Small team (<5)? | ✅ Best | ⚠️ Can work | ⚠️ Can work |
| Large team (5+)? | ⚠️ Can work | ✅ Best | ✅ Best |
| Uncertain requirements? | ✅ Best | ❌ Risky | ⚠️ After infra |
| Well-understood domain? | ⚠️ Can work | ✅ Best | ✅ Best |
| Need solid foundation? | ❌ Risky | ✅ Best | ✅ Best |
| Deadline pressure? | ✅ Best | ❌ Risky | ⚠️ After infra |

---

## Migrating Between Styles

It's possible to switch styles mid-project:

**Chronological → Incremental**: After the foundation is built, switch to feature delivery. This is the mixed approach described above.

**Incremental → Chronological**: If code quality suffers, pause feature work and add a "refactor foundation" phase. Rename existing phases to accommodate.

**Recommendation**: If unsure, start incremental. You can always add a "foundation refactor" phase later. Starting chronological and switching to incremental is harder because stakeholders may lose patience with no visible progress.
