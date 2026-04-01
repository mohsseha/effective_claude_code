# Evidence Report: arch-1

## Hypothesis
Using frozen source-of-truth spec documents (SKILL.md, end-to-end stories, CRITICAL_DEMO) as the single canonical reference that both build agents and audit agents read from -- rather than letting code be the source of truth -- prevented specification drift during multi-agent parallel builds.

## Type: GOOD-IDEA

## Evidence FOR (supports the hypothesis)

- **[line ~10852]** Stories were explicitly frozen and git-tagged before any build work began: `git tag -a e2e-stories-v1 -m "End-to-end stories v1: 16 stories, data reports, optimizer formulation"`. This created an immutable reference point that could not be silently changed by build agents.

- **[line ~10870]** The user established a strict protocol: "4 spec-update agents (running now) -- update specs from stories. 4 cross-audit agents -- each audits another's spec updates (stories are frozen, specs-only edits). Contradiction report -- if any story needs changing, 3+ agents must agree, goes into a report for you." Stories could not be modified unilaterally.

- **[line ~11039]** The system enforced the frozen stories rule in practice: "All 4 spec-update agents done. Now launching cross-audit -- each agent audits another's spec changes (stories are frozen, only specs can be edited). Any story contradictions need 3+ agent agreement."

- **[line ~11386]** The frozen-then-audit process produced verified consistency: "All 4 agents independently confirm: the specification is consistent and ready to build from." Only 3 minor field-name fixes were needed across 16 stories and ~30 spec files -- a remarkably low error rate for a multi-agent parallel effort.

- **[line ~12103-12112]** The user explicitly corrected the assistant when the demo agent risked contamination from code: "yu are doing it wrong I thihnk the demo agent only see the input sorties and it does not get polluted by any fucksups that happening in the code generation." The assistant acknowledged: "the Demo Agent sits on a completely separate track -- it only reads the frozen source-of-truth (stories, specs, seed data, API contracts). It never touches `src/`. The two tracks only converge at Phase 3."

- **[line ~12238]** The two-track architecture was actively maintained: "The demo agent reads **only** from the frozen source of truth -- zero contamination from `src/`."

- **[line ~14158]** The pattern was preserved as a key architectural decision in summaries: "Demo narratives: Pure API call sequences derived from frozen source-of-truth (stories + specs), never from code. Independent track that converges at Phase 3 testing."

- **[line ~13994]** Directory organization reflected the frozen-vs-process distinction: "What stays in `end2end-stories/`: The 16 stories, 4 data reports, math formulation, and workflow diagram. These are the frozen inputs to the system." Process artifacts were explicitly separated from source-of-truth artifacts.

- **[line ~4491]** SKILL.md was defined as the single source of truth in CLAUDE.md, and this was enforced: "Every skill has a `SKILL.md` that is its **single source of truth** (`src/<module>/skills/<skill-name>/SKILL.md`). Python reads metadata from it at registration -- never hardcode name, description, or instructions."

- **[line ~4478]** The SKILL.md pattern was validated as working correctly where it was followed: "Every single data lake interaction from the angels goes through `invoke_skill('data-lake', ...)`. They never import `lake_client` directly. This is the **correct architecture per spec**."

- **[line ~1336]** The user's process rules explicitly linked specs to drift prevention: "Specs must stay consistent with code. If a fix forces a spec change, VoCA and Wisdom verify it doesn't drift from intent."

- **[line ~9270]** The assistant explicitly identified the drift risk and asked the user about it: "The live code has drift from the specs (that's what the gap report showed). If we want stories that test what's *actually* implemented, the agent should read code. If we want stories that test what *should* be implemented, specs are the source." The user chose specs as the authoritative source.

- **[line ~11430]** The frozen specs enabled safe parallelism: "The stories exposed three components that need substantial work to match the spec. These are independent enough to build in parallel" -- because all agents shared the same immutable reference, they could work independently without coordination.

## Evidence AGAINST (contradicts the hypothesis)

- **[line ~4506-4508]** The SKILL.md standard was violated by 5 of 6 modules despite being a "permanent, checked-in instruction": "The VPE **bypasses it entirely** and imports `lake_client` directly. That violates your SKILL.md standard." The frozen spec did not prevent drift in implementation -- agents simply ignored the specification during the v0.5 build.

