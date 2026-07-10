import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

TABLES = {
    "reading": (0.5, 6.0, "reading  (FACT)", [
        "reading_id       INT  PK",
        "reading_ts       DATETIME  (UNIQUE, idx)",
        "appliances_wh    INT   <- target",
        "lights_wh        INT",
    ]),
    "indoor_climate": (5.6, 8.6, "indoor_climate", [
        "reading_id  INT  PK, FK",
        "t1..t9      DOUBLE",
        "rh_1..rh_9  DOUBLE",
    ]),
    "weather": (5.6, 3.2, "weather", [
        "reading_id   INT  PK, FK",
        "t_out, rh_out, tdewpoint  DOUBLE",
        "press_mm_hg, windspeed    DOUBLE",
        "visibility                DOUBLE",
    ]),
}


def box(ax, x, y, title, rows, w=4.2):
    h = 0.5 + 0.42 * len(rows)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.02",
                                fc="#EAF1FB", ec="#2C5EA8", lw=1.6))
    ax.text(x + w / 2, y - 0.32, title, ha="center", va="center",
            fontsize=11, fontweight="bold", color="#1B3B6F")
    ax.plot([x, x + w], [y - 0.55, y - 0.55], color="#2C5EA8", lw=1)
    for i, r in enumerate(rows):
        ax.text(x + 0.15, y - 0.85 - i * 0.42, r, ha="left", va="center",
                fontsize=8.5, family="monospace")
    return (x, y, w, h)


def main():
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 11); ax.set_ylim(0, 9); ax.axis("off")
    coords = {name: box(ax, *vals) for name, (vals) in
              [(n, (v[0], v[1], v[2], v[3])) for n, v in TABLES.items()]}

    # 1:1 relationship arrows from reading to the two child tables
    for child in ("indoor_climate", "weather"):
        x, y, w, h = coords[child]
        rx, ry, rw, rh = coords["reading"]
        ax.add_patch(FancyArrowPatch((rx + rw, ry - 1.0), (x, y - 0.6),
                     arrowstyle="-|>", mutation_scale=14, color="#C44E52", lw=1.6))
        ax.text((rx + rw + x) / 2, (ry - 1.0 + y - 0.6) / 2 + 0.15, "1:1",
                fontsize=9, color="#C44E52", fontweight="bold")

    ax.set_title("ERD - energy_ts  (relational schema, Task 2)",
                 fontsize=13, fontweight="bold")
    out = os.path.join(os.path.dirname(__file__), "erd.png")
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print("Saved", out)


if __name__ == "__main__":
    main()
