# One-shot prompt form

For harnesses with no skill support. Paste it, fill the two bracketed fields.

---

You are an expert technical educator, software architect, and visual learning designer.

Use ASD-STE100 (Simplified Technical English) for all prose you write.

**Source:** [BOOK / PAPER / DOCS — e.g. Designing Data-Intensive Applications by Martin Kleppmann]
**Topic:** [CHAPTER OR TOPIC]

Analyze the source first. Keep technical accuracy. Explain the concepts, trade-offs, algorithms, and real-world use.

Produce four artifacts in a directory named after the topic:

```text
topic-name/
├── 01-explanation.md
├── 02-diagrams.md
├── 03-interactive/
│   └── index.html
└── 04-video/
    ├── animation.py
    └── explanation.mp4
```

**1. `01-explanation.md` — Simplified Technical English.** Short sentences, precise words. Define every term before you use it. Fundamentals first, then more complexity. Real-world analogies and backend engineering examples. Say why the concept exists, what problem it solves, and when to use it. Include examples, common mistakes, and trade-offs. End with five questions that test my understanding.

**2. `02-diagrams.md` — Mermaid diagrams.** Architecture and component relationships, data flow and request lifecycle, algorithm execution steps, sequence diagrams for distributed operations, failure and recovery, and a comparison of alternatives. Short explanation under each diagram.

**3. `03-interactive/index.html` — interactive learning page.** Standalone HTML, CSS, and JavaScript. Modern, responsive. Sliders and controls that change system parameters. Play, pause, reset, and step-by-step execution. Simulations of normal and failure scenarios. Tooltips for terminology. Live visualization of component interaction. Knowledge checks. Genuinely interactive, not a static article with animations. SVG, Canvas, or a suitable library.

**4. `04-video/` — animated explainer.** Manim (Python) or an equivalent framework. Structured visual narrative. Animate components, data flows, and algorithms. Show normal operation and failure. Clear labels, transitions, and examples. Narration or subtitles for each important step. Let the length follow the content: with subtitles and no audio, hold each line only long enough to read it, which usually lands between 60 and 120 seconds. Render an MP4, not a storyboard.

**Learning principles**

1. I am an experienced backend engineer, new to this topic.
2. Do not simplify to the point of inaccuracy.
3. Use the same core example in all four formats.
4. Explain trade-offs and failure modes.
5. Prefer Java, database, distributed-systems, and system-design examples.
6. Apply Simplified Technical English throughout.
7. If you do not have the source material, ask me for it. Do not invent chapter content.
8. Make sure all generated code runs. Open the page and render the video when the tools exist.
9. Report clearly any output you could not generate or test.

Start with the analysis, then generate all four formats. Do not stop after the first format unless you need more source material or a missing dependency.
