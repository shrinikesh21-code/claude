# Ultrahuman Portfolio Workspace

This folder is a living portfolio of the user's work as a **Product Designer at Ultrahuman**. You are its curator. Every chat in this folder exists to capture work, keep it organised and keep the portfolio page current.

The folder is self-contained. The user may zip it and drop it into a new chat on a different Claude account or PC. When you start a session, read this file, `PORTFOLIO.md` and `LOG.md`, then you know everything. Do not ask the user to re-explain past work.

## Files

| Path | Purpose |
|---|---|
| `PORTFOLIO.md` | Single source of truth. Profile header plus every project, ordered by priority. |
| `assets/<project-id>/` | Screens, icons and other files for each project. Keep originals, use lowercase-kebab names. |
| `build.py` | `python3 build.py` regenerates `portfolio.html` and every case study page from `PORTFOLIO.md`. Standard library only. |
| `portfolio.html` | Generated overview page. Never edit by hand. Rebuild instead. |
| `case-studies/<id>.html` | Generated case study page, one per project, linked from its card on the portfolio. Never edit by hand. The build deletes and recreates this folder's pages every time. |
| `LOG.md` | One line per change, newest at the bottom. |
| `E-ruby.html` | Unrelated sample template from an earlier session. Ignore it. |

## `PORTFOLIO.md` format

```
# Title
name:        (leave empty if unknown, never guess)
role / company / tagline / updated: YYYY-MM-DD

## Project title
- id: kebab-case-slug          (matches the folder in assets/)
- priority: P1 | P2 | P3
- status: Live | Shipped | In progress | Concept
- added: YYYY-MM-DD
- tags: comma, separated
- role: optional, defaults to the profile role
- tools: comma, separated
- timeline: optional, for example "Mar to May 2026"
- team: optional, for example "with PM, engineering and brand"
- layout: optional, `phone` for tall mobile screenshots (portfolio card shows the phone, case study puts the story and the screens side by side). Leave out for square or wide images.
- summary: one or two sentences

### Context        free text, paragraphs or "- " bullets
### Problem        optional, what was wrong or missing
### Process        optional, research, references, iterations, decisions
### Solution       optional, what was designed or built
### Outcome        free text, shown in the dark accent card on the case study
### Learnings      optional
### Metrics        "- value | label", for example "- +12% | Add-to-cart rate". Leave empty if none.
### Screens        "- assets/<id>/file.png | Caption", first one is the hero
### To fill in     open questions about this project (internal, never shown on any page)
```

The case study page shows the sections that have content, in the order Context, Problem, Process, Solution, Outcome, Learnings, plus the fact cards, the screens gallery (click to enlarge) and the metrics. Empty sections are skipped, so a thin project gives a short page and a rich one gives a full story. When the user answers a question from "To fill in", move the answer into the right section and delete the question.

Rules for the parser: each project starts with `## `, fields are `- key: value` lines, and sections start with `### ` using exactly the names above. Inline `**bold**` and `[text](https://url)` are supported.

## Priority and ordering

Keep `PORTFOLIO.md` ordered **P1, then P2, then P3**. Within a tier, put the most important or most recent first.

- **P1 · flagship.** Shipped, highly visible, measurable impact, or work the user is proudest of. Gets the large case-study card.
- **P2 · solid.** Shipped and worth showing, but smaller scope or impact.
- **P3 · minor.** Small tweaks, exploration or older work. Shown as a compact row at the bottom.

When adding or changing a project, pick a tier from what the user tells you, say which one you chose and why in one line, and let them override. When the user re-ranks, move the section and update `priority:`. `build.py` sorts the page by tier either way and warns if the file is out of order.

## Workflows

**Add a project.** The user describes it and attaches screens.
1. Copy or save attachments into `assets/<id>/` with clean names. Never delete the user's originals.
2. Add the project section in priority order, filling only what the user said or what you can see in the files.
3. Put anything missing (problem, impact, process, team, timeline) under `### To fill in`. Ask for it at the end of the turn, at most two or three questions.
4. Set `updated:` to today, run `python3 build.py` (this also rebuilds the project's case study page), check for warnings, append a line to `LOG.md`.
5. Commit and push.

**Update an existing project.** Edit its section, add screens, move metrics from "To fill in" into `### Metrics` once the user supplies them, then re-evaluate its priority. Rebuild, log and push.

**Re-prioritise or reorder.** Move sections, update `priority:`, rebuild, log, push.

**Check the result.** After any change to `build.py`, render `portfolio.html` and a case study page with the pre-installed Chromium (Playwright, `executable_path='/opt/pw-browsers/chromium'`) at desktop and 400px widths, and look at it.

**New device or account.** The user drops the zip into a new chat. Unzip if needed, read the three files above, run `python3 build.py` to confirm everything works, then summarise in a few lines what the portfolio currently holds and what is still open in "To fill in".

## Rules

- **Never fabricate.** No invented metrics, dates, teammates, names or outcomes. If you do not know it, leave it out or put it under "To fill in". Inference is allowed only for plain description of what is visible in the assets. Flag any inference to the user.
- **Keep the user's voice.** Write in plain first-person-neutral language, concrete and short. No marketing filler.
- **Never edit `portfolio.html` or anything in `case-studies/` by hand.**
- **Keep it portable.** Relative paths only, no external dependencies beyond the optional Google Fonts link, no absolute paths in any file.
- **Persist everything.** The cloud container is temporary. Commit and push after every change to the branch the session names, and do not open a pull request unless asked.
- Do not store secrets, login details or private company data (internal URLs, unreleased product details) in this folder without the user's explicit say-so, since the folder gets zipped and moved around.

## Design of the generated page

Light grey canvas, large rounded white cards, tight bold grotesk type (Inter) with a muted second line, small uppercase pill tags, a bento stat row with one dark accent card, and case-study cards with context on the left and screens on the right. Dark mode follows the system setting. Reference: the user's four inspiration screenshots (Metaforce-style mission section, case-study carousel, app download card, "Design to convert" bento). Case study pages use the same language: pill tags, large muted-second-line title, fact cards, a white gallery card with soft tiles, divider rows with a pill label, a dark outcome card and a "next project" card. Keep new changes in that language.
