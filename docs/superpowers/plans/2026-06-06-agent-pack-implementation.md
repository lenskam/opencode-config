# Agent Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone deployable agent pack at `~/projects/agents-pack/` with 4 main agents, 23 sub-agent skills, a router, and a deploy script that installs into an existing OpenCode setup without overwriting anything.

**Architecture:** Hybrid approach — main agents defined in `opencode.json` for isolation, sub-agents as OpenCode skills for workflow guidance, a router skill for intent detection and dispatching via `#phrase#` tags.

**Tech Stack:** OpenCode skills (SKILL.md), bash (deploy.sh), JSON (opencode.json merge)

---

### Task 1: Scaffold directory structure

**Files:**
- Create: `~/projects/agents-pack/`
- Create: `~/projects/agents-pack/skills/`
- Create: `~/projects/agents-pack/backups/`

- [ ] **Step 1: Create directories**

```bash
mkdir -p ~/projects/agents-pack/skills/{router,wp-publish,wp-theme,wp-plugin,wp-maintenance,n8n-new,n8n-troubleshoot,n8n-google,n8n-messaging,n8n-gemini,sw-api,sw-web,sw-mobile,sw-devops,sw-db,cc-social,cc-shorts,cc-videos,cc-photo,cc-video_editing,cc-blog,cc-marketing,cc-seo} ~/projects/agents-pack/backups
```

- [ ] **Step 2: Verify**

```bash
ls -d ~/projects/agents-pack/skills/*/
```
Expected: 23 skill directories + router listed

- [ ] **Step 3: Commit**

```bash
cd ~/projects/agents-pack && git init && git add -A && git commit -m "chore: scaffold agent pack directory structure"
```

---

### Task 2: Create opencode.json with agent definitions

**Files:**
- Create: `~/projects/agents-pack/opencode.json`

- [ ] **Step 1: Write opencode.json**

```json
{
  "agent": {
    "agents": {
      "wordpress-dev": {
        "model": "opencode/deepseek-v4-flash-free",
        "instructions": "You are a WordPress development expert. Handle theme development, plugin building, content publishing, and site maintenance. Load the relevant sub-agent skill (wp-publish, wp-theme, wp-plugin, wp-maintenance) based on the user's request."
      },
      "n8n-automations": {
        "model": "opencode/deepseek-v4-flash-free",
        "instructions": "You are an n8n workflow automation expert. Build new automations and troubleshoot existing ones. Expert in Google products, WhatsApp, Telegram, and Gemini integrations. Load the relevant sub-agent skill (n8n-new, n8n-troubleshoot, n8n-google, n8n-messaging, n8n-gemini) based on the task."
      },
      "software-dev": {
        "model": "opencode/deepseek-v4-flash-free",
        "instructions": "You are a full-stack software developer. Handle API design, web apps, mobile apps, DevOps, and database work. Load the relevant sub-agent skill (sw-api, sw-web, sw-mobile, sw-devops, sw-db) based on the request."
      },
      "content-creation": {
        "model": "opencode/deepseek-v4-flash-free",
        "instructions": "You are a content creation expert. Handle social media, short-form video, long-form video, photography, video editing, blog writing, marketing copy, and SEO optimization. Load the relevant sub-agent skill (cc-social, cc-shorts, cc-videos, cc-photo, cc-video_editing, cc-blog, cc-marketing, cc-seo) based on the task."
      }
    }
  }
}
```

- [ ] **Step 2: Verify**

```bash
cat ~/projects/agents-pack/opencode.json | jq '.agent.agents | keys'
```
Expected: `["content-creation", "n8n-automations", "software-dev", "wordpress-dev"]`

- [ ] **Step 3: Commit**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "feat: add agent definitions for 4 main agents"
```

---

### Task 3: Create deploy.sh

**Files:**
- Create: `~/projects/agents-pack/deploy.sh`

- [ ] **Step 1: Write deploy.sh**

```bash
#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "$0")" && pwd)"
OPENCODE_CONFIG="$HOME/.config/opencode"
OPENCODE_JSON="$OPENCODE_CONFIG/opencode.json"
BACKUP_DIR="$PACKAGE_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=== Agent Pack Deploy ==="

