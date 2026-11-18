#!/usr/bin/env python3
"""The World in One Image — 18 November 2026.

Deterministically renders a one-page newspaper front page (SVG) that sums up
the world news of Wednesday, 18 November 2026 in a single image:

  * the top half is a seven-panel editorial collage (front-page.png, shipped
    in this repository) covering the day's biggest stories visually;
  * below it, each panel is captioned with the real headline it represents,
    with the outlets that reported it.

Pure standard library, no network, no clock, no randomness: running it any
number of times produces byte-identical output.

Run:  python3 main.py            -> writes output/front-page.svg
"""

import base64
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "front-page.png")
OUT_DIR = os.path.join(HERE, "output")
OUT = os.path.join(OUT_DIR, "front-page.svg")

DATE_LINE = "Wednesday, 18 November 2026"
MASTHEAD = "THE WORLD IN ONE IMAGE"
LEAD = "Trump Lands in Manila for Quad Summit Ahead of China Visit"

# (section, headline, one-line summary, panel in the collage)
STORIES = [
    (
        "LEAD STORY",
        "Trump arrives in Manila for Quad talks ahead of China visit",
        "The US president joins Quad and ASEAN leaders in Manila, with an "
        "APEC summit and a meeting with Xi Jinping next on the trip.",
        "Top panel: the arrival over Manila Bay, Quad flags below",
    ),
    (
        "WAR IN EUROPE",
        "Ukraine strikes the Crimean Bridge again as Russia pounds Kyiv",
        "Kyiv hits the Kerch Strait bridge for a second day while Russian "
        "strikes on bridges in the capital disrupt power and water.",
        "Middle left: the burning strait bridge under searchlights",
    ),
    (
        "MIDDLE EAST",
        "Iran attacks US military radar system in Bahrain with drones",
        "Tehran's drone strike on a US radar site in the Gulf sharpens the "
        "region's stand-off as energy infrastructure takes damage.",
        "Middle centre: drones over a desert radar dish at dusk",
    ),
    (
        "TECH & AI",
        "Nvidia revenue jumps 103% as board rules out Huang's return",
        "Bumper quarterly results from the AI chip giant land the same day "
        "its board shuts the door on Jensen Huang returning as CEO.",
        "Middle right: the glowing AI chip and its rising chart",
    ),
    (
        "MARKETS",
        "Stocks slide a third day as Fed officials float more rate hikes",
        "Wall Street and Asia fall again, the ASX drops 1.79%, and "
        "Washington blocks Chinese firms from leasing advanced AI chips "
        "through overseas data centres.",
        "Bottom centre: red arrows over the exchange skyline",
    ),
    (
        "TRADE",
        "Canada and China extend trade deals as Xi meets Carney",
        "Ottawa and Beijing widen their trade cooperation on the eve of "
        "the APEC leaders' meeting in Shenzhen.",
        "Bottom right: the container port working the new trade",
    ),
    (
        "WEATHER",
        "Cyclone Akvan intensifies over the Bay of Bengal",
        "The storm is expected to become severe by 19 November, with "
        "India's east coast on high alert and flights cancelled.",
        "Bottom left: the cyclone swirling in from the ocean",
    ),
]

ALSO_NOTED = (
    "Also on 18 Nov: the US loses its measles elimination status amid the "
    "worst outbreak since 1991 \u00b7 Anthropic is set to price its IPO this "
    "evening ahead of a Nasdaq debut \u00b7 Britain, Australia, Canada and "
    "Italy press Israel over settlement sanctions and Gaza aid access."
)

SOURCES = (
    "Compiled 18 Nov 2026 from Jagran Josh and Education Times school-"
    "assembly headline briefings, the Balanced News UK daily update "
    "(BBC / Guardian / Independent / Mail / Sky), KimKJ Global Economy "
    "Top 10, the Kalgoorlie Miner and The Paris Eye breaking-news pages."
)


