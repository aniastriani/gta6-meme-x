#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: a Vice City sunset, the make.fun ghost,
and the thirteen-year wait for GTA 6.

Original artwork drawn with Pillow. The ghost is make.fun's own mark from
its press kit (work/mark-1024.png), composited into the scene the way the
bounty's rules suggest. Everything else — sky, sun, skyline, palms, road
and captions — is drawn here from scratch. No photo, no Rockstar asset.

Output: meme.png, 1080 x 1080, deterministic (no randomness, no clock).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1080
OUT = "meme.png"
# The ghost mark lives beside the repo (work/), never inside it: it is
# make.fun's own press-kit asset, not part of the entry's snapshot.
MARK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "work", "mark-1024.png")

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky(draw):
    """Vice City sunset: deep purple up top, magenta, then orange at the sea."""
    stops = [
        (0.00, (26, 8, 54)),
        (0.35, (96, 32, 116)),
        (0.62, (198, 64, 110)),
        (0.80, (255, 122, 89)),
        (1.00, (255, 176, 102)),
    ]
    for y in range(720):
        t = y / 719
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0) if t1 > t0 else 0
                draw.line([(0, y), (W, y)], fill=lerp(c0, c1, f))
                break


def sun(base):
    """A low sun with a soft glow, left of centre so the ghost stands clear."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    cx, cy, r = 360, 520, 120
    for i in range(6, 0, -1):
        g.ellipse(
            [cx - r * i // 3, cy - r * i // 3, cx + r * i // 3, cy + r * i // 3],
            fill=(255, 214, 130, 26),
        )
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    base.alpha_composite(glow)
    d = ImageDraw.Draw(base)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 170, 255))
    d.ellipse([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14],
              fill=(255, 244, 205, 255))


def skyline(draw):
    """Dark Leonida towers with a few lit windows, along the horizon."""
    tops = [
        (0, 640, 70, 690), (70, 600, 130, 690), (130, 655, 210, 690),
        (210, 590, 280, 690), (280, 650, 360, 690), (360, 610, 430, 690),
        (430, 660, 520, 690), (520, 600, 590, 690), (590, 655, 680, 690),
        (680, 585, 760, 690), (760, 650, 850, 690), (850, 605, 920, 690),
        (920, 660, 1000, 690), (1000, 615, 1080, 690),
    ]
    for x0, y0, x1, y1 in tops:
        draw.rectangle([x0, y0, x1, y1], fill=(38, 14, 64))
    # A handful of lit windows, fixed positions.
    wins = [
        (96, 622), (160, 668), (236, 612), (312, 664), (392, 630),
        (462, 672), (548, 620), (620, 668), (712, 606), (796, 666),
        (880, 626), (952, 672), (1032, 636),
    ]
    for x, y in wins:
        draw.rectangle([x, y, x + 10, y + 14], fill=(255, 214, 130))


def palm(draw, x, y, s, lean):
    """One palm silhouette: a leaning trunk and seven drooping fronds."""
    # Trunk: a chain of short segments curving with the lean.
    px, py = x, y
    for i in range(9):
        nx = px + lean * (i + 1) * 2.2
        ny = py - s * 0.11
        draw.line([(px, py), (nx, ny)], fill=(24, 8, 40), width=int(13 - i))
        px, py = nx, ny
    cx, cy = px, py  # crown
    for k in range(7):
        ang = math.pi * (0.08 + 0.14 * k)  # fan from up-left to up-right
        ex = cx + math.cos(ang) * s * 0.52 * (1 if k % 2 == 0 else -1)
        ey = cy - math.sin(ang) * s * 0.30 + s * 0.16
        mx = (cx + ex) / 2
        my = min(cy, ey) - s * 0.10
        # A frond is a thick quadratic-ish curve, drawn as segments.
        prev = (cx, cy)
        for t_i in range(1, 9):
            t = t_i / 8
            bx = (1 - t) ** 2 * cx + 2 * (1 - t) * t * mx + t * t * ex
            by = (1 - t) ** 2 * cy + 2 * (1 - t) * t * my + t * t * ey
            draw.line([prev, (bx, by)], fill=(24, 8, 40), width=9)
            prev = (bx, by)
    # Coconuts.
    draw.ellipse([cx - 12, cy - 4, cx + 2, cy + 10], fill=(24, 8, 40))
    draw.ellipse([cx + 2, cy - 2, cx + 16, cy + 12], fill=(24, 8, 40))


def road(draw):
    """Dark asphalt foreground with a dashed centre line near the foot."""
    draw.rectangle([0, 690, W, H], fill=(22, 10, 38))
    draw.rectangle([0, 690, W, 700], fill=(255, 176, 102))
    for x in range(40, W, 160):
        draw.rectangle([x, 1036, x + 90, 1052], fill=(255, 214, 130))


def fit_font(text, max_w, start):
    """Largest bold size (down to 28) that fits the line inside max_w."""
    size = start
    while size > 28:
        f = ImageFont.truetype(BOLD, size)
        if f.getbbox(text)[2] <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(BOLD, 28)


def caption(draw, lines, y_top, start_size, gap):
    """Centred white meme text with a thick black outline, one line per row."""
    y = y_top
    for line in lines:
        font = fit_font(line, 1000, start_size)
        box = font.getbbox(line)
        w = box[2] - box[0]
        x = (W - w) // 2 - box[0]
        draw.text(
            (x, y), line, font=font, fill=(255, 255, 255),
            stroke_width=7, stroke_fill=(0, 0, 0),
        )
        y += (box[3] - box[1]) + gap
    return y


def main():
    base = Image.new("RGBA", (W, H), (26, 8, 54, 255))
    draw = ImageDraw.Draw(base)
    sky(draw)
    sun(base)
    draw = ImageDraw.Draw(base)
    skyline(draw)
    # Palms frame the scene, leaning in from both edges, crowns in-frame.
    palm(draw, 130, 760, 300, -0.6)
    palm(draw, 950, 760, 300, 0.6)
    road(draw)
    draw = ImageDraw.Draw(base)

    # The make.fun ghost, worked into the scene: standing on the road to the
    # right of the sun, big enough to read at 480 px, with a soft shadow
    # grounding it. The mark carries its own magenta coin.
    draw.ellipse([570, 846, 830, 870], fill=(0, 0, 0, 90))
    ghost = Image.open(MARK).convert("RGBA")
    ghost = ghost.resize((340, 340), Image.LANCZOS)
    base.alpha_composite(ghost, (530, 520))
    draw = ImageDraw.Draw(base)

    # Captions: the joke up top, the punchline down below.
    caption(draw, ["WAITED 13 YEARS", "FOR GTA 6"], 56, 96, 6)
    caption(draw, ["GTA VI IS OUT.", "MY AGENT GOT PAID ON MAKE.FUN"], 872, 62, 4)

    base.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