# 1. Backup existing opencode.json
if [ -f "$OPENCODE_JSON" ]; then
  mkdir -p "$BACKUP_DIR"
  cp "$OPENCODE_JSON" "$BACKUP_DIR/opencode.json.$TIMESTAMP"
  echo "Backed up $OPENCODE_JSON to $BACKUP_DIR/opencode.json.$TIMESTAMP"
fi

# 2. Symlink skills (additive only — never overwrites)
mkdir -p "$OPENCODE_CONFIG/skills"
for skill_dir in "$PACKAGE_DIR/skills/"*/; do
  skill_name="$(basename "$skill_dir")"
  target="$OPENCODE_CONFIG/skills/$skill_name"
  if [ ! -e "$target" ]; then
    ln -s "$skill_dir" "$target"
    echo "Linked skill: $skill_name"
  else
    echo "Skipped (exists): $skill_name"
  fi
done

# 3. Merge agent definitions into opencode.json
if [ -f "$OPENCODE_JSON" ]; then
  # Use jq to merge the agents section
  PACKAGE_AGENTS=$(jq '.agent.agents' "$PACKAGE_DIR/opencode.json")
  if [ -n "$PACKAGE_AGENTS" ] && [ "$PACKAGE_AGENTS" != "null" ]; then
    jq --argjson agents "$PACKAGE_AGENTS" '.agent.agents = (.agent.agents // {}) * $agents' "$OPENCODE_JSON" > "$OPENCODE_JSON.tmp" && mv "$OPENCODE_JSON.tmp" "$OPENCODE_JSON"
    echo "Merged agent definitions into $OPENCODE_JSON"
  fi
else
  cp "$PACKAGE_DIR/opencode.json" "$OPENCODE_JSON"
  echo "Created $OPENCODE_JSON with agent definitions"
fi

echo "=== Deploy Complete ==="
```

- [ ] **Step 2: Make executable**

```bash
chmod +x ~/projects/agents-pack/deploy.sh
```

- [ ] **Step 3: Commit**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "feat: add deploy.sh for non-destructive installation"
```

---

### Task 4: Router skill

**Files:**
- Create: `~/projects/agents-pack/skills/router/SKILL.md`

- [ ] **Step 1: Write router skill**

```markdown
---
name: router
description: Routes user prompts to the correct agent based on #phrase# tags or intent detection
---

# Router Skill

Invoked at the start of every session. Determines which agent(s) should handle the user's request.

## Detection Logic

1. **Explicit tags:** Scan the user's first message for `#wordpress`, `#n8n`, `#software`, `#content`
   - If found → dispatch directly to that agent
2. **NLP fallback** (no tag found):
   - `wordpress-dev`: publishing, theme, plugin, site, wp-admin, blog post, page
   - `n8n-automations`: workflow, automation, zapier alternative, connect, integrate, trigger
   - `software-dev`: build app, API, web app, mobile app, deploy, database, backend, frontend
   - `content-creation`: write, post, social media, video, edit, SEO, marketing, blog, photo

## Single-Agent Dispatch

Use `@agent-name` or the task tool to route to the appropriate agent.

## Multi-Agent Orchestration

If a task spans multiple agents (e.g., "write a blog post and publish it"), route sequentially:

1. First agent handles their part
2. Pass a summary + artifact path to the next agent
3. Last agent reports the final result

## Cross-Agent Handoff

When handing off between agents, output a structured handoff note:

```
HANDOFF: <receiving-agent-name>
CONTEXT: <summary of what was done>
ARTIFACTS: <paths to files/outputs>
NEXT: <what the next agent should do>
```

## No-Tag Default

If no tag is present and NLP is uncertain, ask the user:
"Which team should handle this? #wordpress, #n8n, #software, or #content?"
```

- [ ] **Step 2: Commit**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "feat: add router skill with tag and NLP detection"
```

---

### Task 5: WordPress agent skills

**Files:**
- Create: `~/projects/agents-pack/skills/wp-publish/SKILL.md`
- Create: `~/projects/agents-pack/skills/wp-theme/SKILL.md`
- Create: `~/projects/agents-pack/skills/wp-plugin/SKILL.md`
- Create: `~/projects/agents-pack/skills/wp-maintenance/SKILL.md`

- [ ] **Step 1: Write wp-publish skill**

