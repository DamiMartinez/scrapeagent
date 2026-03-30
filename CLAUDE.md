# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
poetry install

# Pre-install the Playwright MCP browser tool (avoids timeout on first run)
npm install -g @playwright/mcp

# Run the agent (web UI at http://localhost:8000)
poetry run adk web

# Run all tests
poetry run pytest tests/ -v

# Run a single test file
poetry run pytest tests/test_skills_loader.py -v

# Run a single test by name
poetry run pytest tests/test_skills_loader.py::test_load_valid_skill -v
```

## Architecture

**Single root agent** (`LlmAgent`) defined in `scrapeagent/agent.py`. No sub-agents. The agent's expertise lives in skill files, not the system prompt.

### Skills — Progressive Disclosure (3 levels)

Skills live in `scrapeagent/skills/<skill-name>/SKILL.md`. The ADK `SkillToolset` loads them with progressive disclosure:

- **L1** (startup): `name` + `description` from YAML frontmatter (~100 tokens/skill)
- **L2** (on demand): Full `SKILL.md` body when the agent activates the skill
- **L3** (on demand): Files in `references/` and `assets/` subdirectories

`skills_loader.py` contains the custom `load_skill_from_dir()` because `google.adk` does not expose a built-in loader. It parses YAML frontmatter + markdown body and builds `google.adk.skills.models.Skill` objects manually.

### MCP Toolsets

- **`mcp-server-fetch`** (via `uvx`): Lightweight HTTP for static HTML sites
- **`@playwright/mcp`** (via `npx --headless`): Full browser for JS-heavy sites

Both use `McpToolset` + `StdioConnectionParams(timeout=30.0)`. The 30s timeout is required — the default 5s is too short for npx.

### Custom Tools

- **`save_output`** (`tools/file_tools.py`): Writes scraped data to `./output/` as CSV, JSON, or Markdown
- **`create_skill`** (`tools/file_tools.py`): Creates a new skill directory + `SKILL.md` at runtime; requires agent restart to load

### Model

Configured via `LITELLM_MODEL` env var (default: `gemini/gemini-2.5-flash`). LiteLLM handles all provider routing. See `README.md` for the full model table.

## Adding Skills

Each skill is a directory under `scrapeagent/skills/` with a required `SKILL.md`:

```
scrapeagent/skills/my-site/
├── SKILL.md          # YAML frontmatter + markdown body
├── references/       # optional: additional .md files
└── assets/           # optional: templates, schemas
```

`SKILL.md` must start with `---` YAML frontmatter containing `name`, `description`, and `metadata`. The `description` is the **only field in context at startup** — it must say what data is scraped and when to trigger the skill. Keep skill bodies under 500 lines. See `CONTRIBUTING.md` for the full spec and PR checklist.

## Key Constraints

- `load_skill_from_dir` does not exist in the ADK package — it's in `scrapeagent/skills_loader.py`
- Use `McpToolset` (not `MCPToolset` — deprecated alias)
- `StdioConnectionParams` wraps `StdioServerParameters` — both are required
- New skills require an agent restart (`Ctrl+C` then `adk web`) to be loaded
