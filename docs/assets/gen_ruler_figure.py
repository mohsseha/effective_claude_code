"""
RULER benchmark (NVIDIA) — weighted-average accuracy at 4K -> 1M.

Primary sources:
  - github.com/NVIDIA/RULER README leaderboard (accessed 2026-04-24). 4K..128K,
    13-task weighted average. Verified against raw README 2026-04-24: all nine
    cohort numbers match (e.g. Mistral-Large-2411 128K = 48.1, Llama 3.1 70B
    128K = 66.6, Jamba-1.5-large 128K = 95.1).
  - NVIDIA Nemotron 3 Super tech report (Mar 2026), RULER-500. Nemotron 3 Super
    BF16 plotted at 128K/256K/512K/1M; FP8 at 128K/256K/512K. NVIDIA-reported
    Qwen3.5-122B and GPT-OSS-120B 1M comparison values are plotted as single
    hollow markers at 1M only -- their 128K numbers are NOT disclosed in the
    tech report (see integrity note on nemotron_data in code).

Run:
    uv run --with matplotlib --with numpy \
      python docs/assets/gen_ruler_figure.py

Outputs:
    docs/assets/context-rot-ruler.png            (log-x, primary)
    docs/assets/context-rot-ruler-v2-linear.png  (linear-x companion)
"""
import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

OUT = Path(__file__).parent
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#111827",
    "axes.labelcolor": "#111827",
    "xtick.color": "#4b5563",
    "ytick.color": "#4b5563",
    "text.color": "#111827",
    "axes.titleweight": "600",
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "legend.frameon": False,
})

INK = "#111827"
MUTED = "#6b7280"
BORDER = "#e5e7eb"

# ---- Cohort A: RULER README leaderboard (4K..128K, 13-task weighted avg) ----
X_README = [4, 8, 16, 32, 64, 128]  # K tokens

ruler_readme = {
    "Jamba-1.5-large":       [96.7, 96.6, 96.4, 96.0, 95.4, 95.1],
    "Gemini-1.5-pro":        [96.7, 95.8, 96.0, 95.9, 95.9, 94.4],
    "Qwen2.5-14B-1M":        [97.5, 97.1, 94.6, 94.9, 94.9, 92.2],
    "Qwen3-235B-A22B":       [97.7, 97.2, 96.4, 95.1, 93.3, 90.6],
    "Qwen3-14B":             [98.0, 97.8, 96.4, 96.1, 94.0, 85.1],
    "Qwen3-32B":             [98.4, 96.0, 96.2, 94.4, 91.8, 85.6],
    "GPT-4-1106-preview":    [96.6, 96.3, 95.2, 93.2, 87.0, 81.2],
    "Llama 3.1 70B":         [96.5, 95.8, 95.4, 94.8, 88.4, 66.6],
    "Mistral-Large-2411":    [96.4, 96.3, 95.3, 94.0, 85.9, 48.1],
}

readme_palette = {
    # Stays flat through 128K (blue family)
    "Jamba-1.5-large":    "#1e3a8a",  # navy
    "Gemini-1.5-pro":     "#2563eb",  # blue
    "Qwen2.5-14B-1M":     "#38bdf8",  # sky
    # Degrades gracefully (purple family)
    "Qwen3-235B-A22B":    "#6d28d9",  # deep violet
    "Qwen3-14B":          "#a855f7",  # purple
    "Qwen3-32B":          "#d946ef",  # fuchsia
    # Collapses (red/orange family)
    "GPT-4-1106-preview": "#b45309",  # amber-dark
    "Llama 3.1 70B":      "#ea580c",  # orange
    "Mistral-Large-2411": "#b91c1c",  # red
}

# Vertical offset (points) for 128K end-labels to avoid collisions.
# Top cluster at 128K is tight: 95.1 / 94.4 / 92.2 / 90.6 span only ~4.5
# y-units; at fig scale 1 y-unit ~= 9-10pt of vertical space, and each 8.2pt
# label needs ~10pt of clearance, so we spread the four across ~20pt.
# Qwen3-14B (85.1) / Qwen3-32B (85.6) also collide. Others stand alone
# (GPT-4 81.2, Llama 66.6, Mistral 48.1).
readme_label_dy = {
    "Jamba-1.5-large":   +9,   # 95.1, top of cluster
    "Gemini-1.5-pro":    +2,   # 94.4
    "Qwen2.5-14B-1M":    -5,   # 92.2
    "Qwen3-235B-A22B":   -11,  # 90.6, bottom of cluster
    "Qwen3-14B":         -6,   # 85.1
    "Qwen3-32B":         +6,   # 85.6
}

