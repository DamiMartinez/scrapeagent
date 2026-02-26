---
name: hacker-news
description: Scrape Hacker News front page stories including titles, URLs, scores, authors, and comment counts from news.ycombinator.com. Use when the user mentions Hacker News, HN, ycombinator, or wants tech news stories.
metadata:
  author: scrapeagent
  version: "1.0"
---

# Hacker News Scraper

## Overview
Scrapes the Hacker News front page at https://news.ycombinator.com
No JavaScript required — use the `fetch` tool.

## Instructions

1. Fetch `https://news.ycombinator.com` using the fetch tool
2. The page has 30 story items. Each story spans two `<tr>` elements:
   - Row 1 (`.athing`): title and link
   - Row 2 (`.subtext`): metadata (score, author, comments)

3. For each story extract:
   - `rank`: `.rank` text, strip the trailing `.`
   - `title`: `.titleline > a` text (first `<a>` inside `.titleline`)
   - `url`: `.titleline > a` href — if starts with `item?id=`, prepend `https://news.ycombinator.com/`
   - `domain`: `.sitebit .sitestr` text (may be empty for HN-internal posts)
   - `score`: `.score` text, extract the number (e.g., "342 points" → 342)
   - `author`: `.hnuser` text
   - `age`: `.age a` text (e.g., "3 hours ago")
   - `comments`: last `<a>` in `.subtext` — extract the number, or 0 if "discuss"

4. Save with columns: rank, title, url, domain, score, author, age, comments

## Notes
- HN does not require JS — fetch works fine
- "Ask HN" and "Show HN" posts have internal HN URLs (item?id=...)
- Job posts may have no score/author/comments — handle gracefully with None/empty values
- To scrape a specific page: `https://news.ycombinator.com/?p=2` (page 2), etc.
