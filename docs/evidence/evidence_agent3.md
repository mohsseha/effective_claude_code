# Evidence Report: agent-3

## Hypothesis
Requiring cross-agent audit with a quorum rule (at least 3 agents must agree) before modifying frozen source-of-truth documents prevented spec drift and kept the project's canonical artifacts trustworthy across a multi-day, multi-agent build.

## Type: GOOD-IDEA

## Evidence FOR

1. **Explicit quorum rule was established and communicated.** The orchestrator stated the pipeline clearly: "4 cross-audit agents -- each audits another's spec updates (stories are frozen, specs-only edits). Any story contradictions need 3+ agent agreement" (line ~10870). This was reiterated at line ~11039: "stories are frozen, only specs can be edited. Any story contradictions need 3+ agent agreement." The rule was also captured in the session summary at line ~11670: "Stories are frozen once written; only specs can be edited; story changes need 3+ agent agreement."

2. **Cross-audit was systematically executed in the spec-update phase.** Four specialist agents updated specs, then four different agents cross-audited each other's work in a round-robin pattern (Worker audits Admin, Admin audits Ethics, Ethics audits Infra, Infra audits Worker). All four produced clean verdicts with zero story contradictions found (line ~11164-11171). The table showed: 4 auditors, ~37 files reviewed, 1 minor spec fix (stale builder note), 0 story changes needed.

3. **Cross-audit was also executed in the Phase 2 build.** The build used a formal "B audits A, C audits B, A audits C" pattern for the three parallel workstreams (Optimizer, VPE Socratic, LLM Caching). All three cross-audits completed with "MINOR ISSUES" verdicts -- no blocking problems (lines ~12247, ~12285, ~12307). These audits caught real quality issues: 11 warnings on the Optimizer, missing `seed=42` on the angel agent path, and a type mismatch between `list[dict]` vs `list[SwapCandidate]`.

4. **The "frozen source of truth" concept prevented contamination.** The user explicitly corrected the orchestrator when the Demo Agent's track was muddled with the build track: "the demo agent only see the input stories and it does not get polluted by any fuckups that happening in the code generation" (line ~12103). This led to a clean separation where the Demo Agent read "only from the frozen source of truth -- zero contamination from `src/`" (line ~12238). This architectural choice meant demo narratives were "pure API call sequences derived from frozen source-of-truth (stories + specs), never from code" (line ~14158).

5. **Final consistency reviews confirmed build-readiness.** After cross-audits, four final consistency review agents all independently declared the system "build-ready" with zero story changes needed (line ~11376-11390). The Infra agent's only fix was correcting 3 field names in api-spec.md. The verdict: "Zero story changes needed. Zero contradictions requiring multi-agent agreement" (line ~11390).

6. **The pattern was extended to later phases.** The user requested the same researcher-auditor-summarizer pattern for answering technical questions about hard gates (line ~22112). Cross-audit became an ingrained workflow pattern: "have a different audit agent read the report and verify the facts." This was applied at least 3 times for Q&A workflows and caught issues like off-by-one line numbers in reports.

7. **Spec alignment was maintained across ~30 files.** The commit message confirmed: "Update specs to align with 16 end-to-end stories + cross-audit reports" with ~30 spec files touched (line ~11247). Despite this large surface area, no story contradictions were found across four independent auditors.

8. **Stories were tagged and frozen at a known-good point.** The commit was tagged `e2e-stories-v1` before any spec updates began (line ~10849), creating an immutable baseline that all subsequent work referenced.

## Evidence AGAINST

1. **The quorum rule was never actually invoked to block a change.** Across all cross-audits (spec-update phase, build phase, final consistency reviews), the result was always "zero story contradictions found" and "no story changes needed." The 3+ agent agreement threshold was never tested because no agent ever proposed changing a story. The rule functioned as a deterrent/guardrail rather than an active mechanism.

2. **Earlier agents went off the rails despite eventual cross-auditing.** Before the formal pipeline was established, agents wrote specs to wrong directories (`qa_reports/` instead of `spec/v0.5/`), requiring the orchestrator to discard their output entirely (line ~8160: "spec went to `qa_reports/` instead of `spec/v0.5/`. Discarding this one too"). The cross-audit pattern couldn't prevent this because the agents had wrong instructions, not wrong intent.

