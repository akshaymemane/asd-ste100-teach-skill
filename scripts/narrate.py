#!/usr/bin/env python3
"""Narration for a learning-pack video: synthesize captions, then mux them onto the render.

The video scene writes `narration/timeline.json` while it renders, holding one
entry per caption: the clip it synthesized and the second at which that caption
appeared on screen. This tool lays those clips onto the silent render at exactly
those times, so speech and subtitle stay together.

    # one caption, for a voice test
    python3 narrate.py say "Rounding moves a weight by half a step." --out /tmp/t.aiff

    # attach the narration the render recorded
    python3 narrate.py mux --video media/videos/animation/720p30/explanation.mp4 \
        --timeline narration/timeline.json --out explanation.mp4

    python3 narrate.py voices        # list usable macOS voices

macOS only: it uses the built-in `say` command. On Linux swap `synth()` for
espeak-ng or piper — nothing else in this file is platform specific.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_VOICE = "Samantha"
DEFAULT_RATE = 170          # words per minute


def need(tool: str) -> None:
    if shutil.which(tool) is None:
        sys.exit(f"{tool} not found. Install it, or pick another narration path.")


def synth(line: str, out: Path, voice: str = DEFAULT_VOICE, rate: int = DEFAULT_RATE) -> float:
    """Speak one line into `out`. Returns its duration in seconds."""
    need("say")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(out), line], check=True)
    return duration(out)


def duration(path: Path) -> float:
    need("ffprobe")
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True)
    raw = res.stdout.strip()
    if not raw or raw == "N/A":
        # Some AIFF headers do not carry a duration. Count the samples instead.
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "a:0",
             "-show_entries", "stream=duration", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True)
        raw = res.stdout.strip().rstrip(",")
    return float(raw)


def mux(video: Path, timeline: Path, out: Path, gain: float = 1.0) -> None:
    """Place every clip at its recorded start time and attach the mix to the video."""
    need("ffmpeg")
    entries = json.loads(timeline.read_text())["clips"]
    if not entries:
        sys.exit("timeline holds no clips. Render with NARRATE=1 first.")

    root = timeline.parent
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(video)]
    parts, labels = [], []

    for i, e in enumerate(entries):
        clip = Path(e["path"])
        if not clip.is_absolute():
            clip = root / clip.name if (root / clip.name).exists() else Path(e["path"])
        if not clip.exists():
            sys.exit(f"missing clip: {clip}")
        cmd += ["-i", str(clip)]
        delay = max(0, int(round(e["start"] * 1000)))
        # Every clip becomes stereo 44.1k so amix never has to guess a format.
        parts.append(f"[{i + 1}:a]aresample=44100,aformat=channel_layouts=stereo,"
                     f"adelay={delay}|{delay}[a{i}]")
        labels.append(f"[a{i}]")

    mix = f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0"
    if gain != 1.0:
        mix += f",volume={gain}"
    mix += "[aout]"
    graph = ";".join(parts + [mix])

    cmd += ["-filter_complex", graph, "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", str(out)]
    subprocess.run(cmd, check=True)

    print(f"{out}  {duration(out):.1f}s  {len(entries)} narration clips")


def voices() -> None:
    need("say")
    res = subprocess.run(["say", "-v", "?"], capture_output=True, text=True, check=True)
    for row in res.stdout.splitlines():
        if "en_US" in row or "en_GB" in row:
            print(row)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("say", help="synthesize one line, for a voice test")
    s.add_argument("line")
    s.add_argument("--out", type=Path, required=True)
    s.add_argument("--voice", default=DEFAULT_VOICE)
    s.add_argument("--rate", type=int, default=DEFAULT_RATE)

    m = sub.add_parser("mux", help="attach a recorded narration timeline to a render")
    m.add_argument("--video", type=Path, required=True)
    m.add_argument("--timeline", type=Path, required=True)
    m.add_argument("--out", type=Path, required=True)
    m.add_argument("--gain", type=float, default=1.0)

    sub.add_parser("voices", help="list usable macOS voices")

    args = ap.parse_args(argv)
    if args.cmd == "say":
        print(f"{synth(args.line, args.out, args.voice, args.rate):.2f}s -> {args.out}")
    elif args.cmd == "mux":
        mux(args.video, args.timeline, args.out, args.gain)
    else:
        voices()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
