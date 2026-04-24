---
marp: true
theme: default
paginate: true
footer: "Effective Claude Code | Husain | 2026"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  :root {
    --fg: #1a1f2e;
    --ink: #0d1220;
    --accent: #0f4c5c;
    --accent-deep: #082a33;
    --accent-light: #e6eef0;
    --amber: #b45309;
    --border: #e3e5ea;
    --muted: #5b6472;
    --bg-subtle: #f5f6f8;
    --bg-warm: #fbf7f1;
  }

  /* ─── Base ───────────────────────────────────────────────────── */
  section {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    color: var(--fg);
    background: #ffffff;
    padding: 56px 72px;
    line-height: 1.5;
    letter-spacing: 0;
    border-top: 5px solid var(--accent);
    border-image: linear-gradient(to right, var(--accent) 0 62%, var(--amber) 62% 100%) 1;
  }

  h1 {
    font-weight: 800;
    color: var(--ink);
    font-size: 2.6em;
    line-height: 1.15;
    margin: 0 0 20px;
    border-bottom: none;
  }

  /* H2: every content slide's title. Same size, same rule, always top. */
  h2 {
    font-weight: 700;
    color: var(--ink);
    font-size: 1.6em;
    line-height: 1.2;
    margin: 0 0 22px;
    padding: 0 0 12px;
    border: none;
  }

  h2::after {
    content: "";
    display: block;
    width: 56px;
    height: 3px;
    background: var(--amber);
    margin-top: 12px;
  }

  h3 {
    font-weight: 600;
    color: var(--accent);
    font-size: 0.95em;
    margin: 16px 0 8px;
  }

  p { margin: 12px 0; }

  strong { font-weight: 700; color: var(--ink); }
  em { color: var(--muted); font-style: italic; }

  a {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid var(--amber);
  }
  a:hover { color: var(--amber); }

  /* ─── Code ───────────────────────────────────────────────────── */
  code {
    font-family: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
    font-size: 0.85em;
    background: var(--accent-light);
    border: 1px solid #cfd8da;
    color: var(--accent-deep);
    border-radius: 3px;
    padding: 1px 6px;
  }

  pre {
    background: #0d1b24 !important;
    border-radius: 6px;
    padding: 20px 24px !important;
    border: none;
    position: relative;
    margin: 16px 0;
  }
  pre::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--amber);
    border-radius: 6px 0 0 6px;
  }
  pre code {
    background: transparent;
    border: none;
    color: #e8eef0;
    font-size: 0.82em;
    line-height: 1.55;
    padding: 0;
  }

  /* ─── Tables (editorial: ruled, no box, centered, symmetric padding) ─ */
  table {
    border-collapse: collapse;
    width: 100%;
    max-width: 900px;
    margin: 18px auto;
    font-size: 0.82em;
    background: transparent;
    box-shadow: none;
    border: none;
    border-radius: 0;
    font-variant-numeric: tabular-nums;
    table-layout: auto;
  }
  table thead tr {
    border-top: 2.5px solid var(--ink);
    border-bottom: 1px solid var(--ink);
  }
  table th {
    background: transparent;
    color: var(--ink);
    font-weight: 700;
    text-align: left;
    padding: 12px 14px;
    border: none;
    line-height: 1.25;
    vertical-align: bottom;
  }
  table td {
    padding: 12px 14px;
    text-align: left;
    border: none;
    border-bottom: 1px solid rgba(11, 31, 48, 0.15);
    vertical-align: top;
    line-height: 1.45;
    color: var(--fg);
  }
  table tbody tr:last-child td { border-bottom: 1.5px solid var(--ink); }
  table tbody tr td { background: transparent !important; }
  table th:first-child,
  table td:first-child { padding-left: 0; }
  table th:last-child,
  table td:last-child { padding-right: 0; }
  table td:first-child {
    color: var(--ink);
    font-weight: 600;
  }
  table strong { font-weight: 700; color: var(--ink); }
  table td:first-child strong { color: var(--accent); }

  /* Split-bg tables: tighter, constrained to the column */
  section[style*="background-image"] table,
  section[style*="--marpit-advanced-background-split"] table {
    font-size: 0.74em;
    max-width: 100%;
    margin: 14px 0;
  }
  section[style*="background-image"] table th,
  section[style*="background-image"] table td,
  section[style*="--marpit-advanced-background-split"] table th,
  section[style*="--marpit-advanced-background-split"] table td {
    padding: 9px 10px;
  }

  /* ─── Blockquote ─────────────────────────────────────────────── */
  blockquote {
    border-left: 3px solid var(--amber);
    background: var(--bg-warm);
    padding: 10px 18px;
    margin: 16px 0;
    color: var(--ink);
    font-style: italic;
    border-radius: 0 3px 3px 0;
  }
  blockquote p { margin: 4px 0; }

  /* ─── Lists ──────────────────────────────────────────────────── */
  ul, ol {
    margin: 12px 0;
    padding-left: 1.3em;
  }
  li { margin-bottom: 5px; }
  li::marker { color: var(--amber); }

  /* ─── Footer / pagination ────────────────────────────────────── */
  footer {
    font-size: 0.6em;
    color: var(--muted);
    font-weight: 500;
  }
  section::after {
    font-size: 0.62em;
    color: var(--muted);
    font-weight: 500;
  }

  /* ─── Split-bg content slides (right-side image) ─────────────
     Marp puts a background-image on the section; content fills the
     remaining column. Same layout rules, just slightly smaller type. */
  section[style*="background-image"],
  section[style*="--marpit-advanced-background-split"] {
    font-size: 0.95em;
  }
  section[style*="background-image"] h2,
  section[style*="--marpit-advanced-background-split"] h2 {
    font-size: 1.45em;
  }
  section[style*="background-image"] li,
  section[style*="--marpit-advanced-background-split"] li {
    margin-bottom: 4px;
    line-height: 1.4;
  }
  section[style*="background-image"] table,
  section[style*="--marpit-advanced-background-split"] table {
    font-size: 0.78em;
  }

  /* ─── Hero slides: title slide + closing slide + lead ─────── */
  section.lead,
  section:first-of-type,
  section[id="20"] {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: linear-gradient(180deg, #ffffff 0%, var(--bg-warm) 100%);
  }

  section.lead h1,
  section.lead h2,
  section:first-of-type h1,
  section[id="20"] h2 {
    text-align: center;
  }

  section.lead h2::after,
  section:first-of-type h1::after,
  section[id="20"] h2::after {
    margin-left: auto;
    margin-right: auto;
  }

  section:first-of-type h1 {
    font-size: 3em;
    margin-bottom: 24px;
  }

  section:first-of-type h1::after {
    width: 72px;
    height: 4px;
    margin-top: 20px;
  }

  section:first-of-type p {
    color: var(--muted);
    font-size: 1.05em;
    max-width: 32em;
    margin: 6px 0;
  }

  section:first-of-type strong { color: var(--accent); }

  section[id="20"] h2 {
    font-size: 2.8em;
    font-weight: 800;
  }
  section[id="20"] h2::after {
    width: 96px;
    height: 4px;
    margin-top: 24px;
  }
  section[id="20"] p {
    color: var(--accent);
    font-size: 1.25em;
    font-weight: 700;
  }

  /* ─── Full-bleed image slide ─────────────────────────────────── */
  section.fullbleed {
    padding: 0;
    border: none;
  }
  section.fullbleed::before,
  section.fullbleed::after { display: none; }
---

# Effective Claude Code

A snapshot of best practices for coding with AI agents — April 2026

**Husain Al-Mohssen, PhD**

<!-- _footer: "" -->
<!-- _paginate: false -->

---

## Overview

- **Calibrating experience & expectations** — what's working, what's frustrating?
- The evidence: why naive AI use hurts experienced devs
- Context management & the priority quadrant
- Spec-driven development & verification patterns
- Multi-agent orchestration: what worked, what failed
- Key takeaways & discussion

---

## Software Engineering in 2026: The Uncertainty Is the Point

![bg right:38% 90%](assets/we-didnt-start-the-fire.jpg)

- No one has this figured out. Not us, not anyone.
- The imperfection is permanent, not temporary.
- Our job: build patterns anyway.

A field report, not a playbook.

---

## AI Can Hurt You

![bg right:40% contain](assets/metr-perception-gap.png)

[METR 2025 RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/): 16 experienced OSS developers

- **19% slower** with AI
- *Believed* they were **20% faster**
- **39-point** perception gap

Feb 2026 followup (57 devs): still no significant speedup.

Not anti-AI. Anti-**naive** adoption.

---

## So What Does Work?

Not tips and tricks. **Structural patterns.**

1. How the developer's role changes
2. How to manage agent context and execution
3. How to verify agent output
4. What failed

---

## Context Is Everything

![bg right:45% contain](assets/context-rot-ruler.png)

| Model | 4K | 128K | Drop |
|-------|-----|------|------|
| GPT-4 | 96.6% | 81.2% | -15 pts |
| Mixtral | 94.9% | 44.5% | -50 pts |
| Mistral 7B | 93.6% | 13.8% | -80 pts |

**Agent design = context design.**

Each subagent gets the **minimum context** for its task. Fresh agent with 4K of focus beats a bloated session at 100K.

---

## Context in Practice

![bg right:50% contain](assets/context-claude-code.jpg)

Claude Code's `/context` command shows exactly where your tokens go.

- System prompt, tools, memory, skills, messages
- **Free space** is what matters — that's your agent's working memory
- When free space shrinks, accuracy drops
- Start a fresh session or subagent to reclaim it

---

## Testability Determines Success

Anthropic C compiler case study:

| Metric | Value |
|--------|-------|
| Agents | 16 in parallel |
| Output | ~100K lines of Rust |
| Cost | ~$20K |
| Pass rate | **99%** GCC torture tests |

Carlini: *"Most of my effort went into designing the tests, the environment, the feedback."*

---

## The Testability Spectrum

| Domain | Testability | Agent effectiveness |
|--------|-----------|-------------------|
| Compilers | Binary correct/wrong | Excellent |
| Math proofs | Formal verification | Excellent |
| SWE-bench | Test suites | Good but incomplete |
| Web UI | Selenium/visual | Moderate |
| Business logic | Subjective | Weak without specs |

The agent's capability is the ceiling. **The test infrastructure is the floor.**

---

## Where to Use Agents First

![bg right:50% contain](assets/cc-priority-quadrant.svg)

Start bottom-left, earn your way right.

- **Sweet Spot:** Boilerplate, tests, migrations — easy to build, easy to verify
- **High Leverage:** Compilers, formal proofs — hard but verifiable
- **Risky:** Business logic, UI polish — easy to build, hard to verify
- **Danger Zone:** Architecture, security — hard on both axes

---

## The QA Superpower

![bg right:40% contain](assets/selenium-qa-gate.svg)

Multi-agent changes break the UI in ways unit tests miss.

- Caught avatar mismatch after multi-agent refactoring
- Caught stale refs, React state sync bugs
- Pass/fail tables enabled **parallel fix delegation**

Separated 7 phantom Chrome crashes from 2 real bugs.

---

## Verification by Explanation

Force agents to **show their understanding**.

| Technique | What it catches |
|-----------|----------------|
| Claim-by-claim table | Factual errors in your own descriptions |
| Comparison matrix | Hidden disagreements between agents |
| Accuracy score | Calibrated confidence before sharing |
| **Diagram of understanding** | Misunderstandings BEFORE they become bugs |

The diagram IS the verification. If the agent's picture doesn't match yours, its code won't either.

---

## From Programmer to <span style="color: crimson;">Meta-Programmer</span>

![bg right:40% contain](assets/meta-programming-shift.svg)

You stop writing code. You start designing **agent workflows**.

1. **Design** the workflow
2. **Write** the spec
3. **Review** the output
4. **Iterate** on the spec, not the code

*"dude have an agent do the work don't do it yourself"*

---

## Meta-Programming in Practice

```
Day 1: "Claude, write a function that..."
Day 3: "Start 3 agents to each implement this spec,
        then start 2 auditors to cross-review"
Day 5: "12-agent, 5-phase pipeline with parallelism
        rules, gates, and selection criteria"
```

From **using AI to help me code** to **designing agent systems that produce code**.

44% of activity was still direct coding -- you never fully stop. The leverage is in the orchestration.

---

## Know Your Execution Modes

![bg right:40% contain](assets/three-modes.svg)

| Mode | What it is | When |
|------|-----------|------|
| **Single session** | One conversation, you drive | Simple tasks |
| **Subagents** | Spawned child processes | Parallel work |
| **Agent teams** | Shared task list + messaging | Large efforts (experimental) |

Most patterns in this talk use **subagents**.

---

## What to Say (and Not Say)

| DO | DON'T |
|----|-------|
| "Start 3 agents to each implement this spec" | "Help me write this function" |
| "All work by agents, you only supervise" | Let Claude do the work itself |
| "Have agent A audit agent B's output" | Ask one agent to check its own work |
| Give each agent a role and perspective | Dump everything into one session |

Escalation: "start an agent" → "don't do this yourself" → "ALL agents not you" → "dude have an agent do it"

---

## What Failed

- **Full autonomy is a myth** -- human intervention was constant
  - *"THERE IS NO WAY THEY DID A GREAT JOB"*
  - Rate limits killed all 3 builders in one round
- **Specs don't enforce themselves** -- 5/6 modules violated the frozen spec
- **Same-model auditors are lenient** -- they share blind spots
- **Quorum rules** -- never triggered, untested

---

## Know When to Hold 'Em

![bg right:30% contain](assets/the-gambler-cover.jpg)

> *"You got to know when to hold 'em, know when to fold 'em"*
> -- Kenny Rogers

The new killer SWE skill: **knowing when to review and when to trust.**

| Trust it | Review it | Rewrite it |
|----------|----------|------------|
| Boilerplate, scaffolding | Business logic, API contracts | Security-critical code |
| Tests pass + matches spec | Novel algorithm, edge cases | Anything you can't test |
| Read-only research | External-facing output | Core architecture decisions |

---

## Key Takeaways

1. **Naive AI makes experienced devs slower** (METR 2025)
2. Your job is **meta-programming** -- design agent workflows, not code
3. **Context management** is the core skill -- smaller = more accurate
4. **Testability determines success** -- invest in test infrastructure first
5. **Force agents to show understanding** -- the diagram is the verification
6. **Know when to trust, when to review** -- that's engineering judgment now

---

## Questions & Discussion

**Husain Al-Mohssen**

<!-- _footer: "" -->
<!-- _paginate: false -->

---

<!-- _class: lead -->

# Appendix

---

## Appendix: Frozen Specs Prevent Drift

![bg right:40% contain](assets/frozen-specs.svg)

Git-tagged, immutable specs as single source of truth.

- 16 stories frozen with `git tag -a e2e-stories-v1`
- 4 agents audited ~30 files, only 3 minor fixes
- Build and demo agents read from same frozen source

**Limitation:** Prevents spec-to-spec drift but NOT spec-to-code drift. 5/6 modules violated SKILL.md. Need active enforcement.

---

## Appendix: Build → Test → Audit → Select

![bg right:40% contain](assets/build-test-audit-select.svg)

1. **Build** (parallel): N agents implement same spec
2. **Test** (sequential): automated suite against each
3. **Audit** (parallel): cross-review survivors
4. **Select**: pick the best, or none

Cross-auditors caught 19 real issues. Cross-audit (builder A reviews builder C) beat separate auditor agents.

---

## Appendix: Dedup Poisons Tests

![bg right:40% contain](assets/dedup-trap.svg)

1. API call fails
2. Response gets **cached**
3. Subsequent runs replay the **cached failure**
4. Tests look broken, API is fine

9 debugging steps before finding root cause. Hit twice. Blocked flagship feature.

**Fix:** Never cache errors. TTL-based expiry. No caching in test envs.

---

## Appendix: Three-Agent Fact-Checking

![bg right:40% contain](assets/researcher-auditor-summarizer.svg)

```
Researcher --> Auditor --> Summarizer
```

- 4/27 claims had errors (15% caught)
- Each agent sees only predecessor's output
- 3x latency (6-15 min vs 2-5 min)

**Use when:** sharing externally, making decisions.
**Skip when:** exploring, speed > accuracy.

Give auditors a **specific perspective** for better coverage.

---

## Appendix: Ask for Alternatives

Before committing to any approach:

*"Give me 3 ways to do this with trade-offs for each"*

- Forces the model to explore the solution space, not just its first instinct
- You pick from a menu instead of accepting a default
- Works for architecture, API design, error handling, naming

Don't accept the first answer. Make the model compete with itself.

---

## Appendix: Use the Advisor Sidekick

```bash
./advice.sh
```

Run it in a **separate terminal** alongside your Claude Code session.

- Coaching TUI that knows all the best practices in this talk
- Advises on prompting, agent orchestration, context management, verification
- **Never writes code or touches your files** — only advises
- Gets smarter as you add docs to `docs/`

Ask it things like:
- *"I have a 20-file refactor. How should I structure this?"*
- *"My session is getting long. What should I do?"*
- *"Should I use subagents here?"*

`github.com/mohsseha/effective_claude_code`

---

<!-- _class: fullbleed -->
<!-- _footer: "" -->
<!-- _paginate: false -->

![bg contain](assets/verification-skill-refinement-workflow.png)

---

## Appendix: Session Details

**Friday April 3, 9:30 am – 12:30 pm EDT** · Organized by John Biasi (CTO, LineVision)

### Pre-work (do before the session)

1. **Prerequisite:** At least 2 hours of real use with Claude Code
2. **Read:** [How Coding Agents Work](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/) — Simon Willison (~15 min)
3. **Read:** [Humans and Agents in SWE Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html) — Martin Fowler (~15 min)
4. **Do:** Pick something you actually want built. Spend 1–2 hours building it with Claude Code. Come with notes on what worked, what surprised you, and what frustrated you.

<!-- _footer: "" -->
