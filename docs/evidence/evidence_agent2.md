# Evidence Report: agent-2

## Hypothesis
Running the orchestrator agent and sub-agents against shared mutable state (live Docker services, databases, filesystem) without isolation caused clobbering, forcing sequential fallbacks that negated the parallelism benefits.

## Type: BAD-IDEA

## Evidence FOR

### 1. Chrome process contention — the clearest clobbering incident
Two parallel QA agents (QA-Worker and QA-Admin) ran Selenium tests simultaneously against the same Chrome browser. Chrome sessions crashed, killing downstream tests. The admin suite went from 3/12 passing, with "invalid session id" errors cascading after test 05. The developer had to manually `pkill -9` Chrome processes multiple times, and new Chrome processes kept spawning "likely from the other QA agent" (line ~3015). This required a dedicated fix: unique `--user-data-dir` via `tempfile.mkdtemp` and `--remote-debugging-port=0` per suite (line ~5096).

### 2. E2E narrative testing explicitly designed as serial to avoid clobbering
When testing 4 demo narratives against live Docker services, the orchestrator explicitly stated: "Agents run in SERIES (1 -> 2 -> 3 -> 4) so they don't stomp on each other" (line ~13350). Each agent was told to "Reset system (`docker compose down -v && up --build`, seed data)" before running, and to "Reset system for the next agent" after. Despite this, Agents 3 and 4 were launched in parallel anyway, with Agent 4 "instructed to reset the system before running since Agent 3 may still be using it" (line ~13422) — an implicit acknowledgment of the shared-state problem.

### 3. Alternative demo workflow explicitly built around sequential testing
The user requested a 3-explorer + test-agent workflow. The diagram explicitly labels the test agent as "Sequential: A -> B -> C (no clobber)" (line ~22260). The design rationale states: "Test agent runs sequentially (A then B then C — avoids clobbering shared state like the running UI/backend)" (line ~22357). This is direct evidence the developer recognized and worked around the shared-state problem.

### 4. UI build strategy chosen specifically to avoid shared-state merge conflicts
When choosing a UI build approach, the developer rejected Option C (most parallel) because "the merge agent becomes a bottleneck — if builders make different assumptions about shared state, the merger is doing a mini-rewrite" (line ~17104). Option B was chosen instead, with sequential foundation building followed by parallel screen work on isolated streams.

### 5. Database/MinIO state required full wipes between agent runs
The seed scripts clear all runs and reference data before re-seeding (lines ~220-225). The E2E test agents each required `docker compose down -v && up --build` — a full volume wipe — before they could run cleanly. This scorched-earth approach is the antithesis of safe concurrent access.

### 6. Angel weights desync — a shared-state consistency bug
The API writes angel weights to PostgreSQL while the VPE reads them from MinIO. "The weight dial is disconnected" (line ~7026). Strictly, this is a dual-write consistency bug (two storage backends for one logical value), not a concurrency/clobbering bug between agents. However, it illustrates how shared mutable state across system boundaries produces incorrect behavior when read/write paths diverge.

## Evidence AGAINST

