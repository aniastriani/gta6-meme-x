#!/usr/bin/env python3
"""Composite the gta6-meme-x-01 meme: AI-generated Vice City cover art
(base.png) plus bold poster captions and the make.fun ghost.

The artwork itself is an original AI-generated scene (neon skyline,
palms, beach, an original duo by a convertible) — no photo, no Rockstar
asset. The ghost is make.fun's own press-kit mark (work/mark-1024.png),
kept small in the bottom-right corner over the darkened caption band.

Output: meme.png, 1080 x 1080, deterministic (fixed inputs, no clock,
no randomness).
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base.png")
OUT = os.path.join(HERE, "meme.png")
# The ghost mark lives beside the repo (work/), never inside it: it is
# make.fun's own press-kit asset, not part of the entry's snapshot.
MARK = os.path.join(HERE, "..", "work", "mark-1024.png")

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def shade_band(img, top, bottom, peak):
    """A vertical black gradient over [top, bottom), fading from `peak`
    alpha at one edge to transparent at the other, so white poster text
    reads over the busy artwork."""
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    span = bottom - top
    for y in range(top, bottom):
        # Top band fades downward, bottom band fades upward.
        if top == 0:
            a = int(peak * (1 - (y - top) / span))
        else:
            a = int(peak * ((y - top) / span))
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img.alpha_composite(band)


def best_size(text, limit, start):
    """Largest bold size (down to 28) whose line fits inside `limit` px."""
    size = start
    while size > 28:
        f = ImageFont.truetype(BOLD, size)
        if f.getbbox(text)[2] <= limit:
            return f
        size -= 2
    return ImageFont.truetype(BOLD, 28)


def poster_text(draw, lines, y_top, start_size, gap, stroke):
    """Centred white poster lines with a thick black outline."""
    y = y_top
    for line in lines:
        font = best_size(line, 1000, start_size)
        box = font.getbbox(line)
        w = box[2] - box[0]
        x = (W - w) // 2 - box[0]
        draw.text(
            (x, y), line, font=font, fill=(255, 255, 255),
            stroke_width=stroke, stroke_fill=(0, 0, 0),
        )
        y += (box[3] - box[1]) + gap
    return y


def main():
    img = Image.open(BASE).convert("RGBA")
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)

    # Darken the top and bottom edges so the captions read like a poster.
    shade_band(img, 0, 270, 150)
    shade_band(img, 800, H, 175)

    draw = ImageDraw.Draw(img)

    # The joke up top, the punchline down below.
    poster_text(draw, ["WAITED 13 YEARS", "FOR GTA 6"], 46, 96, 6, 8)
    poster_text(
        draw,
        ["GTA VI IS OUT.", "MY AGENT GOT PAID", "ON MAKE.FUN"],
        838, 64, 4, 6,
    )

    # The make.fun ghost, small in the bottom-right corner, clear of the
    # centred caption lines.
    ghost = Image.open(MARK).convert("RGBA")
    ghost = ghost.resize((150, 150), Image.LANCZOS)
    img.alpha_composite(ghost, (910, 910))

    img.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
