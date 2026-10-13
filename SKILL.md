---
name: teaching-technical-topics
description: "Use when the user wants to be taught a technical topic, book chapter, paper, or system-design concept in depth — \"teach me X\", \"explain chapter N of Designing Data-Intensive Applications\", \"I want to learn consensus/LSM-trees/replication\", \"make me an interactive lesson\", \"build a visual explainer\", \"explain this with diagrams and a video\", or when the user hands over source material and asks for study artifacts. Also use when the user asks for a learning pack, study module, explainer video, or interactive simulation of a technical subject. Not for one-line factual answers."
version: 1.0.0
---

# Teaching Technical Topics (ASD-STE100 Learning Packs)

Turns one technical topic into four learning artifacts that share a single core example: plain-English explanation, Mermaid diagrams, an interactive page, and a rendered video.

**REQUIRED SUB-SKILL:** Use `asd-ste100` for every word of prose you write in these artifacts. That skill owns the lexical and structural rules; this skill owns the learning-pack workflow. Run its linter on `01-explanation.md` and on diagram and video narration text before you report done.

The reader is an **experienced backend engineer who is new to this specific topic**. Write for someone who knows Java, SQL, HTTP, and threads, and does not yet know this algorithm.

## When to Use

- The user names a chapter, paper, or topic and wants to learn it, not just get an answer.
- The user wants diagrams, a simulation, or a video of how a system behaves.
- The user pastes source material (book text, paper, docs) and asks you to teach it.

Do not use for: a single factual lookup, an API signature, a bug fix, or marketing copy.

## Step 0 — Source material gate (blocking)

Ask for the source and stop if you do not have it. **Never invent chapter content.** If the user names a book chapter you cannot read, ask for the text, a PDF path, or permission to teach the topic from general knowledge with that limit stated in `01-explanation.md`.

Confirm two things before generating: the **topic** and the **core example** you will reuse in all four artifacts (one example, four views — this is what makes the pack coherent).

## Step 1 — Environment probe (before promising a video)

```bash
bash scripts/check-env.sh
```

It reports the status of python3, manim, ffmpeg, and node, and prints exact install commands for anything missing. If manim is absent, either install it or take the documented fallback, and say which path you took. Never claim a rendered MP4 you did not render.

## Step 2 — Scaffold

```bash
bash scripts/scaffold.sh <topic-slug>
```

Creates:

```text
topic-slug/
├── 01-explanation.md
├── 02-diagrams.md
├── 03-interactive/
│   └── index.html
└── 04-video/
    ├── animation.py
    └── explanation.mp4
```

## Step 3 — Generate all four artifacts

Do not stop after one artifact. The only legal early stops are: missing source material (Step 0) or a missing dependency you have reported (Step 1).

The per-file content contract is in `references/output-contract.md` — read it before writing each file.

| File | Core requirement | Done when |
|---|---|---|
| `01-explanation.md` | STE prose, every term defined before use, fundamentals → complexity, why it exists, trade-offs, common mistakes, 5 test questions | `ste-lint.py` hard violations = 0 (or justified) |
| `02-diagrams.md` | Mermaid: architecture, data flow, algorithm steps, sequence for distributed ops, failure/recovery, alternative comparison. Short prose under each | Every block parses (see contract for the check) |
| `03-interactive/index.html` | Real simulation: sliders, play/pause/reset/step, failure injection, tooltips, knowledge checks | Opens with zero console errors |
| `04-video/` | Manim source + rendered MP4. Length follows the content: subtitles-only runs 60–120 s, narrated runs minutes | MP4 exists with non-zero duration, or the gap is reported |

## Hard rules

1. **Same core example in all four artifacts.** A reader must recognize the Step-2 example in the video.
2. **No accuracy loss for simplicity.** Flat language, exact mechanics. If a simplification would mislead, keep the detail and define the term.
3. **Always teach trade-offs and failure modes.** A format that only shows the happy path is incomplete.
4. **Interactive means interactive.** An animated article is a failed `03-interactive/`. State changes must come from user input.
5. **Pace the video for how it is received.** Subtitles with no audio need read time, not speech time. A silent 6-minute cut of a 1-minute argument is a defect. See the read-floor rule in the contract.
6. **Test what you ship.** Open the page and read the console; render the video. Report every untested or ungenerated output explicitly.
7. **Examples live in Java, SQL, and distributed-systems terms** where the topic allows.

## Red flags — stop and fix

- About to write chapter content you never read → go back to Step 0.
- About to report "video created" when only `animation.py` exists → report the gap instead.
- The interactive page has a timeline but no input that changes behavior → rule 4 violated.
- Four artifacts use four different examples → rule 1 violated.
- Prose has semicolons, nominalizations, or undefined jargon → run the `asd-ste100` linter.

## Reference

- `references/output-contract.md` — per-file content and verification contract.
- `references/prompt-template.md` — the one-shot prompt form of this workflow, for reuse outside a skill-aware harness.
- `templates/animation.py` — manim starter scene with narration/subtitle pattern.
