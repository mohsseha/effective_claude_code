# Evidence Report: qa-2

## Hypothesis
The API's request deduplication (returning cached failed runs for identical payloads) created a hidden test-poisoning trap that wasted significant debugging time, because the developer and Claude chased phantom failures through container rebuilds, pytest cache clears, and endpoint probing before discovering the stale run was being returned by design.

## Type: BAD-IDEA

## Evidence FOR

### 1. The null-shift-id debugging sequence (lines 21836-21905)
After fixing the actual bug (null `shift_id` causing optimizer crash), Claude went through this sequence before identifying deduplication as the culprit:
- **Step 1**: Rebuilt orchestrator container, reran tests -- "Still failing" (line 21845)
- **Step 2**: Checked container logs for errors -- found nothing (lines 21848-21851)
- **Step 3**: Hypothesized "container may not have picked up the change yet" -- reran test -- still failing (line 21854-21857)
- **Step 4**: Hypothesized "module-scoped fixture is cached" -- ran with `--cache-clear` -- still failing (lines 21860-21863)
- **Step 5**: Hypothesized "run store has the failed run cached" -- manually curled the API with a new run_id (line 21866-21869)
- **Step 6**: Probed three different endpoints (`/runs/`, `/requests/`, `/status/`) trying to understand the state (lines 21872-21878)
- **Step 7**: Checked orchestrator logs again (line 21881)
- **Step 8**: Read the test file (line 21887)
- **Step 9**: Finally curled POST directly and got `"Duplicate request -- returning cached run."` (line 21893-21896)

That is **9 distinct debugging steps** and at least **13 tool invocations** spanning from container rebuilds to pytest cache clears to endpoint probing before the real cause was identified. The fix was trivially reseeding data (1 command).

### 2. The same trap hit earlier with Riley (line 1802)
A summary note documents: "**Cached run preventing retest**: After fixing, resubmitting Riley got 'Duplicate request -- returning cached run.' Fixed by reseeding data to clear cache." This was a separate earlier incident, meaning the deduplication trap was hit **at least twice** across the project.

