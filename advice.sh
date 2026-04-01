#!/usr/bin/env bash
# Effective Claude Code Advisor
# Launches a coaching TUI that advises on Claude Code best practices.
# The advisor reads docs/ for its knowledge base and NEVER modifies files.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/advisor-prompt.txt"

if [ ! -f "$PROMPT_FILE" ]; then
  echo "Error: advisor-prompt.txt not found at $PROMPT_FILE"
  exit 1
fi

SYSTEM_PROMPT="$(cat "$PROMPT_FILE")"

exec claude \
  --append-system-prompt "$SYSTEM_PROMPT" \
  --permission-mode plan \
  -n "effective-advisor"
