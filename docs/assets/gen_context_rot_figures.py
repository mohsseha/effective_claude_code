"""
Generates three candidate figures for docs/context_degradation_2026.md.

Run:
    uv run --with matplotlib /Users/husainal-mohssen/src/effective_claude_code/docs/assets/gen_context_rot_figures.py

Outputs:
    docs/assets/context-rot-2026-v1-lines.png
    docs/assets/context-rot-2026-v2-slope.png
    docs/assets/context-rot-2026-v3-bars.png

Data sources (see context_degradation_2026.md for citations):
  - NoLiMa (arXiv:2502.05167, leaderboard updated Jul 2025)
  - Gemini 2.5 Pro / Gemini 3 Pro model cards (MRCR v2 8-needle)
  - Claude Opus 4.6 announcement (MRCR v2 8-needle @ 1M)
  - Adobe long-context study (Feb 2025), via Understanding AI Nov 2025
"""
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

ACCENT = "#1d4ed8"
INK = "#111827"
MUTED = "#6b7280"
BORDER = "#e5e7eb"

# ---------------------------------------------------------------------------
# FIGURE 1 — NoLiMa accuracy curves (1K -> 32K, 7 models)
# ---------------------------------------------------------------------------
nolima = {
    "GPT-4.1":          [95.6, 95.2, 91.7, 87.5, 84.9, 79.8],
    "GPT-4o":           [98.1, 98.0, 95.7, 89.2, 81.6, 69.7],
    "Llama 3.3 70B":    [94.2, 87.4, 81.5, 72.1, 59.5, 42.7],
    "Llama 3.1 405B":   [89.0, 85.0, 74.5, 60.1, 48.4, 38.0],
    "Gemini 1.5 Pro":   [86.4, 82.7, 75.4, 63.9, 55.5, 48.2],
    "Claude 3.5 Sonnet":[85.4, 84.0, 77.6, 61.7, 45.7, 29.8],
    "Mistral Large 2":  [86.1, 85.5, 73.3, 51.5, 32.6, 18.7],
}
x = [1, 2, 4, 8, 16, 32]

fig, ax = plt.subplots(figsize=(9, 5.2), dpi=180)
palette = ["#1d4ed8", "#2563eb", "#7c3aed", "#9333ea", "#db2777", "#dc2626", "#ea580c"]
for (model, ys), color in zip(nolima.items(), palette):
    ax.plot(x, ys, marker="o", markersize=4, linewidth=1.8, color=color, label=model)
    ax.annotate(model, xy=(x[-1], ys[-1]), xytext=(5, 0), textcoords="offset points",
                fontsize=8, color=color, va="center")

ax.set_xscale("log", base=2)
ax.set_xticks(x)
ax.get_xaxis().set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v)}K"))
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_ylim(0, 100)
ax.set_xlim(0.9, 60)
ax.grid(True, which="major", axis="y", color=BORDER, linewidth=0.8)
ax.set_axisbelow(True)
ax.set_xlabel("Context length (tokens)")
ax.set_ylabel("Accuracy")
ax.set_title("Non-literal retrieval degrades fast — even on frontier models",
             loc="left", pad=14, color=INK)
