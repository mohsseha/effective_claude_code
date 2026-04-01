# Effective Claude Code: Presentation Features

10 candidates extracted from 22K-line transcript of building Angelic Intelligence over 5 days with Claude Code.
Each tested with FOR/AGAINST evidence, self-review, and external references.

---

## ✅ Definitely In

| # | Feature | Confidence | One-liner | Key evidence | Reference |
|---|---------|-----------|-----------|-------------|-----------|
| -1 | **Agent Modes** | -- | Audience needs to understand Claude Code vs Subagents vs Agent Teams before patterns make sense | Most patterns in this deck use subagents; audience needs to know what's available today vs experimental | [agent_modes.md](agent_modes.md) |
| 0 | **METR: AI Can Slow You Down** | -- | METR RCT: experienced devs 19% slower with AI, while believing 20% faster | 39-point perception gap; followup study (57 devs) still no speedup; sets the stage -- we're not cheerleading | [metr.md](metr.md) |
| 1 | **It's All Meta-Programming** | 9/10 | Your job shifts from writing code to designing agent workflows | 9-agent workflow designed in natural language before any code; evolved to 12-agent 5-phase pipeline; "dude have an agent do the work don't do it yourself" | [evidence_meta1.md](evidence/evidence_meta1.md) |

---

## 🤔 Maybe -- Need to Decide

| # | Feature | Confidence | One-liner | Key evidence | Biggest caveat | Reference |
|---|---------|-----------|-----------|-------------|---------------|-----------|
| 2 | **Frozen Specs Prevent Drift** | 7/10 | Git-tagged immutable specs as single source of truth for parallel agents | 16 stories frozen, 4 agents audited ~30 files, only 3 minor fixes needed | Prevents spec-to-spec drift but NOT spec-to-code drift (5/6 modules violated SKILL.md) | [evidence_arch1.md](evidence/evidence_arch1.md) |
| 3 | **Build -> Test -> Audit -> Select** | 7/10 | Parallel builders, sequential test gate, parallel auditors, then select the best | Used 7+ times; cross-auditors caught 19 real issues across 3 build tracks | Human still intervened constantly; rate limits killed all 3 builders once | [evidence_arch3.md](evidence/evidence_arch3.md) |
| 4 | **Selenium QA as Parallel Gate** | 7/10 | E2E tests as binary pass/fail gate on every agent's output | Caught avatar mismatch, stale refs, React state bug after multi-agent refactoring | Most critical bugs were caught by pytest/manual, not Selenium; Chromedriver crash never resolved | [evidence_qa1.md](evidence/evidence_qa1.md) |
| 5 | **Dedup Poisons Tests** | 7/10 | Caching failed API responses creates a hidden test-poisoning trap | 9 debugging steps before finding cached failure; hit the same trap twice; blocked flagship feature | More of a gotcha than a pattern; could fold into "failure modes" slide | [evidence_qa2.md](evidence/evidence_qa2.md) |
| 6 | **Three-Agent Fact-Checking** | 7/10 | Researcher -> Auditor -> Summarizer catches errors before sharing | Auditor found 4/27 claims had errors (15% error rate caught) | Only used twice; 3x latency cost; errors were citation-level not substantive | [evidence_agent1.md](evidence/evidence_agent1.md) |

---

## ❌ Out -- Not Strong Enough

| # | Feature | Confidence | One-liner | Why it's out |
|---|---------|-----------|-----------|-------------|
| 7 | **Quorum Rule for Frozen Docs** | 5/10 | Require 3+ agent agreement before modifying frozen docs | Never triggered. No agent ever proposed a change. Can't tell if it deterred anything or just wasn't needed |
| 8 | **Shared Mutable State** | 4/10 | Agents sharing Docker/DB/browser state causes clobbering | Overstated -- only affected Chrome and DB mutations; vast majority of parallel work was read-only and fine |
| 9 | **Dual Hard-Gate Layers** | 3.5/10 | Hard gates in both scoring and optimizer was redundant | Actually the architecture was defensible (defense in depth). Real problem was implementation bugs, not the design |

---

## Cross-Cutting Patterns

These recur across multiple findings and may deserve their own slide:

| Pattern | Where it appeared | Confidence |
|---------|------------------|------------|
| Delegate, don't do | meta-1, arch-3, agent-1 | High |
| Freeze inputs, version them | arch-1, agent-3 | High |
| Cross-audit > self-review | arch-3, agent-1, qa-3 | High |
| Structured output for delegation | qa-1 | High |
| Isolate agent contexts | arch-1, agent-2 | Medium |
| Serial for mutations, parallel for reads | agent-2, arch-3 | Medium |
| Same-model auditors may be lenient | agent-1, agent-3, qa-3 | Noted |

---

## What Failed or Was Overrated

Worth including as an honesty slide:

- **Full autonomy doesn't work**: Human intervention needed constantly for quality ("THERE IS NO WAY THEY DID A GREAT JOB"), direction, and resource management (rate limits)
- **Specs alone don't enforce themselves**: 5/6 modules violated the frozen spec -- need active audit agents or CI checks
- **Quorum rule**: Untested safety net that never activated
- **Shared-state problems**: Real but narrow (only mutations, not the common case)
