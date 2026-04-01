# Evidence Report: qa-3

## Hypothesis
Using a researcher-then-auditor-then-summarizer three-agent pipeline for investigating production questions produced more accurate and trustworthy answers than single-agent investigation, because the auditor caught factual errors (off-by-one line numbers, date discrepancies) that would have been presented as truth in a single-pass answer.

## Type: GOOD-IDEA

## Evidence FOR

### 1. The auditor caught concrete factual errors in the first use (line 22124)
The first explicit use of the researcher->auditor->summarizer pipeline was for the question "what is a hard gate?" The auditor's verdict: **"23/27 claims fully accurate, 3 off-by-one line numbers, 1 minor date field discrepancy."** This means 4 out of 27 factual claims (15%) had errors that would have been presented as truth without the audit step. The errors were specific and verifiable: wrong line numbers and a date mismatch.

### 2. The developer immediately requested the same pattern again (line 22144)
After seeing the first result, the user explicitly asked: "do the same work flow as above researcher->auditor-> summarizer ALL are agents not yu." The user even emphasized "ALL are agents not yu" -- wanting the full pipeline, not a shortcut. This is a strong trust signal: the developer found enough value in the pattern to demand its reuse.

### 3. The developer designed an even larger multi-agent audit pipeline based on the same principle (lines 22206-22362)
After two rounds of researcher->auditor->summarizer, the user designed a much more elaborate workflow for the alternative demo video: 3 explorers -> test agent -> 3 explorers (revised) -> test agent -> 3 auditors -> selector -> video agent. The auditor pattern was so trusted that it became a foundational design element for subsequent work.

### 4. Auditor pattern caught real issues throughout the project (lines 16912, 17136, 17184)
The transcript reveals a systemic problem: **"Agents 2 and 3 were never audited"** (line 16912) -- the assistant proactively flagged that earlier consistency agents had skipped auditing. When auditors were later launched for those agents, both returned "PASS WITH WARNINGS" with actionable findings (e.g., stale `EMP001` references in comments, `version` field shape mismatch, `EMP004` vs `maria.santos` naming inconsistency). Without auditing, these issues would have been silently accepted.

### 5. The "DON'T GUESS" instruction shows prior negative experience with single-agent answers (line 22112)
The user's original request was emphatic: "DON'T GUESS START AN AGENT TO LOOK THOUGH THE TEXT OF THE SCRIPT AND THEN DO A DEEP DIVE IN THE CODE." The all-caps instruction suggests the developer had prior experience with the assistant guessing or producing shallow answers without code verification. The three-agent pipeline was the user's explicit remedy.

### 6. The summarizer produced a high-quality, externally shareable answer (lines 22130-22140)
The final output was polished enough to "share with the listener" -- it answered both "what" and "why," with specific details (David Park, SHF0035, three workers, zero buffer, access hard gate). The pipeline produced something the founder could confidently relay to a stakeholder, with a report and audit trail available for deeper scrutiny.