fig.text(0.01, 0.01,
         "NoLiMa (arXiv:2502.05167, Jul 2025). Needle-in-haystack without lexical overlap.",
         fontsize=8, color=MUTED)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(OUT / "context-rot-2026-v1-lines.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------------------------------------------------------------------------
# FIGURE 2 — Slopegraph: MRCR v2 8-needle, 128K -> 1M
# ---------------------------------------------------------------------------
# GPT-4.1 dropped: its published MRCR is 2-needle, not comparable to the
# 8-needle v2 numbers used for the other models (apples-to-oranges).
mrcr = {
    "Claude Opus 4.6":   (None,  76.0),
    "Gemini 3 Pro":      (77.0,  26.3),
    "Gemini 2.5 Pro":    (58.0,  16.4),
    "Claude Sonnet 4.5": (None,  18.5),
}
model_colors = {
    "Claude Opus 4.6":    "#1d4ed8",
    "Gemini 3 Pro":       "#7c3aed",
    "Gemini 2.5 Pro":     "#9333ea",
    "Claude Sonnet 4.5":  "#2563eb",
}
# Manual vertical offsets (in points) for 128K-side labels to avoid collisions.
# Right-only (None at 128K) models use offset_y_right for the 1M-side label.
offset_y_left = {
    "Gemini 3 Pro":    12,   # 77.0 — lift above Opus 4.6 "no 128K" stub at 76
    "Gemini 2.5 Pro": -4,    # 58.0 — nudge down
}
offset_y_right = {
    "Claude Opus 4.6":   6,   # 76.0 — above dot
    "Gemini 3 Pro":      0,   # 26.3
    "Gemini 2.5 Pro":   -8,   # 16.4 — below Sonnet 4.5 (18.5)
    "Claude Sonnet 4.5": 6,   # 18.5 — above Gemini 2.5 Pro
}

fig, ax = plt.subplots(figsize=(9, 5.4), dpi=180)
x_left, x_right = 0, 1
for model, (a, b) in mrcr.items():
    color = model_colors[model]
    dy_r = offset_y_right.get(model, 0)
    if a is None:
        # Right-only: draw a dotted "n/a" stub extending leftward so the eye
        # does not read a phantom drop from 0% at 128K.
        ax.plot([x_left, x_right], [b, b], color=color, linewidth=1.0,
                linestyle=(0, (1, 3)), alpha=0.55, zorder=1)
        ax.scatter([x_left], [b], facecolor="white", edgecolor=color,
                   linewidth=1.2, s=28, zorder=2)
        ax.scatter([x_right], [b], color=color, s=40, zorder=3)
        # Stub text sits slightly below the stub line to avoid colliding with
        # adjacent model labels that share a similar y (e.g. Gemini 3 Pro at
        # 77 vs Opus 4.6 at 76).
        ax.annotate("no 128K", xy=(x_left, b), xytext=(-6, -10),
                    textcoords="offset points", fontsize=7.5,
                    color=MUTED, va="center", ha="right", style="italic")
        ax.annotate(f"  {model}: {b:.1f}%", xy=(x_right, b),
                    xytext=(8, dy_r), textcoords="offset points",
                    fontsize=9, color=color, va="center")
    else:
        dy_l = offset_y_left.get(model, 0)
        ax.plot([x_left, x_right], [a, b], color=color, linewidth=2.2, marker="o",
                markersize=6, zorder=2)
        # Model name on the 128K side, offset to avoid collisions.
        ax.annotate(f"{model}", xy=(x_left, a), xytext=(-10, dy_l),
                    textcoords="offset points", fontsize=9, color=color,
                    va="center", ha="right")
        # 1M-side value label uses the right-side offset.
        ax.annotate(f"{b:.1f}%", xy=(x_right, b), xytext=(8, dy_r),
                    textcoords="offset points", fontsize=9, color=color, va="center")
        # 128K value label tracks the model-name offset so they move together.
        ax.annotate(f"{a:.1f}%", xy=(x_left, a), xytext=(-10, dy_l + 12),
                    textcoords="offset points", fontsize=8, color=MUTED,
                    va="center", ha="right")

ax.set_xticks([x_left, x_right])
ax.set_xticklabels(["128K context", "1M context"], fontsize=10, color=INK)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_ylim(0, 100)
ax.set_xlim(-0.38, 1.45)
ax.grid(True, which="major", axis="y", color=BORDER, linewidth=0.8)
ax.set_axisbelow(True)
ax.set_ylabel("MRCR v2 8-needle accuracy")
ax.set_title("The 1M-context cliff — frontier models collapse from 128K to 1M",
             loc="left", pad=14, color=INK)
fig.text(0.01, 0.01,
         "All lines are MRCR v2 8-needle. Sources: Gemini 2.5/3 Pro model cards; "
         "Claude Opus 4.6 & Sonnet 4.5 announcements (Nov 2025). Dotted stub = no "
         "published 128K score (not a drop from 0%).",
         fontsize=7.5, color=MUTED)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(OUT / "context-rot-2026-v2-slope.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------------------------------------------------------------------------
# FIGURE 3 — Bar chart: short-context vs 32K for 4 models (Adobe Feb 2025)
# ---------------------------------------------------------------------------
bars = [
    ("GPT-4o",             99, 70),
    ("Gemini 2.5 Flash",   94, 48),
    ("Claude 3.5 Sonnet",  88, 30),
    ("Llama 4 Scout",      82, 22),
]

fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=180)
import numpy as np
labels = [b[0] for b in bars]
short = [b[1] for b in bars]
long_ = [b[2] for b in bars]
y = np.arange(len(labels))
h = 0.38
ax.barh(y - h/2, short, h, color="#dbeafe", edgecolor=ACCENT, linewidth=1.2,
        label="Short-context baseline")
ax.barh(y + h/2, long_, h, color=ACCENT, edgecolor=ACCENT, linewidth=1.2,
        label="32K tokens")
for i, (s, l) in enumerate(zip(short, long_)):
    ax.text(s + 1.5, i - h/2, f"{s}%", fontsize=9, va="center", color=INK)
    ax.text(l + 1.5, i + h/2, f"{l}%", fontsize=9, va="center", color="white"
            if l > 15 else INK,
            ha="left")
    drop = s - l
    ax.text(101, i, f"  −{drop} pts", fontsize=9, color="#dc2626",
            va="center", fontweight="600")

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=10, color=INK)
ax.invert_yaxis()
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.xaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_xlim(0, 120)
ax.grid(True, which="major", axis="x", color=BORDER, linewidth=0.8)
ax.set_axisbelow(True)
ax.set_xlabel("Accuracy")
ax.set_title("At 32K, every frontier model loses 20–60 points",
             loc="left", pad=14, color=INK)
ax.legend(loc="lower right", frameon=False)
fig.text(0.01, 0.01,
         "Source: Adobe long-context study (Feb 2025), via Understanding AI (Nov 2025).",
         fontsize=8, color=MUTED)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(OUT / "context-rot-2026-v3-bars.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

print("Wrote:")
for name in ("context-rot-2026-v1-lines.png", "context-rot-2026-v2-slope.png", "context-rot-2026-v3-bars.png"):
    p = OUT / name
    print(f"  {p}  ({p.stat().st_size // 1024} KB)")
