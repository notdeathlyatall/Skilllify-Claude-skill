#!/usr/bin/env python3
"""Validate a Claude Skill directory structure and SKILL.md frontmatter.

Usage:
    python validate_skill.py <path-to-skill-folder>

Exit code 0 = valid. Exit code 1 = validation errors (printed to stderr).
Checks:
  - Directory exists
  - SKILL.md exists and is readable
  - YAML frontmatter parses with at least name + description
  - name matches directory name, follows regex rules, no reserved words
  - description follows formatting rules (length, no forbidden substrings)
  - Any referenced scripts/references/assets files exist
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
RESERVED = ("anthropic", "claude")
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
DESC_FORBIDDEN_SUBSTRINGS = (": ", "<", ">", "{", "}")


def _parse_frontmatter(skill_md_text: str) -> dict | None:
    """Extract YAML frontmatter as a dict. Minimal parser, no PyYAML dep.

    Only supports key: value on single lines, between the first --- and second ---.
    Returns None if frontmatter is malformed.
    """
    lines = skill_md_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None
    fm: dict[str, str] = {}
    for raw in lines[1:end_idx]:
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return None
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # Strip matching outer quotes if present (we will warn on quotes in description)
        fm[key] = value
    return fm


def validate_name(name: str, dir_name: str, errors: list[str]) -> None:
    if not name:
        errors.append("frontmatter.name is empty or missing")
        return
    if name != dir_name:
        errors.append(f"frontmatter.name '{name}' does not match directory name '{dir_name}'")
    if len(name) < 2 or len(name) > MAX_NAME_LEN:
        errors.append(f"name length {len(name)} not in 2–{MAX_NAME_LEN}")
    if not NAME_RE.match(name):
        errors.append(
            f"name '{name}' does not match ^[a-z0-9]([a-z0-9-]{{0,62}}[a-z0-9])?$"
            " — must be lowercase letters/digits with single hyphens only, no leading/trailing hyphen"
        )
    lower = name.lower()
    for word in RESERVED:
        if word in lower:
            errors.append(f"name contains reserved word '{word}'")


def validate_description(desc: str, errors: list[str], warnings: list[str]) -> None:
    if not desc:
        errors.append("frontmatter.description is empty or missing")
        return
    if len(desc) > MAX_DESC_LEN:
        errors.append(f"description length {len(desc)} exceeds {MAX_DESC_LEN}")
    for substr in DESC_FORBIDDEN_SUBSTRINGS:
        if substr in desc:
            errors.append(f"description contains forbidden substring {substr!r}")
    # Detect quotes around scalar (heuristic: value starts/ends with matching " or ')
    if (desc.startswith('"') and desc.endswith('"')) or (
        desc.startswith("'") and desc.endswith("'")
    ):
        warnings.append("description is wrapped in quotes — prefer bare YAML scalar; "
                        "if you needed quotes to avoid ': ', rewrite the sentence instead.")
    if "todo" in desc.lower() or "TODO" in desc:
        errors.append("description contains TODO — must be production-ready")
    # Semantic sniff (soft warnings only)
    if "use when" not in desc.lower() and "ask for" not in desc.lower() and "mentions" not in desc.lower():
        warnings.append("description may be missing a 'when to use' clause — "
                        "double-check that it states both what it does and when to trigger")


def find_referenced_files(skill_md_text: str) -> list[str]:
    """Extract local relative paths referenced in SKILL.md body (scripts/, references/, assets/)."""
    refs: list[str] = []
    for m in re.finditer(r"(scripts/|references/|assets/)[\w\-.\\/]+", skill_md_text):
        path = m.group(0).replace("\\", "/")
        refs.append(path)
    return refs


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <path-to-skill-folder>", file=sys.stderr)
        return 2
    folder = Path(argv[1]).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not folder.exists() or not folder.is_dir():
        errors.append(f"skill directory does not exist: {folder}")
        return _report(folder, errors, warnings)

    skill_md = folder / "SKILL.md"
    if not skill_md.exists() or not skill_md.is_file():
        errors.append("SKILL.md not found in skill directory")
        return _report(folder, errors, warnings)

    text = skill_md.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)
    if fm is None:
        errors.append("could not parse YAML frontmatter from SKILL.md (expected --- ... --- block with key: value lines)")
        return _report(folder, errors, warnings)

    if "name" not in fm:
        errors.append("frontmatter missing required field 'name'")
    if "description" not in fm:
        errors.append("frontmatter missing required field 'description'")

    validate_name(fm.get("name", ""), folder.name, errors)
    validate_description(fm.get("description", ""), errors, warnings)

    # Check referenced files exist
    for rel in find_referenced_files(text):
        candidate = folder / rel
        if not candidate.exists():
            errors.append(f"SKILL.md references '{rel}' but no such file exists at {candidate}")

    return _report(folder, errors, warnings)


def _report(folder: Path, errors: list[str], warnings: list[str]) -> int:
    if warnings:
        print(f"VALIDATE {folder.name}: {len(warnings)} warning(s)")
        for w in warnings:
            print(f"  - WARN: {w}")
    if errors:
        print(f"VALIDATE {folder.name}: FAILED with {len(errors)} error(s)", file=sys.stderr)
        for e in errors:
            print(f"  - ERR : {e}", file=sys.stderr)
        return 1
    if not warnings:
        print(f"VALIDATE {folder.name}: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
