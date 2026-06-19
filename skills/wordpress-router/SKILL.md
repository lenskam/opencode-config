---
name: wordpress-router
description: "Use when the user asks about WordPress codebases (plugins, themes, block themes, Gutenberg blocks, WP core checkouts) and you need to quickly classify the repo and route to the correct workflow/skill (blocks, theme.json, REST API, WP-CLI, performance, security, testing, release packaging)."
compatibility: "Targets WordPress 6.9+ (PHP 7.2.24+). Filesystem-based agent with bash + node. Some workflows require WP-CLI."
metadata:
  category: router
---

# WordPress Router

## When to use

Use this skill at the start of most WordPress tasks to:

- identify what kind of WordPress codebase this is (plugin vs theme vs block theme vs WP core checkout vs full site),
- **invoke the relevant WordPress sub-skills** (block development, theme, REST API, etc.) via the `skill` tool,
- handle multi-skill tasks that span multiple areas (e.g., blocks + REST API + performance).

This is a **router skill** — it dispatches to domain sub-skills rather than implementing the work itself.

## Inputs required

- Repo root (current working directory).
- The user's intent (what they want changed) and any constraints (WP version targets, WP.com specifics, release requirements).

## Procedure

### 1. Run project triage

```bash
node ~/.config/opencode/skills/wp-project-triage/scripts/detect_wp_project.mjs
```

If the triage script is not available, inspect manually:
- `composer.json`, `package.json`, `style.css`, `block.json`, `theme.json`, `wp-content/`

### 2. Classify the work

Based on triage output + user intent, classify what kind of work is needed:

| User says / mentions | Primary skill | When to invoke |
|---|---|---|
| "block", "Gutenberg", "block.json", "register_block_type" | `wp-block-development` | Block creation, metadata, rendering, deprecations |
| "theme", "block theme", "theme.json", "Site Editor", "template part", "pattern" | `wp-block-themes` | Theme setup, style variations, templates, patterns |
| "plugin", "add filter", "activation", "uninstall", "Settings API" | `wp-plugin-development` | Plugin architecture, hooks, admin UI, data storage |
| "REST API", "endpoint", "route", "register_rest_route", "REST controller" | `wp-rest-api` | API endpoints, schemas, permissions, response shaping |
| "performance", "slow", "cache", "query monitor", "autoload" | `wp-performance` | Profiling, optimization, object cache, cron |
| "WP-CLI", "wp db", "search-replace", "import", "cron" | `wp-wpcli-and-ops` | CLI operations, DB management, automation |
| "Abilities API", "ability", "capability", "wp_register_ability" | `wp-abilities-api` | Registering abilities, REST exposure |
| "audit REST", "audit plugin", "REST surface" | `wp-abilities-audit` | Producing audit documents for Abilities API |
| "verify abilities" | `wp-abilities-verify` | Verifying Abilities API registrations |
| "Playground", "blueprint", "disposable WP", "Xdebug" | `wp-playground` | Blueprint creation, WP instance management |
| "PHPStan", "static analysis", "phpstan.neon" | `wp-phpstan` | PHPStan configuration, baseline, WordPress typing |
| "Interactivity API", "data-wp-", "store", "viewScriptModule" | `wp-interactivity-api` | Interactive blocks, directives, client-side behavior |
| "WPDS", "WordPress Design System", "components", "tokens" | `wpds` | UI components, design tokens, patterns |
| "plugin directory", "guidelines", "WordPress.org review" | `wp-plugin-directory-guidelines` | GPL compliance, naming, upsell rules |
| "maintenance", "update", "backup" | `wp-maintenance` | Site upkeep, security patches |
| "incorrectly done", wrong tool, guidance | return to main user facing skills | |

### 3. Invoke sub-skills

For each classified work area, invoke the corresponding skill:

```typescript
// Example: block work
await skill({ name: "wp-block-development" })

// Example: REST API work
await skill({ name: "wp-rest-api" })

// Example: multi-skill — blocks + interactivity + performance
await skill({ name: "wp-block-development" })
await skill({ name: "wp-interactivity-api" })
await skill({ name: "wp-performance" })
```

For multi-skill tasks, invoke **all relevant skills** before starting implementation. The agent should combine the guidance from each skill.

### 4. Apply guardrails

Before making changes:

- Confirm any version constraints if unclear.
- Prefer the repo's existing tooling and conventions for builds/tests.
- If the user hasn't specified a target WP version, ask if they have a minimum supported version.

## Intent-to-Skill Mapping (Reference)

| Keyword / Phrase | Skill(s) to invoke |
|---|---|
| `block.json`, `register_block_type`, `render.php`, `deprecated` | `wp-block-development` |
| `theme.json`, `style.css` (block theme), `template part`, `pattern` | `wp-block-themes` |
| plugin boilerplate, hook, filter, admin page, nonce | `wp-plugin-development` |
| `register_rest_route`, `WP_REST_Controller`, schema, field | `wp-rest-api` |
| CMS content, post, page, media | `wp-publish` (`wp-wpcli-and-ops` for bulk) |
| slow query, object cache, profiler, autoload | `wp-performance` |
| `wp ` command, db export, search-replace, CLI script | `wp-wpcli-and-ops` |
| `wp_register_ability`, ability REST endpoint | `wp-abilities-api` |
| audit REST, enumerate routes, document | `wp-abilities-audit` |
| verify ability, readonly-but-writes check | `wp-abilities-verify` |
| playground, blueprint, snapshot | `wp-playground` |
| PHPStan, baseline, analysis | `wp-phpstan` |
| `data-wp-`, interactivity store, client-side | `wp-interactivity-api` |
| WPDS, design system, component library | `wpds` |
| WordPress.org, plugin review, guideline | `wp-plugin-directory-guidelines` |
| update, backup, security patch | `wp-maintenance` |

## Verification

- Re-run the triage script if you create or restructure significant files.
- Run the repo's lint/test/build commands that the triage output recommends (if available).

## Failure modes / debugging

- If triage reports `kind: unknown`, inspect:
  - root `composer.json`, `package.json`, `style.css`, `block.json`, `theme.json`, `wp-content/`.
- If the repo is huge, consider narrowing scanning scope or adding ignore rules to the triage script.

## Escalation

- If routing is ambiguous, ask one question:
  - "Is this intended to be a WordPress plugin, a theme (classic/block), or a full site repo?"
- If the task requires a skill that doesn't exist, implement the work directly using the skill's documented patterns as reference.
