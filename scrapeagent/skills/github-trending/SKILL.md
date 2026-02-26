---
name: github-trending
description: Scrape GitHub Trending page (github.com/trending) for the most-starred repositories. Supports filtering by programming language and time period. Use when the user wants trending GitHub repos, popular open-source projects, or mentions GitHub Trending.
metadata:
  author: scrapeagent
  version: "1.0"
---

# GitHub Trending Scraper

## Overview
Scrapes https://github.com/trending for trending repositories.
GitHub requires JavaScript rendering — use `playwright`.

## Parameters
- `language` (optional): programming language, e.g., python, javascript, rust, go
- `since` (optional): time period — `daily` (default), `weekly`, `monthly`

## URL Construction
- All repos: `https://github.com/trending`
- By language: `https://github.com/trending/python`
- By period: `https://github.com/trending?since=weekly`
- Combined: `https://github.com/trending/python?since=weekly`

Ask the user for filters before scraping. Use defaults if not specified.

## Instructions

1. Construct the URL based on user-specified language and/or period
2. Use playwright to navigate to the URL (GitHub requires JS)
3. Wait for `.Box-row` elements to appear
4. For each `article.Box-row` extract:
   - `rank`: position in list (1-based index)
   - `repo`: `h2 a` text — clean whitespace, format as `owner/repo`
   - `url`: `h2 a` href — prepend `https://github.com` if relative
   - `description`: `p.col-9` text — strip whitespace (may be empty)
   - `language`: `[itemprop="programmingLanguage"]` text (may be empty)
   - `stars`: `a[href$="/stargazers"]` text — extract number, remove commas
   - `forks`: `a[href$="/forks"]` text — extract number, remove commas
   - `stars_today`: `.d-inline-block.float-sm-right` text — extract number

5. Save with columns: rank, repo, url, description, language, stars, forks, stars_today

## Notes
- GitHub uses JS rendering — always use playwright, never fetch
- `stars_today` may say "X stars today" or "X stars this week/month" depending on `since`
- Empty description is normal — save as empty string
- Typically returns 25 repos per page
