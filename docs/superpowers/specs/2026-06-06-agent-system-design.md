# Agent System for B2B Tech Company

## Objective
A multi-agent system within OpenCode that serves as a team of workers for a tech company building B2B products. The system routes user prompts to domain-specific agents that can operate independently or collaborate sequentially.

## Architecture

### Routing Layer
- **Router Skill** (`skills/router/SKILL.md`) — detects intent from user prompts via two mechanisms:
  1. Explicit `#phrase#` tags: `#wordpress`, `#n8n`, `#software`, `#content`
  2. NLP fallback: keyword analysis when no tag is present
- Single-agent tasks → dispatch directly to the matching agent
- Multi-agent tasks → orchestrate sequentially, passing context/artifact paths between agents

### Agents (opencode.json)

Each main agent is defined in `opencode.json` with its own system prompt and model configuration. Sub-agents are implemented as skills under each agent's directory.

---

## Agent: WordPress Dev

**Tag:** `#wordpress`
**Role:** WordPress site development, content publishing, and maintenance.

### Sub-Agent Skills
| Skill | Purpose |
|-------|---------|
| `wp-publish` | Blog/page publishing (priority), media management, draft-to-publish workflow |
| `wp-theme` | Custom theme development, child themes, template hierarchy |
| `wp-plugin` | Custom plugin development, hooks, filters |
| `wp-maintenance` | Updates, backups, security hardening, performance optimization |

---

## Agent: n8n Automations

**Tag:** `#n8n`
**Role:** Building and troubleshooting n8n workflow automations.

### Sub-Agent Skills
| Skill | Purpose |
|-------|---------|
| `n8n-new` | Build new workflows from requirements |
| `n8n-troubleshoot` | Debug and fix broken or failing workflows |
| `n8n-google` | Google Docs, Sheets, Slides, Gmail, Drive integrations |
| `n8n-messaging` | WhatsApp, Telegram messaging integrations |
| `n8n-gemini` | Gemini AI node patterns and integrations |

---

## Agent: Software Dev

**Tag:** `#software`
**Role:** Full-stack web and mobile application development.

### Sub-Agent Skills
| Skill | Purpose |
|-------|---------|
| `sw-api` | API design & development (REST, GraphQL, gRPC) |
| `sw-web` | Full-stack web application development |
| `sw-mobile` | Mobile app development (React Native, etc.) |
| `sw-devops` | Deployment, CI/CD pipelines, infrastructure |
| `sw-db` | Database schema design, migrations, query optimization |

---

## Agent: Content Creation

**Tag:** `#content`
**Role:** Content strategy, creation, and publishing across all formats.

### Sub-Agent Skills
| Skill | Purpose |
|-------|---------|
| `cc-social` | Social media content, scheduling, platform-specific formatting |
| `cc-shorts` | Short-form video (Reels, TikTok, YouTube Shorts) |
| `cc-videos` | Long-form video content planning and scripting |
| `cc-photo` | Photography, image creation and editing |
| `cc-video_editing` | Post-production video editing |
| `cc-blog` | Blog posts, articles, long-form writing |
| `cc-marketing` | Email campaigns, landing pages, ad copy |
| `cc-seo` | Keyword research, on-page SEO, meta optimization |

---

## Cross-Agent Handoff Patterns

When a task spans multiple agents, the router orchestrates sequentially:

1. **Content → WordPress:** Content agent creates blog/social → hands off to WordPress agent for publishing
2. **Software → n8n:** Software agent builds an API → n8n agent creates automations around it
3. **Content → n8n:** Content agent creates a campaign → n8n agent schedules/automates distribution

Handoffs pass a summary and artifact path rather than the full work product to keep context efficient.

## File Structure

```
~/projects/agents-pack/
├── deploy.sh                  # One-command deploy: symlinks skills + merges agent config
├── opencode.json              # Agent definitions to merge into existing config
├── skills/
│   ├── router/SKILL.md        # Router/dispatcher skill
│   ├── wp-publish/SKILL.md
│   ├── wp-theme/SKILL.md
│   ├── wp-plugin/SKILL.md
│   ├── wp-maintenance/SKILL.md
│   ├── n8n-new/SKILL.md
│   ├── n8n-troubleshoot/SKILL.md
│   ├── n8n-google/SKILL.md
│   ├── n8n-messaging/SKILL.md
│   ├── n8n-gemini/SKILL.md
│   ├── sw-api/SKILL.md
│   ├── sw-web/SKILL.md
│   ├── sw-mobile/SKILL.md
│   ├── sw-devops/SKILL.md
│   ├── sw-db/SKILL.md
│   ├── cc-social/SKILL.md
│   ├── cc-shorts/SKILL.md
│   ├── cc-videos/SKILL.md
│   ├── cc-photo/SKILL.md
│   ├── cc-video_editing/SKILL.md
│   ├── cc-blog/SKILL.md
│   ├── cc-marketing/SKILL.md
│   └── cc-seo/SKILL.md
└── backups/                   # Auto-created on deploy
```

### Deploy Mechanism (`deploy.sh`)

1. Creates `backups/` with a timestamped copy of `~/.config/opencode/opencode.json`
2. Symlinks each skill into `~/.config/opencode/skills/` (existing skills untouched)
3. Merges the `agents` section from `opencode.json` into `~/.config/opencode/opencode.json`
4. No changes to MCP servers, plugins, or other configuration

## Success Criteria
- Router correctly dispatches single-agent tasks via `#phrase#` and NLP fallback
- Router orchestrates multi-agent tasks with sequential handoffs
- Each agent loads the correct sub-agent skill for the task
- Agents can be invoked independently by the user
- Cross-agent handoffs preserve context without bloating
