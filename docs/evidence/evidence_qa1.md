# Evidence Report: qa-1

## Hypothesis
Running Selenium QA suites as parallel background agents with structured pass/fail reporting enabled rapid detection of UI-layer regressions after multi-agent code changes, catching cross-cutting issues (avatar filename mismatches, stale name references, React state bugs, toast timing) that would otherwise have shipped in the demo.

## Type: GOOD-IDEA

## Evidence FOR

### 1. Avatar filename mismatch caught immediately
The very first Selenium QA run detected that avatar files were still named `EMP001.jpg` while code referenced `alex.santos.jpg` after multi-agent name refactoring. The assistant noted: "Found it -- the avatar files are still named EMP001.jpg etc. but the code references alex.santos.jpg etc." (line 1526). This was a direct consequence of one agent updating code references while the avatar files were untouched -- exactly the kind of cross-cutting regression multi-agent work creates.

### 2. Stale name references caught ("maria" -> "alex")
test_04 still referenced `test_04_fill_maria_request` after names were changed to gender-neutral. The Fixer-Test04 agent renamed function, call site, and result key from "maria" to "alex" (lines 2891-2894). This is a textbook stale-reference bug that Selenium surfaced.

### 3. Chrome session crash exposed infrastructure fragility
Admin tests showed 3/12 pass, 9/12 fail -- 7 failures from a Chrome session crash after test 05 (line 1582, 2129). This led to building session recovery logic (`_is_session_alive()` + `_create_driver()`) and Chrome process isolation (`--user-data-dir` via `tempfile.mkdtemp`, `--remote-debugging-port=0`) that made parallel QA reliable going forward (lines 5005, 5096).

### 4. React state sync bug caught in test_04
Selenium exposed that `execute_script` with direct `.value =` assignment does not trigger React controlled input state updates, so the submit button never became enabled (line 3150). The fix to use `nativeInputValueSetter`/`nativeSelectValueSetter` with proper event dispatching was a real UI bug that would have broken any programmatic form fill (line 3192).

### 5. Structured tabular pass/fail reporting enabled rapid triage
Every QA run produced structured tables: "12 passed, 0 failed" with per-test status (lines 2919-2937), and bug reports with numbered IDs (BUG-001 through BUG-006), severity levels (P0/P1/P2), and locations. This format was used directly for delegation -- specific fixers were assigned to specific bugs (Fixer-Avatars, Fixer-Chrome, Fixer-Test04).

### 6. Parallel execution revealed process contention
Running worker and admin QA simultaneously crashed Chrome due to shared processes. This was diagnosed specifically because of parallel execution (line 5096) and led to proper isolation (unique `--user-data-dir` + `--remote-debugging-port=0`). Sequential runs would never have surfaced this.

### 7. Multiple successful regression checks after fixes
After each round of fixes, Selenium was re-run as verification: "All 12 admin flow tests passed cleanly" (line 2919), "Chrome isolation verified -- both suites pass in parallel" (line 3807), "All 16 Selenium tests passed" (line 20702). This created a reliable gate for shipping.

### 8. Toast timing bug caught
The settings save toast had an empty `.text` property due to a timing issue where the element existed before text rendered. Selenium caught this (12/13 passed, 1 failed on test_12, line 20678). Fixed by using `textContent` fallback with wait (line 21399).

### 9. Shift selector unicode bug surfaced by user during QA cycle
While Selenium was running, the user noticed `\u` escapes in a dropdown the UI agent created (line 18325). The QA pipeline context made it natural to have another agent fix this immediately.

## Evidence AGAINST

### 1. test_04 was persistently flaky across multiple rounds
test_04 failed in Round 1 (CSS selector mismatch), was "fixed" by Fixer-Test04, but failed again in the next full run (line 3103). It required a third fix attempt (React nativeInputValueSetter, line 3180) before passing. The structured reporting showed FAIL each time but did not accelerate diagnosing the root cause -- three agents took three tries.

### 2. Parallel Chrome execution was initially counterproductive
Running both suites simultaneously caused Chrome crashes that were NOT application bugs -- they were test infrastructure bugs (shared Chrome processes). The first parallel run's admin failures (9/12 fail) were misattributed to application issues before being recognized as infrastructure contention (line 5096). This wasted a triage cycle.

### 3. The Chrome session crash masked real test results
The admin suite's Chrome crash after test 05 meant tests 06-12 were never evaluated in Round 1. The structured report showed "FAIL" for all 7, but the failure was infrastructure, not application. This created noise rather than signal for those 7 tests.

### 4. Selenium could not catch backend/data bugs
The most critical bugs -- incorrect angel scoring, coverage data not reaching the scoring code, VPE passing `None` as `object_` -- were all caught by pytest E2E tests and manual API testing, not Selenium. Selenium only tested the UI rendering layer. The hypothesis overstates what Selenium caught.

### 5. Chromedriver crash remained unfixed throughout
The `re_evaluate` scene consistently crashed chromedriver across all video generation runs (lines 21031, 21447, 21566). This was never resolved -- just worked around with fallback screenshots. The final demo shipped with 12/17 scenes (5 lost to chromedriver crash, line 21635). The QA gate detected the failure every time but could not prevent shipping with degraded output -- a limitation of detection without enforcement.

### 6. Some bugs were caught by the user, not Selenium
The broken avatar images in Chrome were first noticed by the user ("fyi images in chrome look broken", line 1822), not by the Selenium suite. The avatar 404s appeared in Selenium results too, but the user flagged them independently.

## Nuances & Caveats

### The "parallel background agents" framing is slightly misleading
The QA agents ran in parallel with each other, but they also ran in parallel with *fix agents* -- the orchestrator launched Selenium while simultaneously investigating avatar issues (line 1517). This overlapping execution was where the real speed came from, not just parallelizing the two QA suites.

