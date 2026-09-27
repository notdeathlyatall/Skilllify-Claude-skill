---
name: skillfy
description: Design and write complete, production-ready, installable Claude Skill packages including SKILL.md frontmatter, body instructions, scripts, references, and assets folders. Use whenever the user mentions creating a skill, writing a SKILL.md, building a Claude skill package, or asks to /skillfy a topic. Do not use for installing existing skills from URLs or repos.
---

# Skillfy

## 1. Purpose

Skillfy turns a user's idea for a repeatable workflow into a fully written, installable Claude Skill package — the actual files, not pseudocode or a summary. It eliminates the need to manually paste long prompt templates every time a skill is needed, ensuring the output follows the official SKILL.md format, progressive disclosure architecture, and description-writing best practices that make skills trigger reliably in real usage.

## 2. When to use / when NOT to use

**Use when:**

- The user asks to "create a skill," "build a skill," "write a SKILL.md," or uses the phrase `/skillfy <topic>`
- The user pastes or references the Skillfy Master Prompt Template and wants a package produced
- The user describes a repeatable workflow and wants it packaged as a reusable Claude Skill
- The user asks for a skill that contains scripts, references, or assets alongside SKILL.md

**Do NOT use when:**

- The user wants to _install_ an existing skill from GitHub, a marketplace, a URL, or a local folder — use the built-in skill-creator procedure instead
- The user wants to _update_ or modify an already-written SKILL.md without producing the full 5-section package
- The request is a one-off task with no reusable procedure — refuse politely and explain why
- The user only asks for an explanation of the SKILL.md format without wanting files created

## 3. Step-by-step workflow

Follow these twelve steps every time, in order. Do not skip or reorder.

1. **Confirm action and scope.** Decide if the request is a skill write (yes for this skill). Determine project vs global scope using the skill-creator scope rules: if the skill is about this repo's APIs/layout/deploy flow or scope is ambiguous and a workspace exists, choose project. If the user explicitly says global/user-level/across all projects, choose global. If scope is ambiguous and no workspace exists, ask one short question before writing.

2. **Gather the five required inputs.** Ask the user for any that are missing. Do not proceed to step 3 with blanks.
   - SKILL_NAME: the topic / short identifier for the skill (e.g., react-test-writer)
   - ONE-LINE PURPOSE: the single most important thing the skill lets Claude do
   - WHO IS USING THIS: solo user / team / public marketplace (affects tone and jargon level)
   - RESEARCH_SUMMARY: any pre-gathered research from web searches on similar tools, best practices, common pitfalls for this domain. If the user hasn't provided any, do the research yourself in step 3.
   - EXISTING SIMILAR SKILL: whether a similar skill is already installed. If the user doesn't know, check the project and global skill directories yourself. If one exists, document exactly how this new skill is a clear improvement, not a near-duplicate.

3. **Research the domain (if RESEARCH_SUMMARY is empty).** Run web searches covering:
   - Similar existing Claude Skills or tools in this category — what do they do well, what do they miss?
   - Best practices and common pitfalls for the task domain
   - Any libraries, APIs, or file formats the skill will likely need to reference
   - Summarize findings into a RESEARCH_SUMMARY block before proceeding. If web search returns nothing useful, explicitly record that assumption and proceed.

4. **Check for existing similar skills.** Scan `<workspaceFolder>/.trae/skills/` and the global skills root for skills with similar names or descriptions. If found, read their SKILL.md and articulate at least two concrete ways the new skill will differ (better workflow, different scope, new capabilities, improved trigger logic). Write this down. If none found, record "None found."

5. **Normalize and validate the skill name.**
   - Convert to kebab-case: lowercase letters a-z, digits 0-9, single hyphens only
   - Reject consecutive hyphens, leading/trailing hyphens, reserved words "anthropic" and "claude", XML tags
   - Length must be 2–64 characters. If not, propose a valid alternative.
   - The normalized name must match the directory name you will create.

6. **Resolve the destination path.**
   - Project scope: `<workspaceFolder>/.trae/skills/<skill-name>/`
   - Global scope: `<userHome>/<dataFolderName>/skills/<skill-name>/` where dataFolderName is `.trae-cn` for CN sessions or `.trae` for International sessions
   - If the destination directory already exists and the user did not explicitly request an update/replacement, stop and report the existing path — do not overwrite without confirmation.