### 1. Parallel agents on shared state frequently worked fine — for read-only tasks
Many parallel agent runs succeeded without issues:
- Multiple auditor agents (4-5 at a time) reading the same codebase, specs, and data simultaneously produced correct results consistently (lines ~6977, ~9583, ~11124).
- Parallel research agents (e.g., two investigating deployment scripts) worked fine because they only read (line ~86).
- Three parallel data agents (existing-data-expert + 2 verifiers) ran concurrently and produced correct, complementary reports (line ~9317).
- Cross-verification agents (each reviewing another agent's work) ran in parallel without issues.

### 2. Chrome isolation fix was small and effective
The Chrome contention was solved with ~5 lines of config (unique user-data-dir + random debug port). After the fix, "Chrome isolation verified — both suites pass in parallel" (line ~3807). The fix was proportionate and didn't require abandoning parallelism.

### 3. Sequential fallback was chosen proactively, not forced by failures
In the E2E narrative testing case, the serial design was specified upfront before any clobbering occurred. The developer anticipated the problem and designed around it. This is disciplined engineering, not a failure-driven fallback.

### 4. Parallel spec/planning agents were the dominant pattern and worked well
The vast majority of agent work was parallel and successful: spec writing, auditing, cross-verification, story creation, data analysis, research. The 7-agent team (line ~1500), 4-agent story team (line ~9317), 3-auditor team (line ~22310), and numerous 2-3 agent parallel research tasks all completed without shared-state issues. These constituted the bulk of total agent-hours.

### 5. The sequential workaround for E2E tests was actually fast
Agent 4 (demo_4) completed in ~205 seconds (~3.4 minutes). The full 4-agent serial E2E test cycle appears to have completed in under 30 minutes total. For testing against live services that require known database state, serial execution is arguably the correct design regardless of tooling constraints.

### 6. Agents 3 and 4 were launched in parallel despite the serial design — and it worked
The orchestrator launched Agents 3 and 4 simultaneously (lines ~13416-13422), with Agent 4 told to reset first. Agent 4 completed successfully with "System is reset to clean state" (line ~13433). The clobbering risk was managed via a simple convention (reset before run) rather than requiring true locking.

## Nuances & Caveats

1. **The "clobbering" was almost entirely limited to two resource types**: Chrome browser sessions and database/MinIO state. All other parallel agent work (reading code, writing specs, producing reports) was clobber-free because agents wrote to separate output files.

2. **The sequential fallback only applied to a small fraction of total work.** Most parallelism in the project involved read-only analysis, spec writing, or auditing — tasks with no shared mutable state. The serial constraint was specific to agents that mutated live services (Selenium tests, E2E pipeline tests).

3. **The "negated parallelism" claim is overstated.** Sequential testing of 4 narratives against live services took perhaps 30 minutes. Meanwhile, dozens of parallel agent runs for specs, audits, and research saved hours. The net parallelism benefit was strongly positive.

4. **The real architectural gap was the lack of test isolation (per-agent Docker stacks or test databases), not locking.** Adding file locks wouldn't solve the fundamental problem that two agents running different pipeline requests against the same database produce unpredictable state. The correct solution is isolated environments (e.g., Testcontainers-style ephemeral containers per agent) or deterministic test fixtures — not locks. This is a well-established pattern in CI/CD; the novelty here is that AI agents hit the same wall that parallel test suites have hit for years.

5. **Some "sequential fallbacks" were simply correct engineering.** The Selenium pipeline (runner -> auditor -> prioritizer) was sequential because each step depended on the previous output (line ~18322). The alternative demo test agent was sequential because tests against a live UI inherently need a known starting state. These aren't failures of parallelism — they're dependency chains.

## CONFIDENCE SCORE: 4/10

## Verdict

The hypothesis is **partially true but significantly overstated**. Shared mutable state did cause real clobbering in two specific domains: Chrome browser sessions (parallel Selenium tests crashed) and database/MinIO state (E2E tests required serial execution with full wipes). The developer invented effective workarounds: Chrome isolation config, serial test execution with system resets between agents, and vertical-slice agent ownership to minimize integration surface.

However, the claim that sequential fallbacks "negated the parallelism benefits" is not supported by the evidence. The serial constraint applied only to the minority of agent work that mutated live services. The vast majority of parallel agent runs — spec writing, auditing, cross-verification, research, data analysis — worked without issues because they operated on separate output files or were read-only. The project achieved substantial parallelism benefits overall, and the sequential workarounds were both small in scope and appropriate for the problem domain.

The real issue was the absence of per-agent test isolation (separate Docker stacks or databases), not a missing locking mechanism. This aligns with established patterns in the broader ecosystem: every major multi-agent framework (LangGraph, AutoGen, CrewAI) sidesteps the shared-mutable-state problem entirely by restricting agents to message-passing over immutable state or by enforcing sequential turn-taking. None of them offer concurrent write access to shared environments with conflict resolution. The project's experience is not an outlier — it is the expected outcome when agents share mutable external resources without isolation.

## External References

- **[Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** — Defines orchestrator-workers and parallelization patterns but explicitly avoids shared state; recommends "sectioning" (independent subtasks) and "voting" (identical tasks) as the two safe parallelism modes, neither of which involves concurrent mutation.

- **[LangGraph Multi-Agent Workflows](https://blog.langchain.com/langgraph-multi-agent-workflows)** — Describes two state architectures: "shared scratchpad" (all agents see all messages) vs. "independent scratchpads" (agents have private state, only final outputs are shared). The independent-scratchpad pattern directly addresses the clobbering problem observed in this project.

- **[LangGraph State Management Docs](https://docs.langchain.com/oss/python/langgraph/graph-api)** — LangGraph uses reducer functions per state channel to merge concurrent updates deterministically rather than allowing last-write-wins clobbering. Parallel nodes in a "super-step" write through reducers, not raw mutation. Notably, the docs do not address external resource contention (databases, browsers) — only in-memory graph state.

- **[AutoGen Teams and State Management](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html)** — AutoGen enforces sequential turn-taking (round-robin) where "each agent broadcasts its response to all other agents." This design inherently prevents concurrent state conflicts by serializing all agent actions. State is explicitly saveable/loadable per agent, enabling isolation between sessions.

- **[CrewAI Collaboration Patterns](https://docs.crewai.com/concepts/collaboration)** — CrewAI avoids shared mutable state by design: agents communicate via delegation tools and task context parameters (`context=[previous_task]`), not shared memory. The hierarchical process uses a manager agent to serialize task assignment, preventing resource conflicts structurally.

- **[Testcontainers: Getting Started](https://testcontainers.com/getting-started/)** — Directly addresses the per-agent isolation gap identified in this report: "There will be no data conflict issues, even when multiple build pipelines run in parallel because each pipeline runs with an isolated set of services." This is the exact pattern that would have eliminated the E2E test serialization requirement.

- **[Testcontainers: Introduction Guide](https://testcontainers.com/guides/introducing-testcontainers/)** — Documents how shared test infrastructure causes "non-deterministic test results because of the possibility of data corruption and configuration drift" — precisely the problem that forced serial E2E agent execution in this project.

- **[AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation (arXiv:2308.08155)](https://arxiv.org/abs/2308.08155)** — Foundational multi-agent framework paper. Agents are "customizable, conversable" actors with flexible interaction behaviors. The architecture emphasizes conversation-based coordination rather than shared-environment mutation.

- **[Mixture-of-Agents (arXiv:2406.04692)](https://arxiv.org/abs/2406.04692)** — Demonstrates effective multi-agent coordination through a layered architecture where agents consume previous-layer outputs as immutable inputs. Achieves state-of-the-art results without any shared mutable state — each layer's output is frozen before the next layer reads it.

- **[LLM-based Multi-Agents Survey (arXiv:2402.01680)](https://arxiv.org/abs/2402.01680)** — Comprehensive survey of multi-agent LLM systems covering profiling, communication, and capacity-building mechanisms. Confirms that message-passing (not shared-environment mutation) is the dominant coordination pattern across the field.
