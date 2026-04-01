# Claude Code Agent Modes: Reference Guide

Three distinct modes for parallelizing and orchestrating work in Claude Code, from simplest to most complex.

---

## 1. Single Interactive Session

**What it is:** One Claude Code process, one context window, one conversation. The default `claude` experience.

### How it works

Claude operates in an **agentic loop**: gather context -> take action -> verify results, repeating until the task is done. Each loop iteration uses tools (file read/write, shell, search, web) and feeds results back into the next decision. You can interrupt at any point to steer.

Sessions are auto-saved to `~/.claude/projects/{project}/`. Context window fills with conversation history, file contents, command outputs, CLAUDE.md, loaded skills, and system instructions. When context fills up, Claude auto-compacts -- older tool outputs are cleared first, then conversation is summarized.

### Session management

| Command | What it does |
|---|---|
| `claude` | New session |
| `claude -c` / `--continue` | Continue most recent conversation in current directory |
| `claude -r <id-or-name>` / `--resume` | Resume specific session by ID or name |
| `claude --fork-session` | Branch off a resumed session into a new ID (original unchanged) |
| `claude -n "name"` / `--name` | Name a session at start |
| `/rename <name>` | Rename mid-session |
| `/context` | See what's consuming context |
| `/compact [focus]` | Manually compact with optional focus area |

Sessions are tied to directories. Switching git branches changes visible files but keeps conversation history intact.

### When to use

- Most tasks. Single session handles the vast majority of work.
- Anything requiring tight back-and-forth iteration.
- Tasks where phases share significant context (plan -> implement -> test).
- Quick, targeted changes where subagent startup overhead isn't worth it.

### Limitations

- One context window (~200K tokens effective). Long sessions degrade as compaction loses early instructions.
- Sequential execution only -- Claude does one thing at a time.
- Context pollution from verbose tool outputs (test suites, log dumps).

### Running parallel single sessions manually

Use **git worktrees** to run multiple independent Claude sessions on the same repo without file conflicts:

```bash
claude -w feature-auth    # creates worktree at .claude/worktrees/feature-auth
claude -w bugfix-123      # separate worktree, separate branch
```

Each worktree gets its own copy of the codebase. No coordination between sessions -- you are the orchestrator. Worktrees with no changes are auto-cleaned on exit.

### Docs

- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode)
- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Common workflows (worktrees)](https://code.claude.com/docs/en/common-workflows)

---

## 2. Subagents (Agent Tool)

**What it is:** Spawning child Claude instances within a single session. Each subagent gets its own context window, custom system prompt, and configurable tool access. Results return to the parent conversation.

### How it works

When Claude encounters a task matching a subagent's description, it delegates via the **Agent tool** (formerly called Task tool, renamed in v2.1.63). The subagent runs independently in its own context, does its work, and returns a summary to the parent. The parent's context only sees the summary, not the subagent's full transcript.

Key constraint: **subagents cannot spawn other subagents**. No nesting. The parent is always the orchestrator.

### Built-in subagents

| Subagent | Model | Tools | Purpose |
|---|---|---|---|
| **Explore** | Haiku | Read-only | Fast codebase search/analysis. Three thoroughness levels: quick, medium, very thorough |
| **Plan** | Inherits | Read-only | Research agent for plan mode |
| **General-purpose** | Inherits | All | Complex multi-step tasks requiring both reading and writing |
| **Bash** | Inherits | Bash | Terminal commands in separate context |

### Custom subagents

Defined as Markdown files with YAML frontmatter. Three scopes:

| Location | Scope | Priority |
|---|---|---|
| `--agents` CLI flag (JSON) | Current session only | Highest |
| `.claude/agents/` | Project (check into VCS) | 2 |
| `~/.claude/agents/` | All projects (personal) | 3 |
| Plugin `agents/` dir | Where plugin is enabled | Lowest |

Example file at `.claude/agents/code-reviewer.md`:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices. Use proactively after code changes.
tools: Read, Glob, Grep, Bash
model: sonnet
permissionMode: dontAsk
memory: project
---

You are a senior code reviewer. Focus on quality, security, best practices.
Analyze git diff, review modified files, report by priority.
```

### Key configuration fields

| Field | What it controls |
|---|---|
| `tools` / `disallowedTools` | Tool allowlist/denylist |
| `model` | `sonnet`, `opus`, `haiku`, full model ID, or `inherit` |
| `permissionMode` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | Cap on agentic loop iterations |
| `skills` | Preload skill content into subagent context |
| `mcpServers` | Scope MCP servers to this subagent (inline or reference) |
| `hooks` | Lifecycle hooks (PreToolUse, PostToolUse, Stop) |
| `memory` | Persistent memory: `user`, `project`, or `local` scope |
| `background` | `true` to always run as background task |
| `isolation` | `worktree` for git worktree isolation |

### Foreground vs background

- **Foreground**: blocks parent conversation. Permission prompts pass through to you.
- **Background**: runs concurrently. Permissions must be pre-approved at launch (auto-denied otherwise). Press **Ctrl+B** to background a running subagent.

### Invocation patterns

1. **Automatic**: Claude delegates based on description match.
2. **Natural language**: "Use the code-reviewer subagent to look at my changes."
3. **@-mention**: `@"code-reviewer (agent)" review auth module` -- guarantees invocation.
4. **Session-wide**: `claude --agent code-reviewer` -- entire session runs as that subagent.

### Resuming subagents

Subagents can be resumed (they retain full conversation history). Claude uses `SendMessage` with the agent's ID. Transcripts stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`.

### Restricting subagent spawning

In an agent's `tools` field: `Agent(worker, researcher)` limits which subagent types can be spawned. `Agent` without parens allows all. Omitting `Agent` entirely prevents spawning.

### When to use

- Task produces verbose output you don't want in main context (test runs, log analysis).
- Work is self-contained and only the result matters.
- You want to enforce tool restrictions (read-only reviewer, no-write debugger).
- Parallel research on independent topics.
- Cost optimization: route simple tasks to Haiku.

### When NOT to use

- Workers need to communicate with each other (use agent teams).
- Task requires frequent back-and-forth with you.
- Latency-sensitive -- subagents start fresh and need time to gather context.
- For a quick question about current context, use `/btw` instead (no tools, ephemeral).

### Limitations

- No nesting. Subagents cannot spawn subagents.
- Results returning to parent consume parent context. Many detailed subagent results can blow up context.
- Background subagents cannot ask clarifying questions.
- Plugin subagents cannot use `hooks`, `mcpServers`, or `permissionMode` frontmatter.

### Docs

- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Tools reference](https://code.claude.com/docs/en/tools-reference)
- [Skills (related)](https://code.claude.com/docs/en/skills)

---

## 3. Agent Teams

**What it is:** Multiple independent Claude Code instances coordinating as a team. One session is the **team lead**; it spawns **teammates** that work in parallel, communicate directly with each other, and share a task list. Each teammate is a full Claude Code session with its own context window.

### Status: Experimental

Disabled by default. Enable via settings or environment:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Requires Claude Code v2.1.32+.

### How it works

**Architecture:**

| Component | Role |
|---|---|
| Team lead | Main session. Creates team, spawns teammates, coordinates, synthesizes |
| Teammates | Separate Claude Code instances. Work on assigned tasks independently |
| Task list | Shared work items with states: pending, in-progress, completed. Supports dependencies. File-lock based claiming |
| Mailbox | Direct inter-agent messaging system |

**Key difference from subagents:** Teammates message each other directly. They don't have to route through the lead. They share a task list and self-coordinate. Subagents only report back to parent.

**Storage:**
- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`

### Display modes

| Mode | How it works | Requirement |
|---|---|---|
| `in-process` | All teammates in main terminal. Shift+Down to cycle. Works anywhere | None |
| `tmux` / `auto` | Each teammate in own split pane. Click to interact | tmux or iTerm2 with `it2` CLI |

Set via `--teammate-mode` flag or `teammateMode` in settings.json.

### Starting a team

Natural language to the lead:

```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

Claude creates the team, spawns teammates, and coordinates. You confirm before it proceeds.

### Controlling the team

- **Assign tasks**: Tell the lead what to assign to whom, or let teammates self-claim from the shared list.
- **Talk to teammates directly**: Shift+Down (in-process) or click pane (split). Full interaction with any teammate.
- **Require plan approval**: Teammate works in read-only plan mode until lead approves. Lead makes approval decisions autonomously based on criteria you set.
- **Shut down teammates**: "Ask the researcher teammate to shut down." Teammate can approve or reject.
- **Clean up**: "Clean up the team." Always use the lead to clean up. Shut down teammates first.

### Quality gates via hooks

| Hook | When it fires | Use |
|---|---|---|
| `TeammateIdle` | Teammate about to go idle | Exit code 2 sends feedback, keeps teammate working |
| `TaskCompleted` | Task being marked complete | Exit code 2 prevents completion, sends feedback |

### Permissions and context

- Teammates start with the lead's permission settings (`--dangerously-skip-permissions` propagates to all).
- Each teammate loads project context (CLAUDE.md, MCP, skills) fresh -- **lead's conversation history does NOT carry over**.
- Spawn prompt from the lead is the teammate's starting context.

### Communication mechanics

- **message**: Send to one specific teammate.
- **broadcast**: Send to all teammates (costs scale with team size).
- **Automatic idle notifications**: Teammate notifies lead when it finishes.
- **Shared task list**: All agents see task status. Dependencies auto-unblock.

### Token cost

Scales linearly with number of teammates. Each has its own full context window. Anthropic's C compiler experiment: 16 agents, ~2,000 sessions, 2B input tokens, 140M output tokens, ~$20K in API costs, producing a 100K-line Rust C compiler that compiled the Linux kernel.

### When to use

- Teammates need to **share findings and challenge each other** (competing hypotheses debugging).
- Work spans multiple independent modules that benefit from parallel implementation.
- Cross-layer coordination (frontend + backend + tests, each owned by different teammate).
- Research tasks where multiple perspectives add genuine value.
- Tasks large enough that coordination overhead is worth the parallelism.

### When NOT to use

- Sequential tasks or same-file edits (conflicts inevitable).
- Work with many dependencies between tasks.
- Routine tasks where a single session or subagents suffice.
- When token budget is a concern -- agent teams are expensive.

### Recommended team size

Start with **3-5 teammates**. Target **5-6 tasks per teammate**. Beyond 5-6 teammates, coordination overhead and diminishing returns dominate.

### Limitations (current)

- **No session resumption** for in-process teammates. `/resume` and `/rewind` don't restore them.
- **Task status can lag**: teammates sometimes fail to mark tasks complete, blocking dependents.
- **Shutdown is slow**: teammates finish current request before stopping.
- **One team per session**. Clean up before starting another.
- **No nested teams**. Teammates cannot spawn their own teams.
- **Lead is fixed** for the team's lifetime. No promotion/transfer.
- **Permissions set at spawn**. Can change per-teammate after, not at spawn time.
- **Split panes not supported** in VS Code terminal, Windows Terminal, or Ghostty.

### Docs

- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
- [Building a C Compiler with Agent Teams (Anthropic engineering)](https://www.anthropic.com/engineering/building-c-compiler)

---

## Comparison Matrix

| Dimension | Single Session | Subagents | Agent Teams |
|---|---|---|---|
| **Parallelism** | None (or manual via worktrees) | Yes, within one session | Yes, across sessions |
| **Communication** | N/A | Subagent -> parent only | Peer-to-peer + shared task list |
| **Context isolation** | One shared window | Each subagent gets own window | Each teammate gets own window |
| **Context cost to parent** | Everything in one window | Only summaries return | Lead sees messages only |
| **Coordination** | You | Parent agent | Shared task list + messaging |
| **Nesting** | N/A | No (cannot nest) | No (cannot nest teams) |
| **Token efficiency** | Most efficient | Moderate (Haiku routing helps) | Most expensive |
| **Setup complexity** | None | YAML files or --agents JSON | Experimental flag + natural language |
| **Stability** | Production | Production | Experimental |
| **Model flexibility** | One model per session | Per-subagent model selection | Per-teammate model selection |
| **Session resumption** | Full support | Subagents resumable via agent ID | In-process teammates NOT resumable |
| **File conflict risk** | N/A | Low (worktree isolation available) | High if not partitioned carefully |

---

## Decision Flowchart

1. **Is the task simple or requires tight iteration?** -> Single session.
2. **Does it produce verbose output that would pollute context?** -> Subagent.
3. **Can the work be cleanly decomposed into independent pieces where only the result matters?** -> Subagents (parallel, background).
4. **Do workers need to communicate, challenge each other, or coordinate on shared state?** -> Agent teams.
5. **Is it a large effort spanning multiple modules with 10+ tasks?** -> Agent teams with 3-5 teammates.
6. **Budget constrained?** -> Single session or subagents with Haiku routing.

---

## Key URLs

| Resource | URL |
|---|---|
| Claude Code docs home | https://code.claude.com/docs/en/overview |
| How Claude Code works | https://code.claude.com/docs/en/how-claude-code-works |
| CLI reference | https://code.claude.com/docs/en/cli-reference |
| Interactive mode | https://code.claude.com/docs/en/interactive-mode |
| Subagents | https://code.claude.com/docs/en/sub-agents |
| Agent teams | https://code.claude.com/docs/en/agent-teams |
| Tools reference | https://code.claude.com/docs/en/tools-reference |
| Skills | https://code.claude.com/docs/en/skills |
| Common workflows (worktrees) | https://code.claude.com/docs/en/common-workflows |
| Hooks | https://code.claude.com/docs/en/hooks |
| Permissions | https://code.claude.com/docs/en/permissions |
| Settings | https://code.claude.com/docs/en/settings |
| C compiler case study | https://www.anthropic.com/engineering/building-c-compiler |
| 2026 Agentic Coding Trends Report | https://resources.anthropic.com/2026-agentic-coding-trends-report |
| Agent SDK (programmatic usage) | https://platform.claude.com/docs/en/agent-sdk/overview |
