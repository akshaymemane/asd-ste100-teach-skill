# teaching-technical-topics

A Claude Code skill that turns one technical topic — a book chapter, a paper, a system-design concept — into four learning artifacts that share a single core example:

| Artifact | What it is |
|---|---|
| `01-explanation.md` | Simplified Technical English explanation: terms defined before use, trade-offs, common mistakes, five test questions |
| `02-diagrams.md` | Mermaid architecture, data flow, algorithm, sequence, failure/recovery, and alternatives diagrams |
| `03-interactive/index.html` | Standalone simulation: parameter sliders, play/pause/reset/step, failure injection, tooltips, knowledge checks |
| `04-video/` | Manim source plus a rendered MP4. Length follows the content — a subtitles-only cut runs 60–120 s |

This skill extends [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), which owns the controlled-language rules. This one owns the learning-pack workflow and delegates every line of prose to it.

The audience it writes for: an experienced backend engineer who is new to the specific topic. Flat language, exact mechanics, no accuracy traded for simplicity.

## Install

Both skills are needed. User-level install, so they work in every directory on the machine:

```bash
git clone https://github.com/danyuchn/asd-ste100-skill ~/.claude/skills/asd-ste100
git clone https://github.com/akshaymemane/asd-ste100-teach-skill ~/.claude/skills/teaching-technical-topics
```

Optional slash command:

```bash
mkdir -p ~/.claude/commands
cp ~/.claude/skills/teaching-technical-topics/teach.md ~/.claude/commands/teach.md
```

Check the toolchain:

```bash
bash ~/.claude/skills/teaching-technical-topics/scripts/check-env.sh
```

It reports python3, the STE linter, npx, manim, and ffmpeg, and prints the install command for anything missing. Manim needs `brew install cairo pango pkg-config && pip3 install manim` on macOS.

## Use

```text
/teach LSM-trees and B-trees, source: Designing Data-Intensive Applications ch.3
```

Or plain language — the skill triggers on "teach me X", "explain chapter N of …", "make me an interactive lesson", "build a visual explainer".

The skill stops and asks for source material rather than inventing chapter content.

## Layout

```text
SKILL.md                            workflow, hard rules, red flags
references/output-contract.md       per-file content and verification contract
references/prompt-template.md       one-shot prompt for harnesses without skills
scripts/check-env.sh                toolchain probe with install commands
scripts/scaffold.sh                 creates the topic directory tree
templates/animation.py              manim starter scene with subtitle mechanism
teach.md                            slash command source
```

## License

MIT. The ASD-STE100 skill it builds on carries its own license.
