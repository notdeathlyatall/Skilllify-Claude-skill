---
name: your-skill-name
description: <What it does>. Use when the user asks for <trigger A> or <trigger B> — even if they don't say '<canonical term>'. Do not use for <anti-trigger>.
---

# Your Skill Name (Title Case, matches name in kebab-case)

## 1. Purpose

[2–3 sentences. What specific, repeatable problem does this skill solve for the user? Who benefits?]

## 2. When to use / when NOT to use

**Use when:**
- Bulleted list of concrete contexts, file types, or user phrases
- Be explicit

**Do NOT use when:**
- Bulleted list of boundary cases
- At least two concrete anti-triggers beyond the one in the description

## 3. Step-by-step workflow

[Numbered steps, imperative form. What to ask, what to check, which tool to call, in what order. Minimum 4 steps, maximum ~20. Do not write "as needed" — write the order.]

1. Step one
2. Step two
3. Step three
4. Step four

## 4. Expected inputs

| Input | Format | If missing |
|---|---|---|
| thing_a | e.g. path to a .py file | Ask the user explicitly |
| thing_b | e.g. JSON with fields x, y, z | Assume default {x: 0, y: 0, z: 0} and tell the user |

## 5. Expected output format

[Exact shape of the deliverable. If it is a file, state path and format. If it is a chat reply, show a template. Example:]

Write a single file `<output-dir>/result.json` with this exact schema:

```json
{
  "status": "ok | error",
  "items": [
    {"id": "...", "summary": "..."}
  ]
}
```

And reply to the user with a 2–3 sentence summary linking to the file.

## 6. Edge cases and error handling

- **Missing input X:** [exactly what to do]
- **Ambiguous input:** [exactly what to do — ask one clarifying question with 2–4 options, not open-ended]
- **Conflicting instructions:** [exactly what to do — flag, propose resolution, default to which side]
- **Input outside scope:** [exactly what to do — decline explicitly, offer alternative]
- **Required tool/dependency not available:** [exactly what to do — tell user, provide install command, suggest alternative path]
- [Add one skill-specific edge case beyond this minimum five]

## 7. Tone/style rules specific to this skill

- Bullet list. Anything Claude should always do or never do while this skill is active.
- Things like "Always output in British English" or "Never paste more than 100 lines of code at once without asking."
- Skip general tone rules Claude already knows. Only list skill-specific constraints.

## 8. Reference files

[Only if the body would exceed ~500 lines without them. Otherwise delete this section entirely.]

- [references/deep-dive.md](file:///references/deep-dive.md) — read when [condition that triggers loading this file]
