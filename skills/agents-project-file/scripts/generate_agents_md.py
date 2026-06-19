#!/usr/bin/env python3
"""
AGENTS.md Generator — Produce tailored agent instruction files for any project.

Parses project parameters (name, type, key terms, tech stack) and generates a
complete AGENTS.md file following a structured template adapted to the project
type. The output is ready to place in the repository root for AI agent onboarding.

Usage:
    python scripts/generate_agents_md.py \\
        --project-name "FlowPay" \\
        --project-type saas \\
        --key-terms "multi-tenant,subscription billing" \\
        --tech-stack "Next.js + Tailwind + PostgreSQL" \\
        --additional-context "GDPR compliance needed" \\
        --output AGENTS.md

Supported project types:
    saas, mobile-app, landing-page, api-service, e-commerce, internal-tool
"""

import argparse
import json
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


VALID_TYPES = {
    "saas": "SaaS",
    "mobile-app": "Mobile App",
    "landing-page": "Landing Page",
    "api-service": "API Service",
    "e-commerce": "E-commerce",
    "internal-tool": "Internal Tool",
}

VALID_TYPES_LIST = sorted(VALID_TYPES.keys())


def _ensure_list(value) -> List[str]:
    if isinstance(value, str):
        return [t.strip() for t in value.split(",") if t.strip()]
    return list(value)


def _slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-")


def _heading(level: int, text: str) -> str:
    return f"{'#' * level} {text}"


def _table(headers: List[str], rows: List[List[str]]) -> str:
    col_widths = [
        max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))
    ]
    sep = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
    header_line = (
        "| "
        + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        + " |"
    )
    lines = [header_line, sep]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(row))
            + " |"
        )
    return "\n".join(lines)


def _code_block(lang: str, content: str) -> str:
    return f"```{lang}\n{content}\n```"


