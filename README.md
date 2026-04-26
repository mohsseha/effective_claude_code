# Effective Claude Code

Patterns and best practices for using Claude Code effectively, based on building a production platform in 5 days and backed by industry research (METR study, Anthropic engineering, Thoughtworks, etc.).

This repo has two parts: **reference documentation** and a **live advisor service**.

---

## Talk & Slides

[![Watch the talk on YouTube](https://img.youtube.com/vi/zQbD_JMSXnU/maxresdefault.jpg)](https://youtu.be/zQbD_JMSXnU)

📺 **[Watch on YouTube](https://youtu.be/zQbD_JMSXnU)** &nbsp;·&nbsp; 📄 **[Slides (PDF)](docs/slides.pdf)** &nbsp;·&nbsp; 📝 **[Slide source](docs/slides.md)**

---

## Quick Start: The Advisor

The advisor is a coaching TUI that helps you use Claude Code more effectively in real time. Launch it alongside your coding session:

```bash
./advice.sh
```

It opens an interactive Claude Code session that:
- Knows all the best practices in `docs/`
- Coaches you on prompting, agent orchestration, verification, and context management
- **Never writes code or modifies files** — it only advises

Example questions you might ask it:
- "I have a large refactor to do across 20 files. How should I structure this?"
- "My Claude session is getting long and answers are degrading. What should I do?"
- "How do I verify that Claude's output is actually correct?"
- "Should I use subagents for this task?"

### How It Works

`advice.sh` launches Claude Code with `--append-system-prompt` (from `advisor-prompt.txt`) and `--permission-mode plan` so it cannot modify anything. The prompt instructs it to read `docs/` for its knowledge base. As the documentation improves, the advisor automatically gets smarter.

---

## Documentation

All reference material lives in [`docs/`](docs/). See [`docs/README.md`](docs/README.md) for a full index.

### Core Topics

| Topic | Document |
|-------|----------|
| Spec-Driven Development | [`docs/spec_driven_dev.md`](docs/spec_driven_dev.md) |
| Testability Thesis | [`docs/testability_thesis.md`](docs/testability_thesis.md) |
| Context Degradation | [`docs/context_degradation.md`](docs/context_degradation.md) |
| Verification by Explanation | [`docs/verification_by_explanation.md`](docs/verification_by_explanation.md) |
| Agent Commands | [`docs/agent_commands.md`](docs/agent_commands.md) |
| Agent Orchestration Modes | [`docs/agent_modes.md`](docs/agent_modes.md) |
| METR Study (Why Naive AI Fails) | [`docs/metr.md`](docs/metr.md) |

### Presentation

The slide deck (`docs/slides.md`) is a [Marp](https://marp.app/) presentation that accompanies the [YouTube talk](https://youtu.be/zQbD_JMSXnU). The rendered PDF is committed at [`docs/slides.pdf`](docs/slides.pdf); to regenerate it:

```bash
cd docs && ./gen_slides.sh
```

A two-page cheat sheet is also available: open `docs/cheat_sheet.html` in a browser and print to PDF.

---

## Repository Structure

```
effective_claude_code/
├── README.md              # This file
├── advice.sh              # Launches the advisor TUI
├── advisor-prompt.txt     # Coaching prompt (edit to refine advisor behavior)
├── .gitignore
└── docs/
    ├── README.md          # Full index of all documentation
    ├── spec_driven_dev.md
    ├── testability_thesis.md
    ├── context_degradation.md
    ├── verification_by_explanation.md
    ├── agent_commands.md
    ├── agent_modes.md
    ├── metr.md
    ├── features.md
    ├── slides.md          # Marp slide source
    ├── gen_slides.sh      # Slide PDF generator
    ├── cheat_sheet.html   # Two-page cheat sheet (HTML source)
    ├── assets/            # SVG diagrams for slides
    ├── evidence/          # Supporting evidence from transcript analysis
    └── transcripts/       # (gitignored) Raw session transcripts
```

---

## For Contributors and AI Agents

- **To improve advice quality**: Add or refine documents in `docs/`. The advisor reads them at runtime, so changes take effect on the next `./advice.sh` session.
- **To change advisor behavior**: Edit `advisor-prompt.txt`. This is the system prompt appended to Claude Code when the advisor launches.
- **To update the presentation**: Edit `docs/slides.md` (Marp markdown), then run `docs/gen_slides.sh` to regenerate the PDF.
- **Transcripts are gitignored**: The raw Claude Code session transcripts in `docs/transcripts/` were the source material used to create the core documents. They are not checked into the repo. The documentation stands on its own.

## License

This material is shared for educational purposes. The research and patterns are drawn from publicly available sources cited in each document.