7. **Write SKILL.md frontmatter.** Exactly two fields:
   - `name`: unquoted kebab-case identifier, equal to the directory name
   - `description`: plain YAML scalar (no quotes), one line, under 200 characters when possible, never over 1024. Must state what the skill does AND when to use it. Include trigger phrases, synonyms, and contexts. Write it slightly "pushy" so the skill under-triggers less. No `: ` (colon-space), no `<` or `>`, no TODO placeholders. Follow the shape: `Does X. Use when the user asks for Y or Z. Do not use for W.`

8. **Write SKILL.md body.** Cover all eight sub-sections below, in order. Keep the total body under ~500 lines. If any section would make it exceed that, move the excess content to a file under `references/` and add a one-line pointer in SKILL.md telling Claude when to read it.
   1. Purpose: 2–3 sentences on what problem the skill solves.
   2. When to use / when NOT to use: explicit boundary cases.
   3. Step-by-step workflow: numbered, imperative, concrete (what to ask, what to check, what tool to call, in what order).
   4. Expected inputs: list each with format, and per-input rule for when missing (ask vs. assume a sensible default).
   5. Expected output format: exact shape of the deliverable.
   6. Edge cases and error handling: at minimum cover missing input, ambiguous input, conflicting instructions, input outside scope, required tool/dependency not available.
   7. Tone/style rules specific to the skill: anything Claude should always or never do while this skill is active.
   8. (Optional) Reference pointer to a `references/` file for long material.

9. **Create supporting folders and files. Omit empty folders.**
   - `scripts/`: only if there is deterministic, repeatable logic. For each script, state the language, inputs, and outputs.
   - `references/`: only if there is lookup material Claude should read on demand, not always loaded. If a single reference file would exceed ~300 lines, include a table of contents at its top.
   - `assets/`: only if the output uses templates, icons, fonts, or boilerplate files.
   - After creating the tree, show it to the user with a one-line purpose per file beyond SKILL.md.

10. **Write two or more worked examples. At least one must be an edge case.** For each example:
    - Example user prompt: realistic, natural phrasing the user would actually type.
    - What Claude should do, step by step, referencing the numbered workflow steps from SKILL.md section 3.
    - The ideal final output in full (not placeholders). If the output is a file, show its complete contents. If it is a chat reply, show the full reply.

11. **Write test/verification notes and install notes.**
    - Test notes: If output is objectively checkable (code transform, specific file format), list 3–5 concrete pass/fail assertions. If subjective (style, tone, creative), say so explicitly and list 2–3 qualitative reviewer questions.
    - Install notes: Plain-language instructions for exactly which files go in which folder once the skill reaches Claude. List every assumption or guess you made during authoring that the user should double-check or adjust. List every external dependency, API key, or tool access the skill assumes exists.

12. **Validate and report.** Run the validation checklist:
    - Destination path matches chosen scope (project = `<workspaceFolder>/.trae/skills/<skill-folder>/`; global/install = `<userHome>/<dataFolderName>/skills/<skill-folder>/`)
    - Directory name equals `name` in frontmatter
    - SKILL.md has parseable frontmatter and a non-empty body
    - `name` and `description` are unquoted and legal (no reserved words, valid chars, name length 2–64)
    - `description` has no `: `, no `<`, no `>`, no TODO, and includes both what and when
    - Any `scripts/`, `references/`, or `assets/` files referenced in SKILL.md actually exist
    - For each new or modified script, execute it once successfully
      Then create the TodoWrite plan reflecting steps 1–12, execute file writes, and report to the user: the final skill path, the final description, and the directory tree.

## 4. Expected inputs

| Input                  | Format                                                                           | If missing                                                                                                                           |
| ---------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| SKILL_NAME             | Short kebab-case-able identifier or natural-language topic name                  | Ask the user in one short question; do not guess a topic.                                                                            |
| ONE-LINE PURPOSE       | Single sentence stating the core capability                                      | Derive from SKILL_NAME if it is descriptive enough; explicitly label the derivation as an assumption and ask the user to correct it. |
| WHO IS USING THIS      | One of: solo user, team, public marketplace                                      | Default to public marketplace; label this as an assumption and mention it in the install notes.                                      |
| RESEARCH_SUMMARY       | Paragraph of findings from web searches, best practices, similar tools, pitfalls | Perform the research yourself (step 3 of workflow). Do not ask the user.                                                             |
| EXISTING SIMILAR SKILL | Description of any installed similar skill, or "None found"                      | Scan the project and global skill directories yourself. Do not ask the user.                                                         |