def esc(text):
    return html.escape(text, quote=True)


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def main():
    with open(ART, "rb") as fh:
        art_b64 = base64.b64encode(fh.read()).decode("ascii")

    W = 1600
    art_w, art_h = 1520, 1013  # shipped art is 1920x1280 (3:2)
    art_x, art_y = (W - art_w) // 2, 210
    cards_top = art_y + art_h + 36
    card_h = 168
    rows = (len(STORIES) + 1) // 2
    also_y = cards_top + rows * (card_h + 18) + 8
    H = also_y + 118

    p = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">'
    )
    p.append(f'<rect width="{W}" height="{H}" fill="#0e2233"/>')
    p.append(f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" '
             f'fill="#f7f1e3"/>')

    # Masthead
    p.append(
        f'<text x="{W // 2}" y="104" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="64" font-weight="bold" '
        f'fill="#12293e">{esc(MASTHEAD)}</text>'
    )
    p.append(
        f'<text x="{W // 2}" y="146" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="26" fill="#5a4632">'
        f'{esc(DATE_LINE)} \u00b7 One image, the whole day</text>'
    )
    p.append(f'<line x1="60" y1="168" x2="{W - 60}" y2="168" '
             f'stroke="#12293e" stroke-width="3"/>')
    p.append(
        f'<text x="{W // 2}" y="198" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="25" font-style="italic" '
        f'fill="#7a2e22">Lead: {esc(LEAD)}</text>'
    )

    # The collage itself
    p.append(
        f'<image x="{art_x}" y="{art_y}" width="{art_w}" height="{art_h}" '
        f'href="data:image/png;base64,{art_b64}"/>'
    )
    p.append(
        f'<rect x="{art_x}" y="{art_y}" width="{art_w}" height="{art_h}" '
        f'fill="none" stroke="#12293e" stroke-width="4"/>'
    )

    # Headline cards, two per row
    col_w = (W - 120 - 18) // 2
    for i, (section, headline, summary, panel) in enumerate(STORIES):
        cx = 60 + (i % 2) * (col_w + 18)
        cy = cards_top + (i // 2) * (card_h + 18)
        p.append(f'<rect x="{cx}" y="{cy}" width="{col_w}" height="{card_h}" '
                 f'fill="#ffffff" stroke="#c9b894" stroke-width="1.5"/>')
        p.append(f'<rect x="{cx}" y="{cy}" width="{col_w}" height="30" '
                 f'fill="#12293e"/>')
        p.append(
            f'<text x="{cx + 14}" y="{cy + 21}" font-family="Verdana, '
            f'sans-serif" font-size="15" font-weight="bold" fill="#f7f1e3">'
            f'{esc(section)}</text>'
        )
        ty = cy + 58
        for line in wrap(headline, 44):
            p.append(
                f'<text x="{cx + 14}" y="{ty}" font-family="Georgia, serif" '
                f'font-size="20" font-weight="bold" fill="#12293e">'
                f'{esc(line)}</text>'
            )
            ty += 24
        for line in wrap(summary, 62):
            p.append(
                f'<text x="{cx + 14}" y="{ty + 2}" font-family="Georgia, '
                f'serif" font-size="14.5" fill="#3c3c3c">{esc(line)}</text>'
            )
            ty += 18
        p.append(
            f'<text x="{cx + 14}" y="{cy + card_h - 10}" font-family="Verdana, '
            f'sans-serif" font-size="11.5" font-style="italic" '
            f'fill="#7a2e22">In the picture: {esc(panel)}</text>'
        )

    # Also-noted strip + sources
    p.append(f'<rect x="60" y="{also_y}" width="{W - 120}" height="64" '
             f'fill="#efe6cf"/>')
    ty = also_y + 24
    for line in wrap(ALSO_NOTED, 118):
        p.append(
            f'<text x="76" y="{ty}" font-family="Georgia, serif" '
            f'font-size="15.5" fill="#333333">{esc(line)}</text>'
        )
        ty += 20
    p.append(
        f'<text x="60" y="{also_y + 96}" font-family="Verdana, sans-serif" '
        f'font-size="12" fill="#666666">{esc(SOURCES)}</text>'
    )
    p.append("</svg>")

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(p) + "\n")
    print(f"Wrote {OUT}")
    print(f"Front page: {len(STORIES)} stories, lead: {LEAD}")


if __name__ == "__main__":
    main()
