# Effective Claude Code — Documentation

Best-practices reference material for using Claude Code effectively, distilled from a 5-day platform build and backed by industry research.

## Core Documents

| Document | What It Covers |
|----------|---------------|
| [spec_driven_dev.md](spec_driven_dev.md) | Spec-driven development — why the spec, not the code, is the load-bearing artifact when working with AI agents. Surveys Osmani, Karpathy, GitHub Spec Kit, Anthropic, Thoughtworks, and others. |
| [testability_thesis.md](testability_thesis.md) | The testability thesis — AI agents succeed when outputs are concretely verifiable. Anchored by the Anthropic C compiler case study (16 parallel Claudes, 100K lines of Rust). |
| [context_degradation.md](context_degradation.md) | Context length degrades LLM performance. RULER benchmark data, "Lost in the Middle" findings, and why agent design is really context management. |
| [context_degradation_2026.md](context_degradation_2026.md) | 2025–2026 refresh: NoLiMa, MRCR v2 at 1M, Chroma Context Rot, HELMET, SWE-Bench Pro. Includes three candidate replacement figures for the slide deck. |
| [verification_by_explanation.md](verification_by_explanation.md) | Verification by explanation — using structured output (tables, scorecards, audit reports) to make human review of agent work feasible. 12 real examples catalogued. |
| [agent_commands.md](agent_commands.md) | Practical command reference for spawning, controlling, and orchestrating Claude Code agents (subagents, agent teams, exact phrasing that works). |
| [agent_modes.md](agent_modes.md) | Agent orchestration patterns — researcher/auditor/summarizer pipelines, cross-audit, build-test-audit-select. |
| [metr.md](metr.md) | The METR 2025 RCT study — AI made experienced developers 19% slower while they believed they were 20% faster. Why naive adoption fails. |
| [features.md](features.md) | Feature evaluation matrix — which patterns from the 5-day build made the cut and why. Includes confidence scores and cross-cutting themes. |

## Presentation

| File | Purpose |
|------|---------|
| [slides.md](slides.md) | Marp markdown source for the presentation deck. This is the source of truth. |
| [gen_slides.sh](gen_slides.sh) | Generates `slides.pdf` from `slides.md` using Marp CLI. Run `./gen_slides.sh` from this directory. |
| [cheat_sheet.html](cheat_sheet.html) | Two-page cheat sheet (HTML source). Print to PDF from a browser for the handout version. |

## Supporting Material

| Directory | Contents |
|-----------|----------|
| [assets/](assets/) | SVG diagrams used in the slides. Referenced by `slides.md`. |
| [evidence/](evidence/) | Hypothesis JSON files and evidence markdown files from transcript analysis. Supporting data for the core documents. |
| [transcripts/](transcripts/) | **Gitignored.** Raw Claude Code session transcripts (~3MB) that were the source material for all core documents. Not checked into the repo because they contain session-specific data, but they live here locally for reference. |

## For AI Agents

If you're an agent working in this repo:
- The core documents above are your knowledge base for advising on Claude Code best practices.
- `slides.md` is a Marp presentation — edit it as markdown, generate PDF with `gen_slides.sh`.
- `cheat_sheet.html` is hand-authored HTML optimized for 2-page print layout. Edit the HTML directly.
- Asset SVGs are referenced by absolute path in `slides.md` — if paths break, check and update them.
- The transcripts directory may be empty (gitignored) — that's expected. The docs were derived from transcripts but stand on their own.
