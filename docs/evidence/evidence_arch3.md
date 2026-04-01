# Evidence Report: arch-3

## Hypothesis
The multi-agent workflow pattern of "builder agents in parallel -> sequential test agent -> auditor agents in parallel -> selector agent" was an effective architecture for exploring design alternatives without the orchestrating human becoming a bottleneck.

## Type: GOOD-IDEA

## Evidence FOR

### 1. The pattern was used repeatedly and scaled to increasing complexity
The pattern appeared in at least 7 distinct instances across the project, each time with more sophistication:

- **Instance 1 (lines 77-84):** Two independent research agents (Agent A, Agent B) investigated system setup, cross-audited each other, debated solutions, and produced a table report. The human simply kicked them off and collected the result.

- **Instance 2 (lines 1300-1511):** The 9-agent QA workflow (Lead, Sidekick, Startup, QA Primary, QA Secondary, Fixer, VoCA, Wisdom, UI Research). QA agents ran Selenium tests in parallel while fixers patched bugs. VoCA produced 72 requirements, QA agents found real bugs (Riley "Needs Review" instead of "Denied"), and the pipeline iterated to resolution.

- **Instance 3 (lines 3730-3746):** Three parallel icon research agents (VoCA, Wisdom, UI Researcher) each analyzed the Phosphor Icons migration from different angles. The orchestrator synthesized their conflicting recommendations (VoCA said "ready to go," Wisdom said "defer to post-demo," UI Researcher said "2-3 hours") into a clear comparison table for the human.

- **Instance 4 (lines 6520-6671):** Four auditor agents ran in parallel (PRD vs Spec, Spec vs Code, Code vs UI, Demo Narrative), producing separate audit reports. A synthesis agent then combined findings into a gap report and fix prompt.

- **Instance 5 (lines 8016-8036):** Three topic builder agents in parallel (Wire the AI, Build Schedule, Polish Demo) each working in isolated git worktrees, followed by cross-audits where builder agents verified each other's work (A audits C, B audits A, C audits B).

- **Instance 6 (lines 12205-12237):** Phase 2' cross-audits plus a Demo Agent, all 4 running in parallel. Cross-audits caught real issues: "C audits B" found VPE concerns, "B audits A" found optimizer issues. 19 issues were triaged across 3 agents.

- **Instance 7 (lines 22206-22363):** The fully articulated pattern for the alternative demo video: 3 explorers in parallel -> sequential test agent -> 3 explorers revise -> sequential test agent -> 3 auditors in parallel -> selector agent -> video agent. This represents the mature form of the pattern.

### 2. Parallel agents found real bugs that sequential work would have missed
- QA-Worker and QA-Admin running simultaneously discovered different categories of bugs: QA-Worker found Riley's scoring issue, QA-Admin found Chrome session crashes, avatar 404s, and search filter bugs (lines 1578-1584).
- E2E test agents for 4 demo narratives found a P0 bug: justice angel not filtering coverage by shift_id (line 3407-3411).
- Cross-auditors caught spec contradictions that the original builder agents missed (line 6204-6218, factor scoring methods mismatch).
- The "Common Sense" auditor delivered the most devastating finding: "The founder described an AI system. What was built is a rules engine wearing an AI costume" (line 7112).

### 3. The human's bottleneck role was substantially reduced
Throughout the transcript, the human shifted toward high-level decisions while agents worked in parallel. Examples:
- While QA agents ran tests, the lead agent simultaneously fixed avatar images (lines 1517-1538).
- While 3 builder agents worked in worktrees, the human gave brief directional feedback (lines 8016-8036).
- The human repeatedly demanded delegation: "rememeber to use your side-kick agents to do one off work!" (line 2320), "dude have an agent do the work don't do it yourself" (line 22009), "all work needs to be done by agents" (line 18770).

