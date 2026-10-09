#!/usr/bin/env bash
# Usage: router-mode.sh [on|off|status]
set -euo pipefail
dir="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/model-router}"
mkdir -p "$dir"
f="$dir/mode"
case "${1:-status}" in
  on|off) echo "$1" > "$f"; echo "model-router : $1" ;;
  status) echo "model-router : $(cat "$f" 2>/dev/null || echo on)" ;;
  *) echo "Usage: /router [on|off|status]" >&2; exit 1 ;;
esac