class AgentsMDGenerator:
    """
    Generate a complete AGENTS.md file tailored to a project's type and domain.

    Each project type produces a different emphasis in each section of the file.
    The generator uses the provided key terms to customize backend models,
    frontend components, AI commands, and deployment pipelines.
    """

    def __init__(
        self,
        project_name: str,
        project_type: str,
        key_terms: List[str],
        tech_stack: Optional[str] = None,
        additional_context: Optional[str] = None,
    ):
        self.project_name = project_name
        self.project_type = project_type
        self.project_type_label = VALID_TYPES.get(project_type, project_type)
        self.key_terms = key_terms
        self.tech_stack = tech_stack or ""
        self.additional_context = additional_context or ""
        self.slug = _slugify(project_name)
        self.today = datetime.now().strftime("%Y-%m-%d")

    def generate(self) -> str:
        sections = [
            self._title(),
            self._table_of_contents(),
            self._section_overview(),
            self._section_tech_stack(),
            self._section_architecture(),
            self._section_frontend(),
            self._section_backend(),
            self._section_testing(),
            self._section_git_workflow(),
            self._section_deployment(),
            self._section_documentation(),
            self._section_coding_standards(),
            self._section_environment(),
            self._section_ai_productivity(),
            self._section_ai_instructions(),
            self._section_agent_commands(),
            self._section_development_phases(),
            self._section_revision_history(),
            self._footer(),
        ]
        return "\n\n".join(s for s in sections if s)

    def _title(self) -> str:
        return f"# AGENTS.md – {self.project_name}\n\nThis file serves as the primary instruction set for AI agents contributing to **{self.project_name}**."

    def _table_of_contents(self) -> str:
        sections = [
            "Project Overview",
            "Technology Stack",
            "System Architecture & Design Patterns",
            "Frontend Specifications",
            "Backend Specifications",
            "Testing Strategy",
            "Git Workflow",
            "Deployment & CI/CD",
            "Documentation Guidelines",
            "Coding Standards",
            "Environment Setup",
            "AI Productivity Configuration",
            "AI-Specific Instructions",
            "Agent Commands",
            "Development Phases",
            "Revision History",
        ]
        lines = ["## Table of Contents\n"]
        for i, s in enumerate(sections, 1):
            anchor = s.lower().replace(" ", "-").replace("&", "and")
            lines.append(f"{i}. [{s}](#{i}-{anchor})")
        return "\n".join(lines)

    def _section_overview(self) -> str:
        type_desc = {
            "saas": "a multi-tenant SaaS platform",
            "mobile-app": "a mobile application",
            "landing-page": "a marketing landing page",
            "api-service": "a backend API service",
            "e-commerce": "an e-commerce platform",
            "internal-tool": "an internal tool",
        }.get(self.project_type, "a software project")

        terms = ", ".join(self.key_terms[:5])
        features = "\n".join(f"- {t}" for t in self.key_terms)
        roles = self._personas_for_type()

        extra = ""
        if self.additional_context:
            extra = f"\n\n**Additional Context**: {self.additional_context}"

        return textwrap.dedent(
            f"""\
            ## 1. Project Overview

            - **Purpose**: {self.project_name} is {type_desc} focused on {terms}.
            - **Key Features**:
            {features}
            - **User Roles / Personas**:
            {roles}{extra}"""
        )

    def _personas_for_type(self) -> str:
        personas = {
            "saas": "- Admin\n- Workspace Owner\n- Team Member\n- Free User\n- Premium User\n- Guest",
            "mobile-app": "- User\n- Premium Subscriber\n- Content Creator\n- Moderator",
            "landing-page": "- Visitor\n- Lead\n- Customer",
            "api-service": "- Developer\n- Admin\n- Service Account",
            "e-commerce": "- Customer\n- Merchant\n- Admin\n- Support Agent",
            "internal-tool": "- Admin\n- Power User\n- Regular User\n- Auditor",
        }
        return personas.get(self.project_type, "- User\n- Admin")

    def _section_tech_stack(self) -> str:
        stack_rows = []

        inferred = self._infer_stack()
        for layer, tech in inferred:
            if tech:
                stack_rows.append([layer, tech])

        if self.tech_stack:
            parsed = self._parse_tech_stack(self.tech_stack)
            for layer, tech in parsed:
                if tech:
                    found = False
                    for i, (l, _) in enumerate(stack_rows):
                        if l.lower() == layer.lower():
                            stack_rows[i] = [layer, tech]
                            found = True
                            break
                    if not found:
                        stack_rows.append([layer, tech])

        if not stack_rows:
            stack_rows = [["Backend", "To be determined"], ["Frontend", "To be determined"]]

        table = _table(["Layer", "Technology"], stack_rows)
        return f"## 2. Technology Stack\n\n{table}"

    def _infer_stack(self) -> List[List[str]]:
        stacks = {
            "saas": [
                ["Backend", "Node.js + Express / FastAPI / Django"],
                ["Frontend", "Next.js / React / Vue.js"],
                ["Database", "PostgreSQL / MongoDB"],
                ["Cache / Queue", "Redis / Bull / Sidekiq"],
                ["Authentication", "JWT / OAuth 2.0 / Supabase Auth"],
                ["Hosting / Infra", "Vercel / AWS / Railway / Fly.io"],
                ["Payments", "Stripe / Paddle / Lemon Squeezy"],
            ],
            "mobile-app": [
                ["Backend", "Node.js / Firebase / Supabase"],
                ["Frontend", "React Native / Flutter / SwiftUI"],
                ["Database", "SQLite (local) / PostgreSQL (server)"],
                ["Cache", "Redis"],
                ["Auth", "Firebase Auth / OAuth 2.0"],
                ["Push Notifications", "OneSignal / Firebase Cloud Messaging"],
                ["Hosting", "AWS / Google Cloud / Vercel"],
            ],
            "landing-page": [
                ["Frontend", "Next.js / Astro / Hugo"],
                ["Styling", "Tailwind CSS / Bootstrap"],
                ["Analytics", "Plausible / Google Analytics / Fathom"],
                ["Forms", "React Hook Form / Formspree / Web3Forms"],
                ["Hosting", "Vercel / Netlify / Cloudflare Pages"],
                ["CMS", "Contentful / Sanity / Strapi"],
            ],
            "api-service": [
                ["Backend", "FastAPI / Express / Go / Rust"],
                ["Database", "PostgreSQL / MySQL"],
                ["Cache", "Redis"],
                ["Queue", "RabbitMQ / Celery / Bull"],
                ["Auth", "JWT / API Keys / OAuth 2.0"],
                ["Hosting", "Docker + K8s / AWS ECS / Railway"],
                ["Monitoring", "Datadog / Grafana / Sentry"],
            ],
            "e-commerce": [
                ["Backend", "Next.js / Django / Shopify API"],
                ["Frontend", "Next.js / Remix / Nuxt"],
                ["Database", "PostgreSQL"],
                ["Cache", "Redis / Varnish"],
                ["Payments", "Stripe / PayPal / Square"],
                ["Search", "Algolia / Meilisearch / Elasticsearch"],
                ["Hosting", "Vercel / AWS / Shopify"],
            ],
            "internal-tool": [
                ["Backend", "FastAPI / Django / Node.js"],
                ["Frontend", "React / Retool / Streamlit"],
                ["Database", "PostgreSQL / SQLite"],
                ["Auth", "OAuth 2.0 / SAML / SSO"],
                ["Hosting", "Docker / Kubernetes / Railway"],
            ],
        }
        return stacks.get(self.project_type, [])

    def _parse_tech_stack(self, stack_str: str) -> List[List[str]]:
        parts = [s.strip() for s in stack_str.split("+")]
        result = []
        main_layers = {
            "next": "Frontend",
            "react": "Frontend",
            "vue": "Frontend",
            "tailwind": "Styling",
            "prisma": "Database ORM",
            "postgresql": "Database",
            "postgres": "Database",
            "supabase": "Backend / Database",
            "firebase": "Backend / Database",
            "vercel": "Hosting",
            "aws": "Hosting",
            "stripe": "Payments",
            "redis": "Cache",
            "docker": "Containerization",
            "kubernetes": "Orchestration",
            "fastapi": "Backend",
            "express": "Backend",
            "django": "Backend",
            "flask": "Backend",
            "graphql": "API Layer",
            "trpc": "API Layer",
            "prisma": "Database ORM",
            "typeorm": "Database ORM",
        }
        for part in parts:
            lower = part.lower().strip()
            layer = main_layers.get(lower, "Other")
            result.append([layer, part])
        return result

    def _section_architecture(self) -> str:
        archs = {
            "saas": textwrap.dedent(
                """\
                - **Multi-tenant database design**: Row-level tenant isolation using tenant_id on every table.
                - **Subscription lifecycle**: Plan management via Stripe, webhook-driven billing state machine.
                - **Team collaboration**: Workspaces with role-based access control (Owner, Admin, Member).
                - **Background jobs**: Queue for billing events, email notifications, and usage aggregation.
                - **Rate limiting**: Per-tenant API rate limits enforced at the middleware level.
                - **Audit logging**: Immutable log for all billing and administration actions.
                - **Webhook system**: Outbound webhooks for tenant integrations (events: invoice.paid, subscription.canceled)."""
            ),
            "mobile-app": textwrap.dedent(
                """\
                - **Offline-first architecture**: Local SQLite database with background sync engine.
                - **Push notification pipeline**: Device token registration, topic-based notifications.
                - **Biometric authentication**: Face ID / fingerprint integration with fallback to PIN.
                - **State management**: Centralized store with optimistic updates and conflict resolution.
                - **Background processing**: Workout/activity syncing, cache prefetching, content downloads."""
            ),
            "landing-page": textwrap.dedent(
                """\
                - **Static site generation**: SSG with ISR for dynamic content sections.
                - **SEO-first structure**: Semantic HTML, meta tags, Open Graph, JSON-LD structured data.
                - **Analytics pipeline**: Privacy-first analytics with GDPR consent management.
                - **A/B testing framework**: Variant routing based on cookies or feature flags.
                - **Form submission flow**: Client validation -> API -> CRM integration with spam filtering."""
            ),
            "api-service": textwrap.dedent(
                """\
                - **RESTful / GraphQL API design**: Resource-oriented endpoints with versioning.
                - **Microservices architecture**: Domain-driven service decomposition.
                - **Authentication layer**: JWT-based auth with API key support for machine-to-machine.
                - **Rate limiting**: Per-client rate limits with token bucket algorithm.
                - **Caching strategy**: Multi-tier (in-memory + Redis) with cache invalidation patterns.
                - **Observability**: Structured logging, metrics, distributed tracing."""
            ),
            "e-commerce": textwrap.dedent(
                """\
                - **Catalog system**: Product variants, inventory tracking, category tree.
                - **Cart engine**: Session-persistent cart with real-time inventory checks.
                - **Checkout pipeline**: Address validation -> payment -> order confirmation.
                - **Payment orchestration**: Stripe integration with webhook reconciliation.
                - **Search infrastructure**: Full-text + faceted search with Algolia/Meilisearch.
                - **Order lifecycle**: Placed -> Confirmed -> Shipped -> Delivered -> Returned."""
            ),
            "internal-tool": textwrap.dedent(
                """\
                - **Authentication & RBAC**: SSO integration with role-based access control.
                - **Data layer**: Repository pattern with PostgreSQL/SQLite backend.
                - **CRUD scaffolding**: Consistent pattern for create, read, update, delete operations.
                - **Audit trail**: Row-level change tracking with before/after snapshots.
                - **Export pipeline**: CSV/JSON/PDF export with scheduled report generation."""
            ),
        }

        desc = archs.get(
            self.project_type,
            "- Clean architecture with separation of concerns.\n- Repository pattern for data access.",
        )

        return textwrap.dedent(
            f"""\
            ## 3. System Architecture & Design Patterns

            **Design Patterns used**:
            - Repository Pattern
            - Adapter Pattern (for third-party services)
            - Strategy Pattern (for interchangeable algorithms)
            - Observer Pattern (for event-driven features)

            **Architecture highlights**:

            {desc}"""
        )

    def _section_frontend(self) -> str:
        content = {
            "saas": textwrap.dedent(
                """\
                **Pages**:
                - Landing / marketing site
                - Sign-up / login / password reset
                - Dashboard (overview, key metrics, recent activity)
                - Subscription management (plan selection, upgrade/downgrade, billing history)
                - Team management (invite members, roles, permissions)
                - Settings (profile, notifications, API keys, webhooks)
                - Billing portal (Stripe-hosted or custom)

                **Components**:
                - PricingCards (feature comparison, CTA)
                - SubscriptionBadge (current plan, trial days remaining)
                - UsageMeter (API calls, storage, seats)
                - InviteFlow (email invite, accept, role assignment)
                - WebhookTable (endpoints, recent deliveries, retry)"""
            ),
            "mobile-app": textwrap.dedent(
                """\
                **Screens**:
                - Splash / onboarding carousel
                - Sign-up / login with biometric option
                - Home feed / dashboard
                - Detail view with offline indicator
                - Settings (profile, notifications, privacy)
                - Activity log / history

                **Components**:
                - OfflineBanner (shows connectivity status with retry button)
                - BiometricPrompt (Face ID / fingerprint gate)
                - PushToggle (per-category notification settings)
                - SyncIndicator (last sync time, pending changes count)
                - PullToRefresh (force sync on manual pull)"""
            ),
            "landing-page": textwrap.dedent(
                """\
                **Sections**:
                - Hero (headline, CTA, background media)
                - Features / benefits grid
                - Pricing cards (3-tier comparison)
                - Testimonials / social proof carousel
                - FAQ accordion
                - Contact / waitlist form
                - Footer (links, social, legal)

                **Components**:
                - CTASection (primary + secondary buttons, optional lead capture)
                - AnalyticsTracker (page view, event tracking, GDPR consent)
                - ABTestVariant (conditional rendering based on experiment)
                - FormWithValidation (email, name, custom fields, reCAPTCHA)
                - SEOHead (meta tags, OG tags, JSON-LD schema)"""
            ),
            "api-service": textwrap.dedent(
                """\
                **Interface**:
                - API reference (OpenAPI / Swagger UI)
                - Interactive playground (try endpoints)
                - API key management dashboard
                - Usage analytics and rate limit status

                **Components**:
                - ApiKeyTable (keys with permissions, rotation, revoke)
                - EndpointCard (method, path, description, status)
                - UsageChart (requests over time, breakdown by endpoint)
                - WebhookConfig (URL, events, secret, test delivery)"""
            ),
            "e-commerce": textwrap.dedent(
                """\
                **Pages**:
                - Product listing with filters and search
                - Product detail (images, variants, reviews)
                - Cart (line items, quantity, promo code)
                - Checkout (address, payment, review)
                - Order confirmation
                - User account (orders, addresses, preferences)

                **Components**:
                - ProductCard (image, name, price, rating, add-to-cart)
                - CartDrawer (slide-over cart summary)
                - CheckoutStepper (progress indicator)
                - SearchBar (autocomplete, recent searches)
                - ReviewForm (star rating, text, image upload)"""
            ),
            "internal-tool": textwrap.dedent(
                """\
                **Pages**:
                - Login / SSO redirect
                - Dashboard (key metrics, recent activity)
                - Data tables (sortable, filterable, exportable)
                - CRUD forms (create, edit, delete records)
                - Reports (pre-built, custom, scheduled)
                - Admin panel (user management, audit log)

                **Components**:
                - DataTable (sortable columns, search, pagination, row actions)
                - FormBuilder (field templates, validation rules)
                - FilterPanel (multi-field filters, saved presets)
                - ExportButton (CSV, Excel, PDF options)
                - AuditLog (timeline view with before/after diffs)"""
            ),
        }
        return f"## 4. Frontend Specifications\n\n{content.get(self.project_type, 'Standard web interface with responsive design.')}"

    def _section_backend(self) -> str:
        models = self._models_for_type()
        endpoints = self._endpoints_for_type()
        return textwrap.dedent(
            f"""\
            ## 5. Backend Specifications

            **API Design**: RESTful with JSON responses. Versioned via URL prefix (e.g., `/api/v1/`).

            **Core Models**:
            {models}

            **API Endpoints**:
            {endpoints}"""
        )

    def _models_for_type(self) -> str:
        models = {
            "saas": textwrap.dedent(
                """\
                - `Tenant` (id, name, slug, plan, status, created_at)
                - `User` (id, email, name, role, tenant_id, last_login)
                - `Plan` (id, name, price, interval, features, tier)
                - `Subscription` (id, tenant_id, plan_id, status, current_period_start, current_period_end)
                - `Invoice` (id, tenant_id, amount, currency, status, paid_at, stripe_invoice_id)
                - `PaymentMethod` (id, tenant_id, type, last_four, expiry, stripe_pm_id)
                - `AuditLog` (id, tenant_id, actor_id, action, resource, details, timestamp)
                - `WebhookEndpoint` (id, tenant_id, url, secret, events, status)"""
            ),
            "mobile-app": textwrap.dedent(
                """\
                - `User` (id, email, name, auth_provider, biometric_enabled)
                - `Device` (id, user_id, platform, push_token, last_seen)
                - `Notification` (id, user_id, title, body, read_at, created_at)
                - `SyncQueue` (id, user_id, entity_type, entity_id, action, payload, synced_at)
                - `Activity` (id, user_id, type, data, created_at)"""
            ),
            "landing-page": textwrap.dedent(
                """\
                - `FormSubmission` (id, name, email, message, source, created_at)
                - `AnalyticsEvent` (id, session_id, event_type, page, metadata, timestamp)
                - `Lead` (id, email, name, source, status, converted_at)
                - `ABTestVariant` (id, experiment_id, variant, impressions, conversions)
                - `ConsentRecord` (id, visitor_id, consent_type, granted, timestamp)"""
            ),
            "api-service": textwrap.dedent(
                """\
                - `ApiKey` (id, description, key_hash, permissions, expires_at, last_used)
                - `WebhookEndpoint` (id, url, events, secret, retry_config)
                - `UsageRecord` (id, api_key_id, endpoint, status_code, response_time, timestamp)
                - `RateLimit` (id, client_id, window_start, request_count, limit)
                - `AuditLog` (id, actor, action, resource, details, ip_address, timestamp)"""
            ),
            "e-commerce": textwrap.dedent(
                """\
                - `Product` (id, name, description, price, currency, category_id, status)
                - `ProductVariant` (id, product_id, sku, attributes, price_adjustment, stock)
                - `Category` (id, name, slug, parent_id, sort_order)
                - `Cart` (id, session_id, user_id, items, coupon, total)
                - `Order` (id, user_id, status, items, total, shipping_address, payment_intent)
                - `Review` (id, product_id, user_id, rating, title, body, verified_purchase)"""
            ),
            "internal-tool": textwrap.dedent(
                """\
                - `User` (id, email, name, role, department, last_login)
                - `Record` (id, type, data, status, created_by, updated_at)
                - `AuditLog` (id, record_id, action, field, old_value, new_value, actor_id, timestamp)
                - `Report` (id, name, query, schedule, recipients, last_run)
                - `Export` (id, user_id, record_ids, format, status, file_url, created_at)"""
            ),
        }
        return models.get(self.project_type, "- `User` (id, email, name, role, created_at)")

    def _endpoints_for_type(self) -> str:
        endpoints = {
            "saas": textwrap.dedent(
                """\
                - `POST /api/v1/auth/register` — Create account with tenant
                - `POST /api/v1/auth/login` — Authenticate user
                - `GET /api/v1/tenants/me` — Current tenant details
                - `GET /api/v1/subscriptions` — List/current subscription
                - `POST /api/v1/subscriptions/checkout` — Create checkout session
                - `POST /api/v1/subscriptions/cancel` — Cancel subscription
                - `GET /api/v1/invoices` — List invoices
                - `GET /api/v1/team` — List team members
                - `POST /api/v1/team/invite` — Invite team member
                - `GET /api/v1/usage` — Current usage metrics
                - `POST /api/v1/webhooks` — Register outbound webhook
                - `POST /api/v1/webhooks/{id}/test` — Test webhook delivery"""
            ),
            "mobile-app": textwrap.dedent(
                """\
                - `POST /api/v1/auth/register` — Create account
                - `POST /api/v1/auth/login` — Authenticate with optional biometric token
                - `POST /api/v1/devices/register` — Register push notification token
                - `DELETE /api/v1/devices/{id}` — Unregister device
                - `GET /api/v1/notifications` — List notifications
                - `PUT /api/v1/notifications/{id}/read` — Mark as read
                - `POST /api/v1/sync/push` — Push local changes to server
                - `GET /api/v1/sync/pull?since={timestamp}` — Pull changes since last sync"""
            ),
            "landing-page": textwrap.dedent(
                """\
                - `POST /api/forms/submit` — Submit contact/waitlist form (with reCAPTCHA)
                - `GET /api/health` — Health check endpoint
                - `POST /api/analytics/event` — Track analytics event
                - `POST /api/consent/update` — Update GDPR consent preference
                - `GET /api/ab-test/{experiment}` — Get assigned variant"""
            ),
            "api-service": textwrap.dedent(
                """\
                - `POST /api/v1/auth/token` — Exchange credentials for JWT
                - `POST /api/v1/auth/refresh` — Refresh access token
                - `GET /api/v1/keys` — List API keys
                - `POST /api/v1/keys` — Create API key
                - `DELETE /api/v1/keys/{id}` — Revoke API key
                - `GET /api/v1/usage` — Get usage metrics
                - `POST /api/v1/webhooks` — Register webhook
                - `GET /api/v1/health` — Health check
                - `GET /api/v1/status` — Service status"""
            ),
            "e-commerce": textwrap.dedent(
                """\
                - `GET /api/v1/products` — List products (with filters, search, pagination)
                - `GET /api/v1/products/{id}` — Product details with variants
                - `POST /api/v1/cart/items` — Add to cart
                - `PUT /api/v1/cart/items/{id}` — Update cart item quantity
                - `DELETE /api/v1/cart/items/{id}` — Remove from cart
                - `POST /api/v1/checkout` — Create checkout session
                - `POST /api/v1/orders/{id}/cancel` — Cancel order
                - `GET /api/v1/orders` — List user orders
                - `POST /api/v1/products/{id}/reviews` — Submit review"""
            ),
            "internal-tool": textwrap.dedent(
                """\
                - `POST /api/v1/auth/login` — SSO login
                - `GET /api/v1/records` — List records (filter, sort, paginate)
                - `POST /api/v1/records` — Create record
                - `GET /api/v1/records/{id}` — Get record details
                - `PUT /api/v1/records/{id}` — Update record
                - `DELETE /api/v1/records/{id}` — Delete record
                - `GET /api/v1/reports` — List reports
                - `POST /api/v1/reports/{id}/run` — Execute report
                - `GET /api/v1/audit-log` — Query audit log"""
            ),
        }
        return endpoints.get(
            self.project_type,
            "- `POST /api/v1/auth/login` — Authenticate\n- `GET /api/v1/health` — Health check",
        )

    def _section_testing(self) -> str:
        content = {
            "saas": textwrap.dedent(
                """\
                - **Unit tests**: 80%+ coverage on billing logic, plan calculations, rate limiting
                - **Integration tests**: API endpoint tests with test database, Stripe mock
                - **E2E tests**: Critical flows — signup, checkout, team invite, subscription change
                - **Contract tests**: Webhook payloads, Stripe event handling
                - **Load tests**: Multi-tenant concurrency, rate limit enforcement"""
            ),
            "mobile-app": textwrap.dedent(
                """\
                - **Unit tests**: Local SQLite operations, sync conflict resolution, validation logic
                - **Widget tests**: UI component rendering and interaction
                - **Integration tests**: API mocking with offline/online state transitions
                - **Device tests**: Physical device testing for biometrics, push notifications
                - **E2E tests**: Critical user flows on iOS and Android simulators"""
            ),
            "landing-page": textwrap.dedent(
                """\
                - **Visual regression tests**: Screenshot comparison for all viewport sizes
                - **Form validation tests**: Edge cases, spam filtering, required fields
                - **Analytics tests**: Event firing on page load, CTA clicks, form submissions
                - **Performance tests**: Lighthouse CI with thresholds (LCP < 2.5s, CLS < 0.1)
                - **A11y tests**: Axe-core scans for WCAG 2.1 AA compliance"""
            ),
            "api-service": textwrap.dedent(
                """\
                - **Unit tests**: Service layer, validation logic, utility functions
                - **Integration tests**: Database operations, external API mocking
                - **Contract tests**: API response format, status codes, error shapes
                - **Performance tests**: p99 latency under load, throughput benchmarks
                - **Security tests**: Auth bypass attempts, injection patterns, rate limit abuse"""
            ),
            "e-commerce": textwrap.dedent(
                """\
                - **Unit tests**: Pricing calculations, inventory logic, cart operations
                - **Integration tests**: Checkout flow with payment processor mock
                - **E2E tests**: Add to cart -> checkout -> payment confirmation
                - **Payment tests**: Stripe webhook handling, refund processing, failed payments
                - **Load tests**: Black Friday traffic simulation, cart concurrency"""
            ),
            "internal-tool": textwrap.dedent(
                """\
                - **Unit tests**: CRUD operations, validation, authorization checks
                - **Integration tests**: Database queries, export generation, report execution
                - **E2E tests**: Login -> create record -> edit -> delete flow
                - **Security tests**: Role-based access enforcement, data leakage prevention"""
            ),
        }
        return f"## 6. Testing Strategy\n\n{content.get(self.project_type, 'Standard testing with unit, integration, and E2E tests.')}"

    def _section_git_workflow(self) -> str:
        return textwrap.dedent(
            """\
            ## 7. Git Workflow

            **Branching model**: GitHub Flow (or Git Flow for larger teams)

            - `main` — Production-ready, protected branch
            - `develop` — Integration branch (if using Git Flow)
            - `feat/xxx` — Feature branches from `main` or `develop`
            - `fix/xxx` — Bug fix branches
            - `chore/xxx` — Maintenance, dependency updates, CI changes

            **Commit convention**: Conventional Commits

            ```
            feat: Add subscription upgrade flow
            fix: Handle Stripe webhook timeout
            chore: Update dependencies
            docs: Add API authentication guide
            ```

            **PR process**:
            1. Create branch from `main`
            2. Implement changes with tests
            3. Lint + typecheck + test pass
            4. Open PR with description and screenshots (if UI)
            5. At least 1 reviewer approval required
            6. Squash-merge to `main`"""
        )

    def _section_deployment(self) -> str:
        content = {
            "saas": textwrap.dedent(
                """\
                **Environments**: staging, production

                **Staging**: Auto-deployed from `main` branch
                - Preview URLs for each PR via Vercel

                **Production**: Manual promotion from staging
                - Database migrations run as part of deploy
                - Rollback via Vercel instant rollback
                - Feature flags for gradual rollout

                **CI/CD pipeline**:
                1. `npm run lint` + `npm run typecheck`
                2. `npm run test` (unit + integration)
                3. `npm run build`
                4. Deploy to staging
                5. Run E2E tests on staging
                6. Manual approval for production"""
            ),
            "mobile-app": textwrap.dedent(
                """\
                **iOS**: TestFlight (beta) -> App Store
                - Build: `fastlane ios build`
                - Beta: `fastlane ios beta` (TestFlight internal)
                - Release: `fastlane ios release` (App Store)

                **Android**: Internal track -> Play Store
                - Build: `fastlane android build`
                - Beta: `fastlane android beta` (internal track)
                - Release: `fastlane android release` (production)

                **Code push**: Over-the-air updates via EAS Update / CodePush for non-native changes"""
            ),
            "landing-page": textwrap.dedent(
                """\
                **Hosting**: Vercel / Netlify

                **Deploy**:
                - Auto-deploy on merge to `main`
                - Preview deployments for each PR
                - CDN cache invalidation on deploy
                - Atomic deploys (instant rollback)

                **CI checks**:
                1. `npm run lint`
                2. `npm run build`
                3. `npm run lighthouse` (performance budget)
                4. Deploy to production

                **Performance SLA**: Lighthouse >90 all categories"""
            ),
            "api-service": textwrap.dedent(
                """\
                **Containerization**: Docker multi-stage builds

                **Orchestration**: Kubernetes (EKS / GKE / AKS)

                **Environments**: dev, staging, production

                **Deployment strategy**: Rolling update with health checks

                **CI/CD pipeline**:
                1. Lint + typecheck
                2. Unit + integration tests
                3. Build Docker image
                4. Push to container registry
                5. Deploy to staging
                6. Smoke tests on staging
                7. Promote to production"""
            ),
            "e-commerce": textwrap.dedent(
                """\
                **Environments**: staging, production

                **Staging**: Mirrors production with test payment processor

                **Production**: 
                - Deploy during low-traffic window
                - Database migrations: backward-compatible, zero-downtime
                - Cache warm after deploy
                - Feature flags control new checkout flows

                **CI/CD pipeline**:
                1. Lint + typecheck
                2. Unit + integration tests
                3. Build + deploy to staging
                4. E2E checkout tests on staging
                5. Manual approval for production"""
            ),
            "internal-tool": textwrap.dedent(
                """\
                **Deployment**: Docker container to internal server / cloud

                **CI/CD pipeline**:
                1. Lint + typecheck
                2. Unit tests
                3. Build Docker image
                4. Push to internal registry
                5. Deploy with zero-downtime strategy
                6. Smoke test critical paths"""
            ),
        }
        return f"## 8. Deployment & CI/CD\n\n{content.get(self.project_type, 'Standard CI/CD with testing and automated deployment.')}"

    def _section_documentation(self) -> str:
        return textwrap.dedent(
            f"""\
            ## 9. Documentation Guidelines

            - **Inline comments**: Explain why a decision was made, not what the code does
            - **API documentation**: OpenAPI 3.1 spec in `docs/api.yaml`, auto-generated from code
            - **Architecture Decision Records**: ADRs in `docs/adr/` for significant decisions
            - **README.md**: Project overview, quick start, development guide
            - **CONTRIBUTING.md**: How to set up, test, and submit changes
            - **CHANGELOG.md**: Keep a changelog, one entry per significant change
            - **Runbooks**: Operational procedures in `docs/runbooks/`

            **AI-generated documentation** must be reviewed by a human before merging."""
        )

    def _section_coding_standards(self) -> str:
        return textwrap.dedent(
            """\
            ## 10. Coding Standards

            **Language-specific**:
            - TypeScript: Strict mode, no `any`, prefer `type` over `interface`
            - Python: Type hints on all public functions, black formatting
            - Go: `gofmt` + `golangci-lint`, no global state
            - Rust: `clippy` clean, all `unwrap()` justified with comments

            **General rules**:
            - ESLint / Ruff / golangci-lint must pass with zero warnings
            - Prettier / dprint for formatting (enforced in CI)
            - No `console.log` / `print` in committed code (use proper logging)
            - All public functions must have docstrings / JSDoc
            - No hardcoded secrets or URLs — use environment variables
            - Import organization: stdlib → third-party → internal

            **Testing rules**:
            - New feature = at least unit test for core logic
            - Bug fix = regression test before fix
            - Test descriptions state what is being verified"""
        )

    def _section_environment(self) -> str:
        return textwrap.dedent(
            f"""\
            ## 11. Environment Setup

            **Prerequisites**:
            - Node.js >= 18 / Python >= 3.11 / Go >= 1.21 (as applicable)
            - Docker (optional, for local services)
            - Git

            **Step-by-step**:

            ```bash
            # Clone the repository
            git clone https://github.com/org/{self.slug}.git
            cd {self.slug}

            # Install dependencies
            npm install   # or: pip install -r requirements.txt

            # Copy environment variables
            cp .env.example .env
            # Edit .env with your local configuration

            # Set up database
            npm run db:migrate   # or: python manage.py migrate

            # Start development server
            npm run dev           # or: python manage.py runserver
            ```

            **Required environment variables**: (defined in `.env.example`)

            See README.md for complete setup guide."""
        )

    def _section_ai_productivity(self) -> str:
        return textwrap.dedent(
            f"""\
            ## 12. AI Productivity Configuration

            **User-level vs Project-level guidelines**:
            - User-level: ~/.gemini/ or ~/.claude/ for personal preferences
            - Project-level: AGENTS.md (this file) for team-shared configuration

            **Living document principle**:
            When the AI makes a repeated mistake, document the fix here so it learns.
            Examples of patterns to document:

            ✅ **Good examples**:
            - "Always run migrations before deploying: `npm run db:migrate`"
            - "Never commit .env files — they contain secrets"
            - "Use `import type` for type-only imports in TypeScript"
            - "Add regression tests when fixing bugs: test first, then fix"

            ❌ **Bad examples to avoid**:
            - "Writing TODO comments instead of implementing"
            - "Using `any` type instead of proper TypeScript types"
            - "Hardcoding API URLs instead of using environment variables"
            - "Skipping tests because 'it's just a quick fix'"

            **Common mistakes** (add to this list as you encounter them):
            - [Add recurring mistakes here]"""
        )

    def _section_ai_instructions(self) -> str:
        return textwrap.dedent(
            """\
            ## 13. AI-Specific Instructions

            **Interaction guidelines**:
            - Ask clarifying questions before implementing
            - Propose 2-3 approaches when the problem has trade-offs
            - Show diffs or key files when suggesting changes
            - Never modify generated files (dist/, build/, .next/)
            - Never remove code without explaining why

            **Implementation planning protocol**:
            1. Understand the requirement (ask questions if unclear)
            2. Propose approach and get confirmation
            3. Implement with tests
            4. Run linter + typecheck + existing tests
            5. Present result with summary of changes

            **Parallel task execution strategy**:
            - Independent tasks can be executed in parallel
            - Dependent tasks must be executed sequentially
            - When reviewing, review the full file, not just diffs"""
        )

    def _section_agent_commands(self) -> str:
        commands = self._commands_for_type()
        if not commands:
            return ""
        table = _table(["Command", "Purpose", "Step-by-step SOP"], commands)
        return f"## 14. Agent Commands\n\n{table}"

    def _commands_for_type(self) -> List[List[str]]:
        base_commands = [
            ["/lint", "Run linter and auto-fix", "`npm run lint` → fix issues → `npm run lint` again"],
            ["/test", "Run test suite", "`npm run test` → review failures → fix"],
            ["/typecheck", "Run type checker", "`npm run typecheck` → fix type errors"],
            ["/build", "Build project", "`npm run build` → verify no errors"],
        ]
        extra = {
            "saas": [
                ["/deploy-staging", "Deploy to staging environment", "`git push staging main` → verify health endpoint → run smoke tests"],
                ["/provision-tenant", "Create a new tenant for testing", "Run tenant provisioning script → verify tenant isolation → seed test data"],
                ["/test-billing", "Run billing-related tests", "`npm run test -- --testPathPattern=billing` → verify Stripe mock responses"],
                ["/run-migrations", "Run database migrations", "`npm run db:migrate` → verify migration applied → `npm run db:seed` if needed"],
                ["/inspect-webhook", "Inspect Stripe webhook events", "Check Stripe dashboard recent events → compare with webhook handler logs"],
            ],
            "mobile-app": [
                ["/build-ios", "Build iOS app", "`fastlane ios build` → verify archive → upload to TestFlight"],
                ["/build-android", "Build Android app", "`fastlane android build` → generate AAB → upload to Play Console"],
                ["/test-push", "Test push notifications", "Send test push via FCM console → verify device receives → check notification tap handling"],
                ["/generate-screenshots", "Generate app store screenshots", "`fastlane snapshot` → verify screenshots → upload to App Store Connect"],
            ],
            "landing-page": [
                ["/deploy", "Deploy to production", "Merge PR to `main` → Vercel auto-deploys → verify staging → promote to production"],
                ["/test-seo", "Run SEO audit", "Check meta tags, OG tags → run structured data test → verify sitemap → check robots.txt"],
                ["/check-lighthouse", "Run Lighthouse audit", "`npx lighthouse https://staging.url --view` → verify scores >90 → address issues"],
                ["/run-ab-test", "Run A/B test", "Configure variant → set experiment split → deploy → monitor conversion metrics"],
            ],
            "api-service": [
                ["/test-endpoint", "Test a specific API endpoint", "`curl` or Postman → verify response status, body, headers"],
                ["/check-openapi", "Validate OpenAPI spec", "`npm run openapi:validate` → check for breaking changes → regenerate docs"],
                ["/run-load-test", "Run load tests", "`k6 run tests/load/smoke.js` → check p95 latency → review error rate"],
            ],
            "e-commerce": [
                ["/test-checkout", "Run full checkout E2E", "Run Cypress checkout test → verify Stripe test payment → confirm order creation"],
                ["/check-inventory", "Check inventory levels", "Query stock levels → identify low-stock SKUs → generate reorder report"],
                ["/test-stripe-webhook", "Test Stripe webhook handling", "Use Stripe CLI to trigger events → verify handler processes → check order status"],
            ],
            "internal-tool": [
                ["/run-migrations", "Run database migrations", "`npm run db:migrate` → verify migration applied"],
                ["/test-auth", "Test authentication flow", "Test SSO login → verify RBAC → test permission boundaries"],
                ["/export-data", "Export data to CSV/Excel", "`python scripts/export.py --format csv` → verify output"],
            ],
        }
        return base_commands + extra.get(self.project_type, [])

    def _section_development_phases(self) -> str:
        phases = {
            "saas": textwrap.dedent(
                """\
                **Phase 1 (MVP)**: Authentication, user management, basic subscription with Stripe
                **Phase 2 (Core)**: Team collaboration, webhook system, dashboard analytics
                **Phase 3 (Scale)**: Usage-based pricing, advanced billing, multi-region support
                **Phase 4 (Enterprise)**: SSO, audit logging, custom contracts, SLA monitoring"""
            ),
            "mobile-app": textwrap.dedent(
                """\
                **Phase 1 (MVP)**: Authentication, core feature, offline read mode
                **Phase 2 (Engagement)**: Push notifications, social features, content creation
                **Phase 3 (Monetization)**: Premium subscriptions, in-app purchases, ads
                **Phase 4 (Scale)**: Multi-language, personalization, advanced analytics"""
            ),
            "landing-page": textwrap.dedent(
                """\
                **Phase 1 (Launch)**: Hero, features, pricing, contact form, analytics
                **Phase 2 (Optimize)**: A/B testing, heatmaps, conversion optimization
                **Phase 3 (Scale)**: Blog, case studies, multi-language support
                **Phase 4 (Retain)**: User portal, email sequences, retargeting"""
            ),
            "api-service": textwrap.dedent(
                """\
                **Phase 1 (Core)**: Authentication, CRUD endpoints, basic rate limiting
                **Phase 2 (Reliability)**: Caching, monitoring, error tracking, documentation
                **Phase 3 (Scale)**: Webhooks, usage tiers, multi-region deployment
                **Phase 4 (Enterprise)**: SSO, audit logs, SLA guarantees"""
            ),
            "e-commerce": textwrap.dedent(
                """\
                **Phase 1 (MVP)**: Product catalog, cart, checkout, payment processing
                **Phase 2 (Trust)**: Reviews, ratings, order tracking, customer support
                **Phase 3 (Scale)**: Multi-vendor, marketplace, promotions engine
                **Phase 4 (Optimize)**: Personalization, recommendations, loyalty program"""
            ),
            "internal-tool": textwrap.dedent(
                """\
                **Phase 1 (MVP)**: Authentication, core CRUD, basic reporting
                **Phase 2 (Usability)**: Advanced filters, export, role-based access
                **Phase 3 (Automation)**: Scheduled reports, notifications, integrations
                **Phase 4 (Scale)**: SSO, audit logs, custom workflows"""
            ),
        }
        return f"## 15. Development Phases\n\n{phases.get(self.project_type, 'Phased rollout with iterative feature delivery.')}"

    def _section_revision_history(self) -> str:
        return textwrap.dedent(
            """\
            ## 16. Revision History

            | Date | Change | Reason |
            |------|--------|--------|
            | {today} | Initial AGENTS.md created | Project setup |

            ---

            *This AGENTS.md is a living document. Update it whenever new patterns emerge or mistakes are corrected.*""".format(
                today=self.today
            )
        )

    def _footer(self) -> str:
        return ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a tailored AGENTS.md file for a software project."
    )
    parser.add_argument(
        "--project-name",
        required=True,
        help="Name of the project (e.g., 'FlowPay')",
    )
    parser.add_argument(
        "--project-type",
        required=True,
        choices=VALID_TYPES_LIST,
        help=f"Type of project. Choices: {', '.join(VALID_TYPES_LIST)}",
    )
    parser.add_argument(
        "--key-terms",
        required=True,
        help="Comma-separated list of key terms (e.g., 'multi-tenant,subscription billing')",
    )
    parser.add_argument(
        "--tech-stack",
        default="",
        help="Technology stack (e.g., 'Next.js + Tailwind + PostgreSQL')",
    )
    parser.add_argument(
        "--additional-context",
        default="",
        help="Additional context (compliance needs, target audience, etc.)",
    )
    parser.add_argument(
        "--output",
        default="AGENTS.md",
        help="Output file path (default: AGENTS.md)",
    )

    args = parser.parse_args()

    if args.project_type not in VALID_TYPES:
        print(
            f"Error: Invalid project type '{args.project_type}'. "
            f"Valid types: {', '.join(VALID_TYPES_LIST)}",
            file=sys.stderr,
        )
        sys.exit(2)

    if not args.project_name.strip():
        print("Error: Project name cannot be empty.", file=sys.stderr)
        sys.exit(1)

    if not args.key_terms.strip():
        print("Error: Key terms cannot be empty.", file=sys.stderr)
        sys.exit(1)

    key_terms = _ensure_list(args.key_terms)
    if len(key_terms) == 0:
        print("Error: At least one key term is required.", file=sys.stderr)
        sys.exit(1)

    generator = AgentsMDGenerator(
        project_name=args.project_name.strip(),
        project_type=args.project_type,
        key_terms=key_terms,
        tech_stack=args.tech_stack.strip(),
        additional_context=args.additional_context.strip(),
    )

    try:
        content = generator.generate()
    except Exception as exc:
        print(f"Error: Failed to generate AGENTS.md: {exc}", file=sys.stderr)
        sys.exit(3)

    if not content.strip():
        print("Error: Generated content is empty.", file=sys.stderr)
        sys.exit(3)

    output_path = Path(args.output)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
    except OSError as exc:
        print(f"Error: Could not write output file '{output_path}': {exc}", file=sys.stderr)
        sys.exit(3)

    print(f"AGENTS.md generated successfully: {output_path.resolve()}")
    print(f"Project: {args.project_name} ({args.project_type})")
    print(f"Key terms: {', '.join(key_terms)}")
    word_count = len(content.split())
    print(f"Content: ~{word_count} words across ~{content.count(chr(10)) + 1} lines")
    sys.exit(0)


if __name__ == "__main__":
    main()
