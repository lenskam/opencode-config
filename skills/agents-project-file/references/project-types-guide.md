# Project Types Guide — Section Customization Reference

This document details how each section of the generated AGENTS.md is customized for the six supported project types. Use it as a reference when extending or modifying the generator.

## Section-by-Section Customization

### 1. Project Overview
| Type | Emphasis |
|------|----------|
| SaaS | Multi-tenant platform, subscription billing, team collaboration |
| Mobile App | Offline-first, push notifications, biometric auth |
| Landing Page | SEO-optimized, analytics tracking, form submissions |
| API Service | RESTful/GraphQL API, rate limiting, API key management |
| E-commerce | Product catalog, cart, checkout, payment processing |
| Internal Tool | SSO integration, CRUD scaffolding, RBAC |

### 2. Technology Stack
Default stacks per type (overridable by user input):
| Type | Frontend | Backend | Database | Additional |
|------|----------|---------|----------|------------|
| SaaS | Next.js/React | Node.js/FastAPI/Django | PostgreSQL/MongoDB | Redis, Stripe, Vercel |
| Mobile App | React Native/Flutter | Node.js/Firebase | SQLite/PostgreSQL | OneSignal, Firebase Auth |
| Landing Page | Next.js/Astro | — | — | Tailwind, Plausible, Vercel |
| API Service | — | FastAPI/Express/Go | PostgreSQL | Redis, RabbitMQ, Docker+K8s |
| E-commerce | Next.js/Remix | Next.js/Django | PostgreSQL | Algolia, Stripe, Redis |
| Internal Tool | React/Retool | FastAPI/Django | PostgreSQL/SQLite | SSO, Docker |

### 3. System Architecture & Design Patterns
| Type | Architecture Highlights |
|------|----------------------|
| SaaS | Multi-tenant DB, subscription lifecycle, webhook system, rate limiting, audit logging |
| Mobile App | Offline-first, push notifications, biometric auth, state management, background sync |
| Landing Page | SSG/ISR, SEO-first, A/B testing, form pipeline, analytics |
| API Service | REST/GraphQL, microservices, JWT+API keys, multi-tier caching, observability |
| E-commerce | Catalog system, cart engine, checkout pipeline, payment orchestration, search |
| Internal Tool | SSO+RBAC, repository pattern, CRUD scaffolding, audit trail, export pipeline |

### 4. Frontend Specifications
| Type | Pages/Screens | Key Components |
|------|--------------|----------------|
| SaaS | Dashboard, subscription mgmt, team mgmt, settings, billing portal | PricingCards, SubscriptionBadge, UsageMeter, InviteFlow, WebhookTable |
| Mobile App | Splash, login, home feed, detail view, settings, activity log | OfflineBanner, BiometricPrompt, PushToggle, SyncIndicator |
| Landing Page | Hero, features, pricing, testimonials, FAQ, contact, footer | CTASection, AnalyticsTracker, ABTestVariant, FormWithValidation |
| API Service | API reference (Swagger), playground, API key dashboard, usage analytics | ApiKeyTable, EndpointCard, UsageChart, WebhookConfig |
| E-commerce | Product listing, detail, cart, checkout, confirmation, account | ProductCard, CartDrawer, CheckoutStepper, SearchBar, ReviewForm |
| Internal Tool | Login/SSO, dashboard, data tables, CRUD forms, reports, admin panel | DataTable, FormBuilder, FilterPanel, ExportButton, AuditLog |

### 5. Backend Specifications
| Type | Core Models | API Endpoints |
|------|-------------|---------------|
| SaaS | Tenant, User, Plan, Subscription, Invoice, PaymentMethod, AuditLog, WebhookEndpoint | Auth, subscriptions, invoices, team, usage, webhooks (12 endpoints) |
| Mobile App | User, Device, Notification, SyncQueue, Activity | Auth, devices, notifications, sync (8 endpoints) |
| Landing Page | FormSubmission, AnalyticsEvent, Lead, ABTestVariant, ConsentRecord | Form submit, health, analytics, consent, A/B test (5 endpoints) |
| API Service | ApiKey, WebhookEndpoint, UsageRecord, RateLimit, AuditLog | Auth, keys, usage, webhooks, health (9 endpoints) |
| E-commerce | Product, ProductVariant, Category, Cart, Order, Review | Products, cart, checkout, orders, reviews (9 endpoints) |
| Internal Tool | User, Record, AuditLog, Report, Export | Auth, records, reports, audit log (9 endpoints) |

