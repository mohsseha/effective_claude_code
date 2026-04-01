# Spec-Driven Development in the Age of AI Coding Agents

**Thesis:** When working with AI coding agents, the specification -- not the code -- is the load-bearing artifact. Code becomes a generated, disposable, regenerable byproduct. The spec is what you version, review, and defend.

---

## Sources at a Glance

| Person / Source | Role / Affiliation | Key Claim | Link |
|---|---|---|---|
| Addy Osmani | Engineering Lead, Google | Specs are the "single source of truth" for AI agents; use a Specify -> Plan -> Tasks -> Implement workflow | [How to write a good spec for AI agents](https://addyosmani.com/blog/good-spec/) |
| Addy Osmani | Engineering Lead, Google | AI-augmented (not automated) engineering requires classic discipline applied to agent collaboration | [My LLM coding workflow going into 2026](https://addyosmani.com/blog/ai-coding-workflow/) |
| Andrej Karpathy | Co-founder, OpenAI; former Tesla AI | Coined "vibe coding" (Feb 2025), then declared it passe in favor of "agentic engineering" -- orchestrating agents under structured oversight | [2025 LLM Year in Review](https://karpathy.bearblog.dev/year-in-review-2025/) |
| Deepak Babu Piskala | Researcher (arXiv) | Proposes three levels of spec rigor (spec-first, spec-anchored, spec-as-source); specs invert the traditional dev workflow | [arXiv 2602.00180](https://arxiv.org/abs/2602.00180) |
| Den Delimarsky | Principal PM, GitHub | Specs are "living, executable artifacts" and the "shared source of truth"; agents can't read minds, they need contracts | [GitHub Blog: Spec-driven development](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) |
| GitHub | Spec Kit (open source) | Four-phase gated workflow: Specify, Plan, Tasks, Implement -- with human review checkpoints at each gate | [github/spec-kit](https://github.com/github/spec-kit) |
| Anthropic | Claude Code documentation | "Explore first, then plan, then code"; CLAUDE.md as persistent spec; recommends writing spec then starting fresh session to implement | [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) |
| Anthropic | Engineering blog | Long-running agents need structured feature inventories and progress files; agents drift without explicit scaffolding | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| Thoughtworks | Technology Radar (Nov 2025) | Placed SDD in "Assess" ring; calls it the key emerging practice of 2025 but warns workflows remain "elaborate and opinionated" | [Technology Radar: SDD](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development) |
| Thoughtworks | Blog | SDD addresses the failure mode of vibe coding: too fast, too haphazard, too much unmaintainable one-off code | [Unpacking SDD](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) |
| Martin Fowler | Thoughtworks | Tested Kiro, spec-kit, and Tessl; found agents ignore spec instructions, create duplicates, and claim success when builds fail; warns of MDD parallels | [SDD Tools Analysis](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) |
| Leigh Griffin & Ray Carroll | InfoQ | SDD makes architecture executable and enforceable through continuous validation | [InfoQ: When Architecture Becomes Executable](https://www.infoq.com/articles/spec-driven-development/) |
| Simon Willison | Independent developer, Datasette creator | Formalizing "agentic engineering patterns"; robust test suites give agents "superpowers"; warns of "house of cards code" | [Agentic Engineering Patterns](https://simonwillison.net/2025/Jun/29/agentic-coding/) |
| Steve Yegge & Gene Kim | Sourcegraph / IT Revolution | "The IDE is dead by 2026"; developers shift from writing code to articulating intent and managing agent ensembles; three-loop framework for AI-assisted dev | [Pragmatic Engineer interview](https://newsletter.pragmaticengineer.com/p/steve-yegge-on-ai-agents-and-the) |
| Kent Beck | Creator of XP, TDD | Experiments with AI tools confirm that test-first discipline (a form of spec) remains essential even when agents write the code | [TDD, AI agents and coding](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) |

---

## 1. What Thought Leaders Are Saying

### Addy Osmani: Specs as the Bridge Between Intent and Reliable Output

Osmani's position is the most operationally detailed. In [How to write a good spec for AI agents](https://addyosmani.com/blog/good-spec/), he argues that a spec is the "single source of truth for both humans and AI agents." His framework covers six areas every spec should address: commands, testing, project structure, code style, git workflow, and boundaries (what agents must never touch).

His workflow is explicitly gated: Specify, Plan, Tasks, Implement -- with human validation at each gate. This mirrors GitHub Spec Kit's structure, and Osmani has endorsed it. In [My LLM coding workflow going into 2026](https://addyosmani.com/blog/ai-coding-workflow/), he emphasizes that the best results come from "applying classic software engineering discipline to AI collaborations" -- not from giving agents more autonomy, but from giving them better specs.

Key insight: specs should focus on **what and why**, not the nitty-gritty **how**. The agent fills in the how. The human owns the what.

### Andrej Karpathy: From Vibes to Engineering

Karpathy coined "vibe coding" in [February 2025](https://karpathy.bearblog.dev/year-in-review-2025/) to describe the practice of "fully giving in to the vibes, embracing exponentials, and forgetting that the code even exists." It was a provocation -- and it worked. The term became [Collins Dictionary's Word of the Year for 2025](https://en.wikipedia.org/wiki/Vibe_coding).

But by early 2026, Karpathy himself declared vibe coding passe. His replacement term is **"agentic engineering"**: "'agentic' because the new default is that you are not writing the code directly 99% of the time, you are orchestrating agents who do and acting as oversight -- 'engineering' to emphasize that there is an art & science and expertise to it."

The arc from vibe coding to agentic engineering is the arc from "let the AI figure it out" to "give the AI a spec and verify the output." Karpathy's evolution mirrors the industry's.

### Anthropic: Explore, Plan, Then Code

Anthropic's own [Claude Code best practices](https://code.claude.com/docs/en/best-practices) are explicit: "Letting Claude jump straight to coding can produce code that solves the wrong problem." The recommended workflow has four phases: Explore (read files, understand context), Plan (create detailed implementation plan), Implement (code against the plan), Commit.

Anthropic goes further in their engineering blog post on [effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). They recommend structured feature inventories (JSON-formatted, initially marked "failing"), progress files (`claude-progress.txt`), and explicit testing as alignment mechanisms. The key finding: "agents tend toward one-shot approaches," so explicit feature inventories prevent them from prematurely declaring work complete.

Their recommended interview pattern is particularly telling: start with a minimal prompt, have Claude interview you about edge cases and tradeoffs, then write a complete spec to `SPEC.md`, then **start a fresh session** to implement it. The spec is the handoff artifact between sessions. The conversation is disposable; the spec persists.

### Martin Fowler: The Skeptic's Critique

Fowler's [analysis of Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) is the most rigorous critique available. He tested these tools on real tasks and found:

- Kiro turned a small bug fix into "4 user stories with a total of 16 acceptance criteria" -- "like using a sledgehammer to crack a nut"
- Agents frequently ignored spec instructions: "it just took them as a new specification and generated them all over again, creating duplicates"
- He found himself preferring to "review code than all these markdown files"
- He warns of parallels to Model-Driven Development (MDD), which "never took off for business applications" because it "sits at an awkward abstraction level"

Fowler's critique is important because it identifies a real tension: **specs can become bureaucracy if they're not the right size for the problem**. But notably, even Fowler doesn't argue against specs -- he argues against over-specified specs for small tasks and tools that enforce a single workflow regardless of problem size.

### Simon Willison: Tests as Executable Specs

Willison's [agentic engineering patterns](https://simonwillison.net/2025/Jun/29/agentic-coding/) emphasize that "having a robust test suite is like giving the agents superpowers -- they can validate and iterate quickly when tests fail." His coinage of "house of cards code" describes the failure mode of unspecified agent output: code that looks right but collapses under scrutiny.

This aligns with a key insight: **tests are specs**. A test suite is a machine-readable specification. When you give an agent tests to pass, you're giving it a spec. When you give it a written spec without tests, you're trusting the agent to interpret natural language correctly -- which, as Fowler demonstrated, it frequently does not.

### Steve Yegge and Gene Kim: Intent as Source Code

Yegge's prediction that "the IDE is dead... it will be gone by 2026" ([Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/steve-yegge-on-ai-agents-and-the)) is provocative, but the underlying argument is about where developers spend their time. If agents write the code, the developer's primary artifact becomes the **intent specification** -- the description of what should exist. Yegge and Kim's three-loop framework for AI-assisted development formalizes this, organizing work into loops that each require specification, execution, and verification.

---

## 2. Key Arguments FOR Specs as the Primary Artifact

### 2.1 Agents Cannot Read Minds

Den Delimarsky of GitHub [states it plainly](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/): AI agents "are exceptional at pattern completion, but not at mind reading." Without a spec, the agent must guess at unstated requirements. It will produce code that compiles but does not match intent. The spec eliminates the guessing.

### 2.2 Code Is Now Cheap; Intent Is Expensive

When an agent can generate 500 lines of code in seconds, the bottleneck shifts. Writing code is no longer the hard part. Knowing what code to write -- and being able to verify that the output matches intent -- is the hard part. The spec captures the expensive thing (intent) and lets the cheap thing (code generation) be automated.

### 2.3 Specs Enable Multi-Agent Coordination

The [arXiv paper](https://arxiv.org/abs/2602.00180) and [Augment Code's analysis](https://www.augmentcode.com/guides/what-is-spec-driven-development) both identify this as critical: in multi-agent workflows, "every agent reads from and writes to the same living spec, so the Coordinator, Implementors, and Verifier stay aligned." Without a shared spec, each agent operates from its own interpretation of conversation context, producing misaligned assumptions that only surface during integration.

### 2.4 Specs Survive Context Window Limits

This is the most practical argument. Anthropic's [best practices](https://code.claude.com/docs/en/best-practices) note that "Claude's context window fills up fast, and performance degrades as it fills." A conversation is ephemeral and degrades. A spec file on disk is permanent. Anthropic explicitly recommends writing a spec, then starting a **fresh session** to implement it. The spec is the bridge across context boundaries.

### 2.5 Specs Enable Verification

As Osmani, Willison, and Anthropic all emphasize, the single highest-leverage thing you can do is give the agent a way to verify its work. A spec with test cases, acceptance criteria, and success conditions enables this. Without a spec, "you become the only feedback loop, and every mistake requires your attention" ([Anthropic](https://code.claude.com/docs/en/best-practices)).

### 2.6 Specs Are Reviewable by Humans

Reviewing a 50-line spec is faster and more reliable than reviewing 500 lines of generated code. The spec describes intent in human language. The code describes mechanism in machine language. Humans are better at validating intent than mechanism. (Fowler's counterpoint -- that verbose specs can themselves become a burden -- is valid, but the answer is better specs, not no specs.)

---

## 3. Key Arguments AGAINST (or Limitations)

### 3.1 The Waterfall Trap

Thoughtworks [warns](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) that SDD can recreate waterfall's failure modes: too much upfront specification, too little iteration. Fowler's experiments confirm this -- when a small bug fix becomes 4 user stories with 16 acceptance criteria, something has gone wrong. The mitigation is to right-size specs: a one-line bug fix gets a one-line spec; a new feature gets a full spec document.

### 3.2 Non-Determinism Undermines Spec-as-Source

Fowler [observes](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) that "the mapping from spec to code is non-deterministic -- the same specification given to the same model on different days produces different implementations." This is a fundamental limitation of treating specs as compilable source code. Specs work best as **contracts and constraints**, not as deterministic compilation inputs.

### 3.3 Spec Maintenance Is Real Work

Specs can drift from code just as code drifts from requirements. If the spec is not actively enforced (through tests, CI, or agent validation), it becomes stale documentation -- exactly the failure mode that traditional software specs have always suffered from.

### 3.4 Agents Ignore Specs Anyway

Fowler's most damning finding: agents "ignore the notes... just took them as a new specification and generated them all over again, creating duplicates." Current LLMs do not reliably follow all instructions in long, detailed specifications. This is a capability limitation, not a conceptual one -- it will improve -- but it is real today.

### 3.5 Review Fatigue

Fowler found that extensive markdown artifacts created "a tedious review experience." If the spec is so long that reviewing it is harder than reviewing the code, it has failed its purpose. Specs must be concise enough to actually read.

### 3.6 Tool Lock-in and Immaturity

Thoughtworks [notes](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development) that SDD tools "behave inconsistently based on task size and type" and that "tool-specific specification formats create lock-in risk." The ecosystem is immature -- Kiro, spec-kit, and Tessl all launched in 2025 and are still evolving rapidly.

---

## 4. Frozen, Versioned Specs Prevent Drift in Multi-Agent Workflows

This is where the argument becomes strongest. Consider a workflow with multiple agents:

1. **Agent A** writes the backend implementation
2. **Agent B** writes the frontend
3. **Agent C** writes the tests
4. **Agent D** performs security review

Each agent runs in a separate context window. Each has no memory of the others' conversations. What keeps them aligned?

Without a frozen spec, the answer is: nothing. Each agent interprets its prompt independently. Agent A decides the API returns `camelCase` keys. Agent B assumes `snake_case`. Agent C writes tests for a third interpretation. You discover this at integration time, after all four agents have consumed their context budgets.

With a **frozen, versioned spec committed to version control**:

- Every agent reads the same `spec.md` and `tasks.md` from the repo
- The spec defines the API contract, data formats, and acceptance criteria
- If an agent's output doesn't match the spec, the mismatch is detectable -- by tests, by CI, or by a reviewer comparing output to spec
- The spec can be updated through a deliberate, reviewable process (a PR to the spec file), not through conversational drift

Anthropic's guidance on [long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) confirms this pattern. They use structured feature inventories and progress files precisely because "agents tend toward one-shot approaches" and will "prematurely declare work complete" without explicit, file-based tracking. The `claude-progress.txt` pattern is a lightweight spec -- a persistent, file-based source of truth that survives context boundaries.

The [arXiv paper](https://arxiv.org/abs/2602.00180) formalizes this with three levels of rigor:

| Level | Description | When to Use |
|---|---|---|
| **Spec-first** | Write the spec before any code; use it to guide implementation | New features, greenfield projects |
| **Spec-anchored** | Spec guides and validates ongoing development; updated as decisions emerge | Evolving systems, multi-sprint work |
| **Spec-as-source** | Spec generates or verifies code directly; code is a derived artifact | API contracts, schema-driven systems |

For multi-agent workflows, **spec-anchored** is the practical sweet spot. The spec is versioned in git. Agents read it at the start of each session. Changes to the spec go through code review. The spec is the contract between agents, between sessions, and between humans and machines.

---

## 5. The Emerging Consensus

Despite the criticisms, a rough consensus is forming across these sources:

1. **Vibe coding is a starting point, not a destination.** Karpathy's own evolution from coining "vibe coding" to advocating "agentic engineering" captures the industry's trajectory.

2. **Specs don't have to be heavyweight.** The best specs are concise, focused on what and why, and include testable acceptance criteria. Fowler's critique of over-specified workflows is valid, but it's a critique of bad specs, not of specs themselves.

3. **Tests are the most important form of spec.** Willison, Osmani, and Anthropic all converge on this: give the agent a way to verify its own work. A test suite is a machine-readable spec that the agent can execute against.

4. **The spec is the handoff artifact.** When you switch context windows, switch agents, switch sessions, or switch humans -- the spec is what persists. Conversations are ephemeral. Code is regenerable. The spec is the durable artifact.

5. **The tooling is immature but the pattern is sound.** Spec-kit, Kiro, and Tessl are v0.x tools. But the underlying pattern -- write a spec, gate the workflow, verify against the spec -- is robust and will survive regardless of which tools win.

The strongest version of this argument: **in a world where code is generated, the spec is source code.** It is what you version-control, review, and defend. It is the artifact that carries intent across context boundaries, agent boundaries, and session boundaries. It is the load-bearing artifact.

---

## References

- Osmani, A. [How to write a good spec for AI agents](https://addyosmani.com/blog/good-spec/)
- Osmani, A. [My LLM coding workflow going into 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- Osmani, A. [The future of agentic coding](https://addyosmani.com/blog/future-agentic-coding/)
- Karpathy, A. [2025 LLM Year in Review](https://karpathy.bearblog.dev/year-in-review-2025/)
- Piskala, D.B. [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180)
- Delimarsky, D. [Spec-driven development with AI (GitHub Blog)](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- GitHub. [spec-kit repository](https://github.com/github/spec-kit)
- Anthropic. [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- Anthropic. [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Fowler, M. [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Thoughtworks. [Spec-driven development (Technology Radar)](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development)
- Thoughtworks. [Unpacking one of 2025's key new AI-assisted engineering practices](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- Willison, S. [Agentic Engineering Patterns](https://simonwillison.net/2025/Jun/29/agentic-coding/)
- Yegge, S. [Steve Yegge on AI Agents and the Future of Software Engineering (Pragmatic Engineer)](https://newsletter.pragmaticengineer.com/p/steve-yegge-on-ai-agents-and-the)
- Beck, K. [TDD, AI agents and coding with Kent Beck (Pragmatic Engineer)](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent)
- Griffin, L. & Carroll, R. [Spec Driven Development: When Architecture Becomes Executable (InfoQ)](https://www.infoq.com/articles/spec-driven-development/)
