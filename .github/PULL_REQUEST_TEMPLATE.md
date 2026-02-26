## Type of Change

- [ ] New scraping skill
- [ ] Bug fix
- [ ] Documentation update
- [ ] Other: <!-- describe -->

## Description

<!-- What does this PR do? Why? -->

## Checklist

- [ ] Skill name is kebab-case and clearly describes site + data type
- [ ] `description` field covers what it scrapes AND when to trigger it
- [ ] Extraction instructions include exact CSS selectors (tested against the live site)
- [ ] Tool selection is correct (`fetch` vs `playwright`)
- [ ] Skill has been tested locally with `adk web`
- [ ] No hardcoded credentials or API keys in any file
- [ ] Skill body is under 500 lines