3. **Cross-audit consistently found only "MINOR ISSUES."** Every single audit in the transcript came back as either "Clean" or "MINOR ISSUES." This raises the question of whether the auditing agents were truly critical reviewers or just rubber-stamping. The Phase 2 audits found cosmetic issues (missing seed parameters, type mismatches) but nothing that would constitute spec drift or source-of-truth corruption.

4. **Hardcoded seed data diverged from live scoring despite audits.** The deep-dive audit at lines ~19400-19416 revealed that seeded angel scores were hand-authored and significantly diverged from what live scoring would produce (e.g., seed `supportive_action=0.72` vs live heuristic yielding `0.30`). This was flagged as "[H1] HARDCODED" but was a design choice, not something the cross-audit process caught or prevented during the spec/story phase.

5. **The process required significant coordination overhead.** The multi-phase workflow involved: 4 story-writing agents, 4 verification agents, 4 spec-update agents, 4 cross-audit agents, 4 final consistency review agents, then 3 build agents, 3 cross-audit agents, plus triage agents. That is roughly 26 agent invocations for the spec/build cycle. Whether this overhead was justified given the "zero contradictions found" result is debatable.

6. **Some audits were forgotten or skipped until the user asked.** The orchestrator admitted: "Agents 2 and 3 were never audited -- they completed, I reported their results, and we moved on" (line ~16912). The user had to explicitly request the audits: "yes to 'So -- want me to launch 2 auditors for Agents 2 and 3?'" This suggests the cross-audit discipline was not self-enforcing.

## Nuances & Caveats

- **The quorum rule was a preventive mechanism, not a corrective one.** Its value may lie in the behavioral constraint it imposed (agents knew stories were frozen and could not modify them) rather than in catching violations after the fact. This parallels BFT literature where conservative quorum thresholds deter unsafe actions even when never invoked -- the threat of needing consensus raises the bar for proposing changes at all.

- **"Frozen" was not absolute.** The user explicitly said stories could change IF 3+ agents agreed. This was a pragmatic escape hatch that preserved the immutability guarantee while allowing for genuine errors. That it was never needed could mean the stories were well-written, or that the bar was high enough to discourage frivolous changes. Both explanations are consistent with the deterrence model.

- **The cross-audit pattern caught real issues in the build phase** (type mismatches, missing determinism parameters, missing test coverage) even if it found nothing in the spec phase. The value distribution was uneven across phases. This matches research showing majority voting and cross-review yield the largest gains on reasoning/code tasks, less so on knowledge/specification tasks.

- **The separation of frozen inputs from mutable code was arguably more impactful than the quorum rule itself.** The user's insistence that the Demo Agent never touch `src/` and only read from frozen specs/stories was the key architectural insight. The quorum rule was a supporting mechanism for this separation. This mirrors the ADR (Architecture Decision Record) pattern in software governance: once accepted, a decision is immutable; changes require a new record with its own review process.

- **The pattern worked because a human orchestrator enforced it.** The user repeatedly corrected the AI orchestrator's workflow (e.g., "you are doing it wrong" about the demo agent track, "dude have an agent do the work don't do it yourself"). Without active human supervision, the cross-audit pipeline might have degraded. The orchestrator skipped audits for Agents 2 and 3 until prompted, demonstrating that quorum discipline requires enforcement infrastructure, not just a stated rule.

- **The hypothesis conflates three distinct mechanisms.** The evidence actually supports a composite of (a) immutable tagging of source documents, (b) cross-agent review, and (c) a quorum threshold for modifications. Each contributed differently. The tagging (git tag `e2e-stories-v1`) created the baseline. Cross-review caught code-level defects. The quorum rule was never exercised. Treating these as one "quorum rule" hypothesis obscures which mechanism did the actual work.

## CONFIDENCE SCORE: 5/10

The score remains unchanged after self-review. The frozen-document discipline and cross-audit pattern are well-supported (7-8/10 individually). The quorum rule specifically is unsupported by direct evidence (2/10) since it was never triggered. The composite score reflects this split. External literature confirms that untested guardrails have deterrence value but cannot be credited with preventing failures that may never have occurred regardless.

## Verdict

The hypothesis is **partially supported but overstated**. It bundles three mechanisms and attributes the outcome to the one that was never tested.

