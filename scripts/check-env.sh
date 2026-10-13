#!/usr/bin/env bash
# Reports which parts of the learning-pack toolchain exist, and how to install the rest.
# Exit 0: every artifact is producible. Exit 1: the video stage is blocked.
set -u

ok() { printf '  OK      %s (%s)\n' "$1" "$2"; }
miss() { printf '  MISSING %s\n            install: %s\n' "$1" "$2"; }

video_blocked=0
echo "learning-pack toolchain"
echo

echo "prose + diagrams"
if command -v python3 >/dev/null; then ok python3 "$(python3 -V 2>&1)"; else miss python3 "brew install python@3.12"; fi
LINT="$HOME/.claude/skills/asd-ste100/scripts/ste-lint.py"
if [ -f "$LINT" ]; then ok ste-lint.py "$LINT"; else miss "asd-ste100 skill" "git clone https://github.com/danyuchn/asd-ste100-skill ~/.claude/skills/asd-ste100"; fi
if command -v npx >/dev/null; then ok "npx (mermaid check)" "$(npx --version 2>/dev/null)"; else miss "npx" "brew install node"; fi

echo
echo "video"
MANIM=""
if command -v manim >/dev/null; then
  MANIM=$(command -v manim)
elif python3 -c "import manim" 2>/dev/null; then
  MANIM="python3 -m manim"
else
  # manim is commonly installed into a virtualenv rather than onto PATH.
  for cand in "$HOME"/.venvs/*/bin/manim "$HOME"/venv*/bin/manim ./venv/bin/manim ./.venv/bin/manim; do
    [ -x "$cand" ] && MANIM="$cand" && break
  done
fi
if [ -n "$MANIM" ]; then
  ok manim "$MANIM"
  printf '            render with: %s -qm 04-video/animation.py <SceneName>\n' "$MANIM"
else
  miss manim "brew install cairo pango pkg-config && python3 -m venv ~/.venvs/manim && ~/.venvs/manim/bin/pip install manim"
  video_blocked=1
fi
if command -v ffmpeg >/dev/null; then ok ffmpeg "$(ffmpeg -version 2>&1 | head -1 | cut -d' ' -f1-3)"; else miss ffmpeg "brew install ffmpeg"; video_blocked=1; fi

echo "narration (optional)"
if command -v say >/dev/null; then
  ok "say (macOS TTS)" "$(say -v '?' 2>/dev/null | wc -l | tr -d ' ') voices"
  printf '            render with: NARRATE=1 manim -qm 04-video/animation.py <SceneName>\n'
else
  printf '  ABSENT  say — narration unavailable, ship the subtitles-only cut\n'
fi

echo
if [ "$video_blocked" -eq 1 ]; then
  echo "Video stage blocked. Either run the install command above, or take the"
  echo "frame-capture fallback in references/output-contract.md. Report which one."
  exit 1
fi
echo "All four artifacts are producible."