```markdown
---
name: wp-publish
description: WordPress content publishing — pages, blog posts, media management
---

# WordPress Content Publishing

## Workflow
1. Accept content (text, images, metadata) from user or handoff
2. Create/edit post via WordPress MCP tools
3. Set categories, tags, featured image, SEO meta
4. Preview before publishing
5. Publish or schedule

## Tools
- WordPress MCP: `wordpress_publish_post`, `wordpress_update_post`, `wordpress_get_posts`
- Media: upload and set featured images

## Priority
Blog posts and pages are the highest priority task for this skill.
```

- [ ] **Step 2: Write wp-theme skill**

```markdown
---
name: wp-theme
description: WordPress theme development — custom themes, child themes, template hierarchy
---

# WordPress Theme Development

## Workflow
1. Understand design requirements
2. Create child theme from parent or build custom theme
3. Implement template files (header, footer, single, archive, page)
4. Add theme support (features, widgets, menus)
5. Enqueue styles and scripts properly
6. Test responsiveness and cross-browser
7. Document customization hooks

## Best Practices
- Follow WordPress coding standards
- Use `wp_enqueue_style` / `wp_enqueue_script` (never hardcode)
- Escape output with `esc_html()`, `esc_attr()`, etc.
- Use `get_template_part()` for reusable components
```

- [ ] **Step 3: Write wp-plugin skill**

```markdown
---
name: wp-plugin
description: WordPress plugin development — custom plugins, hooks, filters
---

# WordPress Plugin Development

## Workflow
1. Understand the functionality needed
2. Scaffold plugin structure (main file, readme, assets)
3. Implement using hooks (actions/filters) and shortcodes
4. Add settings page if needed
5. Ensure proper activation/deactivation/uninstall hooks
6. Test with WordPress coding standards

## Best Practices
- Unique prefix for all functions and classes
- Never use `extract()` or `$_REQUEST` directly
- Sanitize inputs with `sanitize_*()` functions
- Validate nonces on form submissions
- Use `WP_Query` with proper arguments (never raw SQL)
```

- [ ] **Step 4: Write wp-maintenance skill**

```markdown
---
name: wp-maintenance
description: WordPress site maintenance — updates, backups, security, performance
---

# WordPress Maintenance

## Tasks
- **Updates:** WordPress core, themes, plugins — test on staging first
- **Backups:** Database export + file system backup before any change
- **Security:** Check user roles, audit installed plugins, review login attempts, enable 2FA
- **Performance:** Review caching plugins, optimize images, check database query times, enable CDN
- **Health Check:** Use Site Health, review error logs, check PHP memory limits
```

- [ ] **Step 5: Commit**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "feat: add WordPress agent skills (publish, theme, plugin, maintenance)"
```

---

### Task 6: n8n automations agent skills

**Files:**
- Create: `~/projects/agents-pack/skills/n8n-new/SKILL.md`
- Create: `~/projects/agents-pack/skills/n8n-troubleshoot/SKILL.md`
- Create: `~/projects/agents-pack/skills/n8n-google/SKILL.md`
- Create: `~/projects/agents-pack/skills/n8n-messaging/SKILL.md`
- Create: `~/projects/agents-pack/skills/n8n-gemini/SKILL.md`

- [ ] **Step 1: Write n8n-new skill**

```markdown
---
name: n8n-new
description: Build new n8n workflow automations from requirements
---

# n8n New Workflow Builder

## Workflow
1. Elicit requirements: trigger, actions, conditions, error handling
2. Design the workflow (trigger → filter → action(s) → output)
3. Build using n8n MCP tools
4. Configure credentials securely
5. Test with sample data
6. Activate and document

## Pattern Library
- **Webhook → Transform → Notify:** Incoming data, transform with Code node, send notification
- **Schedule → Fetch → Store:** Cron trigger, HTTP Request, database insert
- **Form Trigger → Process → Respond:** n8n form, split/merge, respond to webhook
```

- [ ] **Step 2: Write n8n-troubleshoot skill**

```markdown
---
name: n8n-troubleshoot
description: Debug and fix broken or failing n8n workflows
---

# n8n Troubleshooting

## Workflow
1. Identify the failing workflow and exact error
2. Check: credentials expired? API changes? Data format mismatch?
3. Enable workflow execution logs
4. Test each node in isolation
5. Fix the issue (update credentials, fix expressions, add error handling)
6. Add error workflows or retry logic if missing
7. Document the fix

