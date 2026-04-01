# METR Studies on AI Coding Assistant Productivity

Reference material for presentations on AI augmentation effectiveness.

---

## Study 1: The Original RCT (July 2025)

**Title:** "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"

**Authors:** Joel Becker, Nate Rush, Elizabeth Barnes, David Rein (METR)

**Published:** July 10, 2025 (blog post); July 12, 2025 (arXiv preprint, revised July 25, 2025)

**arXiv:** [2507.09089](https://arxiv.org/abs/2507.09089)

**Blog post:** https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/

**Code/data:** https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs

### Methodology

- **Design:** Randomized controlled trial (RCT). Each task randomly assigned to AI-allowed or AI-disallowed condition.
- **Participants:** 16 experienced open-source developers, averaging 5 years of prior experience and ~1,500 commits on their respective projects.
- **Repositories:** Large, mature open-source repos averaging 22,000+ GitHub stars and 1M+ lines of code.
- **Tasks:** 246 real issues (bug fixes, features, refactors) sourced from the developers themselves, averaging ~2 hours each.
- **Tools used:** Primarily Cursor Pro with Claude 3.5/3.7 Sonnet (frontier models at the time).
- **Data collection:** Screen recordings and self-reported implementation times.
- **Compensation:** $150/hour.
- **Period:** February -- June 2025.

### Key Quantitative Findings

| Metric | Value |
|--------|-------|
| Actual effect of AI on completion time | **+19% slower** (AI increased task time) |
| 95% confidence interval | +2% to +39% slower |
| Developer pre-study forecast | 24% faster with AI |
| Developer post-study self-assessment | 20% faster with AI |
| Expert predictions | 38--39% faster with AI |
| AI generation acceptance rate | <44% of generations accepted |

The result is statistically significant. With 246 tasks and within-developer comparison (each developer did tasks in both conditions), there was sufficient power to reject the null hypothesis of zero effect.

### The Perception Gap

The single most striking finding: **developers believed AI made them 20% faster even after the study, when it actually made them 19% slower.** This ~39 percentage-point gap between perceived and actual productivity impact suggests developers cannot reliably self-assess AI's effect on their own productivity.

Hypothesized reasons for the perception gap:
- AI-assisted coding requires less cognitive effort, creating an illusion of speed through reduced mental strain.
- Developers can multitask while waiting for AI outputs, making time feel more productive.
- The interactive, conversational nature of AI assistance feels enjoyable and engaging.

### METR's Hypotheses for the Slowdown

METR identified five contributing factors:

1. **Overoptimism and overuse:** Developers had inflated expectations of AI usefulness and used AI even on tasks they could have completed faster alone. AI was not required on AI-allowed tasks, but developers chose to use it heavily.

2. **Low generation quality / acceptance rates:** Less than 44% of AI generations were accepted. Developers spent significant time reviewing, testing, and modifying code only to reject it. The review-reject cycle consumed time without producing output.

3. **Poor codebase integration:** AI struggled to match existing code style, conventions, and architectural patterns in large mature codebases. Outputs required substantial rewriting.

4. **Verification and context-switching overhead:** Interpreting, correcting, and adapting AI-generated code imposed friction. Developers lost flow state by switching between writing code and reviewing AI suggestions.

5. **Deep expertise negated AI's advantage:** AI was least effective when developers already had high prior exposure to the codebase and did not need external resources like documentation. For developers who already know the codebase deeply, AI adds overhead without commensurate benefit.

### METR's Three Reconciliation Frameworks

METR offered three ways to reconcile their negative findings with positive results from benchmarks and industry anecdotes:

1. **The study underestimates AI's capabilities** -- e.g., specific population (very experienced devs on very large codebases) may not generalize.
2. **Benchmarks and anecdotes overestimate capabilities** -- lab settings and self-reports are unreliable measures of real-world productivity.
3. **Both measure complementary but distinct task subsets** -- AI may help on certain task types but not others.

---

## Study 2: The Late-2025 Follow-Up and Design Change (February 2026)

**Title:** "We are Changing our Developer Productivity Experiment Design"

**Published:** February 24, 2026

**URL:** https://metr.org/blog/2026-02-24-uplift-update/

### What They Did

Starting August 2025, METR ran a larger follow-up experiment:
- **57 developers** (10 from original study + 47 newly recruited)
- **143 repositories** (including smaller, more greenfield, less mature repos than the original study)
- **800+ tasks**
- **$50/hour** compensation (down from $150/hour)
- Same task-level randomization design as the original

### Quantitative Results (Unreliable per METR)

| Subgroup | Estimated AI Speedup | 95% CI |
|----------|---------------------|--------|
| Original 10 developers | **-18%** (i.e., 18% slower) | -38% to +9% |
| Newly recruited developers | **-4%** (i.e., 4% slower) | -15% to +9% |

Neither result is statistically significant (CIs cross zero). The overall sample-wide estimate was approximately 6% speedup, but METR explicitly states they consider this data unreliable.

### Why METR Considers the Data Unreliable

METR identified severe methodological problems that biased their results:

1. **Selection/attrition bias (the critical issue):** Throughout 2025, adoption of agentic tools (Claude Code, Codex) surged. An increasing share of developers refused to participate because they did not want to work without AI, even at $50/hour. This systematically excluded developers most likely to benefit from AI, biasing the remaining sample toward developers who get less value from AI.

2. **Task selection bias:** **30--50% of developers** reported deliberately avoiding submitting tasks they believed AI could accelerate, because they didn't want those tasks randomly assigned to the no-AI condition. This means the task pool was depleted of exactly the tasks where AI would show the largest benefit.

3. **Quality confounds:** Developers produced different quality outputs between conditions -- e.g., more documentation, more tests, or subjectively better code when using AI. Time-to-completion alone missed these quality differences.

4. **Time-tracking problems with agentic tools:** Developers multitasked while agents ran (browsing, other work), making wall-clock time an unreliable measure of effort.

5. **Task-type shifts:** Developers chose fundamentally different types of tasks when they knew AI would be available.

6. **Incomplete compliance:** Some developers did not complete AI-disallowed assignments.

### Heterogeneity Analysis (LessWrong independent analysis)

An independent analysis of the late-2025 data found significant variation:
- Tasks developers predicted would benefit from AI: **~12% speedup**
- The developer with highest estimated speedup: **~25% speedup**
- After heuristic adjustment for selection bias (assuming 50% of high-uplift tasks were withheld): possibly **~20% speedup** overall, though this is speculative.

Source: https://www.lesswrong.com/posts/dFmQThALG8EdZFqgL/assessing-heterogeneity-in-metr-s-late-2025-developer

### METR's New Direction

METR is abandoning the task-level randomized design in favor of:
- Shorter, more intensive experiments with higher pay
- Observational data (GitHub commits, tool usage transcripts)
- Questionnaire and time-use studies
- Fixed-task experiments (all developers do the same task, randomized into AI/no-AI)
- Developer-level randomization instead of task-level

---

## Notable Reactions and Rebuttals

### Positive Reception

- **Sean Goedecke** called it "the best study on AI-in-engineering" he had seen, praising the use of real-world tasks, current tools, and experienced developers. He found the perception gap the most important finding. His additional hypothesis: "pure software" projects (compilers, libraries) have higher quality standards, making AI-generated code less acceptable. ([Blog post](https://www.seangoedecke.com/impact-of-ai-study/))

- **DX (formerly Getdx)** provided detailed analysis noting the study's methodological rigor and arguing the findings highlight "task-model fit" rather than blanket AI ineffectiveness. ([Analysis](https://getdx.com/blog/unpacking-metri-findings-does-ai-slow-developers-down/))

### Firsthand Participant Account

- **Domenic Denicola** (jsdom maintainer, 1M+ LOC codebase) published a detailed account of his participation (9 AI-allowed tasks, 10 without AI, March 15 -- April 20, 2025). Key observations:
  - AI struggled to follow existing codebase conventions despite abundant examples
  - Models relied on outdated training data rather than reading current specifications (e.g., fabricating a fictional constant `CSSRule.LAYER_STATEMENT_RULE`)
  - Agents got stuck in loops on basic operations (linter fixes, file sorting, directory traversal)
  - AI made repetitive tasks more engaging but did not make them faster
  - His recommendation: run multiple AI agents in parallel on separate subtasks rather than pair-programming with one agent sequentially
  - Source: https://domenic.me/metr-ai-productivity/

### Common Criticisms and Counterarguments

| Criticism | Counterargument |
|-----------|----------------|
| "The developers just weren't good at using AI" | Participants chose their own tools and workflows; they were not forced into specific tooling. The issue is task-model fit, not developer aptitude. |
| "The sample size (N=16) is too small" | 246 tasks with within-subject design provided sufficient statistical power. The late-2025 study scaled to 57 developers and 800+ tasks with similar directional results. |
| "AI tools have improved since early 2025" | METR's late-2025 study with newer tools still showed no statistically significant speedup. Selection bias makes the newer data hard to interpret, but the improvement is not clearly demonstrated. |
| "The tasks were wrong for AI" | Tasks were real issues selected by the developers themselves as valuable work. However, METR acknowledges these may not represent the full distribution of tasks where AI excels. |
| "This only applies to experienced developers on large codebases" | This is partially valid -- METR's own reconciliation framework acknowledges the specific population may limit generalizability. The late-2025 study included more diverse repos but encountered selection bias. |

### Industry Responses

- **Augment Code** published a guide acknowledging the 19% slowdown and offering prescriptive advice for avoiding the pitfalls identified in the study. ([Guide](https://www.augmentcode.com/guides/why-ai-coding-tools-make-experienced-developers-19-slower-and-how-to-fix-it))
- **Faros AI** argued the study's lab conditions miss how AI is used in real-world workflows with broader organizational context. ([Analysis](https://www.faros.ai/blog/lab-vs-reality-ai-productivity-study-findings))
- **MIT Technology Review** (December 2025) cited the METR study in a broader piece questioning AI coding hype. ([Article](https://www.technologyreview.com/2025/12/15/1128352/rise-of-ai-coding-developers-2026/))

### METR's Own Response to Reception

METR published "Notes on Scientific Communication at METR" (August 11, 2025) reflecting on how to prevent misinterpretation. They deliberately packed "crucial context into the title and subtitle" to reduce overgeneralization, specifying developer experience level, project complexity, and sample size. They stated they prioritize "accuracy, integrity and rigor, even when that means giving up opportunities to have more influence." ([Post](https://metr.org/blog/2025-08-11-science-comms-at-metr/))

---

## Key Takeaways for Presentations

1. **The only RCT on AI coding productivity found a 19% slowdown** for experienced developers on large, mature codebases. This is the highest-quality causal evidence available as of early 2026.

2. **Developers cannot self-assess AI's impact on their productivity.** The 39-percentage-point gap between perceived benefit (+20%) and actual effect (-19%) is the most policy-relevant finding. Surveys and self-reports about AI productivity gains should be treated with extreme skepticism.

3. **The follow-up study could not produce clean data** because developers increasingly refused to work without AI -- itself an interesting finding about perceived vs. actual dependency.

4. **AI's benefit likely varies enormously** by task type, codebase maturity, and developer familiarity. The average effect may be negative even if specific use cases show strong positive effects.

5. **Low acceptance rates (<44%) are a key mechanism.** When most AI-generated code is rejected, the time spent prompting, waiting, reviewing, and rejecting is pure overhead.

---

## Full Source List

- METR blog post (original study): https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- arXiv paper: https://arxiv.org/abs/2507.09089
- GitHub repo with data/code: https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs
- METR follow-up post: https://metr.org/blog/2026-02-24-uplift-update/
- METR science communication post: https://metr.org/blog/2025-08-11-science-comms-at-metr/
- Domenic Denicola participant account: https://domenic.me/metr-ai-productivity/
- Sean Goedecke analysis: https://www.seangoedecke.com/impact-of-ai-study/
- DX analysis: https://getdx.com/blog/unpacking-metri-findings-does-ai-slow-developers-down/
- LessWrong heterogeneity analysis: https://www.lesswrong.com/posts/dFmQThALG8EdZFqgL/assessing-heterogeneity-in-metr-s-late-2025-developer
- Augment Code guide: https://www.augmentcode.com/guides/why-ai-coding-tools-make-experienced-developers-19-slower-and-how-to-fix-it
- Faros AI analysis: https://www.faros.ai/blog/lab-vs-reality-ai-productivity-study-findings
- MIT Technology Review: https://www.technologyreview.com/2025/12/15/1128352/rise-of-ai-coding-developers-2026/