### 6. Testing Strategy
| Type | Focus Areas |
|------|-------------|
| SaaS | Billing logic unit tests, Stripe mock integration, E2E checkout flows, webhook contract tests, multi-tenant load tests |
| Mobile App | SQLite operations, widget tests, offline/online transitions, device testing, E2E on simulators |
| Landing Page | Visual regression, form validation edge cases, analytics event firing, Lighthouse CI, a11y scans |
| API Service | Service layer unit tests, DB integration, contract tests, p99 latency benchmarks, auth bypass tests |
| E-commerce | Pricing calculations, checkout integration, Stripe webhook handling, Black Friday load tests |
| Internal Tool | CRUD operations, DB queries, RBAC enforcement, export generation |

### 7-17. Shared Sections
Sections 7 (Git Workflow), 9 (Documentation), 10 (Coding Standards), 11 (Environment Setup), 12 (AI Productivity), 13 (AI Instructions), and 16 (Revision History) are consistent across all project types with minor variable substitution (project name, slug).

### 8. Deployment & CI/CD
| Type | Strategy | CI/CD Pipeline |
|------|----------|----------------|
| SaaS | Vercel staging + production, DB migrations as part of deploy | lint → test → build → deploy staging → E2E → manual prod |
| Mobile App | TestFlight (iOS) + Internal track (Android), fastlane automation | Build → beta → release tracks |
| Landing Page | Vercel/Netlify auto-deploy, CDN cache invalidation | lint → build → lighthouse → deploy |
| API Service | Docker multi-stage + Kubernetes rolling update | lint → test → docker build → staging → smoke → prod |
| E-commerce | Staging + production with feature flags, low-traffic window deploy | lint → test → build → staging → E2E → manual prod |
| Internal Tool | Docker container to internal server/cloud | lint → test → docker build → deploy → smoke test |

### 14. Agent Commands
| Type | Base Commands | Extra Commands |
|------|--------------|----------------|
| SaaS | /lint, /test, /typecheck, /build | /deploy-staging, /provision-tenant, /test-billing, /run-migrations, /inspect-webhook |
| Mobile App | /lint, /test, /typecheck, /build | /build-ios, /build-android, /test-push, /generate-screenshots |
| Landing Page | /lint, /test, /typecheck, /build | /deploy, /test-seo, /check-lighthouse, /run-ab-test |
| API Service | /lint, /test, /typecheck, /build | /test-endpoint, /check-openapi, /run-load-test |
| E-commerce | /lint, /test, /typecheck, /build | /test-checkout, /check-inventory, /test-stripe-webhook |
| Internal Tool | /lint, /test, /typecheck, /build | /run-migrations, /test-auth, /export-data |

### 15. Development Phases
| Type | Phase 1 (MVP) | Phase 2 | Phase 3 | Phase 4 |
|------|---------------|---------|---------|---------|
| SaaS | Auth, user mgmt, basic Stripe | Team collab, webhooks, analytics | Usage-based pricing, multi-region | SSO, audit logs, custom contracts |
| Mobile App | Auth, core feature, offline read | Push notifications, social, content creation | Premium subs, IAP, ads | Multi-language, personalization |
| Landing Page | Hero, features, pricing, contact | A/B testing, heatmaps, CRO | Blog, case studies, i18n | User portal, email sequences |
| API Service | Auth, CRUD, rate limiting | Caching, monitoring, docs | Webhooks, usage tiers, multi-region | SSO, audit logs, SLA |
| E-commerce | Catalog, cart, checkout | Reviews, tracking, support | Multi-vendor, marketplace | Personalization, loyalty |
| Internal Tool | Auth, core CRUD, reporting | Filters, export, RBAC | Scheduled reports, notifications | SSO, audit logs, workflows |

## Common Personas by Type
| Type | User Roles |
|------|------------|
| SaaS | Admin, Workspace Owner, Team Member, Free User, Premium User, Guest |
| Mobile App | User, Premium Subscriber, Content Creator, Moderator |
| Landing Page | Visitor, Lead, Customer |
| API Service | Developer, Admin, Service Account |
| E-commerce | Customer, Merchant, Admin, Support Agent |
| Internal Tool | Admin, Power User, Regular User, Auditor |

## Extending the Generator
To add a new project type:
1. Add entry to `VALID_TYPES` dict in `generate_agents_md.py`
2. Add content dict entry in each of the 6 type-specific section methods
3. Add persona list in `_personas_for_type()`
4. Add stack in `_infer_stack()`
5. Add commands in `_commands_for_type()`
6. Add phases in `_section_development_phases()`
7. Update `SKILL.md` trigger section, analysis table, and keywords
8. Add entry to this guide
