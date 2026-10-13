"""Manim starter for a learning-pack explainer video.

Render:
    manim -ql animation.py LearningPack     # draft
    manim -qm animation.py LearningPack     # 720p keeper
    manim -qh animation.py LearningPack     # 1080p final

Check the length with:
    ffprobe -v error -show_entries format=duration -of csv=p=0 explanation.mp4

Replace TOPIC, the beat list, and the body of each beat. Keep the subtitle
mechanism: every beat states one idea in Simplified Technical English.
"""

from manim import (
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    Rectangle,
    Scene,
    Text,
    VGroup,
    Write,
    BLUE,
    DOWN,
    GREY_B,
    LEFT,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    config,
)

TOPIC = "TOPIC"
SUBTITLE_SIZE = 26
config.output_file = "explanation"

# This template carries subtitles and no narration audio, so each pause only
# has to last long enough to READ the line, not to speak it. CUT picks length:
#   "short" — the whole argument at reading pace, usually 60-120 seconds
#   "full"  — every sub-step shown, for a slower study pass
# Never stretch a silent cut to speaking pace. Cut captions instead.
CUT = "short"
SHORT = CUT == "short"

PACE = 0.6 if SHORT else 2.5      # multiplies every pause
RUN = 0.55 if SHORT else 1.0      # multiplies every animation run_time


class Subtitles:
    """One persistent subtitle line at the bottom of the frame."""

    def __init__(self, scene: Scene):
        self.scene = scene
        self.current: Text | None = None

    def say(self, line: str, hold: float = 2.5) -> None:
        new = Text(line, font_size=SUBTITLE_SIZE, color=GREY_B).to_edge(DOWN, buff=0.4)
        if self.current is None:
            self.scene.play(FadeIn(new, run_time=0.4))
        else:
            self.scene.play(FadeOut(self.current, run_time=0.2), FadeIn(new, run_time=0.4))
        self.current = new
        # A caption with no narration must stay up long enough to read: about
        # 3.3 words per second, plus a moment to move the eye back to the plot.
        read_floor = len(line.split()) / 3.3 + 0.7
        self.scene.wait(max(hold * PACE, read_floor))

    def clear(self) -> None:
        if self.current is not None:
            self.scene.play(FadeOut(self.current, run_time=0.3))
            self.current = None


def node(label: str, color=BLUE) -> VGroup:
    box = Rectangle(width=2.6, height=1.1, color=color)
    return VGroup(box, Text(label, font_size=24).move_to(box))


class LearningPack(Scene):
    """Beats: problem, naive attempt, break, mechanism, normal path, failure, recovery, trade-offs."""

    def play(self, *animations, **kwargs):
        """Scale every animation by RUN so one knob sets the whole cut's tempo."""
        for anim in animations:
            if hasattr(anim, "run_time"):
                anim.run_time = anim.run_time * RUN
        if "run_time" in kwargs:
            kwargs["run_time"] = kwargs["run_time"] * RUN
        super().play(*animations, **kwargs)

    def construct(self) -> None:
        self.sub = Subtitles(self)
        self.title_card()
        self.problem()
        self.mechanism()
        self.failure_and_recovery()
        self.tradeoffs()

    def title_card(self) -> None:
        title = Text(TOPIC, font_size=54, color=WHITE)
        self.play(Write(title))
        self.wait(1.2)
        self.play(FadeOut(title))

    def problem(self) -> None:
        self.sub.say("One machine holds all the data. The machine fails. The data is gone.", 3)
        single = node("Server", RED).move_to(LEFT * 3)
        self.play(Create(single))
        self.sub.say("The fix is more than one copy. More copies create a new problem: agreement.", 3)
        self.play(FadeOut(single))

    def mechanism(self) -> None:
        # Replace with the core example used in 01-explanation.md and 03-interactive/.
        leader = node("Leader").move_to(UP * 1.5)
        follower_a = node("Follower A").move_to(DOWN * 1 + LEFT * 3.2)
        follower_b = node("Follower B").move_to(DOWN * 1 + RIGHT * 3.2)
        edges = VGroup(
            Arrow(leader.get_bottom(), follower_a.get_top(), buff=0.1),
            Arrow(leader.get_bottom(), follower_b.get_top(), buff=0.1),
        )
        self.play(Create(leader))
        self.play(Create(follower_a), Create(follower_b))
        self.play(Create(edges))
        self.sub.say("The leader takes every write. It sends each write to the followers.", 3)
        self.cluster = VGroup(leader, follower_a, follower_b, edges)

    def failure_and_recovery(self) -> None:
        leader = self.cluster[0]
        self.play(leader.animate.set_color(RED))
        self.sub.say("The leader stops. No node takes writes. The system is unavailable.", 3)
        self.play(self.cluster[1].animate.set_color(YELLOW))
        self.sub.say("A follower is promoted. Writes continue. Unreplicated writes are lost.", 3.5)

    def tradeoffs(self) -> None:
        self.play(FadeOut(self.cluster))
        self.sub.clear()
        rows = VGroup(
            Text("Synchronous: no lost writes, slow, blocks on a dead follower", font_size=28),
            Text("Asynchronous: fast, survives a dead follower, can lose writes", font_size=28),
        ).arrange(DOWN, buff=0.6)
        self.play(FadeIn(rows))
        self.wait(3)
        self.play(FadeOut(rows))
