# ScrapeAgent

[![CI](https://github.com/DamiMartinez/scrapeagent/actions/workflows/ci.yml/badge.svg)](https://github.com/DamiMartinez/scrapeagent/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-1.26%2B-4285F4.svg)](https://google.github.io/adk-docs/)

An open-source, community-driven web scraping agent powered by [Google ADK](https://google.github.io/adk-docs/) and [Agent Skills](https://agentskills.io/). Clone it, add your API key, and start scraping any website through a conversational interface — no cloud infrastructure required.

Site-specific scraping knowledge lives in **Agent Skill files** (plain Markdown), not in the agent code. Anyone can contribute new scraping recipes by adding a `SKILL.md` file without touching Python.

---

## Prerequisites

| Tool | Purpose | Install |
|---|---|---|
| Python 3.11+ | Runtime | [python.org](https://www.python.org/downloads/) |
| Poetry | Python package manager | `pip install poetry` |
| Node.js + npx | Runs `@playwright/mcp` browser tool | [nodejs.org](https://nodejs.org/) |
| uv + uvx | Runs `mcp-server-fetch` HTTP tool | `pip install uv` |

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/DamiMartinez/scrapeagent.git
cd scrapeagent

# 2. Install Python dependencies
poetry install

# 3. Pre-install the MCP browser tool (avoids timeout on first run)
npm install -g @playwright/mcp

# 4. Configure your API key
cp .env.example .env
# Edit .env — set GOOGLE_API_KEY (or the key for your chosen provider)

# 5. Start the agent
poetry run adk web

# 6. Open http://localhost:8000 and start scraping
```

---

## Supported Models

ScrapeAgent uses [LiteLLM](https://docs.litellm.ai/docs/providers) for model-agnostic support. Set `LITELLM_MODEL` in your `.env` and provide the matching API key.

| Model | `LITELLM_MODEL` value | API key env var | Notes |
|---|---|---|---|
| Gemini 2.5 Flash | `gemini/gemini-2.5-flash` | `GOOGLE_API_KEY` | Default. Free tier available. |
| Gemini 2.0 Flash | `gemini/gemini-2.0-flash` | `GOOGLE_API_KEY` | Lighter alternative |
| GPT-4o | `openai/gpt-4o` | `OPENAI_API_KEY` | OpenAI hosted |
| Claude Sonnet 4.6 | `anthropic/claude-sonnet-4-6` | `ANTHROPIC_API_KEY` | Anthropic hosted |
| Llama 3.2 (local) | `ollama/llama3.2` | _(none required)_ | Fully local via Ollama |

---

## Available Skills

Skills are the brain of ScrapeAgent. Each skill documents how to scrape a specific website.

| Skill | What it scrapes | Trigger phrases |
|---|---|---|
| `hacker-news` | Front page stories: title, URL, score, author, comments | "Hacker News", "HN", "ycombinator" |
| `github-trending` | Trending repos by language and time period | "GitHub trending", "popular repos" |
| `skill-creator` | Helps you create new skills through conversation | "Create a skill", "document how to scrape" |

---

## Architecture: How It Works

ScrapeAgent is intentionally simple: one root agent with MCP browser tools and an ADK `SkillToolset`. The "expertise" lives in skill files, not in the agent's prompt.

```
┌─────────────────┬─────────────────────────┬────────────────────────────────┬────────────────────────┐
│      Level      │       What loads        │              When              │          Size          │
├─────────────────┼─────────────────────────┼────────────────────────────────┼────────────────────────┤
│ L1 — Metadata   │ name + description only │ At startup, for every skill    │ ~100 tokens per skill  │
├─────────────────┼─────────────────────────┼────────────────────────────────┼────────────────────────┤
│ L2 — Instruc-   │ Full SKILL.md body      │ Only when the agent decides    │ <5000 tokens (1 skill) │
│      tions      │                         │ the skill is relevant          │                        │
├─────────────────┼─────────────────────────┼────────────────────────────────┼────────────────────────┤
│ L3 — Resources  │ Files in references/    │ Only if skill instructions     │ On demand              │
│                 │ and assets/             │ reference them                 │                        │
└─────────────────┴─────────────────────────┴────────────────────────────────┴────────────────────────┘
```

**Why this matters:** A community library of 50 skills costs ~5,000 tokens at startup (50 × ~100 token descriptions). The full instruction payload for any given task is only 1–2 skill bodies. Without this pattern, baking all scraping instructions into a monolithic system prompt would blow the context window and degrade quality as the skill library grows.

### Components

```
scrapeagent/
├── agent.py          # Wires together LiteLLM model, MCP toolsets, and SkillToolset
├── prompt.py         # Minimal orchestration prompt — expertise is in skills
├── tools/
│   └── file_tools.py # save_output (CSV/JSON/MD) and create_skill
└── skills/
    ├── hacker-news/  # One directory per skill
    ├── github-trending/
    └── skill-creator/
```

---

## Adding New Skills

### Method 1: Ask the agent

```
"Create a skill to scrape quotes from quotes.toscrape.com"
```

The agent will investigate the site, identify CSS selectors, and call `create_skill` to write the `SKILL.md` file. Restart the agent (`Ctrl+C` then `adk web`) to load the new skill.

### Method 2: Write it manually

Create a directory under `scrapeagent/skills/` following the [Agent Skills spec](https://agentskills.io/specification):

```
scrapeagent/skills/
└── my-site/
    ├── SKILL.md          # required
    ├── references/       # optional: extra .md files
    └── assets/           # optional: templates, examples
```

`SKILL.md` structure:

```markdown
---
name: my-site
description: One or two sentences describing what this scrapes and when to use it.
metadata:
  author: your-github-handle
  version: "1.0"
---

# My Site Scraper

## Overview
...

## Instructions
...
```

> **Important:** The directory name (e.g. `my-site/`) must exactly match the `name` field in `SKILL.md` frontmatter. The skill loader enforces this and will raise an error if they differ.

See `scrapeagent/skills/hacker-news/SKILL.md` for a complete example.

---

## Output Files

Scraped data is saved to `./output/` (gitignored). Three formats are supported:

| Format | Flag | Example filename |
|---|---|---|
| CSV | `format="csv"` (default) | `output/hn_stories_2024-02-26.csv` |
| JSON | `format="json"` | `output/github_trending_python.json` |
| Markdown | `format="md"` | `output/hn_stories_today.md` |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to write and submit new skills. All skill contributions are welcome — no Python knowledge required.
