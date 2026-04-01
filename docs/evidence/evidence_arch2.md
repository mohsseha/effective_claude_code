# Evidence Report: arch-2
## Hypothesis
"Implementing hard gates (non-negotiable policy denials) inside the angel scoring layer rather than exclusively in the optimizer created a dual-enforcement architecture that confused the developers and required repeated deep-dive investigations to explain."

## Type: BAD-IDEA

## Evidence FOR (supports the hypothesis)

- **[line ~1628]** The developer's own fix was "too aggressive" because the relationship between angel-level hard gates and VPE enforcement was unclear: "My fix was too aggressive — treating ALL factor=0.0 as a hard gate denial. The spec says only `equality` (on global rules violations) and `access` (on coverage breach) are hard gates, but `equality=0.0` here is a soft policy violation (notice_days) that should be overridden by the emergency context." This required multiple iterations to get right — first too broad, then narrowed to access-only, then equality had to be re-added with exemptions.

- **[line ~1798-1801]** A cascade of layered bugs: "VPE ignoring hard gates: VPE used pure weighted score to determine outcome, completely ignoring `should_proceed=False` from angel council_position." Then "Hard gate check too aggressive: First implementation checked ALL factors at 0.0 as hard gates." Then "Riley 'escalated' instead of 'denied': Multiple cascading issues - coverage data not loading (list crash), then coverage found but VPE not enforcing hard gate." The dual-layer design meant bugs had to be traced through angel scoring, VPE synthesis, and their interaction.

- **[line ~7298]** Investigation found hard gates were incomplete in VPE: "`_HARD_GATE_FACTORS` at line 163 only contains `{"access"}` — missing `"equality"`." This shows the dual-enforcement architecture led to inconsistency between layers — the angel scored equality as a hard gate but the VPE only enforced access.

- **[line ~7306]** Emergency exemption logic was broken in the angel layer due to subtle data path issues: "Justice `_score_equality` at line 104 exempts `urgency in ("urgent", "emergency")` but the live test used `"critical"`, which is not in the list. Also, `request_type` is read from `payload` (line 103) instead of the request top-level, so `emergency_reschedule` requests never trigger the exemption either." Hard gate policy logic embedded in the angel was fragile and hard to get right.

- **[line ~13407]** A P0 bug was caused by angel-level hard gate implementation: "BUG-004 — justice angel doesn't filter coverage by shift_id, so the access hard gate never fires correctly for non-default shifts." The angel was doing coverage checks (an operational concern) and getting them wrong.

- **[line ~13656]** The root cause of BUG-004 was the angel doing optimizer-level work: "the `fetch_justice_context()` function queried coverage records with only `{"type": "coverage"}` and took `records[0]`, meaning it always got whichever coverage record appeared first regardless of which shift was being evaluated."

- **[line ~1973]** Data contract mismatches between seed data and scoring code affected hard gates at the angel level: "Coverage structure mismatch — The scoring code expects `{"current": N, "minimum": M}` with `"type": "coverage"`. The seed script writes an array of per-date records with `required`/`assigned` fields and no `type` field. The access hard gate (which should deny David's request due to minimum staffing) never fires."

- **[line ~2184]** Hard gate not firing led to wrong outcomes that required investigation: "Riley Park: 'Needs Review' instead of 'Denied' — the live scoring puts Riley in the escalation band (0.4-0.6) rather than triggering the access hard gate. This means the per-shift coverage lookup for Riley's shift (SHF0035) isn't producing `access=0.0` in the live pipeline."

- **[line ~15962]** The null shift_id problem was caused by angel-level coverage checks: "The problem: the justice angel's coverage check (`fetch_justice_context()`) uses the `shift_id` to look up how many workers are assigned to that specific shift. With `shift_id: null`, it can't determine if approving Maria's request would leave the shift understaffed. The coverage hard gate — the thing we fixed in BUG-004 — relies on filtering by `shift_id`."

- **[line ~10519-10562]** The optimizer math formulation explicitly acknowledges the redundancy: "This is the access hard gate from the justice angel, enforced again at the optimizer level." And: "the optimizer independently validates constraint 1 as a cross-check." This confirms the dual-enforcement was a deliberate choice but required formal documentation to explain.

- **[line ~22179]** The user directly asked "Shouldn't this happen at the optimizer, not the angel level?" — proving the architecture was confusing even to the project owner.

- **[line ~12003]** Conflict detection had to be patched to account for hard gates at the angel level: "The interface spec says conflict should be flagged 'if angels disagree significantly (score difference > 0.4, or one has a hard gate).' The old code only checked score divergence. Fixed to also detect when any angel has a hard gate factor (equality/access) at 0.0." The hard gate at the angel level created secondary integration concerns.

