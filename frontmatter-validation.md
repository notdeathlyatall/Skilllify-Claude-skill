# Frontmatter Validation Rules

Reference for checking `name` and `description` fields in SKILL.md YAML frontmatter. This file is the source of truth for what passes and what fails.

## name field rules

**Regex:** `^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$`

| Rule | Pass | Fail |
|---|---|---|
| Length 2–64 chars | `pdf-extractor` (13) | `x` (1), `a` 65 times |
| Lowercase letters a-z only | `my-skill`, `skill2025` | `My-Skill`, `PDFExtractor` |
| Digits 0-9 allowed | `test-v1`, `db-2-sql` | (digits are fine anywhere except reserved) |
| Single hyphens between segments | `foo-bar-baz` | `foo--bar`, `foo---baz` |
| No leading or trailing hyphen | `my-skill` | `-my-skill`, `my-skill-` |
| No reserved words anywhere in string | — | `anthropic-tools`, `my-claude-skill` |
| No XML tags, no angle brackets | — | `<skill>`, `foo<bar>` |
| No spaces, no underscores, no dots | `foo-bar` | `foo bar`, `foo_bar`, `foo.bar` |

Reserved words that are forbidden (case-insensitive substring match):
- `anthropic`
- `claude`

The `name` value in frontmatter MUST equal the parent directory name exactly. If the directory is `react-test-writer/`, the frontmatter must say `name: react-test-writer`.

## description field rules

| Rule | Pass | Fail |
|---|---|---|
| Non-empty string | (any text) | Empty, whitespace only |
| Max 1024 chars | any ≤ 1024 | 1025+ chars |
| No `: ` (colon-space) substring | `Use this for X — Y` | `Use this for X: Y` |
| No `<` character | — | any string with `<` |
| No `>` character | — | any string with `>` |
| Bare scalar (unquoted) in YAML | `description: foo bar baz` | `description: "foo bar"` or `description: 'foo bar'` |
| Contains both "what" and "when" semantic content | See pattern below | Description that only says what it does without when |
| No TODO, no `{PLACEHOLDERS}` | — | Any string containing `TODO` or `{` `}` brackets used as blanks |

Description semantic check (not regex, human or LLM review):
1. First clause states what the skill does in plain language.
2. There is at least one concrete trigger phrase, preferably 2+, covering synonyms and user-vernacular wording.
3. There is exactly one concrete "Do not use for" anti-trigger scenario that cuts off the most likely false-positive case.

## Optional frontmatter fields

These are allowed in Create/Update but not required. During Install, preserve them as-is without rewriting.

| Field | Purpose | Notes |
|---|---|---|
| `license` | SPDX identifier e.g. `MIT` | Optional, marketplace-facing |
| `allowed-tools` | Space-separated tool restrictions e.g. `Bash(python:*) WebFetch` | Optional advanced restriction |
| `metadata` | Mapping of author/version/etc | Optional custom fields |
| `compatibility` | `claude-code, claude.ai` | Optional surface indicator |
| `context` | Execution context hint | Optional advanced |
| `agent` | Agent control hints | Optional advanced |

When creating a new skill from scratch, only write `name` and `description`. Do not add optional fields unless the user explicitly asks for them. Less frontmatter = fewer parsing edge cases.

## Full valid example

```yaml
---
name: pdf-extractor
description: Extracts text, tables, and form fields from PDFs into Markdown or JSON. Use when the user uploads a PDF, asks to pull text or parse tables from a PDF document, or read form data. Do not use for image-only scanned PDFs that require OCR.
---
```

Why this passes:
- name: 13 chars, kebab-case, no reserved words
- name matches directory name `pdf-extractor/`
- description: 271 chars (well under 1024)
- description has no `: `, no `<>`
- description is unquoted
- What it does clause → "Extracts text, tables, and form fields from PDFs into Markdown or JSON."
- When clauses → "uploads a PDF, asks to pull text or parse tables from a PDF document, or read form data"
- Do not use for → "image-only scanned PDFs that require OCR"
- No TODO, no placeholders

## Invalid examples and why

```yaml
---
name: my-claude-skill
description: Helps with things.
---
```
Invalid: name contains reserved word `claude`. Description is too vague, no when, no anti-trigger.

```yaml
---
name: PDF Extractor
description: "Extract content: text, tables, images from PDF. Use when PDF is uploaded."
---
```
Invalid: name has uppercase and space. Description is quoted and contains `: `.

```yaml
---
name: myskill
description: Does the thing <see docs>. TODO fill this in later.
---
```
Invalid: description has `<` and `>` chars, contains `TODO`, has no concrete when, no anti-trigger.