### 4. The auditor step caught errors that builders missed
- Cross-audits (Phase 2') found 19 issues across 3 parallel build tracks, all of which were triaged and categorized by severity (line 13100).
- Admin bypass design change was discovered through auditing: demo narratives incorrectly routed schedule_requirement through the pipeline when it should have been direct CRUD (lines 12800-12816).
- Spec contradiction reports identified factor scoring method mismatches, recommendation type mismatches, and dead code (lines 6207-6218).

## Evidence AGAINST

### 1. The human frequently had to intervene, override, and re-launch
- The user rejected the MBA consultant agent entirely: "no the MBA is wrong stop him kill him" (line 6880). The orchestrator had to discard that agent's output.
- The user had to re-launch all 3 topic agents because the orchestrator gave them overly specific instructions: "no stupid you are being too specific give them the freedom" (line 8001). The entire first round of 3 parallel builder agents was wasted.
- The user demanded deeper audits: "THERE IS NO WAY THEY DID A GREAT JOB" (line 7825), requiring v2 and v3 audit rounds.
- Rate limits killed all 3 builder agents in one round, producing zero code (line 7784).

### 2. The sequential test step was a genuine bottleneck
- The Test Agent had to run each explorer's e2e test sequentially "A -> B -> C" to avoid clobbering shared state (line 22257-22261). This means the parallelism gained in the explore phase was partially negated by the serial test phase.
- E2E testing was slow because agents used manual curl-by-curl testing initially: "manual curl testing is slow" (line 13413). The approach was changed mid-stream to pytest scripts.
- Selenium agents occasionally crashed Chrome sessions, invalidating all subsequent tests in the batch (line 2118: "invalid session id -- the Chrome session died after test 05, killing all remaining tests").

### 3. Coordination overhead was significant
- The Lead Agent pattern required constant status tables, polling for agent completion via sleep loops, and manual checking of output files (lines 1513-1514, 1543-1544, 1566).
- Agent output files had to be read and interpreted manually by the orchestrating agent. There was no structured inter-agent communication protocol.
- The user had to repeatedly ask "are you stuck?" (line 2323) and "where are we in the steps?" (line 13105), suggesting the workflow's state was opaque.

### 4. Not all parallel agents produced useful work
- UI Research Agent was explicitly "lower priority" and "not a blocker" (lines 1394-1397). Its contribution to the project was minimal relative to computation spent.
- The Sidekick Agent role was defined but barely used; the Lead Agent frequently did work directly instead of delegating (line 1922: "point taken about delegation!").
- Some agents completed much faster than others, leaving expensive compute idle while waiting for synchronization points.

### 5. The pattern degraded under resource constraints
- Docker Hub timeouts repeatedly disrupted the workflow (lines 1450, 9206).
- Context window exhaustion forced mid-workflow summaries and continuations (lines 1652-1658, multiple session handoffs).
- The user hit rate limits at critical moments, stalling the entire pipeline (line 7784).

## Nuances & Caveats

### The pattern evolved significantly over time
Early uses (Agent A/B research) were simple 2-agent parallel with manual synthesis. By the end (alt demo workflow, line 22206), the pattern had matured into a 5-phase pipeline with 3 explorers, sequential testing, revision loops, 3 auditors with distinct lenses, a selector, and a video production agent. This evolution itself is evidence that the pattern was productive enough to invest in refining.

### The human's role shifted from bottleneck to director
The user explicitly moved from doing work to supervising: "all work needs to be done by agents" and "you will only supervise" (line 18770). This is the intended outcome of the pattern. However, the user still had to make critical judgment calls (killing the MBA, redirecting spec locations, demanding deeper audits), which means the pattern reduced but did not eliminate the human bottleneck.

### The cross-audit variant appeared to be the most valuable innovation
Having builder agents audit each other's work (A audits C, B audits A, C audits B) appeared more effective than having separate auditor agents in this project, likely because the builders already had deep context. This was introduced around line 11617 and consistently produced actionable findings. Note: this is a single-project observation, not a controlled comparison.

### The pattern worked better for exploratory/creative tasks than for implementation
The 3-explorer approach for demo scripts (each exploring a different angle: soft denial, VPE debate, weight slider) was well-suited to creative divergence. The 3-builder approach for code (Wire AI, Schedule View, Polish Demo) was more fragile because code changes can conflict, requiring isolated worktrees and careful merge coordination.

### Shared state was the primary structural constraint
The sequential test requirement exists because multiple agents cannot safely modify the same database, Docker containers, or browser simultaneously. This is a fundamental limitation that the pattern worked around rather than solved.

## External References

- **[Mixture-of-Agents Enhances Large Language Model Capabilities (Wang et al., 2024)](https://arxiv.org/abs/2406.04692)** -- Foundational paper showing that layered multi-LLM ensembles outperform single models; the parallel-then-aggregate structure directly parallels the explore-then-select pattern used here.

- **[ChatDev: Communicative Agents for Software Development (Qian et al., 2023)](https://arxiv.org/abs/2307.07924)** -- Assigns role-playing agents (CEO, CTO, Programmer, Tester) to phases of the SDLC; demonstrates that agent specialization with structured handoffs can produce working software, though with a sequential rather than parallel pipeline.

- **[MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework (Hong et al., 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/6507b115562bb0a305f1958ccc87355a-Paper-Conference.pdf)** -- Uses SOPs and document-based inter-agent communication to coordinate specialized agents; validates that structured protocols reduce the coordination overhead observed in our ad-hoc file-based approach.

- **[AgentMesh: A Cooperative Multi-Agent Generative AI Framework for Software Development Automation (Khanzadeh, 2025)](https://arxiv.org/abs/2507.19902)** -- Planner/Coder/Debugger/Reviewer pipeline; explicitly discusses error propagation and context scaling as key limitations, corroborating our "evidence against" findings.

- **[Multi-Agent Software Development through Cross-Team Collaboration (2024)](https://arxiv.org/abs/2406.08979)** -- Studies cross-team orchestration where agent teams review each other's outputs; aligns with our finding that cross-audit (builder A audits builder C) was particularly effective.

- **[Multi-agent workflows often fail. Here's how to engineer ones that don't. (GitHub Blog, 2025)](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/)** -- Identifies missing structure (not model capability) as the primary failure mode; recommends typed schemas and action schemas, directly relevant to our coordination overhead findings.

- **[AI Agent Orchestration Patterns (Microsoft Azure Architecture Center)](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)** -- Catalogs orchestrator-worker, sequential, and parallel branching/joining patterns as formal design patterns; provides the taxonomic context for our fork-join-audit-select pattern.

- **[OpenAI Codex: Parallel Agent Tasks for Software Development (OpenAI, 2025-2026)](https://openai.com/index/introducing-codex/)** -- Production system where multiple coding agents work in parallel on isolated cloud environments; validates the isolated-worktree approach used in our Instance 5.

- **[Verdent: Multi-Agent SWE-bench System (2025)](https://www.verdent.ai/blog/swe-bench-verified-technical-report)** -- State-of-the-art coding agent system with explicit code-review subagent as a quality gate; demonstrates that the audit/verification stage is becoming standard in production multi-agent coding systems.

- **[A Practical Guide for Designing, Developing, and Deploying Production-Grade Agentic AI Workflows (2025)](https://arxiv.org/html/2512.08769v1)** -- Covers workflow decomposition and multi-agent design patterns with an engineering lifecycle lens; provides academic grounding for the pattern evolution observed in our project.

- **[AI Coding Agents in 2026: Coherence Through Orchestration, Not Autonomy (Mike Mason)](https://mikemason.ca/writing/ai-coding-agents-jan-2026/)** -- Argues that orchestration quality matters more than individual agent capability; consistent with our finding that the pattern's value came primarily from the coordination structure rather than from any single agent's output.

## CONFIDENCE SCORE: 7/10

The evidence strongly supports that the pattern was effective at reducing the human bottleneck and producing higher-quality outputs through parallel exploration and cross-auditing. However, it was not without significant overhead (coordination, failed launches, human intervention needed for course corrections) and had genuine structural weaknesses (sequential test bottleneck, shared state conflicts, resource constraints). The pattern was clearly a net positive, but calling it frictionless would be inaccurate.

## Verdict

**GOOD-IDEA, CONFIRMED WITH CAVEATS.** The multi-agent parallel-build/sequential-test/parallel-audit/select pattern demonstrably enabled the human to operate at a higher level of abstraction, produced better outputs through diverse exploration, and caught real bugs through cross-auditing. The pattern improved over time as the team refined it. The main caveats are: (1) the human still had to intervene frequently for quality control and course correction, (2) the sequential test phase was a genuine bottleneck that partially negated parallel gains, (3) coordination overhead was non-trivial, and (4) the pattern was fragile under resource constraints (rate limits, Docker timeouts, context window exhaustion). The pattern's greatest strength was in the audit/cross-verification phase, where parallel agents with different lenses consistently surfaced issues that a single-pass approach would likely have overlooked. External literature (ChatDev, MetaGPT, AgentMesh, Verdent) corroborates both the promise and the pitfalls observed here: structured multi-agent pipelines with verification stages are becoming a recognized pattern, but coordination overhead and shared-state conflicts remain open problems across the field.