- **[line ~19222]** The LLM agent path also had the bug: "The PydanticAI agent's `query_coverage` tool also returns all coverage records without filtering by shift_id. The LLM would see records for shifts at minimum staffing and potentially score access as 0.0." The dual architecture meant the bug had to be fixed in multiple code paths.

## Evidence AGAINST (contradicts the hypothesis)

- **[line ~22181]** The assistant provided a clear, principled defense: "It happens at both, intentionally. The Justice angel checks coverage as an *ethical* question — is it fair to remaining workers? The optimizer checks it again as an *operational* reality check — can this plan physically work? If we only checked in the optimizer, the angels would debate and recommend approval without knowing it was impossible, creating a confusing audit trail. By checking in the angel first, the hard gate fires early, the VPE reasons around it, and the audit trail is coherent end-to-end. The optimizer is the final safety net. Defense in depth, not redundancy."

- **[line ~4800]** The architecture was explicitly chosen for safety: "Hard gates stay safe. Justice's equality and access factors are deterministic policy checks. They MUST produce 0.0 when policy is violated or coverage is breached. An LLM cannot be trusted with this. Option A keeps these in Python."

- **[line ~4342]** The decision architecture was clearly articulated: "The decision (approve/deny/escalate) is fully deterministic — weighted angel scores + hard gates. The LLM debate is purely for the audit trail." This clarity suggests the architecture was well-understood conceptually even if implementation was buggy.

- **[line ~4717]** When wiring LLM agents, the hard gate separation was handled cleanly: "The hard gates (equality, access) must remain deterministic. The LLM scores the soft factors (voice, respect, trust) but Python still runs the policy-compliance and coverage-adequacy checks." The architecture created a natural separation of concerns.

- **[line ~5627]** The PydanticAI plan preserved the pattern: "Justice's equality and access factors are enforced deterministically in Python after the LLM returns. `enforce_hard_gates()` reads the same lake data and overrides the LLM's score to 0.0 if policy/coverage rules are violated. The LLM's original score is preserved in the explanation for audit trail." This shows the pattern scaled to new implementations.

- **[line ~11304]** Cross-story consistency was strong: "The pipeline flow, thresholds (approve >= 0.6, deny <= 0.4), hard gate behavior, angel weight mechanics, optimizer multi-shift solving, and audit traceability are described identically across all stories." The architecture was consistently understood at the spec level.

- **[line ~11994]** Hard gates and debate coexisted well: "Hard gates don't suppress debate: The socratic path runs `run_debate()` before checking hard gates, so debate always executes regardless of hard gate status." This design choice meant the audit trail was always complete.

- **[line ~9361]** Hard gate denial was a compelling demo story: "Story 2 — Hard Gate Denial: James submits a last-minute routine request that violates the notice-days policy. The justice angel's equality hard gate fires (score 0.0), forcing a denial regardless of other scores." The feature was valuable enough to be a core demo scenario.

- **[line ~10333]** The handoff was clean in theory: "If any angel hard gate factor (access or equality) scored 0.0, the VPE produces a 'deny' directive regardless of weights. The optimizer must honor this — it is encoded in the directive verb, not checked independently by the optimizer." The dual enforcement had a well-defined protocol.

- **[line ~6239]** Audit-friendly output was a benefit: "Changed access factor from generic 'Automatic block' to consistent format with LLM advisory score preserved: `'HARD GATE: coverage cannot be maintained; post-approval staffing below minimum (LLM scored 0.20)'`." The angel-level hard gate produced better audit explanations than a silent optimizer constraint would.

## Nuances & Caveats

