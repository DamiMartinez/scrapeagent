import csv
import json
from pathlib import Path
from typing import Any


def save_output(
    data: list[dict[str, Any]],
    filename: str,
    format: str = "csv",
) -> str:
    """
    Save scraped data to a file.

    Args:
        data: List of dicts representing scraped rows/records.
        filename: Output filename without extension.
        format: Output format — "csv", "json", or "md".

    Returns:
        Confirmation message with the output file path.
    """
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    filepath = output_dir / f"{filename}.{format}"

    if format == "csv":
        if not data:
            return "No data to save."
        keys = list(data[0].keys())
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    elif format == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    elif format == "md":
        if not data:
            return "No data to save."
        keys = list(data[0].keys())
        lines = ["| " + " | ".join(keys) + " |"]
        lines.append("| " + " | ".join(["---"] * len(keys)) + " |")
        for row in data:
            lines.append("| " + " | ".join(str(row.get(k, "")) for k in keys) + " |")
        filepath.write_text("\n".join(lines), encoding="utf-8")

    else:
        return f"Unknown format '{format}'. Use csv, json, or md."

    return f"Saved {len(data)} records to {filepath}"


def create_skill(
    skill_name: str,
    description: str,
    instructions: str,
    references: dict[str, str] | None = None,
) -> str:
    """
    Create a new skill directory with SKILL.md and optional reference files.

    Args:
        skill_name: Kebab-case skill name matching the Agent Skills spec (e.g., 'amazon-products').
                    Must be lowercase, hyphenated, no consecutive hyphens, no leading/trailing hyphens.
        description: 1-2 sentence description. Must describe what it scrapes AND when to use it.
        instructions: Full markdown body for the SKILL.md file (the scraping instructions).
        references: Optional dict mapping filename -> content for the references/ subdirectory.

    Returns:
        Confirmation message with the created skill path.
    """
    skills_dir = Path(__file__).parent.parent / "skills"
    skill_dir = skills_dir / skill_name

    if skill_dir.exists():
        return (
            f"Skill '{skill_name}' already exists at {skill_dir}. "
            "Choose a different name or delete the existing skill first."
        )

    skill_dir.mkdir(parents=True)

    skill_md = f"""---
name: {skill_name}
description: {description}
metadata:
  author: community
  version: "1.0"
---

{instructions}
"""
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    if references:
        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        for fname, content in references.items():
            (refs_dir / fname).write_text(content, encoding="utf-8")

    return f"Created skill '{skill_name}' at {skill_dir}. Restart the agent to load the new skill."