### Structured reporting served delegation more than detection
The per-test pass/fail tables were most valuable for assigning fix tasks to sub-agents (e.g., "Fixer-Test04", "Fixer-Chrome", "Fixer-Avatars" at line 2963-2965). Detection was binary (something failed), but the structured format made it possible to dispatch fixes in parallel without re-reading logs.

### The QA pattern evolved significantly through the session
Early runs were ad-hoc (two QA agents with bug report markdown files). Later runs became more systematic (16-test CRITICAL_DEMO suite, background bash commands with exit codes). The final pattern (background Selenium run -> check results -> fix -> re-run) was refined through trial and error, not designed upfront.

### Selenium was most valuable for UI-layer regressions specifically
Avatar mismatches, CSS selector drift, React state sync, toast timing -- these are all UI-layer issues that unit tests and API tests would not catch. The hypothesis correctly identifies the category of bugs Selenium is good at catching, but these were not the most critical bugs in the system.

### The "would otherwise have shipped" claim is partially supported
The avatar filename mismatch and stale name references would have produced broken images and wrong names in the demo -- visible, embarrassing failures. The toast timing bug would have been invisible to most viewers. The Chrome crashes were infrastructure problems, not application bugs, and would not have affected end users.

## CONFIDENCE SCORE: 7/10

## Verdict

**SUPPORTED WITH CAVEATS.** The Selenium QA suites running as parallel background agents caught real UI-layer regressions -- avatar filename mismatches, stale name references, React state sync bugs, and toast timing issues -- that were direct consequences of multi-agent code changes. The structured pass/fail reporting was genuinely useful for delegating fixes to sub-agents in parallel. However, the hypothesis overstates the pattern's effectiveness: (1) the most critical bugs (scoring logic, VPE null handling, hard gate behavior) were caught by pytest and manual testing, not Selenium; (2) parallel execution initially created infrastructure contention (Chrome crashes) that produced misleading failure signals; (3) test_04 was persistently flaky across three fix attempts despite structured reporting; and (4) a chromedriver crash was never resolved, causing 5/17 demo scenes to ship degraded. The pattern is a genuine good idea for UI regression detection in multi-agent workflows, but it is one layer of a multi-layer testing strategy, not a standalone gate. External research corroborates both the value (AI-generated code has ~1.7x more issues, making automated gates essential) and the limitation (E2E tests alone miss logic, security, and semantic bugs that require deeper verification).

## External References

- **[Vibe Coding in Practice: Motivations, Challenges, and a Future Outlook (arXiv 2510.00328)](https://arxiv.org/abs/2510.00328)** — Grey literature review of 518 practitioner accounts finding 36% of vibe coders skip QA entirely and 18% exhibit "uncritical trust" in AI output, directly supporting the need for automated test gates.
- **[State of AI vs Human Code Generation Report (CodeRabbit, 2025)](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)** — Analysis of 470 GitHub PRs showing AI-co-authored code contains ~1.7x more issues overall, with logic errors 75% more common and security issues 2.74x higher, validating that AI-generated code needs heavier automated verification.
- **[AI Assistant Code Quality 2025 (GitClear)](https://www.gitclear.com/ai_assistant_code_quality_2025_research)** — 211M changed lines analyzed across 5 years; AI assistants drove 4x more code cloning and measurable tech debt, supporting the claim that multi-agent code changes create cross-cutting regressions.
- **[Hidden Risks of AI-Generated Code & How to Catch Them (Testkube)](https://testkube.io/blog/testing-ai-generated-code)** — Practical guide arguing AI code "looks right and passes existing tests" but fails on edge cases, recommending full test suites on every commit and snapshot testing for critical paths.
- **[Debugging AI-Generated Code: 8 Failure Patterns & Fixes (Augment Code)](https://www.augmentcode.com/guides/debugging-ai-generated-code-8-failure-patterns-and-fixes)** — Catalogs common AI code failure modes including stale references, incorrect assumptions about state, and silent regressions -- patterns matching exactly what our Selenium suite caught.
- **[Playwright MCP: AI-Powered Test Automation (TestLeaf, 2026)](https://www.testleaf.com/blog/playwright-mcp-ai-test-automation-2026/)** — Describes the Planner/Generator/Healer agent pattern for self-healing E2E tests, a more mature version of the ad-hoc QA agent pattern we evolved during the session.
- **[Beyond Vibe Coding: The Case for Spec-Driven AI Development (The New Stack)](https://thenewstack.io/vibe-coding-spec-driven/)** — Argues that vibe coding without specification and verification gates produces unreliable software, advocating for structured test gates as a necessary complement.
- **[Your AI Coding Assistants Will Overwhelm Your Delivery Pipeline (AWS, 2025)](https://aws.amazon.com/blogs/enterprise-strategy/your-ai-coding-assistants-will-overwhelm-your-delivery-pipeline-heres-how-to-prepare/)** — Enterprise perspective on how AI-generated code volume demands stronger automated gates, parallel test execution, and intelligent test selection -- all patterns relevant to our multi-agent QA approach.
- **[Vibe-Coding Meets QA: What Happens When AI Writes 30% of Your Code? (Katalon)](https://katalon.com/resources-center/blog/vibe-coding-meets-qa-what-happens-when-ai-writes-30-of-your-code-1)** — Recommends stable regression coverage on every change when using AI coding, noting that fast iteration causes regressions and non-functional quality is typically under-tested.
- **[Generative Coding: 2026 Breakthrough Technology (MIT Technology Review)](https://www.technologyreview.com/2026/01/12/1130027/generative-coding-ai-software-2026-breakthrough-technology/)** — MIT Tech Review's recognition of generative coding as a breakthrough technology, with discussion of the verification gap that automated testing must fill.