1. **Data contract issues were amplified by the architecture, not independent of it**: The original report understated this. Yes, the repeated failures (coverage structure mismatch, missing burden indicators, policy format mismatch) were about seed data not matching scoring code expectations. But having *two consumers* of the same coverage data (angel + optimizer) meant each bug had a larger blast radius and had to be fixed in more places (see the shift_id fix required in both `fetch_justice_context()` and the PydanticAI agent's `query_coverage` tool). A single enforcement point would have had the same data bugs but half the fix surface.

2. **The confusion was real but resolvable**: The user asked "Shouldn't this happen at the optimizer, not the angel level?" but was satisfied by the "defense in depth" explanation. The confusion lasted one conversational turn, not a prolonged investigation. This is a point in favor of the architecture — it was explainable.

3. **The angel-level check serves a genuinely different purpose**: The angel checks coverage as an ethical input to the debate ("is it fair to remaining workers?"). The optimizer checks it as a physical constraint ("can this plan work?"). This maps well to the established pattern of validation at different architectural layers serving different failure modes (see Kraemer in External References). The shared data dependency creates coupling, but the *questions being asked* are distinct.

4. **Implementation complexity was front-loaded**: Once BUG-004 was fixed and emergency exemptions were sorted out, the hard gate system appears to have been stable. The bugs were concentrated in the early build phase. This matches the Fowler observation that rule systems are "easy to set up, but very hard to maintain" — except here the hard part was setup, and maintenance appears manageable.

5. **The dual enforcement caught real issues**: The optimizer "cross-check" (constraint 1 validating coverage independently of the directive verb) means a bug in the angel hard gate would be caught downstream. This safety net has value even if it adds complexity.

6. **The "FOR" evidence overstates the case**: Many items in the FOR section describe bugs that would exist in *any* implementation touching coverage data. The truly architectural bugs — where the dual-layer design itself caused the problem — are narrower: the `_HARD_GATE_FACTORS` inconsistency between angel and VPE (line ~7298), the "too aggressive" hard gate check (line ~1628), and the need to fix the same data query bug in multiple code paths (line ~19222). The rest are data contract bugs that happened to surface in the angel layer.

## External References

- **[Martin Fowler — Rules Engine (bliki)](https://martinfowler.com/bliki/RulesEngine.html)** — Fowler warns that rule systems create "implicit program flow" that is "easy to set up, but very hard to maintain." His advice to keep rules in a "narrow context" supports the angel hard gate design (domain-specific, limited scope) but also explains why the interaction between angel rules and VPE enforcement was hard to debug.

- **[The Layer Anti-Pattern (devmethodologies)](https://devmethodologies.blogspot.com/2012/10/the-layer-anti-pattern.html)** — Describes how redundant error-handling across layers (citing the OSI model) creates "overhead and redundancy." Argues that shared logic should become a library, not a duplicated layer. Partially supports the hypothesis, but the angel and optimizer are not mere wrappers — they ask different questions of the same data.

- **[Florian Kraemer — About Validation and Anti-Corruption Layers](https://florian-kraemer.net/software-architecture/2024/02/16/About-Validation-and-Anti-Corruption-Layers.html)** — Directly relevant. Argues that validation appearing at multiple layers is *not* duplication when each layer serves a different purpose: input validation ("the bouncer"), domain invariants ("the enforcer"), and database constraints ("last line of defense"). This is the strongest external support for the angel/optimizer split — the angel enforces ethical invariants, the optimizer enforces operational constraints.

- **[AlgoCademy — Why Your Code Duplication Isn't Always Bad](https://algocademy.com/blog/why-your-code-duplication-isnt-always-bad-a-pragmatic-approach-to-the-dry-principle/)** — Cites Sandi Metz: "Duplication is far cheaper than the wrong abstraction." Argues that when two pieces of code serve different conceptual purposes and may evolve independently, keeping them separate prevents harmful coupling. Supports the dual-enforcement design when angel and optimizer checks have different semantic intent.

- **[Nected — Rules Engine Design Patterns](https://www.nected.ai/blog/rules-engine-design-pattern)** — Advocates for a centralized rules engine as "a single source of truth for all business-critical decision-making logic." This cuts against the dual-enforcement pattern — if hard gates are business-critical rules, they arguably belong in one place. However, the angel hard gates are not purely business rules; they are ethical scoring inputs that also happen to encode policy.

- **[EU Ethics By Design for AI (PDF)](https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/guidance/ethics-by-design-and-ethics-of-use-approaches-for-artificial-intelligence_he_en.pdf)** — EU guidance distinguishes ethical constraints (what *should* be done) from operational governance (how to *ensure* it gets done). This maps to the angel/optimizer split: the angel embeds ethical judgment into the scoring pipeline, while the optimizer enforces operational feasibility. The separation is principled, not accidental.

- **[Medium — Enforcing Business Rules in Multi-Layered Web Applications](https://medium.com/@taras.bidyuk/enforcing-business-rules-in-multi-layered-web-applications-be714ab0cac7)** — Argues business rules belong in the domain/business layer and should not be duplicated into presentation or data layers. Warns that scattered enforcement leads to inconsistency — which is exactly what happened with the `_HARD_GATE_FACTORS` mismatch between angel and VPE.

## CONFIDENCE SCORE: 3.5/10

## Verdict
The hypothesis is weakly supported, and the external research nudged my confidence *down* slightly. The dual-enforcement architecture caused real implementation pain — the `_HARD_GATE_FACTORS` inconsistency, the "too aggressive" check, and the multi-path bug fixes are genuine architectural costs. But the established software engineering literature makes a strong case that validation at different layers is not duplication when each layer answers a different question. The angel asks "is this ethically acceptable?" and the optimizer asks "is this operationally feasible?" — these are distinct failure modes, matching the pattern Kraemer describes. Fowler's warning about implicit program flow in rule systems is relevant to the debugging difficulty, but the hard gates are a narrow, deterministic rule set (two factors, binary output), not a sprawling rule engine. The Metz principle ("duplication is far cheaper than the wrong abstraction") further supports keeping the checks separate rather than forcing them into a single enforcement point that conflates ethical and operational concerns. This is better characterized as a sound architecture with a steep learning curve and real consistency risks at the data layer, not a bad idea.