# ---- Cohort B: Nemotron 3 Super tech report (Mar 2026), RULER-500 ----
# Nemotron 3 Super BF16/FP8 @ 128K/256K/512K: verified against the HuggingFace
# model card benchmarks table (primary):
#   https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-FP8
#   (accessed 2026-04-24; BF16 128/256/512K = 96.79/96.60/96.09,
#    FP8  128/256/512K = 96.85/96.33/95.66).
# Nemotron 3 Super BF16 @ 1M = 91.75, Qwen3.5-122B @ 1M = 91.33,
# GPT-OSS-120B @ 1M = 22.30: NVIDIA-reported comparison numbers, corroborated
# across the NVIDIA Nemotron research page
#   (https://research.nvidia.com/labs/nemotron/Nemotron-3-Super/) and
# third-party coverage quoting the tech report table
#   (https://llm-stats.com/blog/research/nemotron-3-super-launch;
#    https://www.learnaiforge.com/articles/nvidia-nemotron-3-super-open-model-benchmarks-2026).
# The primary PDF
#   (https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)
# was not machine-readable via WebFetch at audit time.
#
# INTEGRITY NOTE: An earlier version plotted Qwen3.5-122B at (128K, 95.0) and
# GPT-OSS-120B at (128K, 80.0) as "cohort-top anchors." Those 128K numbers are
# NOT disclosed in any primary source -- the Nemotron report only releases
# Qwen3.5-122B and GPT-OSS-120B at 1M as single comparison points. The anchors
# have been removed. Each of those two models is now plotted as a single hollow
# marker at 1M to signal "one disclosed datapoint, no trajectory."
nemotron_data = {
    "Nemotron 3 Super BF16": {
        "x": [128, 256, 512, 1024],
        "y": [96.79, 96.60, 96.09, 91.75],
        "color": "#047857",
        "hollow": False,
    },
    "Nemotron 3 Super FP8": {
        "x": [128, 256, 512],
        "y": [96.85, 96.33, 95.66],
        "color": "#10b981",
        "hollow": False,
    },
    "Qwen3.5-122B": {
        "x": [1024],
        "y": [91.33],  # NVIDIA-reported 1M-only comparison; 128K not disclosed
        "color": "#0891b2",
        "hollow": True,
    },
    "GPT-OSS-120B": {
        "x": [1024],
        "y": [22.30],  # NVIDIA-reported 1M-only comparison; 128K not disclosed
        "color": "#be123c",
        "hollow": True,
    },
}

# At 1M, Nemotron 3 Super BF16 (91.75) and Qwen3.5-122B (91.33) are only ~0.4
# y-units apart -> spread them vertically. GPT-OSS-120B 22.30 is below ylim=40
# (see callout below for the off-chart treatment).
nemotron_label_dy = {
    "Nemotron 3 Super BF16": +9,    # 1M: 91.75 -> up (clears Qwen3.5-122B)
    "Nemotron 3 Super FP8":  +5,    # 512K: 95.66 -> slightly up, clears BF16
    "Qwen3.5-122B":          -9,    # 1M: 91.33 -> down, clears BF16 label
    "GPT-OSS-120B":          0,     # 1M: 22.30, off-chart (see callout)
}

