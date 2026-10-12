#!/usr/bin/env bash
# Creates the learning-pack directory tree for one topic.
# Usage: bash scaffold.sh <topic-slug> [parent-dir]
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: bash scaffold.sh <topic-slug> [parent-dir]" >&2
  exit 2
fi

slug=$(printf '%s' "$1" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-')
parent=${2:-.}
root="$parent/$slug"
here=$(cd "$(dirname "$0")/.." && pwd)

if [ -e "$root" ]; then
  echo "refusing to overwrite existing $root" >&2
  exit 1
fi

mkdir -p "$root/03-interactive" "$root/04-video"
: > "$root/01-explanation.md"
: > "$root/02-diagrams.md"
: > "$root/03-interactive/index.html"
cp "$here/templates/animation.py" "$root/04-video/animation.py"

echo "$root"
find "$root" -type f | sort
echo
echo "next: fill 01 and 02, build 03, then render 04 with"
echo "  manim -qm $root/04-video/animation.py LearningPack"
