#!/usr/bin/env python3
"""Build entry.png — the final one-image summary of 18 November 2026.

Build-time tool only (uses Pillow, which the grader never runs): it takes
the seven-panel editorial collage in front-page.png, lays it under a
masthead that names the day, and captions it with the day's seven biggest
headlines in short, large, high-contrast type that stays legible when the
image is scaled down to ~300 px wide.

The result is written to entry.png beside this script, at 1024x1024 and at
most 1 MiB: a true PNG is used when it fits, otherwise the same pixels are
saved as JPEG bytes under the entry.png name (the competition rules tell
PNG and JPEG apart by their first bytes and allow either under that name).

Run:  python3 build_image.py   ->  writes entry.png
"""

import io
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ART_PATH = os.path.join(HERE, "front-page.png")
OUT_PATH = os.path.join(HERE, "entry.png")

W = H = 1024
MAX_BYTES = 1048576

NAVY = (18, 41, 62)
CREAM = (247, 241, 227)
WHITE = (255, 255, 255)
INK = (16, 24, 32)
RED = (140, 43, 27)
GOLD = (232, 199, 102)
CARD_BORDER = (201, 184, 148)

DATE_LINE = "Wednesday, 18 November 2026"
MASTHEAD = "THE WORLD IN ONE IMAGE"
FOOTER = "The whole day in one picture - 18 November 2026"

# (tag, headline) — wording kept short on purpose so the type can stay big.
STORIES = [
    ("LEAD", "Trump arrives in Manila for Quad talks ahead of China visit"),
    ("UKRAINE", "Ukraine strikes Crimean Bridge again; Russia pounds Kyiv"),
    ("IRAN", "Iran attacks US radar in Bahrain with drones"),
    ("NVIDIA", "Nvidia revenue jumps 103%"),
    ("MARKETS", "Stocks slide a third day as Fed floats more rate hikes"),
    ("TRADE", "Canada & China extend trade deals: Xi meets Carney"),
    ("STORM", "Cyclone Akvan intensifies over the Bay of Bengal"),
]

FONT_DIR = "/usr/share/fonts/truetype/liberation"
DEJAVU_DIR = "/usr/share/fonts/truetype/dejavu"


def font(filename, size, fallback_dir=DEJAVU_DIR):
    path = os.path.join(FONT_DIR, filename)
    if not os.path.exists(path):
        path = os.path.join(fallback_dir, filename.replace("Liberation", "DejaVu"))
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap measured with the real font, never by char count."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def build_canvas():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # --- Masthead: navy band, title in cream, the date in gold, both big.
    draw.rectangle([0, 0, W, 126], fill=NAVY)
    title_font = font("LiberationSerif-Bold.ttf", 46)
    date_font = font("LiberationSans-Bold.ttf", 33)
    draw.text((W // 2, 10), MASTHEAD, font=title_font, fill=CREAM,
              anchor="ma")
    draw.text((W // 2, 68), DATE_LINE, font=date_font, fill=GOLD,
              anchor="ma")
    draw.rectangle([0, 126, W, 132], fill=RED)

    # --- The collage art, cover-cropped to a wide band under the masthead.
    art = Image.open(ART_PATH).convert("RGB")
    art = ImageOps.fit(art, (W - 48, 396), Image.LANCZOS)
    img.paste(art, (24, 144))
    draw.rectangle([24, 144, W - 24, 144 + 396], outline=NAVY, width=4)

    # --- Headline cards: one per story, white on cream, ink-black bold
    # type with a coloured tag chip so each story reads at a glance.
    headline_font = font("LiberationSans-Bold.ttf", 28)
    tag_font = font("LiberationSans-Bold.ttf", 19)
    text_x = 196
    text_width = W - 48 - text_x + 24 - 16
    y = 556
    for i, (tag, headline) in enumerate(STORIES):
        lines = wrap(draw, headline, headline_font, text_width)
        row_h = len(lines) * 34 + 16
        accent = RED if i == 0 else NAVY
        draw.rectangle([24, y, W - 24, y + row_h], fill=WHITE,
                       outline=CARD_BORDER, width=2)
        draw.rectangle([24, y, 36, y + row_h], fill=accent)
        # Tag chip: fixed-width label so the headlines line up in a column.
        draw.rectangle([48, y + 10, 184, y + row_h - 10], fill=accent)
        tag_w = draw.textlength(tag, font=tag_font)
        draw.text((48 + (136 - tag_w) / 2, y + row_h / 2), tag,
                  font=tag_font, fill=WHITE, anchor="lm")
        ty = y + 8
        for line in lines:
            draw.text((text_x, ty), line, font=headline_font, fill=INK)
            ty += 34
        y += row_h + 8

    # --- Footer strip repeats the date so the day survives any crop.
    footer_font = font("LiberationSans-Bold.ttf", 23)
    draw.rectangle([0, H - 44, W, H], fill=NAVY)
    draw.text((W // 2, H - 38), FOOTER, font=footer_font, fill=GOLD,
              anchor="ma")
    assert y <= H - 52, f"caption cards overflow: last card ends at {y}"
    return img


def save_within_limit(img, path):
    """PNG if it fits in 1 MiB, else JPEG bytes (rules allow either)."""
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    data = buf.getvalue()
    if len(data) <= MAX_BYTES:
        with open(path, "wb") as fh:
            fh.write(data)
        return "PNG", len(data)
    for quality in (88, 84, 80, 76, 72, 68, 64, 60):
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True,
                 progressive=False, subsampling=1)
        data = buf.getvalue()
        if len(data) <= MAX_BYTES:
            with open(path, "wb") as fh:
                fh.write(data)
            return "JPEG", len(data)
    raise SystemExit("could not fit the image within 1 MiB")


def main():
    img = build_canvas()
    fmt, size = save_within_limit(img, OUT_PATH)
    print(f"Wrote {OUT_PATH}")
    print(f"format={fmt} bytes={size} dimensions={img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
