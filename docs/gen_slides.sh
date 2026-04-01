#!/usr/bin/env bash
# Generates slides.pdf from slides.md using Marp CLI.
# Run from the docs/ directory, or from anywhere — the script finds its own location.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -f slides.md ]; then
    echo "Error: slides.md not found in $SCRIPT_DIR" >&2
    exit 1
fi

npx @marp-team/marp-cli slides.md -o slides.pdf --allow-local-files
echo "Opening slides.pdf..."
open slides.pdf