## Common Issues
- Expired OAuth tokens → re-authenticate
- API rate limits → add wait nodes
- Schema changes → update field mappings
- Missing error handling → add error triggers
```

- [ ] **Step 3: Write n8n-google skill**

```markdown
---
name: n8n-google
description: Google product integrations — Docs, Sheets, Slides, Gmail, Drive
---

# n8n Google Integrations

## Available Nodes
- **Google Sheets:** Read/write/append rows, create sheets, update cells
- **Google Docs:** Create/edit documents, insert text/images
- **Google Slides:** Create presentations, add slides, update content
- **Gmail:** Send emails, read inbox, manage labels, search
- **Google Drive:** Upload/download files, manage folders, share

## Auth
- Uses Google OAuth2 service account or OAuth2 credentials
- Store credentials securely in n8n credentials store
```

- [ ] **Step 4: Write n8n-messaging skill**

```markdown
---
name: n8n-messaging
description: Messaging platform integrations — WhatsApp, Telegram
---

# n8n Messaging Integrations

## WhatsApp
- Use WhatsApp Business API or WhatsApp Cloud API node
- Send templates, text, media, interactive messages
- Handle incoming messages via webhook

## Telegram
- Use Telegram node
- Send messages, photos, documents, keyboards
- Handle bot commands via webhook trigger
- Use inline keyboards for interactive responses
```

- [ ] **Step 5: Write n8n-gemini skill**

```markdown
---
name: n8n-gemini
description: Gemini AI integrations in n8n workflows
---

# n8n Gemini AI Patterns

## Patterns
- **Content Generation:** Trigger → Gemini generate → Store/Send
- **Classification:** Incoming text → Gemini classify → Route to different branches
- **Extraction:** Raw text → Gemini extract structured data → Database insert
- **Summarization:** Long content → Gemini summarize → Email/Slack notification
- **Multimodal:** Image upload → Gemini describe → Store metadata

## Note
- Use the HTTP Request node with Gemini API if no native Gemini node exists
- Configure API key via n8n credentials
- Set appropriate temperature and token limits per use case
```

- [ ] **Step 6: Commit**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "feat: add n8n agent skills (new, troubleshoot, google, messaging, gemini)"
```

---

### Task 7: Software dev agent skills

**Files:**
- Create: `~/projects/agents-pack/skills/sw-api/SKILL.md`
- Create: `~/projects/agents-pack/skills/sw-web/SKILL.md`
- Create: `~/projects/agents-pack/skills/sw-mobile/SKILL.md`
- Create: `~/projects/agents-pack/skills/sw-devops/SKILL.md`
- Create: `~/projects/agents-pack/skills/sw-db/SKILL.md`

- [ ] **Step 1: Write sw-api skill**

```markdown
---
name: sw-api
description: API design and development — REST, GraphQL, gRPC
---

# API Development

## Workflow
1. Design schema/contract first (OpenAPI for REST, SDL for GraphQL)
2. Implement endpoints with proper validation
3. Add authentication (JWT, OAuth2, API keys)
4. Write integration tests
5. Generate API documentation

## Best Practices
- REST: Resource-oriented URLs, proper HTTP methods, versioning
- GraphQL: Resolver patterns, N+1 prevention, query complexity limits
- All: Input validation, error handling, rate limiting, logging
```

- [ ] **Step 2: Write sw-web skill**

```markdown
---
name: sw-web
description: Full-stack web application development
---

# Web Application Development

## Workflow
1. Review requirements and design
2. Scaffold project (Next.js, FastAPI, or chosen stack)
3. Implement frontend components
4. Build backend APIs
5. Connect frontend to backend
6. Test end-to-end
7. Deploy

## Stack Preferences
- Frontend: Next.js, React, TypeScript
- Backend: FastAPI, Node.js, Go
- Styling: Tailwind CSS
- State: React Query, Zustand
```

- [ ] **Step 3: Write sw-mobile skill**

```markdown
---
name: sw-mobile
description: Mobile application development
---

# Mobile Development

## Workflow
1. Review requirements and design mockups
2. Scaffold project (React Native / Expo)
3. Implement screens and navigation
4. Connect to backend APIs
5. Handle offline mode, push notifications
6. Test on device/simulator
7. Build for distribution
```

- [ ] **Step 4: Write sw-devops skill**

