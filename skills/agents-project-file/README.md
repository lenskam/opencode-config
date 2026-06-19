# agents-project-file

Generate production-ready `AGENTS.md` files for AI agents working on software projects. Supports 6 project types: SaaS, Mobile App, Landing Page, API Service, E-commerce, and Internal Tool.

## Quick Start

```bash
# Direct invocation
python scripts/generate_agents_md.py \
  --project-name "FlowPay" \
  --project-type saas \
  --key-terms "multi-tenant,subscription billing,team collaboration" \
  --tech-stack "Next.js + Tailwind + Prisma + PostgreSQL + Stripe + Vercel" \
  --output AGENTS.md
```

## Installation

### OpenCode (auto-detected on this platform)

```bash
./install.sh
```

### Other Platforms

```bash
./install.sh --platform cursor   # Cursor
./install.sh --platform claude-code  # Claude Code
./install.sh --platform copilot  # GitHub Copilot
./install.sh --all               # All detected platforms
```

## Usage via Skill

Once installed, activate the skill with natural language:

```
/agents-project-file Project: FlowPay, Type: SaaS, Key Terms: multi-tenant, subscription billing, Tech: Next.js + Stripe
```

Or without the prefix:

```
Create an AGENTS.md for a new SaaS project
Make a GEMINI.md for my landing page
Generate agent instructions for an API service
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate_agents_md.py` | Main AGENTS.md generator |
| `install.sh` | Cross-platform skill installer |

## Supported Project Types

- `saas` — Multi-tenant SaaS platforms
- `mobile-app` — React Native / Flutter apps
- `landing-page` — Marketing sites
- `api-service` — Backend API services
- `e-commerce` — Online stores
- `internal-tool` — Internal business tools

## License

MIT