### 7. Nearly all audits in the transcript found issues
Across the build-phase audits, every instance returned "PASS WITH WARNINGS" with actionable findings: the hard gate Q&A (4/27 claims wrong), consistency agents (stale references, type mismatches), technical audits (Maria's null shift_id), and re-evaluate audits. The second Q&A pipeline use reported "Both audits passed" without detailing specific findings, so it is unclear whether that was a true clean pass or simply terse reporting. Regardless, the auditor step surfaced issues in the majority of cases.

## Evidence AGAINST

### 1. The errors caught were minor, not substantive (line 22124)
The auditor found "3 off-by-one line numbers, 1 minor date field discrepancy" but confirmed "All substantive facts verified." The core answer about what hard gates are and why David was denied was correct from the researcher alone. The off-by-one line numbers would not have misled the listener -- they were citation precision errors, not factual errors about system behavior.

### 2. No direct comparison with a single-agent answer exists
The transcript never shows the same question answered by both a single agent and the three-agent pipeline. We cannot empirically compare quality. The hypothesis assumes single-agent would have been worse, but the researcher's 23/27 accuracy rate (85%) suggests it was already quite good. The summarizer's output may not have differed materially from what a single careful agent would produce.

### 3. The second pipeline use produced no visible auditor corrections (line 22162)
When the pattern was reused for the follow-up questions (staffing buffer and optimizer vs angel), the assistant simply reported "Both audits passed" with no specific errors mentioned. This suggests the researcher may have been more careful the second time, or the questions were easier -- either way, the auditor added no visible value in that round.

### 4. Cost and latency are non-trivial
Each pipeline invocation required three sequential agent calls. The transcript shows agent calls routinely taking 2-5 minutes each. A three-agent serial pipeline therefore took roughly 6-15 minutes per question, compared to 2-5 minutes for a single-agent answer. For a time-pressured demo preparation, this is a significant overhead -- especially when the auditor's corrections were cosmetic.

### 5. The pattern was user-imposed, not emergently discovered
The developer prescribed the exact pipeline architecture ("3 AGNETS IN SERIES WOULD BE RUNNING"). The assistant did not independently discover that auditing improved quality. This means the evidence supports "the developer believed it was a good idea" more than "it objectively produced better results."

### 6. Auditor pattern was already standard practice for build work
Throughout the transcript, cross-audits were used extensively for code builds, spec reviews, and consistency checks (lines 12312-12329, 16820-16826, etc.). The Q&A application was just extending an existing pattern. The value of auditing was already proven in the build context; applying it to Q&A was incremental, not revolutionary.

## Nuances & Caveats

1. **Selection bias in error reporting.** The auditor explicitly quantified errors in the first use (4/27) but not in subsequent uses ("Both audits passed"). We do not know if later audits found zero errors or simply did not report minor ones.

2. **The real value may be confidence, not accuracy.** The developer needed to share answers with external stakeholders (a "listener" who attended the demo). The audit trail (report + audit file saved to disk) provided defensible provenance. Even if the answer was 85% correct without auditing, the developer could not *know* that without the audit step.

3. **The pattern scales poorly.** For the hard gate question, serial execution was fine (one question, one answer needed). But the user immediately started designing parallel pipelines with 3 researchers + 3 auditors for the alternative demo workflow (line 22206), suggesting awareness that serial three-agent pipelines would not scale to larger tasks.

4. **Off-by-one line numbers matter more than they seem.** In a codebase investigation, wrong line numbers mean the reader cannot verify claims by looking at the cited code. For an audit trail on a "fairness platform," citation accuracy is arguably part of the value proposition. The auditor catching these errors was more significant than "minor" implies.

5. **The "DON'T GUESS" trigger.** The user's emphatic instruction suggests accumulated frustration with prior single-agent answers in the same or earlier sessions. The three-agent pipeline may have been solving a trust problem more than an accuracy problem.

## External References

- **[Chain-of-Verification Reduces Hallucination in Large Language Models (Dhuliawala et al., ACL 2024)](https://arxiv.org/abs/2309.11495)** — Meta's CoVe method has an LLM draft a response, generate verification questions, answer them independently, then revise. Directly analogous to the researcher->auditor pattern: a separate verification step catches errors the generator missed. CoVe more than doubled precision on list-based QA (0.17 to 0.36) and cut hallucinated entities from 2.95 to 0.68.

- **[Improving Factuality and Reasoning in Language Models through Multiagent Debate (Du et al., ICML 2024)](https://arxiv.org/abs/2305.14325)** — Multiple LLM instances propose answers, critique each other over rounds, and converge. Significantly improved factual validity and reduced hallucinations across math, strategy, and factuality benchmarks. Supports the idea that cross-agent critique (not just self-reflection) yields better outputs.

- **[Large Language Models Cannot Self-Correct Reasoning Yet (Huang et al., ICLR 2024)](https://arxiv.org/abs/2310.01798)** — Shows that LLMs struggle to self-correct without external feedback, and performance can degrade after self-correction attempts. This is the key theoretical justification for using a *separate* auditor agent rather than asking the researcher to self-check: intrinsic self-correction is unreliable, but external verification (from a distinct agent with a distinct prompt) sidesteps this limitation.

- **[Multi-LLM-Agents Debate: Performance, Efficiency, and Scaling Challenges (ICLR Blogposts 2025)](https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/)** — A critical counterpoint: multi-agent debate does not consistently outperform simpler single-agent strategies when controlling for compute budget. Aligns with our AGAINST evidence #4 (cost/latency overhead) and tempers the claim that multi-agent is categorically superior.

- **[FACT-AUDIT: An Adaptive Multi-Agent Framework (ACL 2025)](https://aclanthology.org/2025.acl-long.17.pdf)** — A multi-agent fact-checking framework with specialized roles (retrieval, reasoning, auditing). Demonstrates that role-specialized agent pipelines outperform monolithic approaches for verification tasks, directly paralleling the researcher/auditor/summarizer division of labor.

- **[DelphiAgent: A Trustworthy Multi-Agent Verification Framework (Elsevier, 2025)](https://www.sciencedirect.com/science/article/abs/pii/S0306457325001827)** — Uses multiple LLMs emulating the Delphi method for fact verification. Surpasses single-LLM baselines and matches supervised systems without training. Supports the principle that structured multi-agent deliberation improves trustworthiness.

- **[Detecting Hallucinations in LLMs Using Semantic Entropy (Nature, 2024)](https://www.nature.com/articles/s41586-024-07421-0)** — Proposes entropy-based detection of confabulations. Contextualizes the problem: hallucination is measurable and persistent, reinforcing why a verification step adds value even when the generator is "mostly right."

## CONFIDENCE SCORE: 7/10

The evidence clearly shows the auditor caught real errors (15% of claims in the first use) and the developer valued the pattern enough to reuse and expand it. The errors caught were citation-level (line numbers and dates, not substantive behavioral claims), there is no controlled comparison with single-agent answers, and the second use produced no visible corrections. However, external research strengthens the case: CoVe demonstrates that self-verification materially reduces hallucinations; Huang et al. show that *self*-correction is unreliable, justifying a separate auditor agent; and multi-agent debate literature confirms factual accuracy gains from cross-agent critique. The pattern likely improved answer quality at the margins while providing a larger boost to developer confidence and answer defensibility. Upgraded from 6 to 7 based on the external research alignment.

## Verdict

**PARTIALLY SUPPORTED, WITH LITERATURE BACKING.** The three-agent pipeline did catch factual errors that a single-agent answer would have included -- this is directly evidenced by the 4/27 error rate on the first use. The claim that this produced "more accurate and trustworthy answers" is only partially supported by the transcript alone: the substantive content was already correct from the researcher, and the errors caught were citation-level rather than meaning-level. However, the pattern is well-grounded in current research. The CoVe paper shows verification steps cut hallucinations by 50%+; the Huang et al. finding that LLMs cannot self-correct reasoning justifies using a *separate* auditor agent; and multi-agent debate research confirms that cross-agent critique improves factuality. The strongest transcript evidence for the pattern's value is the developer's behavioral response -- immediately reusing, expanding, and trusting the output for external stakeholders. The pattern's primary contribution was providing *verifiable confidence* rather than *dramatically different answers*, and that confidence is now supported by both observed behavior and peer-reviewed research.
