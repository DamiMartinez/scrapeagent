"""Tests for scrapeagent/tools/file_tools.py — no API keys or MCP servers needed."""

import csv
import json
from pathlib import Path

import pytest

import scrapeagent.tools.file_tools as ft


SAMPLE_DATA = [
    {"title": "Hello World", "score": "100", "url": "https://example.com"},
    {"title": "Foo & Bar", "score": "42", "url": "https://foo.com"},
]


# ---------------------------------------------------------------------------
# save_output — CSV
# ---------------------------------------------------------------------------


def test_save_output_csv_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = ft.save_output(SAMPLE_DATA, "test", format="csv")
    assert "2 records" in result
    out = tmp_path / "output" / "test.csv"
    assert out.exists()
    with open(out, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2
    assert rows[0]["title"] == "Hello World"
    assert rows[1]["score"] == "42"


def test_save_output_csv_empty_returns_message(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = ft.save_output([], "empty", format="csv")
    assert result == "No data to save."


# ---------------------------------------------------------------------------
# save_output — JSON
# ---------------------------------------------------------------------------


def test_save_output_json_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = ft.save_output(SAMPLE_DATA, "test", format="json")
    assert "2 records" in result
    out = tmp_path / "output" / "test.json"
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["url"] == "https://example.com"


def test_save_output_json_empty_writes_empty_array(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = ft.save_output([], "empty", format="json")
    assert "0 records" in result
    out = tmp_path / "output" / "empty.json"
    assert json.loads(out.read_text()) == []


# ---------------------------------------------------------------------------
# save_output — Markdown
# ---------------------------------------------------------------------------


def test_save_output_md_creates_table(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = ft.save_output(SAMPLE_DATA, "test", format="md")
    assert "2 records" in result
    out = tmp_path / "output" / "test.md"
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "| title | score | url |" in content
    assert "| --- |" in content
    assert "Hello World" in content
    assert "Foo & Bar" in content


def test_save_output_md_empty_returns_message(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = ft.save_output([], "empty", format="md")
    assert result == "No data to save."


# ---------------------------------------------------------------------------
# save_output — unknown format
# ---------------------------------------------------------------------------


def test_save_output_unknown_format(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = ft.save_output(SAMPLE_DATA, "test", format="xml")
    assert "Unknown format" in result
    assert "xml" in result


# ---------------------------------------------------------------------------
# create_skill
# ---------------------------------------------------------------------------


def _patch_file(monkeypatch, tmp_path):
    """Point the module's __file__ into tmp_path so skills land there."""
    fake_file = tmp_path / "scrapeagent" / "tools" / "file_tools.py"
    monkeypatch.setattr(ft, "__file__", str(fake_file))
    return tmp_path / "scrapeagent" / "skills"


def test_create_skill_creates_skill_md(tmp_path, monkeypatch):
    _patch_file(monkeypatch, tmp_path)
    result = ft.create_skill(
        "test-site",
        "Scrapes test data from test-site.",
        "## Instructions\n\nFetch the page and extract items.",
    )
    assert "test-site" in result
    skill_md = tmp_path / "scrapeagent" / "skills" / "test-site" / "SKILL.md"
    assert skill_md.exists()
    content = skill_md.read_text(encoding="utf-8")
    assert "name: test-site" in content
    assert "Scrapes test data" in content
    assert "## Instructions" in content


def test_create_skill_with_references(tmp_path, monkeypatch):
    _patch_file(monkeypatch, tmp_path)
    result = ft.create_skill(
        "ref-site",
        "A skill with references.",
        "Do stuff.",
        references={"schema.md": "# Schema\n\nid, name, price"},
    )
    assert "ref-site" in result
    refs_dir = tmp_path / "scrapeagent" / "skills" / "ref-site" / "references"
    assert refs_dir.is_dir()
    assert (refs_dir / "schema.md").read_text() == "# Schema\n\nid, name, price"


def test_create_skill_duplicate_returns_error(tmp_path, monkeypatch):
    _patch_file(monkeypatch, tmp_path)
    ft.create_skill("dup-site", "First.", "Instructions.")
    result = ft.create_skill("dup-site", "Second.", "More instructions.")
    assert "already exists" in result
    assert "dup-site" in result
