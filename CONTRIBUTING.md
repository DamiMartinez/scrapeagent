# Contributing to ScrapeAgent

The easiest way to contribute is to add a new **Agent Skill** — a Markdown file that teaches the agent how to scrape a specific website. No Python knowledge required.

---

## Skill Naming Conventions

- Use kebab-case, all lowercase: `amazon-products`, `reddit-posts`, `linkedin-jobs`
- Include both the site name and the data type: `hacker-news` not just `news`
- Keep skills focused and single-purpose:
  - `reddit-posts` and `reddit-comments` are better than one fat `reddit` skill
  - Smaller skills = less context loaded per turn = better agent performance
- No consecutive hyphens, no leading/trailing hyphens

---

## SKILL.md Structure

Every skill is a directory under `scrapeagent/skills/` containing at minimum a `SKILL.md` file.

```
scrapeagent/skills/
└── my-site-data/
    ├── SKILL.md          # required
    ├── references/       # optional: additional .md reference files
    └── assets/           # optional: templates, schemas, examples
```

### SKILL.md format

```markdown
---
name: my-site-data
description: |
  One to two sentences. Describe WHAT data it scrapes and WHEN to trigger it.
  Example: "Scrape product listings from example.com including name, price, and rating.
  Use when the user mentions example.com or wants product data."
metadata:
  author: your-github-handle
  version: "1.0"
---

# My Site Data Scraper

## Overview
What this skill does and the target URL.

## Parameters (if applicable)
- param: description

## URL Construction
How to build the URL from parameters.

## Tool to use
- `fetch` for static HTML (no JavaScript required)
- `playwright` for JavaScript-rendered pages

## Extraction Instructions

Step-by-step guide with exact CSS selectors. Example:

1. Fetch `https://example.com/listings`
2. For each `.product-card` element extract:
   - `name`: `.product-title` text
   - `price`: `.price` text, strip `$`
   - `rating`: `.stars` data-rating attribute
3. Save with columns: name, price, rating

## Notes
- Rate limits, authentication requirements, edge cases
```

### Description guidelines

The `description` field is the **only thing loaded into the agent's context at startup** (L1 metadata). Make it count:

- Say what site it scrapes and what data it returns
- Include the trigger words a user might say ("when the user mentions X")
- Keep it under 3 sentences
- Bad: `"Scrapes a website."` Good: `"Scrapes product listings from Amazon including title, price, ASIN, and rating. Use when the user mentions Amazon, product prices, or ASIN numbers."`

---

## Testing a Skill Locally

1. Add your skill directory to `scrapeagent/skills/`
2. Start the agent: `adk web`
3. Ask the agent to perform the scrape your skill covers
4. Verify the output file in `./output/`
5. Check that the correct skill was triggered (the agent will mention it)

---

## Context Window Guidelines

> **Keep skills focused and under 500 lines.**

The ADK Skills system uses progressive disclosure: only the skill description loads at startup (~100 tokens), and the full SKILL.md body loads only when the agent activates the skill. Bloated skills degrade performance for every user because:

- More tokens loaded per turn = less room for scraped HTML content
- Large skills are less likely to be followed precisely
- One skill per data type is better than one mega-skill per site

---

## PR Checklist

Before submitting a pull request with a new skill:

- [ ] Skill name is kebab-case and clearly describes site + data type
- [ ] `description` field covers what it scrapes AND when to trigger it
- [ ] Extraction instructions include exact CSS selectors (tested against the live site)
- [ ] Tool selection is correct (`fetch` vs `playwright`)
- [ ] Edge cases are documented (empty fields, JS requirement, pagination)
- [ ] Skill has been tested locally with `adk web`
- [ ] No hardcoded credentials or API keys in any file
- [ ] Skill body is under 500 lines

---

## Resources

- [Agent Skills specification](https://agentskills.io/specification)
- [Google ADK documentation](https://google.github.io/adk-docs/)
- [LiteLLM model providers](https://docs.litellm.ai/docs/providers)
- [mcp-server-fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
- [@playwright/mcp](https://github.com/microsoft/playwright-mcp)
