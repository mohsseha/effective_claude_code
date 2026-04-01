# CLAUDE.md

## What This Repo Is

This repo contains best-practices documentation on using Claude Code effectively, plus an advisor service that coaches developers in real time. It is a public repo.

## Repo Structure

- `docs/` — All reference material (deep-dive articles, slides, cheat sheet, assets, evidence). See `docs/README.md` for a full index.
- `advice.sh` — Launches the advisor TUI. Uses `--append-system-prompt` from `advisor-prompt.txt` and `--permission-mode plan`. The advisor NEVER modifies files.
- `advisor-prompt.txt` — The coaching system prompt. Edit this to change advisor behavior.
- `docs/slides.md` — Marp presentation source. Generate PDF with `docs/gen_slides.sh`.
- `docs/cheat_sheet.html` — Hand-authored HTML, print to PDF from browser.
- `docs/transcripts/` — Gitignored. Raw session transcripts used to create the docs. May be empty on clone.
- `docs/evidence/` — Supporting evidence files from transcript analysis.
- `docs/assets/` — SVG diagrams referenced by `slides.md`.

## Key Conventions

- `docs/slides.md` uses absolute paths for images. If slides break, check the asset paths.
- Generated artifacts (slides.pdf, cheat_sheet.pdf) are gitignored — regenerate from sources.
- The core documents in `docs/` serve double duty: presentation reference AND the advisor's knowledge base. Improving docs improves the advisor.

## Common Tasks

- **Improve the advisor**: Edit `advisor-prompt.txt` or add/refine docs in `docs/`.
- **Update slides**: Edit `docs/slides.md`, then run `docs/gen_slides.sh`.
- **Add new best practice**: Create a new `.md` file in `docs/`, add it to `docs/README.md`, and reference it in `advisor-prompt.txt` so the advisor knows about it.