```markdown
---
name: sw-devops
description: Deployment, CI/CD, infrastructure
---

# DevOps

## Workflow
1. Set up CI/CD pipeline (GitHub Actions, GitLab CI)
2. Configure staging/production environments
3. Deploy application (Docker, VPS, serverless)
4. Set up monitoring and logging
5. Configure domains, SSL, CDN

## Tools
- CI/CD: GitHub Actions, GitLab CI
- Containers: Docker, Docker Compose
- Hosting: VPS, AWS, DigitalOcean, Vercel
- Monitoring: Sentry, Uptime monitoring
```

- [ ] **Step 5: Write sw-db skill**

```markdown
---
name: sw-db
description: Database schema design, migrations, query optimization
---

# Database Work

## Workflow
1. Design schema from requirements
2. Create migrations
3. Write queries with proper indexing
4. Optimize slow queries (EXPLAIN ANALYZE)
5. Set up backups and recovery

## Best Practices
- Use migrations for schema changes (never raw DDL in production)
- Index columns used in WHERE, JOIN, ORDER BY
- Use connection pooling
- Regular backups with point-in-time recovery
- Monitor query performance
```

- [ ] **Step 6: Commit**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "feat: add software dev agent skills (api, web, mobile, devops, db)"
```

---

### Task 8: Content creation agent skills

**Files:**
- Create: `~/projects/agents-pack/skills/cc-social/SKILL.md`
- Create: `~/projects/agents-pack/skills/cc-shorts/SKILL.md`
- Create: `~/projects/agents-pack/skills/cc-videos/SKILL.md`
- Create: `~/projects/agents-pack/skills/cc-photo/SKILL.md`
- Create: `~/projects/agents-pack/skills/cc-video_editing/SKILL.md`
- Create: `~/projects/agents-pack/skills/cc-blog/SKILL.md`
- Create: `~/projects/agents-pack/skills/cc-marketing/SKILL.md`
- Create: `~/projects/agents-pack/skills/cc-seo/SKILL.md`

- [ ] **Step 1: Write cc-social skill**

```markdown
---
name: cc-social
description: Social media content creation and scheduling
---

# Social Media Content

## Workflow
1. Determine platform (LinkedIn, Twitter/X, Instagram, Facebook, TikTok)
2. Craft platform-optimized copy (character limits, tone, hashtags)
3. Create or source accompanying visuals
4. Schedule for optimal posting times
5. Engage with comments and mentions
```

- [ ] **Step 2: Write cc-shorts skill**

```markdown
---
name: cc-shorts
description: Short-form video content — Reels, TikTok, YouTube Shorts
---

# Short-Form Video

## Workflow
1. Research trending formats and sounds
2. Write script (hook in first 3 seconds)
3. Plan visual elements (text overlays, transitions, effects)
4. Produce or direct recording
5. Edit for platform specs (9:16, 60s max, captions)
6. Optimize title, description, hashtags
```

- [ ] **Step 3: Write cc-videos skill**

```markdown
---
name: cc-videos
description: Long-form video content planning and scripting
---

# Long-Form Video

## Workflow
1. Topic research and outline
2. Write script with timestamps
3. Plan B-roll, graphics, and transitions
4. Record or direct production
5. Structure with intro → body → outro
6. Optimize title, thumbnail, description, chapters
```

- [ ] **Step 4: Write cc-photo skill**

```markdown
---
name: cc-photo
description: Photography and image creation/editing
---

# Photo & Image

## Tasks
- Product photography planning and execution
- Image editing (color correction, retouching, resizing)
- Graphic design for social media, ads, blog featured images
- Stock photo sourcing and licensing
- Maintain brand visual consistency
```

- [ ] **Step 5: Write cc-video_editing skill**

```markdown
---
name: cc-video_editing
description: Post-production video editing
---

# Video Editing

## Workflow
1. Review raw footage and select best takes
2. Rough cut assembly
3. Add transitions, effects, color grading
4. Audio cleanup, background music, voiceover sync
5. Add captions, text overlays, CTAs
6. Export in platform-required format
7. Thumbnail creation
```

- [ ] **Step 6: Write cc-blog skill**

```markdown
---
name: cc-blog
description: Blog posts, articles, long-form writing
---

# Blog Writing

