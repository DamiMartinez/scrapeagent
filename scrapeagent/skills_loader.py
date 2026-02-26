"""Load Agent Skills from directory structure into google.adk.skills.models.Skill objects."""

from __future__ import annotations

import pathlib

import yaml
from google.adk.skills.models import Frontmatter, Resources, Skill


def load_skill_from_dir(skill_dir: pathlib.Path) -> Skill:
    """Parse a skill directory into a Skill object.

    Expected layout:
        skill_dir/
            SKILL.md          # YAML frontmatter + markdown body (required)
            references/*.md   # optional reference files
            assets/*          # optional asset files
    """
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

    raw = skill_md_path.read_text(encoding="utf-8")

    # Split YAML frontmatter from markdown body
    if not raw.startswith("---"):
        raise ValueError(f"{skill_md_path} must start with YAML frontmatter (---)")

    parts = raw.split("---", 2)
    # parts[0] = '' | parts[1] = frontmatter YAML | parts[2] = body
    fm_data = yaml.safe_load(parts[1])
    body = parts[2].strip() if len(parts) > 2 else ""

    metadata = fm_data.get("metadata", {}) or {}
    frontmatter = Frontmatter(
        name=fm_data["name"],
        description=fm_data["description"],
        metadata={str(k): str(v) for k, v in metadata.items()},
    )

    # Load references/ (markdown files)
    references: dict[str, str] = {}
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for f in sorted(refs_dir.glob("*.md")):
            references[f.name] = f.read_text(encoding="utf-8")

    # Load assets/ (any file type, read as text)
    assets: dict[str, str] = {}
    assets_dir = skill_dir / "assets"
    if assets_dir.is_dir():
        for f in sorted(p for p in assets_dir.iterdir() if p.is_file()):
            assets[f.name] = f.read_text(encoding="utf-8")

    return Skill(
        frontmatter=frontmatter,
        instructions=body,
        resources=Resources(references=references, assets=assets),
    )
