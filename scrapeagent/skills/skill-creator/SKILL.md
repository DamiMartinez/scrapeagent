---
name: skill-creator
description: Create a new agent skill that documents how to scrape a specific website. Use when the user wants to add a new scraping recipe, document a new website, or contribute to the community skills library.
metadata:
  author: scrapeagent
  version: "1.0"
---

# Skill Creator

## Purpose
Help users create well-structured skills documenting how to scrape specific websites.
New skills are saved to the `skills/` directory and become immediately usable after an agent restart.

## Workflow

### Step 1 — Gather requirements
Ask the user:
- What website do they want to scrape? (get the exact URL)
- What specific data fields do they need?
- Any special requirements? (login, pagination, JS rendering, rate limits)

### Step 2 — Investigate the website (if needed)
- Use fetch to retrieve the page HTML
- If the page appears empty, switch to playwright
- Identify exact CSS selectors for each required data field
- Note whether JS is required (use playwright vs fetch)

### Step 3 — Generate the skill name
- Kebab-case, all lowercase, e.g.: `amazon-products`, `reddit-posts`, `linkedin-jobs`
- Must clearly represent the website and data type

### Step 4 — Write the instructions
Follow the template at [assets/SKILL_TEMPLATE.md](assets/SKILL_TEMPLATE.md).
Key sections to include:
- Overview with the target URL(s)
- URL construction (if parameterized)
- Step-by-step extraction with exact CSS selectors
- Column/field names for the output
- Notes on edge cases, rate limits, JS requirements

### Step 5 — Create the skill
Call the `create_skill` tool with:
- skill_name: the kebab-case name
- description: 1-2 sentences covering what it scrapes and when to trigger it
- instructions: the full markdown body from Step 4

### Step 6 — Confirm
Tell the user the skill was created and that they need to restart the agent (`Ctrl+C` then `adk web`) to load it.