## Workflow
1. Topic research and keyword analysis
2. Outline structure (H1, H2, H3 hierarchy)
3. Write engaging intro with clear thesis
4. Develop body with evidence, examples, data
5. Strong conclusion with CTA
6. Proofread and edit
7. Add meta description and internal links
8. Hand off to WordPress agent for publishing if needed
```

- [ ] **Step 7: Write cc-marketing skill**

```markdown
---
name: cc-marketing
description: Marketing copy, email campaigns, landing pages, ad copy
---

# Marketing Content

## Workflow
1. Define campaign goal and target audience
2. Write ad copy (Google Ads, Facebook Ads, LinkedIn)
3. Create email sequences (welcome, nurture, promotional)
4. Design landing page copy
5. A/B test variations
6. Track conversion metrics
```

- [ ] **Step 8: Write cc-seo skill**

```markdown
---
name: cc-seo
description: SEO optimization — keyword research, on-page, meta
---

# SEO Optimization

## Workflow
1. Keyword research (search volume, difficulty, intent)
2. On-page optimization (title tags, meta descriptions, headers, URL structure)
3. Content optimization (keyword density, LSI, readability)
4. Technical SEO (schema markup, sitemap, page speed, mobile-friendliness)
5. Internal/external linking strategy
6. Track rankings and iterate
```

- [ ] **Step 9: Commit**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "feat: add content creation agent skills (social, shorts, videos, photo, editing, blog, marketing, seo)"
```

---

### Task 9: Create README

**Files:**
- Create: `~/projects/agents-pack/README.md`

- [ ] **Step 1: Write README**

```markdown
# Agents Pack

A deployable agent pack for OpenCode that adds 4 specialized agents and 23 sub-agent skills for a B2B tech company.

## Agents

| Tag | Agent | Purpose |
|-----|-------|---------|
| `#wordpress` | WordPress Dev | Themes, plugins, publishing, maintenance |
| `#n8n` | n8n Automations | Workflow automation, Google/WhatsApp/Telegram/Gemini integrations |
| `#software` | Software Dev | APIs, web apps, mobile apps, DevOps, databases |
| `#content` | Content Creation | Social media, video, photo, blog, marketing, SEO |

## Install

```bash
cd ~/projects/agents-pack
chmod +x deploy.sh
./deploy.sh
```

This symlinks skills into `~/.config/opencode/skills/` and merges agent definitions into your existing `opencode.json`. Your existing setup is backed up to `backups/`.

## Usage

Include the tag in your prompt:
- `#wordpress publish a blog post about our new product`
- `#n8n create a workflow that emails me when a form is submitted`
- `#software build a REST API for user management`
- `#content write a LinkedIn post about AI trends`

Without a tag, the router skill detects intent automatically.

## Structure

```
agents-pack/
├── deploy.sh           # Non-destructive installer
├── README.md
├── opencode.json       # Agent definitions
├── skills/
│   ├── router/         # Intent detection and dispatching
│   ├── wp-*/           # WordPress sub-agent skills
│   ├── n8n-*/          # n8n sub-agent skills
│   ├── sw-*/           # Software dev sub-agent skills
│   └── cc-*/           # Content creation sub-agent skills
└── backups/            # Timestamped backups of opencode.json
```
```

- [ ] **Step 2: Commit**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "docs: add README with install and usage instructions"
```

---

### Task 10: Deploy and verify

**Files:** none (deployment step)

- [ ] **Step 1: Run deploy.sh**

```bash
cd ~/projects/agents-pack && bash deploy.sh
```

Expected output shows skills linked and agent definitions merged.

- [ ] **Step 2: Verify skills are linked**

```bash
ls -la ~/.config/opencode/skills/ | grep "wp-\|n8n-\|sw-\|cc-\|router"
```
Expected: symlinks to `~/projects/agents-pack/skills/*` listed

- [ ] **Step 3: Verify agent config merged**

```bash
jq '.agent.agents | keys' ~/.config/opencode/opencode.json
```
Expected: `["content-creation", "n8n-automations", "software-dev", "wordpress-dev"]` plus any pre-existing agents

- [ ] **Step 4: Quick smoke test from opencare**

```bash
cd ~/projects/opencare && timeout 30 opencode run "hello" --print-logs 2>&1 | grep -c "successfully created client"
```
Expected: all MCP servers start (count >= 6)

- [ ] **Step 5: Commit final state**

```bash
cd ~/projects/agents-pack && git add -A && git commit -m "chore: initial deploy and verify"
```