**What worked:** Freezing documents at a git-tagged baseline and running systematic cross-audits kept ~30 spec files and 16 stories internally consistent across a multi-day build with 20+ agent invocations. The cross-audit pattern caught real code-level defects (type mismatches, missing determinism parameters). The frozen-input separation kept the demo track clean. These are genuinely impressive coordination outcomes.

**What remains unproven:** The specific "3-agent quorum" threshold was never triggered. No agent ever proposed modifying a frozen story, so we cannot distinguish between (a) the quorum rule deterred changes, (b) the stories were simply correct, or (c) agents lacked the affordance to propose story changes regardless. The rule may have had deterrence value -- BFT literature supports this -- but we have no counterfactual.

**Bottom line:** The frozen-document-plus-cross-audit discipline was the load-bearing mechanism. The quorum rule was a reasonable but untested safety net. Recommending the composite pattern is justified; claiming the quorum threshold specifically prevented spec drift is not.

## External References

- **[A Byzantine Fault Tolerance Approach towards AI Safety (deVadoss, 2025)](https://arxiv.org/abs/2504.14668)** -- Directly maps BFT quorum mechanisms to AI safety, arguing that requiring consensus among multiple AI modules before acting mirrors the deterrence logic used in this project's quorum rule.

- **[Voting or Consensus? Decision-Making in Multi-Agent Debate (ACL Findings, 2025)](https://arxiv.org/abs/2502.19130)** -- Compares voting vs. consensus protocols for multi-agent LLMs; finds voting improves reasoning tasks by 13.2% and consensus improves knowledge tasks by 2.8%, supporting the observation that cross-audit value was uneven across task types.

- **[Debate or Vote: Which Yields Better Decisions in Multi-Agent LLMs? (2025)](https://arxiv.org/abs/2508.17536)** -- Shows that simple majority voting accounts for most performance gains attributed to multi-agent debate, suggesting the cross-audit structure (not the deliberation depth) was the key contributor in this project.

- **[Reaching Agreement Among Reasoning LLM Agents (Ruan & Wang, 2025)](https://arxiv.org/pdf/2512.20184)** -- Examines how LLM agents revise solutions during consensus, noting that classical quorum intersection properties do not directly transfer because agents actively update beliefs -- relevant to why the static quorum rule was never triggered.

- **[LLM Voting: Human Choices and AI Collective Decision-Making (AAAI AIES, 2024)](https://arxiv.org/html/2402.01766v3)** -- Surveys voting mechanisms for LLM collectives; confirms that aggregated "wisdom of crowds" yields lower error rates than single agents, provided voter diversity and independence -- both present in the round-robin audit pattern used here.

- **[Multi-Agent Collaboration Mechanisms: A Survey of LLMs (2025)](https://arxiv.org/html/2501.06322v1)** -- Comprehensive survey of multi-agent LLM coordination patterns including voting, debate, and structured review; provides taxonomic context for the cross-audit pattern used in this project.

- **[When the Crowd Gets It Wrong -- Limits of Collective Wisdom in ML (Scientific Reports, 2025)](https://www.nature.com/articles/s41598-025-08273-y)** -- Identifies conditions where crowd wisdom fails: correlated agents and shared biases. Relevant because all auditing agents in this project used the same underlying LLM, limiting true independence.

- **[Architecture Decision Records (ADR) -- AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)** -- Documents the immutable-once-accepted pattern for architectural decisions: changes require a new ADR that supersedes the old one. Directly parallels the "frozen stories, new ADR needed for changes" discipline used in this project.

- **[Consensus Algorithms for Coordinating Agreement in Distributed Agent Systems (2025)](https://notes.muthu.co/2025/11/consensus-algorithms-for-coordinating-agreement-in-distributed-agent-systems/)** -- Overview of quorum-based consensus for multi-agent systems; notes that overlapping quorums ensure consistency without a central coordinator, though this project relied on a human coordinator throughout.

- **[Multi-Agent Coordination Strategies (Galileo, 2025)](https://galileo.ai/blog/multi-agent-coordination-strategies)** -- Practical guide to multi-agent coordination patterns including quorum thresholds for high-impact decisions; recommends the pattern used here but notes it requires enforcement infrastructure to be self-sustaining.