- **[line ~4550]** The violation was systemic, not isolated: "VoCA ran a grep and found it's not just VPE -- **6 modules bypass the skill layer**." Only the angels followed the SKILL.md pattern. The pipeline, API, gateway, optimizer, and audit all used direct imports. Having a frozen spec document did not automatically prevent code from deviating.

- **[line ~5106]** VoCA's 72-requirement checklist -- derived from the frozen specs -- failed to catch the architectural violation: "User was furious that VoCA's 72 requirements didn't catch that VPE and 5 other modules bypass the invoke_skill() pattern. VoCA owned the failure."

- **[line ~1967]** The most damaging bug in the system was a data contract mismatch that the frozen specs did not prevent: "The core problem is a data contract mismatch between the seed script and the scoring code." The seed data used different schemas from what the scoring code expected, and no frozen spec document caught this during the build phase -- it was only found during runtime QA.

- **[line ~6571]** Despite the elaborate frozen-spec process, the demo runnability was rated 3/10: "Demo runnability is low (3/10) -- three critical gaps prevent the demo from running as written: 1. Live scoring produces wrong outcomes." The frozen specs described the desired behavior but did not prevent the code from producing wrong results.

- **[line ~7130-7132]** Even after a detailed spec and plan were written for LLM tool-use in angels, the implementation was never wired up: "None of it is called. The angel entry points still use heuristic scoring functions that do direct `client.py` reads with hardcoded partition paths." The frozen spec existed but the chain was "broken at the first link."

- **[line ~1064]** Documentation artifacts themselves drifted from code despite being meant as canonical: "BOOTSTRAP.md duplicates knowledge. The bootstrap procedure is essentially what `run/up` + `seed_demo_data.py` + `seed_employee_profiles.py` do. Having a separate markdown file that manually documents the same sequence is a maintenance liability -- when scripts change, the doc drifts."

- **[line ~1058]** Parallel implementations drifted even within operational scripts: "`run/up` and `scripts/start.sh` are redundant. Both start Docker, wait for health, and print status. They differ in minor ways... they just diverge."

## Nuances & Caveats

- The frozen spec pattern worked best as a **coordination mechanism between agents** (preventing them from stepping on each other) rather than as a **correctness guarantee** (preventing code from deviating from spec). Stories and specs were immutable references that enabled safe parallelism, but agents could still produce code that violated the specs. Recent research on "context drift" in parallel AI agents confirms this distinction: shared specs solve the coordination problem but not the conformance problem (Lumenalta, 2026).

- The pattern was most effective during the **story-writing and spec-update phases** (lines ~9300-11400), where 4 specialist agents independently wrote stories, then 4 other agents cross-audited, and all confirmed "build-ready." It was less effective during the **code build phases**, where agents had freedom to implement and often took shortcuts.

- The user's anger about SKILL.md violations (~line 4484, 4538) suggests they expected frozen specs to be self-enforcing. In practice, the specs needed active enforcement through audit agents -- they did not prevent drift passively. This matches the emerging consensus in Spec-Driven Development (SDD): specs must be paired with automated validation in CI/CD to actually prevent drift (Kinde, 2025; GitHub Spec Kit, 2025).

- The two-track architecture (build vs. demo) was a genuine innovation: keeping the demo agent isolated from code meant demo narratives could not be contaminated by implementation bugs. This is the strongest validation of the frozen-spec pattern. It functions as what the agent drift literature calls "scoped, role-specific context" -- each agent sees only the information relevant to its role, preventing cross-contamination.

- The "3+ agent agreement to change a story" rule was never actually triggered -- no stories needed changing. This is an untested safety mechanism, not evidence for or against the pattern.

