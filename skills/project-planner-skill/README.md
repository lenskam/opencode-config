# project-planner-skill

Plan software projects by eliciting features and user journeys, then generating phased LLM instruction files for AI-assisted development.

Supports SaaS, mobile apps, landing pages, API services, e-commerce, and full-stack web applications.

## Installation

### Universal Path (works with 6+ tools)

```bash
git clone <repo-url> ~/.agents/skills/project-planner-skill
```

Works with Codex CLI, Gemini CLI, Kiro, Antigravity, and other tools that read `~/.agents/skills/`.

### Using install.sh (Recommended)

```bash
chmod +x install.sh
./install.sh                          # Auto-detect platform
./install.sh --platform opencode      # OpenCode
./install.sh --platform cursor        # Cursor (auto-generates .mdc)
./install.sh --all                    # All detected platforms
./install.sh --dry-run                # Preview without installing
```

### Alternative: npx

```bash
npx skills add <repo-url>
```

### Manual Installation

| Platform | Copy to |
|----------|---------|
| Universal | `~/.agents/skills/project-planner-skill/` |
| Claude Code | `~/.claude/skills/project-planner-skill/` or `.claude/skills/project-planner-skill/` |
| GitHub Copilot | `.github/skills/project-planner-skill/` |
| Cursor | `.cursor/rules/project-planner-skill/` |
| Windsurf | `.windsurf/rules/project-planner-skill/` |
| Cline | `.clinerules/project-planner-skill/` |
| Codex CLI | `~/.agents/skills/project-planner-skill/` |
| Gemini CLI | `~/.gemini/skills/project-planner-skill/` |
| Kiro | `.kiro/skills/project-planner-skill/` |
| Trae | `.trae/rules/project-planner-skill/` |
| Goose | `~/.config/goose/skills/project-planner-skill/` |
| OpenCode | `~/.config/opencode/skills/project-planner-skill/` |
| Roo Code | `.roo/rules/project-planner-skill/` |
| Antigravity | `.agents/skills/project-planner-skill/` |

## Prerequisites

No external dependencies or API keys required. This skill uses only the agent's built-in capabilities.

## Usage Examples

### Example 1: New SaaS Project

```
You: /project-planner-skill I want to build a team task management SaaS

Agent: (asks 7 questions in sequence)
  1. Project goal? "A Trello-like app for small teams"
  2. User personas? "Admin, Team Member"
  3. Core MVP features? "Create project, add tasks, assign members"
  ...

Result: docs/dev/features.md, docs/dev/user-journeys.md, PHASE_1.md...
```

### Example 2: Mobile Fitness App

```
You: Plan a mobile app for tracking fitness goals

Agent: (adapts questions for mobile project type)
  ...
Result: Phased implementation plan for iOS/Android app
```

### Example 3: API-first Project

```
You: Create phases for my inventory management API

Agent: (uses chronological style since it's API-first)
  ...
Result: Layer-by-layer phases starting with database schema
```

### Example 4: Feature Addition

```
You: /project-planner-skill Add a payment feature to my existing app

Agent: (focuses on the single feature, generates 1-2 phases)
  ...
Result: docs/dev/features.md with payment feature + phased plan
```

### Example 5: Full-Stack Landing Page

```
You: Break down my landing page into phases

Agent: (generates chronological phases for landing page)
  ...
Result: Phases for hero section, signup flow, testimonials, etc.
```

## Troubleshooting

### Skill doesn't activate when I type /project-planner-skill

**Cause**: Skill not installed or not in the correct path for your platform.

**Solution**:
1. Verify installation: `ls ~/.config/opencode/skills/project-planner-skill/SKILL.md` (for OpenCode)
2. Re-run `./install.sh --platform opencode` to fix path
3. Start a new session and try again

### The generated phase files don't reference the right skills

**Cause**: The template defaults to standard skills. Use your judgment to adjust the AI-Specific Instructions section in each phase file.

### The output seems generic

**Cause**: The quality of the output depends on the detail of your answers. Be specific when describing features and user journeys. The more detail you provide, the better the phases.

### Can I edit the generated files?

Yes. The generated files are starting points. Edit features.md, user-journeys.md, and any phase files to match your exact needs before implementation begins.

## License

MIT