## 5. Expected output format

The deliverable is a complete skill directory with the following files actually written to disk:

```
<skill-name>/
├── SKILL.md                    # Required. YAML frontmatter (name + description) + 8-section body
├── scripts/                    # Optional. Deterministic code. One line of purpose per file shown to user.
├── references/                 # Optional. On-demand lookup material. TOC if file >300 lines.
└── assets/                     # Optional. Templates, icons, boilerplate copied verbatim into output.
```

Plus a chat reply to the user containing, in order:

1. Confirmation that the skill was written and the final destination path
2. The final `description` line from frontmatter (for quick review)
3. Section B: the exact folder tree with one-line purpose per file beyond SKILL.md
4. Section C: two worked examples (minimum) with full output
5. Section D: test/verification notes
6. Section E: install notes, assumptions, and dependencies

## 6. Edge cases and error handling

- **Missing SKILL_NAME:** Ask exactly one short, friendly question: "What would you like the skill to be called or what topic should it cover?" Do not invent a name. If the user still does not provide one after two prompts, stop and explain you need a topic to proceed.
- **Ambiguous ONE-LINE PURPOSE / topic overlap with existing skill:** If the user's request could describe an already-installed skill, read the existing SKILL.md, summarize the overlap in 1–2 sentences, and ask the user whether to (a) improve/update the existing skill instead, or (b) proceed and document how the new skill is different. Do not silently create a near-duplicate.
- **Conflicting instructions:** If WHO IS USING THIS contradicts the tone implied by ONE-LINE PURPOSE (e.g., "public marketplace" plus hyper-specific internal jargon), flag the conflict, show both sides, and propose a resolution. Default to the narrower scope unless told otherwise.
- **Input outside scope:** If the user asks for something that is not a repeatable workflow (e.g., a single code write, a one-off email), decline explicitly, explain that skills are for reusable procedures, and offer to help without a skill instead.
- **Required tool/dependency unavailable:** If the skill design calls for a script or reference that depends on a library the environment lacks, note the dependency in both SKILL.md section 4 and in install notes. Provide an install command (pip install X, npm i Y) in install notes. Do not silently rely on a dependency being present.
- **Destination directory already exists:** Stop. Report the exact existing path. Ask whether the user wants to update, overwrite, or choose a different name. Do not write any files until the user answers.
- **Web search returns no relevant results during research:** Record the assumption "No domain-specific research was found via web search; proceeding with general skill authoring best practices only" and include this line in install notes under assumptions.

## 7. Tone/style rules specific to this skill

- Write for another Claude instance first, and a human reviewer second. Do not pad with explanations Claude already knows (what Markdown is, what YAML is, basic coding concepts).
- Use imperative form in workflow steps: "Check X" not "You should check X".
- Do not add comments to code unless the user's skill topic specifically requires them.
- Never include TODO placeholders, `{BRACKETED_PATTERNS}`, or "fill this in later" sections in output files the user will install. Every file you write must be production-ready.
- When comparing to an existing skill, be concrete and fair. Say "Existing X only covers Y; new skill adds Z and follows step-by-step W" not "Existing X is bad."
- Be explicit about every assumption you make. List them all in the install notes section E so the user can review.
- Keep SKILL.md body under 500 lines. Prefer tight numbered steps over paragraphs. Move long material to references/ with a pointer line.

## 8. Reference files

For detailed guidance on writing trigger descriptions (the single hardest part of skill authoring) and the full frontmatter validation rules, read:

- [description-writing-guide.md](file:///c:/Users/User/Desktop/Yogesh%20workspace/AI/Skillify/.trae/skills/skillfy/references/description-writing-guide.md) — when you are about to draft the `description` frontmatter field
- [frontmatter-validation.md](file:///c:/Users/User/Desktop/Yogesh%20workspace/AI/Skillify/.trae/skills/skillfy/references/frontmatter-validation.md) — when you need to verify a name or description string is syntactically valid
