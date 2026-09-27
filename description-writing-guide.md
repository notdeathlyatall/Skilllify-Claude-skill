# Description Writing Guide

The `description` field in SKILL.md frontmatter is the only thing Claude reads before deciding whether to load your skill. Write it poorly and your skill will never trigger. This guide teaches you how to write it so it fires reliably.

## The golden pattern

Shape every description like this, in this exact order:

```
<What it does in plain language>. Use when the user asks for <trigger phrase A> or <trigger phrase B> — even if they don't use the word '<canonical term>'. Do not use for <wrong scenario>.
```

Why this shape works:
1. **What it does** comes first — a judge skimming a list can tell at a glance.
2. **Specific trigger phrases** — synonyms, paraphrases, and contexts. The more concrete, the less under-triggering.
3. **"Even if they don't use the word…"** clause — explicitly covers user phrasing that isn't your canonical term.
4. **Do not use for** — one concrete anti-trigger to cut down false positives.

## What counts as a trigger phrase

Good trigger phrases are things a real user actually types, not internal jargon:

- Canonical term: "budget" → also include: spending plan, monthly expenses, track money, where did my money go
- Canonical term: "code review" → also include: look at this diff, check this PR, before I merge, is this ready, review my code
- Canonical term: "skill authoring" → also include: create a skill, write a SKILL.md, build a Claude skill, /skillfy, make me a skill

Bad trigger phrases:
- "When relevant"
- "As needed"
- Any single word without synonyms or contexts

## Pushiness calibration

Claude tends to under-trigger skills. The description needs to be slightly assertive. Scale:

| Pushiness | Example | When to use |
|---|---|---|
| Too timid | "Helps with budgets." | Never. Your skill will never fire. |
| Good | "Tracks income and expenses into a monthly budget. Use when the user mentions a budget, spending plan, monthly expenses, or asks to track money — even if they don't use the word 'budget' explicitly. Do not use for business financial forecasting." | Default. Use this for every skill. |
| Too aggressive | "ALWAYS USE THIS FOR ANYTHING MONEY RELATED IN EVERY CONVERSATION" | Never. You will get false positives on every dollar sign. |

## Hard formatting rules (non-negotiable)

If you break any of these, the YAML will either fail to parse or your description will be silently truncated or mis-routed.

1. **No colon-space** `: ` anywhere. If you need a separator, use an em-dash `—` or reword to "including".
2. **No angle brackets** `<` or `>`. Not even in examples.
3. **No quotes** around the scalar. Leave it bare. A description with `: ` inside it forces quoting — so rewrite to avoid `: ` instead of quoting.
4. **No TODO, no placeholders, no `{BRACKETS}`.** The description must be production-ready.
5. **One line.** No line breaks. If it's too long, cut synonyms, not the anti-trigger.
6. **Target under 200 characters** when possible. Absolute hard ceiling is 1024 characters — anything over that is rejected at load time. Count: if you are past ~150, start trimming.
7. **Both "what" and "when" must be present.** A description that only says what it does without when-to-use will under-trigger. A description that only says when without what will confuse the router.

## Description scoring checklist

Before you finalize a description, run through this:

- [ ] States what the skill does in the first clause
- [ ] Lists 2+ concrete trigger phrases the user would actually type
- [ ] Has the "even if they don't use the word…" clause or equivalent synonym coverage
- [ ] Has exactly one concrete "Do not use for…" anti-trigger
- [ ] Contains no `: `, no `<`, no `>`, no quotes
- [ ] Is a single bare YAML line, under ~200 chars, definitely under 1024
- [ ] Name in frontmatter matches directory name exactly

## Worked examples of before/after

**Topic: weekly report generator**

Before (bad):
```
Generates weekly reports.
```
Why bad: No when. No synonyms. No anti-trigger. 22 chars of nothing.

After (good):
```
Generates structured weekly status reports from project notes or data. Use when the user asks for a weekly report, status update, project summary, or wants to summarize recent activity — even if they say 'quick update' or 'catch me up'. Do not use for one-off meeting agendas.
```

**Topic: PDF text extractor**

Before (bad):
```
Extract text from PDFs. Use when relevant.
```
Why bad: "Use when relevant" is useless. No trigger phrases. No anti-trigger.

After (good):
```
Extracts text, tables, and form fields from PDF files into structured Markdown or JSON. Use when the user uploads a PDF, asks to pull text from a PDF, parse PDF tables, or read form data out of a PDF document. Do not use for PDFs that only contain scanned images with no selectable text — OCR is out of scope.
```

**Topic: React test writer**

Before (bad):
```
Write tests for React components using Jest and React Testing Library.
```
Why bad: No when. No what-people-actually-say triggers. No anti-trigger.

After (good):
```
Writes unit and integration tests for React components with Jest and React Testing Library. Use when the user asks to write tests for a component, add tests, test coverage, 'can you test this', or asks for Jest/RTL specs. Do not use for E2E tests with Playwright or Cypress.
```