# ---- Cohort C: Nemotron 3 Nano tech report (Dec 2025), RULER base-model ----
# Source: NVIDIA Nemotron 3 Nano Technical Report (arxiv:2512.20848), Table 2
# "Base Model Evaluations" -- RULER 0-shot acc at 64K/128K/256K. Verified
# against arxiv.org/html/2512.20848v1 on 2026-04-24. Same evaluation variant
# (0-shot acc) as the README cohort. The paper also reports post-trained
# RULER-100 @ 256K/512K/1M (N-3-Nano 92.92/91.25/86.34; Qwen3-30B-A3B-Thinking
# 89.40/84.00/77.50), but those use a different eval (RULER-100) and are NOT
# mixed here to keep the line comparable.
nano_data = {
    "Nemotron 3 Nano (Base)": {
        "x": [64, 128, 256],
        "y": [87.50, 82.92, 75.44],
        "color": "#065f46",
    },
    "Qwen3-30B-A3B (Base)": {
        "x": [64, 128],
        "y": [63.55, 60.69],
        "color": "#831843",
    },
}

nano_label_dy = {
    "Nemotron 3 Nano (Base)": -6,
    "Qwen3-30B-A3B (Base)":   -6,
}


def draw(ax, *, xscale):
    # --- Regime bands: faint backgrounds naming the two regimes ---
    # "Graceful" zone: models ending above 90% at 128K/1M
    ax.axhspan(90, 100, facecolor="#10b981", alpha=0.06, zorder=0)
    # "Cliff" zone: models dropping below 50%
    ax.axhspan(40, 50, facecolor="#dc2626", alpha=0.06, zorder=0)

    # Zone labels name the models in each regime so the two-regime story is
    # readable without tracing individual lines.
    # On the log figure zone labels sit at far-left (x=4.2). On the linear
    # zoom (xlim starts at 96), shift them just past the 128K gridline so they
    # remain inside the visible axes area.
    zone_x = 4.2 if xscale == "log" else 132
    ax.text(zone_x, 93.5,
            "Graceful: Jamba, Gemini 1.5, Nemotron 3 Super",
            fontsize=7.8, color="#047857", fontweight="600",
            va="center", ha="left", alpha=0.9)
    ax.text(zone_x, 45,
            "Cliff: Mistral-Large, GPT-OSS-120B (at 1M)",
            fontsize=7.8, color="#b91c1c", fontweight="600",
            va="center", ha="left", alpha=0.9)

    # README cohort lines (solid)
    for model, ys in ruler_readme.items():
        c = readme_palette[model]
        ax.plot(X_README, ys, marker="o", markersize=4, linewidth=1.8, color=c,
                label=model)
        dy = readme_label_dy.get(model, 0)
        ax.annotate(model, xy=(X_README[-1], ys[-1]), xytext=(6, dy),
                    textcoords="offset points", fontsize=8.2, color=c,
                    va="center")

    # Nemotron / 1M extension lines (dashed to signal different cohort/source).
    # Hollow-marker variants (Qwen3.5-122B, GPT-OSS-120B) are single disclosed
    # datapoints at 1M with no connecting line -- their 128K values are not
    # published in the Nemotron tech report, so any line would be a guess
    # (see integrity note on nemotron_data above).
    for model, d in nemotron_data.items():
        hollow = d.get("hollow", False)
        if hollow:
            ax.plot(d["x"], d["y"], marker="s", markersize=6.5, linewidth=0,
                    markerfacecolor="white", markeredgecolor=d["color"],
                    markeredgewidth=1.8, label=model)
        else:
            ax.plot(d["x"], d["y"], marker="s", markersize=4.5, linewidth=1.8,
                    linestyle="--", color=d["color"], label=model)
        dy = nemotron_label_dy.get(model, 0)
        ax.annotate(model, xy=(d["x"][-1], d["y"][-1]), xytext=(6, dy),
                    textcoords="offset points", fontsize=8.2,
                    color=d["color"], va="center", fontweight="600")

    # Nemotron 3 Nano cohort (dash-dot, triangle markers) -- Dec 2025 tech report
    for model, d in nano_data.items():
        ax.plot(d["x"], d["y"], marker="^", markersize=4.5, linewidth=1.8,
                linestyle="-.", color=d["color"], label=model)
        dy = nano_label_dy.get(model, 0)
        ax.annotate(model, xy=(d["x"][-1], d["y"][-1]), xytext=(6, dy),
                    textcoords="offset points", fontsize=8.2,
                    color=d["color"], va="center", fontweight="600")

    # 128K boundary line
    ax.axvline(128, color="#9ca3af", linewidth=1.0, linestyle=":", zorder=0)
    # Boundary annotation (tightened). On the log figure the text fits to the
    # LEFT of the 128K line (plenty of room 4K-128K). On the linear zoom the
    # left side is ~3% of the axes; flip the anchor so the text grows RIGHT
    # from the line into the visible 128K-1M region.
    if xscale == "log":
        _bndry_ha, _bndry_dx = "right", -8
    else:
        _bndry_ha, _bndry_dx = "left", +8
    ax.annotate(
        "README ends here -> Nemotron extends to 1M",
        xy=(128, 42), xytext=(_bndry_dx, 0), textcoords="offset points",
        fontsize=7.8, color=MUTED, ha=_bndry_ha, va="center",
        fontstyle="italic",
    )

    # Cohort brackets: rendered just ABOVE the plot area (axes fraction coords)
    # so they never collide with data lines. Both log and linear scales map
    # the 128K boundary to different axes-x fractions; compute them.
    if xscale == "log":
        frac_128 = math.log2(128 / 3.5) / math.log2(1800 / 3.5)
    else:
        # Linear xlim is (96, 1080); keep frac_128 in sync so the bracket
        # lines anchor on the 128K gridline, not the old (0, 1100) frame.
        frac_128 = (128 - 96) / (1080 - 96)

    by = 1.015
    pad = 0.003
    # Left bracket: README cohort (4K -> 128K)
    ax.annotate("", xy=(pad, by), xytext=(frac_128 - pad, by),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="|-|", color=MUTED,
                                linewidth=0.8, shrinkA=0, shrinkB=0),
                annotation_clip=False)
    ax.text(frac_128 / 2, by + 0.022,
            "2025 README cohort (4K-128K)",
            transform=ax.transAxes,
            fontsize=7.6, color=MUTED, ha="center", va="bottom",
            clip_on=False)
    # Right bracket: Nemotron extension (128K -> 1M)
    ax.annotate("", xy=(frac_128 + pad, by), xytext=(1 - pad, by),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="|-|", color=MUTED,
                                linewidth=0.8, shrinkA=0, shrinkB=0),
                annotation_clip=False)
    ax.text((frac_128 + 1) / 2, by + 0.022,
            "2026 Nemotron extension (128K-1M)",
            transform=ax.transAxes,
            fontsize=7.6, color=MUTED, ha="center", va="bottom",
            clip_on=False)

    # Mistral-Large-2411 headline callout: 96.4 (4K) -> 48.1 (128K) = -48 pts
    # Anchor at the Mistral 128K endpoint (48.1); place label above-left so it
    # sits in the empty space between the descending line and the "README ends
    # here" boundary note.
    # Linear xlim starts at 96, so the original (70, 60) anchor now falls
    # outside the axes and gets clipped. Nudge it right into the visible
    # frame while keeping the arrow pointing at Mistral's 128K endpoint.
    mistral_text_xy = (48, 58) if xscale == "log" else (155, 60)
    ax.annotate(
        "-48 pts",
        xy=(128, 48.1), xytext=mistral_text_xy,
        textcoords="data",
        fontsize=9, color="#b45309", fontweight="700", ha="center",
        arrowprops=dict(arrowstyle="->", color="#b45309", linewidth=1.2,
                        shrinkA=2, shrinkB=2),
    )

    # GPT-OSS-120B callout at 1M: NVIDIA-reported RULER-500 = 22.30 at 1M.
    # The hollow marker sits at (1024, 22.30), below ylim=40, so we anchor the
    # arrow at (1024, 40) -- the visible bottom edge of the chart at 1M -- and
    # point down-right to make the off-chart value legible. The "-58 pts"
    # phrasing used earlier silently baselined against the fabricated
    # (128K, 80) anchor; we now state only what the primary source discloses.
    if xscale == "log":
        gpt_text_xy = (250, 58)
    else:
        gpt_text_xy = (720, 62)
    ax.annotate(
        "22% at 1M\n(off chart, NVIDIA-reported)",
        xy=(1024, 40), xytext=gpt_text_xy,
        textcoords="data",
        fontsize=9, color="#be123c", fontweight="700", ha="center",
        arrowprops=dict(arrowstyle="->", color="#be123c", linewidth=1.2,
                        shrinkA=2, shrinkB=2),
    )

    if xscale == "log":
        ax.set_xscale("log", base=2)
        xticks = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
        ax.set_xlim(3.5, 1800)
    else:
        # Linear companion: zoom to the 128K -> 1M range where linear distance
        # actually carries information. The 4K -> 128K story is already told
        # by the log figure; in linear-x it compresses to a useless ~12%
        # strip. README lines appear as single endpoint markers at 128K to
        # signal "this cohort ends here"; Nemotron/Nano trajectories become
        # legible at true linear spacing.
        xticks = [128, 256, 512, 1024]
        ax.set_xlim(96, 1080)

    ax.set_xticks(xticks)
    ax.get_xaxis().set_major_formatter(mticker.FuncFormatter(
        lambda v, _: ("1M" if int(v) == 1024 else f"{int(v)}K")))
    ax.set_yticks([40, 50, 60, 70, 80, 90, 100])
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.set_ylim(40, 100)
    ax.grid(True, which="major", axis="y", color=BORDER, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Context length (tokens)")
    ax.set_ylabel("RULER weighted-average accuracy")

    # --- Line-style key (inside axes). Small proxy artists so the reader can
    # distinguish solid / dashed / dash-dot at projection distance without
    # re-reading the caption. Placed lower-left on the log figure (sits over
    # the empty sub-50% strip, right of "Cliff zone" banner) and lower-right
    # on the linear zoom (where the left edge is crowded with 128K labels).
    from matplotlib.lines import Line2D
    _style_proxies = [
        Line2D([0], [0], color=INK, linewidth=1.8, linestyle="-",
               marker="o", markersize=4, label="solid = README (4K-128K)"),
        Line2D([0], [0], color=INK, linewidth=1.8, linestyle="--",
               marker="s", markersize=4.5,
               label="dashed = Nemotron 3 Super (128K-1M)"),
        Line2D([0], [0], color=INK, linewidth=1.8, linestyle="-.",
               marker="^", markersize=4.5,
               label="dash-dot = Nemotron 3 Nano (base)"),
    ]
    _leg_loc = "lower left" if xscale == "log" else "lower right"
    _leg = ax.legend(handles=_style_proxies, loc=_leg_loc,
                     fontsize=7.4, handlelength=2.6, handletextpad=0.6,
                     labelcolor=INK, borderpad=0.5, borderaxespad=0.6,
                     frameon=True, fancybox=False, edgecolor=BORDER,
                     facecolor="white", framealpha=0.92)
    _leg.get_frame().set_linewidth(0.6)


def render(path: Path, *, xscale: str, title: str):
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=180)
    draw(ax, xscale=xscale)
    ax.set_title(title, loc="left", pad=26, color=INK)

    fig.text(
        0.01, 0.055,
        "Primary: github.com/NVIDIA/RULER README leaderboard (accessed 2026-04-24; "
        "cohort numbers verified). Hsieh et al., arXiv:2404.06654 (COLM 2024). "
        "13-task weighted average.",
        fontsize=7.6, color=MUTED,
    )
    fig.text(
        0.01, 0.028,
        "Extension (dashed, 128K->1M): NVIDIA Nemotron 3 Super tech report (Mar 2026), "
        "RULER-500. Qwen3.5-122B and GPT-OSS-120B shown as hollow markers at 1M only "
        "(NVIDIA-reported comparison; 128K not disclosed).",
        fontsize=7.6, color=MUTED,
    )
    fig.text(
        0.01, 0.002,
        "Cohort caveat: the NVIDIA/RULER public README has NOT been refreshed with "
        "GPT-5.x, Claude Opus 4.6/4.7, or Gemini 3.x. Newest README entries are Qwen3 (mid-2025).",
        fontsize=7.6, color="#b91c1c",
    )

    fig.tight_layout(rect=[0, 0.09, 1, 1])
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {path}")


TITLE = "RULER (NVIDIA): two regimes — flat, or cliff"

render(OUT / "context-rot-ruler.png", xscale="log", title=TITLE)
render(OUT / "context-rot-ruler-v2-linear.png", xscale="linear", title=TITLE)