### 3. Deduplication was identified as a blocker for the weight-change demo feature (lines 16077-16089)
The analysis found: "**Blocker: Gateway cache.** If you resubmit the same request after changing weights, the gateway returns the cached old result." This meant the entire Big Dial demo (the product's key differentiator -- changing angel weights and seeing outcomes change) could not work until cache bypass was implemented. The gap was explicitly noted: "No test submits the SAME request under different weights to verify outcome flip -- Needs the cache bypass before this test can work."

### 4. Deduplication cached FAILED runs, not just successful ones
The most pernicious aspect: the cache returned a **failed** run from a previous bug. A well-designed dedup system might only cache successful outcomes. Caching failures means that fixing a bug does not fix the user experience until the cache is manually cleared -- a silent, invisible trap.

### 5. The workaround (reseeding) was a blunt instrument
The fix each time was `python scripts/seed_demo_data.py` -- a full data reseed that wipes and recreates everything. This is not a targeted fix for cache invalidation; it is a nuclear option that masks the underlying design problem.

## Evidence AGAINST

### 1. The re-evaluate endpoint was eventually built as a proper solution (lines 16307-16388)
Rather than just patching the cache, a `POST /runs/{run_id}/re-evaluate` endpoint was built (~60 lines + tests). This reuses existing angel scores with current weights, which is actually a more sophisticated solution than cache bypass alone. The deduplication problem forced the team to build a better abstraction.

### 2. Deduplication serves a legitimate purpose for the frontend (line 19626-19629)
The H2 finding explicitly notes that the backend's "cache-hit deduplication mechanism" protects against double-submit race conditions on the frontend. Without it, fast double-clicks could create duplicate runs "cluttering the clean demo narrative."

### 3. Claude identified the root cause in a single conversation
While the debugging sequence involved 9 steps, it all happened within one continuous session. There is no evidence of this spanning multiple conversations or days. The total wall-clock time was likely 10-20 minutes (based on the tool call cadence).

### 4. The deduplication behavior was documented in the system architecture (line 556)
The `gateway_cache` table was listed in the system's data architecture documentation. It was not a secret or undocumented feature.

### 5. skip_cache was identified as a simple fix (line 16078)
When the problem was clearly diagnosed, the recommended fix was "~10 lines" -- add a `skip_cache=true` param to `POST /requests`. The problem was not architecturally intractable.

## Nuances & Caveats

1. **The debugging sequence looks worse than it was.** Claude first suspected the container hadn't rebuilt, then pytest caching, then module-scoped fixtures -- all reasonable hypotheses to check before suspecting the API itself was deduplicating. The confusion was that the test's POST request was returning a stale run_id, which looks identical to a container-not-rebuilt scenario from the test's perspective.

2. **Caching failed runs is the real anti-pattern, not deduplication itself.** If the gateway only cached completed/successful runs, the null-shift-id debugging loop would not have occurred. The fix went through but the test kept getting the old *failed* result -- that is the poisonous behavior.

3. **This is a recurring pattern in the project.** The `__pycache__` staleness (line 2395) caused a similar "fixture not found" false failure. The `run_id`-in-prompt anti-pattern (line 15681) effectively disabled LLM caching by accident. Stale state was a systemic theme, not isolated to gateway deduplication.

4. **The Riley incident (earlier) should have been a warning.** The fact that deduplication was hit once with Riley (line 1802) and then hit again with the null-shift-id test suggests a failure to learn from the first incident. No `skip_cache` parameter or test-mode cache bypass was added after the first occurrence.

5. **The weight-change blocker was the most consequential impact.** The debugging time itself was modest, but the architectural implication -- that the product's flagship demo feature (Big Dial) could not work without cache bypass -- was a more significant consequence of the deduplication design.

## CONFIDENCE SCORE: 7/10

The core claim holds: caching failed runs created a debugging trap hit at least twice, and the same design blocked the Big Dial demo feature. The "significant debugging time" framing slightly overstates -- total time across both incidents was likely 20-40 minutes, not hours. External research confirms that caching error responses in idempotency systems is a recognized anti-pattern (Stripe explicitly caches all outcomes but expires keys after 24 hours; the IETF draft defers error-caching policy to implementers, implying it is not obvious). The report's analysis aligns with established literature on test pollution from shared mutable state.

## Verdict

**PARTIALLY CONFIRMED.** The deduplication feature did create a test-poisoning trap hit at least twice, and Claude did chase phantom failures through container rebuilds, pytest cache clears, and endpoint probing before identifying the real cause. The "significant debugging time" framing is somewhat exaggerated -- each episode resolved in one session. The deeper problem was not deduplication per se but caching *failed* runs without expiry or bypass, which turned a useful idempotency mechanism into a silent test-poisoning trap. The most consequential impact was the architectural blocker it created for the Big Dial demo feature, which required building a dedicated re-evaluate endpoint to work around. External literature validates this as a known class of bug: Fowler's "Eradicating Non-Determinism in Tests" identifies shared persistent state as the top cause of test pollution, and Stripe's own idempotency design includes a 24-hour key expiry specifically to prevent indefinite stale caching.

## External References

- **[Eradicating Non-Determinism in Tests](https://martinfowler.com/articles/nonDeterminism.html)** -- Fowler identifies shared persistent state (including databases and caches) as the #1 cause of test pollution; recommends rebuilding state fresh per test or using transaction rollback.
- **[Stripe API: Idempotent Requests](https://docs.stripe.com/api/idempotent_requests)** -- Stripe caches results "regardless of whether it succeeds or fails" but expires keys after 24 hours; demonstrates that even when caching errors, a TTL prevents indefinite poisoning.
- **[Designing Robust and Predictable APIs with Idempotency (Stripe Blog)](https://stripe.com/blog/idempotency)** -- Describes Stripe's retry-safe idempotency design with exponential backoff; cached results are returned for completed operations to prevent duplicate side effects.
- **[Implementing Stripe-like Idempotency Keys in Postgres](https://brandur.org/idempotency-keys)** -- Reference implementation storing both success and failure outcomes; recommends a reaper process to delete keys after ~72 hours to prevent stale cache accumulation.
- **[IETF Draft: Idempotency-Key HTTP Header](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header)** -- Proposed standard says servers "SHOULD respond with the result of the previously completed operation, success or an error" but defers expiry policy to implementers, implying no consensus on caching errors indefinitely.
- **[Making Retries Safe with Idempotent APIs (AWS Builders' Library)](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)** -- AWS pattern: use caller-provided tokens with atomic transactions; emphasizes returning semantically equivalent responses (not "AlreadyExists" errors) to avoid changing client execution flow.
- **[pytest Fixture Documentation: Scoping and Teardown](https://docs.pytest.org/en/latest/how-to/fixtures.html)** -- Documents how module/session-scoped fixtures create shared state risk; recommends function-scope default and yield fixtures for guaranteed cleanup.
- **[Tests That Sometimes Fail (Sam Saffron)](https://samsaffron.com/archive/2019/05/15/tests-that-sometimes-fail)** -- Practical catalog of flaky test causes including leaked global state and database sequence collisions; advocates random test ordering to surface hidden dependencies.
- **[TOTT: Avoiding Flakey Tests (Google Testing Blog)](https://testing.googleblog.com/2008/04/tott-avoiding-flakey-tests.html)** -- Google's guidance on test isolation: use unique resources per test, prefer dependency injection over shared state, mock external systems to eliminate cross-test interference.
