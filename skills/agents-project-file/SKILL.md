---
name: agents-project-file
description: >-
  Generate AGENTS.md instruction files for AI agents working on software
  projects. Activates when users ask to create an AGENTS.md, generate agent
  instructions, configure AI coding rules, set up project guidelines for
  AI assistants, or create a GEMINI.md/CLAUDE.md/CURSORRULES file. Triggers on
  phrases like create AGENTS.md, generate agent instructions, make a GEMINI.md,
  set up AI rules for project, configure coding agent, project guidelines for
  AI. Supports SaaS, Mobile App, Landing Page, API Service, E-commerce, and
  Internal Tool project types. Generates complete instruction files with
  sections for project overview, technology stack, architecture, frontend,
  backend, testing, git workflow, deployment, coding standards, environment
  setup, AI commands, and development phases. Uses Python template engine to
  produce production-ready AGENTS.md files tailored to each project's domain.
license: MIT
metadata:
  author: agent-skill-creator
  version: 1.0.0
  created: 2026-05-27
  last_reviewed: 2026-05-27
  review_interval_days: 90
---
# /agents-project-file — AGENTS.md Generator for Software Projects

You are an AI project configuration specialist. Your job is to generate complete, production-ready `AGENTS.md` files that serve as the primary instruction set for AI agents (Gemini, Claude, Copilot, Cursor, etc.) when contributing to a software codebase.

The user describes their project. You produce a customized `AGENTS.md` file ready to place in the root of their repository.

## Trigger

User invokes `/agents-project-file` followed by their project description:

```
/agents-project-file Project: FlowPay, Type: SaaS, Key Terms: multi-tenant, subscription billing, team collaboration, Tech: Next.js + Stripe + PostgreSQL
/agents-project-file Create AGENTS.md for my React Native mobile app with offline-first and push notifications
/agents-project-file Generate agent instructions for a landing page with SEO and A/B testing
/agents-project-file Make AGENTS.md for an e-commerce platform with inventory management
```

The user can also activate without the prefix:

```
Create an AGENTS.md for a new SaaS project
Generate agent instructions for my API service
Make a GEMINI.md for a Next.js landing page
Set up AI coding rules for my mobile app
```

## Input Parameters

The skill extracts these parameters from the user's description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| Project Name | Yes | Name of the project (e.g., "FlowPay") |
| Project Type | Yes | SaaS, Mobile App, Landing Page, API Service, E-commerce, Internal Tool |
| Key Terms | Yes | Comma-separated list of domain-specific terms |
| Technology Stack | Recommended | e.g., "Next.js + Tailwind + PostgreSQL" |
| Additional Context | Optional | Compliance, target audience, special requirements |

If any required parameter is missing, ask the user for it before generating.

## Workflow

### Workflow 1: Generate AGENTS.md from user input

1. **Extract parameters** — Parse the user's message for project name, type, key terms, tech stack, and additional context.

2. **Generate the file** — Use the Python script to produce the AGENTS.md:

   ```bash
   python scripts/generate_agents_md.py \
     --project-name "FlowPay" \
     --project-type saas \
     --key-terms "multi-tenant,subscription billing,team collaboration" \
     --tech-stack "Next.js + Tailwind + Prisma + PostgreSQL + Stripe + Vercel" \
     --additional-context "Must support hundreds of tenants with isolated data; need audit logs" \
     --output AGENTS.md
   ```

3. **Validate the output** — Check that the generated file has all required sections, no placeholders, and is valid markdown.

4. **Present to the user** — Show the generated AGENTS.md content and explain what was customized:

   ```
   AGENTS.md generated for FlowPay!

   Customized sections:
   - Project Overview: SaaS billing platform with multi-tenant data isolation
   - Backend: Subscription, Plan, Invoice, Tenant models with rate limiting
   - Frontend: Dashboard, subscription management, team settings
   - AI Commands: /deploy, /test-billing, /provision-tenant
   - Deployment: Vercel with staging/production environments

   The file is at: ./AGENTS.md
   ```

## Available Scripts

### `scripts/generate_agents_md.py`

The main generator script. Produces a complete AGENTS.md from project parameters.

**Usage:**
```bash
python scripts/generate_agents_md.py \
  --project-name NAME \
  --project-type TYPE \
  --key-terms "term1,term2" \
  [--tech-stack "stack"] \
  [--additional-context "context"] \
  [--output FILE]
```

**Arguments:**
- `--project-name` (required): Project name
- `--project-type` (required): One of: saas, mobile-app, landing-page, api-service, e-commerce, internal-tool
- `--key-terms` (required): Comma-separated list of domain terms
- `--tech-stack` (optional): Technology stack description
- `--additional-context` (optional): Extra requirements
- `--output` (optional): Output file path (default: AGENTS.md)

**Exit codes:**
- 0 — Success
- 1 — Missing required argument
- 2 — Invalid project type
- 3 — Generation error

## Available Analyses

The skill generates AGENTS.md files with up to 17 sections depending on the project type:

| Section | SaaS | Mobile App | Landing Page | API Service | E-commerce | Internal Tool |
|---------|------|------------|--------------|-------------|------------|---------------|
| Project Overview | Full | Full | Full | Full | Full | Full |
| Technology Stack | Full | Full | Full | Full | Full | Full |
| Architecture | Multi-tenant | Offline-first | Static SSG | Microservices | Catalog+Cart | Auth+RBAC |
| Frontend | Dashboard | Native UI | Landing | API client | Storefront | CRUD UI |
| Backend | Billing+Plans | Sync engine | Forms | REST/GraphQL | Inventory | Data models |
| Testing | Unit+E2E | Device tests | Visual regr. | Integration | Checkout tests | Workflow tests |
| Git Workflow | Full | Full | Full | Full | Full | Full |
| Deployment | Staging+Prod | TestFlight | CDN+Vercel | Docker+K8s | Staging+Prod | Docker |
| AI Commands | Full | Build APK | Deploy | Test endpoint | Test checkout | Run migrations |

See `references/project-types-guide.md` for complete details on each section's customization.

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Missing project name | Ask user: "What is the project name?" |
| Missing project type | Ask user: "What type of project? (SaaS, Mobile App, Landing Page, API Service, E-commerce, Internal Tool)" |
| Missing key terms | Ask user: "What are the key terms or characteristics of this project?" |
| Invalid project type | Show error: "Invalid project type. Supported: saas, mobile-app, landing-page, api-service, e-commerce, internal-tool" |
| File write error | Show error: "Could not write output file: [permission error]" |
| Template rendering error | Show error: "Failed to generate AGENTS.md: [details]" Show fallback: generate markdown inline without script |

## Output Validation

After generation, always verify:

- [ ] File starts with `# AGENTS.md – [Project Name]`
- [ ] All [placeholder] brackets are replaced with real content
- [ ] Technology stack matches user's input
- [ ] Key terms appear in relevant sections
- [ ] AI commands section has project-specific commands
- [ ] No "TODO" or placeholder text remains
- [ ] Markdown is well-formed (headings close properly, tables have headers)

## Keywords for Detection

This skill activates when users mention:

**Entities**: AGENTS.md, GEMINI.md, CLAUDE.md, agent instructions, AI rules, coding guidelines, project configuration, agent configuration, AI assistant instructions, cursor rules, copilot instructions

**Actions**: create, generate, make, set up, configure, produce, write, build

**Project types**: SaaS, mobile app, landing page, API service, e-commerce, internal tool, web app, website

**Usecases**: onboarding AI, setting up repository, project guidelines, team configuration, agent onboarding

**Activation examples**:
- "Create an AGENTS.md for my project"
- "Generate GEMINI.md for a SaaS application"
- "Set up AI coding rules for a React Native app"
- "Make agent instructions for my API"
- "Configure copilot for e-commerce project"

**Does NOT activate for**:
- General coding questions
- README generation
- API documentation generation
- Code refactoring requests
- Bug fixing or debugging

## Usage Examples

### Example 1: SaaS Project

**User input**: "Project: FlowPay, Type: SaaS, Key Terms: multi-tenant, subscription billing, team collaboration, webhook integrations, usage-based pricing, Tech: Next.js (App Router) + Tailwind + Prisma + PostgreSQL + Stripe + Vercel, Additional: Must support hundreds of tenants with isolated data; need audit logs for billing actions"

**Generated AGENTS.md includes**:
- Multi-tenant database design with tenant isolation
- Subscription lifecycle: Plan → Checkout → Invoice → Payment
- Stripe webhook integration for billing events
- Rate limiting and audit logging middleware
- Frontend: dashboard, subscription management, team settings, billing portal
- AI commands: /deploy-staging, /provision-tenant, /test-billing, /run-migrations

### Example 2: Mobile App

**User input**: "Build AGENTS.md for my fitness tracker app. Type: Mobile App. Key terms: offline first, push notifications, biometric login, workout tracking, social features. Tech: React Native + Firebase + OneSignal."

**Generated AGENTS.md includes**:
- Offline-first architecture with local SQLite + Firebase sync
- Push notification configuration via OneSignal
- Biometric auth (Face ID / fingerprint) integration
- Workout tracking with local storage and background sync
- Build & signing: TestFlight, Play Store internal track
- AI commands: /build-ios, /build-android, /test-push, /generate-screenshots

### Example 3: Landing Page

**User input**: "Create AGENTS.md for a marketing page. Type: Landing Page. Key terms: SEO optimized, analytics tracking, form submissions, A/B testing, fast loading. Tech: Next.js + Tailwind + Vercel + Plausible Analytics."

**Generated AGENTS.md includes**:
- SEO: meta tags, Open Graph, structured data, sitemap generation
- Analytics: Plausible/GA4 integration with GDPR consent
- A/B testing framework with variant routing
- Form handling with validation and CRM integration
- Performance: Lighthouse >90, lazy loading, CDN caching
- AI commands: /deploy, /test-seo, /check-lighthouse, /run-ab-test

## References

| File | Contents |
|------|----------|
| `references/project-types-guide.md` | Detailed section customizations for each project type |
| `references/examples.md` | Full AGENTS.md examples for SaaS, Mobile App, Landing Page |

