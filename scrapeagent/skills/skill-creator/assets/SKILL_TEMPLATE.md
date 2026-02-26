# {Website Name} Scraper

## Overview
What this skill scrapes and why.
Target URL: {base_url}

## Parameters (if applicable)
- param1: description (e.g., language filter)
- param2: description (e.g., time period: daily/weekly/monthly)

## URL Construction
- Base URL: {base_url}
- With filters: {base_url}/{param1}?{param2}=value

## Tool to use
- [ ] `fetch` — static HTML, no JavaScript needed
- [ ] `playwright` — JavaScript rendering required

## Extraction Instructions

1. Navigate to {url}
2. For each `{item_css_selector}` element extract:
   - `field1`: `{css_selector}` — `.text` or `['attribute']`
   - `field2`: `{css_selector}` — `.text` or `['attribute']`
   - `field3`: `{css_selector}` — `.text` or `['attribute']`
3. Handle pagination (if applicable):
   - Find the "next page" link: `{next_page_selector}`
   - Continue until no next page or limit reached
4. Save results with columns: field1, field2, field3, ...

## Notes
- Rate limiting: {any rate limit notes}
- Authentication: {required / not required}
- Edge cases: {any edge cases to handle}
