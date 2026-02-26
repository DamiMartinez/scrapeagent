"""Tests for scrapeagent/skills_loader.py — no API keys or MCP servers needed."""

import pathlib

import pytest

from scrapeagent.skills_loader import load_skill_from_dir


VALID_SKILL_MD = """\
---
name: test-skill
description: Scrapes test data for unit testing purposes.
metadata:
  author: pytest
  version: "1.0"
---

# Test Skill

## Instructions

Fetch the page and extract items.
"""


def _write_skill(skill_dir: pathlib.Path, content: str) -> None:
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_load_valid_skill(tmp_path):
    skill_dir = tmp_path / "test-skill"
    _write_skill(skill_dir, VALID_SKILL_MD)

    skill = load_skill_from_dir(skill_dir)

    assert skill.frontmatter.name == "test-skill"
    assert "unit testing" in skill.frontmatter.description
    assert skill.frontmatter.metadata["author"] == "pytest"
    assert "## Instructions" in skill.instructions


def test_load_skill_with_references(tmp_path):
    skill_dir = tmp_path / "ref-skill"
    _write_skill(skill_dir, VALID_SKILL_MD)
    refs = skill_dir / "references"
    refs.mkdir()
    (refs / "schema.md").write_text("# Schema\n\nid, name", encoding="utf-8")

    skill = load_skill_from_dir(skill_dir)

    assert "schema.md" in skill.resources.references
    assert "id, name" in skill.resources.references["schema.md"]


def test_load_skill_with_assets(tmp_path):
    skill_dir = tmp_path / "asset-skill"
    _write_skill(skill_dir, VALID_SKILL_MD)
    assets = skill_dir / "assets"
    assets.mkdir()
    (assets / "template.md").write_text("# Template", encoding="utf-8")

    skill = load_skill_from_dir(skill_dir)

    assert "template.md" in skill.resources.assets
    assert "Template" in skill.resources.assets["template.md"]


def test_load_skill_no_references_or_assets(tmp_path):
    skill_dir = tmp_path / "bare-skill"
    _write_skill(skill_dir, VALID_SKILL_MD)

    skill = load_skill_from_dir(skill_dir)

    assert skill.resources.references == {}
    assert skill.resources.assets == {}


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------


def test_missing_skill_md_raises(tmp_path):
    skill_dir = tmp_path / "no-skill-md"
    skill_dir.mkdir()

    with pytest.raises(FileNotFoundError, match="SKILL.md not found"):
        load_skill_from_dir(skill_dir)


def test_missing_frontmatter_raises(tmp_path):
    skill_dir = tmp_path / "no-frontmatter"
    _write_skill(skill_dir, "# No frontmatter here\n\nJust a body.")

    with pytest.raises(ValueError, match="frontmatter"):
        load_skill_from_dir(skill_dir)