- The cross-audit pattern (each agent audits another's work, never their own) was consistently applied and produced clean results, but the audits focused on **spec-to-spec consistency**, not **spec-to-code conformance**. The latter is where most drift actually occurred.

- The frozen specs also functioned as what Chen et al. (2026) call **adaptive behavioral anchoring** -- a mechanism that re-grounds agents to original intent when their outputs begin drifting. The git-tagged stories served this role: any agent could be pointed back to the frozen reference to resolve ambiguity. This anchoring role is distinct from (and more valuable than) simple documentation.

## Self-Review Notes (added after re-reading)

- The original report's hypothesis says frozen specs "prevented specification drift." This is an overstatement that the body already corrects. More precisely: frozen specs **prevented spec-to-spec drift and enabled safe parallelism** but **did not prevent spec-to-code drift**. The hypothesis should be read with this qualification.

- The AGAINST evidence is strong but needs context: the SKILL.md violations happened during the v0.5 build phase, which predated the frozen-story/cross-audit process (introduced at ~line 9270). The frozen-spec pattern was a learned response to earlier drift failures, not the cause of them. The report could have made this timeline distinction clearer.

- The report does not overstate the two-track architecture finding. External research (SoA framework, Lumenalta tactics) independently validates that isolating agent contexts prevents contamination -- this is now a recognized best practice, not a novel claim.

## CONFIDENCE SCORE: 7/10

Score unchanged after external research. The literature strongly validates the core finding (frozen specs work for coordination, fail for conformance without enforcement). No contradicting evidence was found -- if anything, the SDD movement validates this exact pattern. The score stays at 7 rather than moving higher because the spec-to-code drift failure remains a significant caveat that limits how strongly we can endorse the pattern in isolation.

## Verdict

The frozen source-of-truth pattern was a genuinely effective coordination mechanism for multi-agent parallel work, particularly during specification authoring and cross-verification phases. It enabled 4+ agents to work independently on interrelated specs and produce a verified-consistent result with minimal conflicts. However, the pattern had a clear limitation: it prevented specification-to-specification drift but did not prevent specification-to-code drift. Agents could (and did) produce code that violated the frozen specs, and the violations were only caught through runtime QA or manual user review, not through the spec documents themselves. The pattern is a good idea that needs to be paired with active enforcement (automated conformance checks or code-level audit agents) to fully deliver on its promise.

This finding aligns with the emerging Spec-Driven Development (SDD) methodology, which treats specifications as the source of truth but explicitly requires automated validation tooling to close the spec-to-code gap. The pattern also maps to the "adaptive behavioral anchoring" mitigation strategy identified in agent drift research. The project's experience is not an outlier -- it reflects a general principle that is now being codified as industry best practice.

## External References

- **[Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems](https://arxiv.org/abs/2601.04170)** -- Defines three types of drift (semantic, coordination, behavioral) in multi-agent LLM systems and proposes mitigation strategies including "adaptive behavioral anchoring," which is exactly what frozen specs provide.

- **[Why Your Multi-Agent System Might Be Slowly Breaking Down](https://co-r-e.com/method/agent-drift-multi-agent)** -- Accessible summary of the agent drift problem; identifies context window pollution and autoregressive error compounding as root causes, both of which frozen specs help mitigate by providing a stable external reference.

- **[Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants (arXiv)](https://arxiv.org/abs/2602.00180)** -- Academic paper formalizing Spec-Driven Development with three rigor levels (spec-first, spec-anchored, spec-as-source). Directly validates the "spec as source of truth" pattern used in this project.

- **[Spec-Driven Development with AI: GitHub Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)** -- GitHub's open-source toolkit for spec-driven AI development. Key quote: "We're moving from 'code is the source of truth' to 'intent is the source of truth.'" Validates the pattern but emphasizes specs must be living documents with iterative review checkpoints.

- **[8 Tactics to Reduce Context Drift with Parallel AI Agents](https://lumenalta.com/insights/8-tactics-to-reduce-context-drift-with-parallel-ai-agents)** -- Practical guide identifying "central shared task spec" as Tactic #1 for preventing drift in parallel agent workflows. Also validates scoped context isolation (the two-track architecture used in this project).

- **[Spec Drift: The Hidden Problem AI Can Help Fix (Kinde)](https://www.kinde.com/learn/ai-for-software-engineering/ai-devops/spec-drift-the-hidden-problem-ai-can-help-fix/)** -- Defines spec drift as "code behavior diverging from documentation" and proposes AI-powered continuous detection in CI/CD pipelines. Directly supports the report's conclusion that frozen specs need active enforcement to prevent spec-to-code drift.

- **[Multi-Agent Collaboration Mechanisms: A Survey of LLMs](https://arxiv.org/abs/2501.06322)** -- Comprehensive survey of collaboration mechanisms in multi-agent LLM systems, covering coordination protocols and shared context patterns relevant to the frozen-spec approach.
