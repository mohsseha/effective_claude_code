# Context Length Degrades LLM Performance: Why Agent Design Is Context Management

## Sources

| Source | Key Finding | URL |
|--------|------------|-----|
| **RULER** (Hsieh et al., 2024) | Only half of models claiming 32K+ context maintain satisfactory performance at 32K | https://arxiv.org/abs/2404.06654 |
| **Lost in the Middle** (Liu et al., 2024, TACL) | U-shaped accuracy: models retrieve well from beginning/end, poorly from middle | https://arxiv.org/abs/2307.03172 |
| **BABILong** (NeurIPS 2024) | Models effectively use only 10-20% of their context window | https://arxiv.org/abs/2406.10149 |
| **Many-Shot Jailbreaking** (Anthropic, 2024) | Power-law scaling of in-context effects as context grows | https://www.anthropic.com/research/many-shot-jailbreaking |
| **Gemini 1.5 Tech Report** (Google, 2024) | Even Gemini degrades on multi-needle retrieval at long contexts | https://arxiv.org/abs/2403.05530 |

---

## The Data: RULER Benchmark

The RULER benchmark (Hsieh et al., 2024) tests 13 tasks beyond simple needle-in-a-haystack, including multi-hop tracing, aggregation, and QA. Results across context lengths:

| Model | 4K | 8K | 16K | 32K | 64K | 128K | Drop |
|-------|-----|-----|------|------|------|-------|------|
| **GPT-4** | 96.6% | 96.2% | 95.6% | 93.8% | 87.0% | 81.2% | -15.4 pts |
| **Command-R 35B** | 96.8% | 95.5% | 93.8% | 87.4% | 76.3% | 59.2% | -37.6 pts |
| **Mixtral 8x7B** | 94.9% | 93.0% | 87.3% | 75.8% | 60.2% | 44.5% | -50.4 pts |
| **Mistral 7B** | 93.6% | 88.0% | 72.5% | 48.3% | 28.1% | 13.8% | -79.8 pts |

Key finding: **"Only half of the evaluated long-context models can maintain satisfactory performance at the length of 32K."**

Even GPT-4, the best performer, loses 15 points. Smaller models collapse catastrophically -- Mistral 7B goes from 94% to 14%.

---

## Lost in the Middle

Liu et al. (2024) showed a **U-shaped accuracy curve**: models retrieve information well from the beginning and end of the context, but accuracy drops 10-20% for information placed in the middle. This means:

- Position matters, not just total length
- Agents that dump everything into context are gambling on WHERE the critical info lands
- Structured, minimal context avoids the middle entirely

---

## BABILong: You're Only Using 10-20%

The BABILong benchmark (NeurIPS 2024) tested reasoning across very long contexts and found:

- Models effectively utilize only **10-20% of their claimed context window**
- RAG methods plateau at ~60% accuracy on single-fact QA regardless of context length
- Performance on multi-fact reasoning degrades much faster than single-fact retrieval

---

## The Practical Argument: Agent Design = Context Management

This data directly supports a key principle of effective Claude Code usage:

### Why subagents with small contexts beat one giant session

1. **All models degrade** -- even the best (GPT-4, Claude) lose accuracy at long contexts
2. **The degradation is task-dependent** -- complex reasoning degrades faster than simple retrieval
3. **You can't control where critical info lands** -- the "lost in the middle" effect means stuffing context is a gamble

### What this means for agent orchestration

- **Each subagent should get the minimum context needed** for its specific task
- **Don't share full conversation history** between agents -- extract and pass only what's relevant
- **Fresh agents > continued sessions** for tasks that need accuracy -- no accumulated noise
- **The orchestrator's job is context curation** -- deciding what goes in and what stays out

### The connection to meta-programming

When you design a multi-agent workflow, you're making context management decisions:
- Which spec files does this builder need? (Not all of them)
- What does the auditor need to see? (The output + the spec, not the builder's reasoning)
- What does the summarizer need? (The audited output, not the raw research)

Every agent boundary is a context boundary. Every context boundary is a quality decision.

---

## The Slide Pitch

**"Your job isn't prompt engineering. It's context engineering."**

- At 4K tokens, every model scores 93%+
- At 128K tokens, most models are below 50%
- Subagents with focused context > one session with everything
- Agent design IS context design

Chart: `assets/context-degradation.svg`
