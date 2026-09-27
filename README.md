# Skillfy

**Finds, researches, and drafts a complete Claude Skill package for any topic you name.**

Skillfy is a meta-skill: instead of writing a Claude Skill by hand, you name a topic, and Skillfy does the legwork — research, overlap-checking, and a ready-to-paste prompt — so another AI can generate the actual files for you.

---

## What it does

When you type `/skillfy <topic>`, Skillfy will:

1. __Search the web__ for existing similar tools, skills, and best practices on that topic
2. __Check your installed skills__ for anything overlapping — if something similar already exists, it tells you and asks whether you want an upgraded version anyway, instead of silently duplicating it
3. __Generate a detailed prompt__ — not the skill itself — covering the full `SKILL.md` spec, folder structure, worked examples, and edge cases
4. Hand you that prompt to paste into ChatGPT (or another AI), which produces the actual skill files for you to install

---

## Why a prompt, not the skill directly?

Skillfy is designed to hand off the *file generation* step to a second AI, so you get:

- A **second, independent pass** at the design before anything is installed
- The chance to **review and tweak** the generated files before they touch your Claude setup
- A **consistent, thorough spec** every time — no shortcuts, no half-written sections

---

## Usage

```
/skillfy budget tracker
/skillfy meeting notes summarizer
/skillfy pdf invoice extractor
```

Just the topic — Skillfy fills in the research and the prompt template automatically.

---

## Output format

Each run produces:

- A **fully-detailed prompt** (~10k characters) ready to paste into another AI
- That AI returns:
  - `SKILL.md` — frontmatter + step-by-step instructions
  - `scripts/` *(if needed)* — deterministic logic
  - `references/` *(if needed)* — lookup docs Claude reads on demand
  - `assets/` *(if needed)* — templates/icons/fonts used in output
  - At least **2 worked examples**, including one edge case
  - Install notes

---

## Installing Skillfy itself

1. Go to the **latest release** on the repo's Releases page
2. **Download the `.zip`** for that release
3. **Extract** the zip on your computer (you should end up with a folder containing `SKILL.md`, and optionally `scripts/`, `references/`, `assets/`)
4. Open the **skill maker / skill upload page** in Claude
5. **Drag the extracted folder** (or the `.zip`, depending on what the uploader accepts) into it
6. **Name it `skillfy`** when prompted
7. Click **Add** to install it
8. **Use it** — type `/skillfy <topic>` in any chat to run it

## Installing a Skillfy-generated skill

1. Save the returned files into a folder matching the skill's `name`
2. Drop `SKILL.md` (and any subfolders) into your Claude skills location
3. Restart/refresh so Claude picks it up
4. Test it with one of the worked example prompts before relying on it

---

## License

MIT — see `LICENSE`. Full credit: **[Your Name]**.

---

*Built with Skillfy, for building more Skillfy-made skills.*
