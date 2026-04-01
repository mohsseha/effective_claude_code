# Claude Code Agent Management: Practical Command Reference

A hands-on guide to spawning, controlling, and orchestrating agents in Claude Code. Covers subagents (production), agent teams (experimental), and the exact phrasing that works (and doesn't) when telling Claude Code to delegate.

---

## Table of Contents

1. [Subagents (Agent Tool)](#1-subagents-agent-tool)
2. [Agent Teams (Experimental)](#2-agent-teams-experimental)
3. [Do's and Don'ts -- Practical Phrasing](#3-dos-and-donts----practical-phrasing)
4. [Sources](#4-sources)

---

## 1. Subagents (Agent Tool)

Subagents are child Claude instances spawned within a single session. Each gets its own context window, custom system prompt, and configurable tool access. Results return to the parent conversation as a summary. **Production-ready.**

### 1.1 Spawning a Subagent

There are four ways to invoke a subagent, from least to most explicit:

| Method | Syntax | Guarantees invocation? |
|--------|--------|----------------------|
| **Automatic** | Just describe the task; Claude delegates if it matches a subagent's `description` | No -- Claude decides |
| **Natural language** | `Use the code-reviewer subagent to look at my changes` | Usually -- Claude still decides |
| **@-mention** | `@"code-reviewer (agent)" review auth module` | **Yes** -- guaranteed |
| **Session-wide** | `claude --agent code-reviewer` (CLI flag) | **Yes** -- entire session runs as that agent |

### 1.2 Giving a Subagent a Specific Task, Personality, or Perspective

**Option A: Custom agent file** (persistent, reusable)

Create `.claude/agents/security-reviewer.md`:

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: dontAsk
memory: project
---

You are a senior security engineer. Focus exclusively on:
- Authentication and authorization flaws
- Input validation gaps
- Secret exposure
- Injection vulnerabilities

Report findings by severity: Critical > Warning > Info.
```

**Option B: Inline via CLI** (ephemeral, one session only)

```bash
claude --agents '{
  "security-reviewer": {
    "description": "Security-focused code reviewer",
    "prompt": "You are a senior security engineer. Focus on auth flaws, injection, secret exposure.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "perf-reviewer": {
    "description": "Performance-focused code reviewer",
    "prompt": "You are a performance engineer. Focus on N+1 queries, memory leaks, unnecessary allocations.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "haiku"
  }
}'
```

**Option C: Natural language in conversation** (ad hoc)

```
Start 2 agents to look at this issue independently:
- Agent A: focus on security implications
- Agent B: focus on performance impact
Have them research independently and report findings.
```

This works. Claude creates two general-purpose subagents with the system prompts you described. From real usage transcript:

> **User:** "startt 2 agents to look at this issue of how the system is setup... I want them indidependently resarch this and then audit each others work"
>
> **Claude:** `[Tool: Agent - Agent A: system setup research]` `[Tool: Agent - Agent B: system setup research]` "Both agents are running in the background researching independently."

### 1.3 Running Multiple Agents in Parallel

Just ask for it. Claude spawns them as background tasks automatically when given parallel work:

```
Research the authentication, database, and API modules in parallel using separate subagents
```

Or be more explicit:

```
Launch 3 background agents:
1. Agent A: audit all deployment scripts in run/ and scripts/
2. Agent B: audit all Docker configurations
3. Agent C: audit all environment variable usage
Run them in parallel. Compile results when all finish.
```

### 1.4 Naming Agents and Sending Messages

Agents are automatically named based on the task description Claude gives them. You can see names in the tool invocation: `[Tool: Agent - Agent A: system setup research]`.

**Resuming / messaging a completed agent:**

Claude tracks agent IDs internally. To continue a subagent's work:

```
Continue that code review and now analyze the authorization logic
```

Claude uses `SendMessage` with the agent's ID to resume it with full conversation history intact.

**Transcript location:** `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`

### 1.5 Foreground vs Background

| Mode | Behavior | Permissions | When to use |
|------|----------|------------|-------------|
| **Foreground** | Blocks parent conversation | Permission prompts pass through to you | Interactive tasks, tasks needing clarification |
| **Background** | Runs concurrently | Must be pre-approved at launch; auto-denied otherwise | Long-running tasks, parallel research |

**To background a running agent:** Press `Ctrl+B`

**To force background in agent definition:**
```yaml
---
name: test-runner
background: true
---
```

**To ask Claude to run in background:**
```
Run this in the background
```

**To disable all background tasks:**
```bash
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1
```

### 1.6 Isolation with Git Worktrees

Add `isolation: worktree` to the agent's frontmatter:

```yaml
---
name: feature-builder
description: Implements features in isolated branches
isolation: worktree
tools: Read, Write, Edit, Bash, Grep, Glob
---
```

This gives the subagent a temporary copy of the repository. The worktree is automatically cleaned up if the subagent makes no changes. This prevents file conflicts when multiple agents write code simultaneously.

You can also manually create worktrees for parallel interactive sessions:

```bash
claude -w feature-auth    # creates worktree at .claude/worktrees/feature-auth
claude -w bugfix-123      # separate worktree, separate branch
```

### 1.7 Key Configuration Fields (Full Reference)

| Field | What it controls | Example |
|-------|-----------------|---------|
| `name` | Unique identifier (lowercase + hyphens) | `code-reviewer` |
| `description` | When Claude should delegate (critical for auto-delegation) | `"Reviews code for quality. Use proactively after changes."` |
| `tools` | Tool allowlist | `Read, Grep, Glob, Bash` |
| `disallowedTools` | Tool denylist (removed from inherited set) | `Write, Edit` |
| `model` | `sonnet`, `opus`, `haiku`, full model ID, or `inherit` | `haiku` |
| `permissionMode` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` | `dontAsk` |
| `maxTurns` | Cap on agentic loop iterations | `20` |
| `skills` | Preload skill content into context | `[api-conventions, error-handling]` |
| `mcpServers` | Scope MCP servers to this subagent | See docs |
| `hooks` | Lifecycle hooks (PreToolUse, PostToolUse, Stop) | See docs |
| `memory` | Persistent memory: `user`, `project`, or `local` | `project` |
| `background` | Always run as background task | `true` |
| `isolation` | Git worktree isolation | `worktree` |

### 1.8 Common Mistakes / Things That Don't Work

| Mistake | Why it fails |
|---------|-------------|
| Expecting subagents to talk to each other | Subagents only report back to the parent. They cannot message peers. From transcript: "Since there's no multi-agent SendMessage tool available, I'll deliver the full analysis directly." |
| Expecting subagents to spawn subagents | No nesting. Subagents cannot spawn other subagents. |
| Spawning many detailed subagents | Each result returns to the parent's context. Many detailed results blow up the parent's context window. |
| Forgetting background agents can't ask questions | Background agents auto-deny permission prompts not pre-approved. They also cannot ask clarifying questions. |
| Not restarting session after creating agent file | Subagents are loaded at session start. Use `/agents` to reload without restarting. |

### 1.9 Managing Subagents with /agents

The `/agents` command provides an interactive interface:

```
/agents          # in-session: view, create, edit, delete agents
claude agents    # CLI: list all configured agents without starting a session
```

---

## 2. Agent Teams (Experimental)

Multiple independent Claude Code instances coordinating as a team. One session is the **team lead**; it spawns **teammates** that work in parallel, communicate directly with each other, and share a task list.

### 2.1 Enabling Agent Teams

Add to your `settings.json` (project or user level):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Requires Claude Code **v2.1.32+**. Check: `claude --version`.

### 2.2 Creating a Team

Just tell Claude what team you want in natural language:

```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

Claude creates the team, spawns teammates, and coordinates. You confirm before it proceeds.

**Specifying models and count:**

```
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

**Requiring plan approval:**

```
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

The teammate works in read-only plan mode until the lead approves their approach.

### 2.3 Shared Task List and Messaging

| Component | How it works |
|-----------|-------------|
| **Task list** | Shared work items with states: pending, in-progress, completed. Supports dependencies. File-lock based claiming prevents race conditions. |
| **Message** | Send to one specific teammate |
| **Broadcast** | Send to all teammates (costs scale with team size -- use sparingly) |
| **Idle notifications** | Teammate auto-notifies lead when it finishes |
| **Self-claim** | After finishing a task, teammate picks up next unassigned, unblocked task |

**Storage locations:**
- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`

### 2.4 Display Modes

| Mode | How it works | Setup needed |
|------|-------------|-------------|
| `in-process` | All teammates in main terminal. `Shift+Down` to cycle. | None |
| `tmux` / `auto` | Each teammate in own split pane. Click to interact. | tmux or iTerm2 with `it2` CLI |

Set via settings:
```json
{ "teammateMode": "in-process" }
```

Or CLI flag:
```bash
claude --teammate-mode in-process
```

**In-process controls:**
- `Shift+Down` -- cycle through teammates
- `Enter` -- view a teammate's session
- `Escape` -- interrupt a teammate's current turn
- `Ctrl+T` -- toggle the task list

### 2.5 Controlling the Team

| Action | How |
|--------|-----|
| **Assign tasks** | Tell the lead what to assign to whom, or let teammates self-claim |
| **Talk to teammate directly** | `Shift+Down` (in-process) or click pane (split) |
| **Require plan approval** | Tell lead at spawn time; teammate stays read-only until lead approves |
| **Redirect a teammate** | Navigate to them and type new instructions |
| **Shut down a teammate** | `"Ask the researcher teammate to shut down"` -- teammate can approve or reject |
| **Clean up team** | `"Clean up the team"` -- always use the lead to clean up, shut down teammates first |
| **Keep lead from doing work itself** | `"Wait for your teammates to complete their tasks before proceeding"` |

### 2.6 Quality Gates via Hooks

| Hook | When it fires | Exit code 2 effect |
|------|--------------|-------------------|
| `TeammateIdle` | Teammate about to go idle | Sends feedback, keeps teammate working |
| `TaskCompleted` | Task being marked complete | Prevents completion, sends feedback |

### 2.7 Limitations and Gotchas

| Limitation | Detail |
|-----------|--------|
| **No session resumption** for in-process teammates | `/resume` and `/rewind` don't restore them. Lead may try to message dead teammates. Tell it to spawn new ones. |
| **Task status can lag** | Teammates sometimes fail to mark tasks complete, blocking dependents. Nudge manually. |
| **Shutdown is slow** | Teammates finish current request before stopping. |
| **One team per session** | Clean up before starting another. |
| **No nested teams** | Teammates cannot spawn their own teams. |
| **Lead is fixed** | No promotion/transfer during team lifetime. |
| **Permissions set at spawn** | All teammates inherit lead's mode. Can change per-teammate after, not at spawn. |
| **Split panes not supported** in VS Code terminal, Windows Terminal, or Ghostty | Use in-process mode instead. |
| **Lead may do work itself** | Common problem. Explicitly tell it to delegate (see phrasing guide below). |
| **Token costs scale linearly** | Each teammate has its own full context window. Budget accordingly. |

### 2.8 Recommended Team Sizing

| Team size | Best for |
|-----------|----------|
| **3-5 teammates** | Most workflows. Sweet spot for parallelism vs coordination overhead. |
| **5-6 tasks per teammate** | Keeps everyone productive without excessive context switching. |
| **Beyond 6 teammates** | Diminishing returns. Coordination overhead dominates. |

---

## 3. Do's and Don'ts -- Practical Phrasing

### 3.1 Delegation Phrasing That Works

These are real phrases from production usage that successfully got Claude Code to delegate work to agents rather than doing it itself.

#### DO: Phrases That Work

| Phrase | Why it works |
|--------|-------------|
| `"Start 2 agents to look at this independently"` | Clear count, clear independence. Claude spawns two background agents immediately. |
| `"Launch 3 background agents: 1. [task] 2. [task] 3. [task]"` | Numbered list with explicit "background" keyword. Unambiguous. |
| `"Have them debate with each other to come up with a recommendation"` | Sets up adversarial dynamic. Agents produce competing proposals. |
| `"Run them in parallel. Compile results when all finish."` | Explicit parallel + compile pattern. |
| `"Use the code-reviewer subagent to look at my changes"` | Names a specific subagent. High delegation rate. |
| `@"code-reviewer (agent)" review auth module` | @-mention. Guaranteed invocation. |
| `"Delegate all hands-on work to [agent name]"` | Role assignment within a team structure. |
| `"Wait for your teammates to complete their tasks before proceeding"` | Prevents lead from doing work itself. |
| `"dude have an agent do the work don't do it yourself"` | Direct, unambiguous. Works. (Real transcript.) |
| `"all work needs to be done by agents, you will only supervise"` | Sets supervisor-only mode for the session. (Real transcript, used repeatedly.) |
| `"create agent as appropriate"` | Gives Claude permission to delegate freely. |
| `"Five agents running in background"` with a status table | Claude confirms delegation with a table showing agent/task/status. Good pattern. |

#### DON'T: Phrases That Cause Problems

| Phrase | What goes wrong |
|--------|----------------|
| `"Can you look into this?"` | Claude does the work itself. No delegation signal. |
| `"Research this topic"` | Too vague. Claude may delegate to Explore or just do it itself. |
| `"Have agents discuss among themselves"` | Subagents **cannot** message each other. Only agent teams support peer communication. Claude may fake it by running them sequentially. |
| `"Let them audit each other's work"` | With subagents, each agent runs independently. They don't see each other's output. The parent synthesizes. |
| Describing a 9-agent team structure without using agent teams | Claude will try to spawn 9 subagents, but subagents can't communicate. You need agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) for peer coordination. |
| `"Don't be too prescriptive with agent instructions"` | Can backfire -- agents with vague instructions produce vague results. |
| Not specifying "background" | Claude may run agents in foreground (blocking), serializing what should be parallel. |

### 3.2 Structuring a Multi-Agent Workflow Prompt

Here is a battle-tested prompt structure from real usage that successfully coordinated multiple agents:

```
## Team Structure

1. Lead Agent: Coordinates the team but does as little direct work as
   possible. Routes tasks, unblocks agents, keeps the loop moving.
   Delegates all hands-on work to agents.

2. [Role] Agent: [Specific task and boundaries].
   [What tools/files they should use].

3. [Role] Agent: [Specific task and boundaries].
   [What tools/files they should use].

## Workflow

1. [Agent A] does [task]
2. [Agent B] does [task] in parallel
3. When both finish, [Agent C] synthesizes
4. Repeat until [exit condition]

## Constraints

- Each builder works in an isolated git worktree (not main branch)
- Auditors are READ-ONLY -- they reject or approve, never edit
- All work needs to be done by agents, you will only supervise
```

### 3.3 Forcing Claude to NOT Do Work Itself

This is the single most common friction point. Claude's default behavior is to do work itself rather than delegate. Here are the escalating levels of instruction:

| Level | Instruction | Reliability |
|-------|------------|-------------|
| 1. Gentle | `"Use agents for this"` | ~60% -- Claude often still does some work |
| 2. Explicit | `"Launch background agents for all tasks. Do not do the work yourself."` | ~80% |
| 3. Role-based | `"You are the lead. Your only job is to coordinate agents. Delegate ALL hands-on work."` | ~90% |
| 4. Confrontational | `"dude have an agent do the work don't do it yourself"` | ~95% (real transcript) |
| 5. Session rule | `"all work needs to be done by agents, you will only supervise"` at session start | ~95% (real transcript, set as persistent instruction) |
| 6. CLAUDE.md rule | Add to `.claude/CLAUDE.md`: `"Always delegate implementation work to subagents. The main conversation should only coordinate and synthesize."` | ~98% -- persists across sessions |

From real transcripts, the user had to repeatedly escalate:
- `"also leader i see you are doing a lot of work yourself didn't we tell you to have a deputy do your long running task ??????!!!!!!!!!!!!!!!!!!!!"`
- `"delegate"` (x3)
- `"create agent as appropriate"`

The pattern that finally stuck was establishing the rule at session start and reinforcing in CLAUDE.md.

### 3.4 DO/DON'T Quick Reference Table

| DO | DON'T |
|----|-------|
| Name specific agents or roles | Say "look into this" without delegation signal |
| Say "background" explicitly for parallel work | Assume Claude will parallelize |
| Number your agents (Agent 1, Agent 2...) | Give a vague blob of tasks |
| Set "you will only supervise" as a session rule | Hope Claude will delegate on its own |
| Use @-mentions for guaranteed invocation | Rely on automatic delegation for critical paths |
| Give each agent a distinct, non-overlapping scope | Have agents work on the same files |
| Use `isolation: worktree` when agents write code | Let multiple agents edit the same files |
| Start with 3-5 agents | Spawn 10+ agents (diminishing returns, high cost) |
| Use agent teams when peers need to communicate | Use subagents when you need peer-to-peer messaging |
| Use subagents for focused tasks with summary return | Use agent teams for simple parallelizable work |
| Put delegation rules in CLAUDE.md | Rely on per-message instructions only |
| Use `permissionMode: dontAsk` for background agents | Forget to pre-approve permissions for background work |
| Check on agent progress periodically | Let a team run unattended for too long |

### 3.5 Example: Complete Multi-Agent QA Workflow

This is adapted from a real production session that ran 9 agents for QA testing:

```
The system is deployed. Manual testing failed. We need automated QA.

All testing happens through Selenium -- agents drive a real browser
against the live system. No shortcuts.

Agents:

1. Lead Agent: Coordinates but does as little direct work as possible.
   Routes tasks, unblocks agents. Delegates all hands-on work.

2. Startup Agent: Brings up the full system. Verifies it's running
   before QA begins. Stays available to restart between test rounds.

3. QA Worker Agent: Runs worker-facing Selenium tests. Reports bugs in
   structured format.

4. QA Admin Agent: Runs admin-facing Selenium tests. Reports bugs in
   structured format.

5. Fixer Agent: Receives bugs from QA agents. Debugs and patches.
   Minimal fixes -- patch, don't rebuild.

6. VoCA Agent: Product owner. Writes non-negotiable requirements.
   Triages bugs (major only get fixed).

Workflow:
1. Startup Agent brings system up
2. Both QA agents test via Selenium simultaneously
3. Bug reports flow in -> VoCA triages (major only)
4. Fixer patches while QA keeps testing
5. Repeat until no major bugs remain
6. One QA agent runs demo script end to end

All work needs to be done by agents, you will only supervise.
```

---

## 4. Sources

### Official Documentation

| Resource | URL |
|----------|-----|
| Claude Code docs home | https://code.claude.com/docs/en/overview |
| Subagents (create custom) | https://code.claude.com/docs/en/sub-agents |
| Agent teams | https://code.claude.com/docs/en/agent-teams |
| CLI reference | https://code.claude.com/docs/en/cli-reference |
| Tools reference | https://code.claude.com/docs/en/tools-reference |
| Interactive mode | https://code.claude.com/docs/en/interactive-mode |
| Common workflows (worktrees) | https://code.claude.com/docs/en/common-workflows |
| Hooks | https://code.claude.com/docs/en/hooks |
| Permissions | https://code.claude.com/docs/en/permissions |
| Settings | https://code.claude.com/docs/en/settings |
| Skills | https://code.claude.com/docs/en/skills |
| Plugins | https://code.claude.com/docs/en/plugins |
| Environment variables | https://code.claude.com/docs/en/env-vars |
| Model configuration | https://code.claude.com/docs/en/model-config |
| How Claude Code works | https://code.claude.com/docs/en/how-claude-code-works |

### Case Studies and Blog Posts

| Resource | URL |
|----------|-----|
| Building a C Compiler with Agent Teams (Anthropic engineering) | https://www.anthropic.com/engineering/building-c-compiler |
| 2026 Agentic Coding Trends Report | https://resources.anthropic.com/2026-agentic-coding-trends-report |

### Local Reference Files

| File | What it contains |
|------|-----------------|
| `/Users/husainal-mohssen/src/effective_claude_code/agent_modes.md` | Comprehensive comparison of single session vs subagents vs agent teams |
| `/Users/husainal-mohssen/src/effective_claude_code/cc-transcript-filtered.md` | Real session transcripts showing multi-agent workflows in practice |

---

*Last updated: 2026-03-19*
