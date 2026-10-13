# Output contract

One contract per file. Read the row for the artifact you are about to write, then write it.

## 1. `01-explanation.md`

Required sections, in this order:

1. `# <Topic>` — one sentence on what the topic is.
2. `## The problem it solves` — the failure or cost that exists without this mechanism.
3. `## Terms` — a definition list. Every term you use later appears here first. No forward references.
4. `## How it works` — fundamentals first, then one layer of complexity per subsection. Number the steps when the mechanism is sequential.
5. `## The core example` — the single example reused by all four artifacts. Name it explicitly: "This example returns in `02-diagrams.md`, `03-interactive/`, and `04-video/`."
6. `## Real-world analogy` — one analogy, then the exact point where the analogy breaks.
7. `## Code` — Java or SQL where the topic allows. Runnable or clearly marked as a fragment.
8. `## Trade-offs` — a table: approach, what you gain, what you pay, when to pick it.
9. `## Common mistakes` — each entry: the mistake, why it is tempting, what it costs.
10. `## When not to use this` — the conditions that make the mechanism the wrong choice.
11. `## Test yourself` — exactly five questions, ordered from recall to design judgment. Answers in a collapsed block.

Verification:

```bash
python3 ~/.claude/skills/asd-ste100/scripts/ste-lint.py 01-explanation.md
```

Exit 0 required. If a hard violation must stay (a quoted term, an exact API name), keep it and add one line under the heading that says why.

## 2. `02-diagrams.md`

Required diagrams. Skip one only when the topic has no such aspect, and say so in one line.

| Diagram | Mermaid type | Must show |
|---|---|---|
| Architecture | `graph TD` / `flowchart` | Components and what each one owns |
| Data flow | `flowchart LR` | The request lifecycle end to end |
| Algorithm | `flowchart TD` | Decision points and loops, not prose boxes |
| Distributed operation | `sequenceDiagram` | Every message, with ordering |
| Failure and recovery | `sequenceDiagram` or `stateDiagram-v2` | The fault, detection, and recovery path |
| Alternatives | `graph LR` or a table | The same workload under two designs |

Rules:

- Under every diagram, 2–5 sentences in STE that say what the reader should see in it.
- Label edges with the real operation (`fsync`, `AppendEntries`, `COMMIT`), not `step 1`.
- Node text stays short. Detail belongs in the prose below the diagram.

Verification (node present):

```bash
npx -y @mermaid-js/mermaid-cli -i 02-diagrams.md -o /tmp/mmd-check.md
```

A parse failure names the diagram. If `npx` is unavailable, state that diagrams were not machine-checked.

## 3. `03-interactive/index.html`

Standalone. No build step, no network fetch at runtime; inline the CSS and JS or ship sibling files in the same directory.

Required controls:

- Parameter inputs (`range`, `select`) that change simulation behavior while it runs — replica count, latency, batch size, isolation level, whatever the topic exposes.
- Transport: play, pause, reset, and single-step. Step must advance exactly one logical event.
- A failure switch: kill a node, drop a packet, stall a disk, partition the network.
- Tooltips on every technical term, triggered by hover and by focus.
- Live state view: queues, logs, offsets, or whichever state the mechanism mutates. It updates as the simulation runs.
- At least two knowledge checks that mark an answer right or wrong and explain why.

Implementation notes:

- SVG for structure that gets labels and tooltips; Canvas when more than ~200 moving elements.
- Drive animation from a logical event clock, not from CSS transition timing — single-step needs discrete events.
- Keyboard: space toggles play, arrow steps, `r` resets.
- Dark and light both legible; responsive down to 420 px.

Verification: open it and read the console.

```bash
open 03-interactive/index.html   # then check the console via the browser tools
```

Zero errors required. Report any check you could not run.

## 4. `04-video/`

- `animation.py` — manim scenes. Start from `templates/animation.py`.
- `explanation.mp4` — rendered. **Length follows the content, never a target.**
- Assets (audio, SVG, data) in the same directory.

**Pace it for how the viewer receives it, not for a duration.**

| The video has | Each beat lasts | Typical total |
|---|---|---|
| Subtitles only, no audio | long enough to READ the line | 60–120 s |
| Narration audio | long enough to SPEAK the line | the same script, 20–40% longer |

Speech runs near 3 words per second and reading near 3.3, so a narrated cut of
the same script lands a little above the silent one. A narrated video measured
in many minutes means the script is long, not that narration costs minutes.

A silent video paced for speech feels broken, because the viewer finished reading
six seconds ago and is watching a still frame. Compute the floor instead of
guessing: `seconds = words / 3.3 + 0.7`. Hold each caption for at least that,
and let the total land where it lands.

When the total runs long, cut captions and shorten their wording. Do not speed
them below the read floor — that trades comprehension for a number.

Default to the short cut. Offer the long one when the topic has more sub-steps
than a single pass can carry. The template exposes this as `CUT = "short"`.

**Narration (optional, macOS).** Ask before adding it — a synthetic voice suits
some packs and grates in others. With `NARRATE=1` each caption speaks itself:
the scene synthesizes the line, holds the caption for exactly as long as the
clip runs, and records the second it appeared. Speech then sets the pace and the
read floor stops applying.

```bash
NARRATE=1 manim -qm 04-video/animation.py <SceneName>
python3 ~/.claude/skills/teaching-technical-topics/scripts/narrate.py mux \
    --video 04-video/media/videos/animation/720p30/explanation.mp4 \
    --timeline 04-video/narration/timeline.json --out 04-video/explanation.mp4
```

`NARRATE_VOICE` and `NARRATE_RATE` pick the voice and words per minute
(`narrate.py voices` lists them). Verify the sync rather than trusting it:

```bash
ffmpeg -hide_banner -i 04-video/explanation.mp4 -af silencedetect=noise=-40dB:d=0.5 \
    -f null - 2>&1 | grep silence_end
```

Each `silence_end` must match a `start` in `timeline.json`. A drift means the
caption and the voice disagree, which is worse than no narration at all.

Narration makes the video longer than the silent cut, and that is correct:
speech is slower than reading. Do not then trim the pauses to claw the time back.

Narrative shape: problem → naive approach → why it breaks → the mechanism → normal operation walked through on the core example → failure scenario → recovery → trade-off summary.

Every scene carries a subtitle. Narration audio is optional; subtitles are not.

Render:

```bash
manim -qm 04-video/animation.py --write_to_movie
# -ql while iterating, -qh for the final pass
```

Then confirm the file is real:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 04-video/explanation.mp4
```

Fallback when manim cannot be installed: build the scenes as timed states in the interactive page, capture frames with a headless browser, and assemble with `ffmpeg -framerate 30 -i frame-%04d.png -c:v libx264 -pix_fmt yuv420p explanation.mp4`. Say in the report that the fallback path produced the video.

If no video could be produced, leave `animation.py` complete and runnable, ship no MP4 at all (an empty or placeholder file reads as a delivered video), and report the exact blocker plus the command the user needs to run.
