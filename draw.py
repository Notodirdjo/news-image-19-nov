#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page as a PNG.

The picture is a newspaper front page: a navy masthead naming the paper
and the day, five story blocks with a coloured region tag, a bold
headline and a short plain summary each, and an "ALSO TODAY" strip at
the foot with four shorter items. Every word comes from the verified
brief for this competition; nothing is invented here.

Run: python3 draw.py  -> writes entry.png beside this file (1024x1024).
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (247, 243, 234)      # off-white newsprint
INK = (24, 24, 24)           # near-black text
NAVY = (20, 38, 74)          # masthead band
RED = (178, 34, 34)          # single red accent
RULE = (150, 148, 138)       # thin grey rule
FOOT_BG = (232, 228, 218)    # footer strip background

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


STORIES = [
    {
        "tag": "SHENZHEN",
        "colour": (31, 58, 95),
        "headline": "Trump, Xi and Putin hold first three-way summit",
        "summary": (
            "The three leaders met in Shenzhen at APEC and agreed to talks "
            "on cutting nuclear risks. Ukraine, Iran and trade were "
            "discussed; no major deal was announced."
        ),
    },
    {
        "tag": "THE HAGUE",
        "colour": (15, 118, 110),
        "headline": "UN court: Myanmar committed Rohingya genocide",
        "summary": (
            "The court found genocidal intent in the 2017 crackdown, about "
            "10,000 Rohingya killed, and ordered investigations, "
            "compensation and the return of the displaced."
        ),
    },
    {
        "tag": "GAMING",
        "colour": (107, 33, 168),
        "headline": "GTA VI launches worldwide after a 13-year wait",
        "summary": (
            "Grand Theft Auto VI went on sale around the world on Thursday, "
            "rolling out at local midnight in each region. It is on "
            "PlayStation 5 and Xbox Series X|S only."
        ),
    },
    {
        "tag": "MARKETS",
        "colour": (22, 101, 52),
        "headline": "Anthropic IPO raises about $81 billion, a record",
        "summary": (
            "The company behind the Claude chatbot priced shares at $83 in "
            "its initial public offering, with trading starting on Thursday."
        ),
    },
    {
        "tag": "KERCH BRIDGE",
        "colour": (185, 28, 28),
        "headline": "Ukraine hits the bridge a third time this week",
        "summary": (
            "Russia said Ukraine attacked the Crimean Bridge again. The "
            "rail section was hit and train traffic halted, days after the "
            "main road arch fell into the strait."
        ),
    },
]

ALSO_TODAY = [
    "Bangladesh unrest spreads; Muhammad Yunus's ancestral home is set "
    "ablaze, four killed.",
    "Israeli tanks push into central Gaza beyond the Yellow Line, "
    "despite the ceasefire.",
    "Cyclone Akvan nears India's Andhra Pradesh-Odisha coast, due to "
    "land on Friday.",
    "A Van Gogh sells for $190.4 million at Sotheby's, a record for "
    "the artist.",
]


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 40
    text_w = W - 2 * margin

    # --- Masthead: navy band with the paper's name -------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title = font(BOLD, 56)
    d.text((W / 2, 30), "THE WORLD IN ONE DAY", font=title,
           fill=(255, 255, 255), anchor="ma")

    # --- Date line, in red, under a red rule -------------------------
    d.rectangle([0, 118, W, 124], fill=RED)
    date_font = font(BOLD, 40)
    d.text((W / 2, 140), "Thursday 19 November 2026", font=date_font,
           fill=NAVY, anchor="ma")
    d.line([margin, 196, W - margin, 196], fill=RULE, width=2)

    # --- Five story blocks -------------------------------------------
    tag_font = font(BOLD, 21)
    head_font = font(BOLD, 30)
    body_font = font(REG, 22)
    y = 214
    for i, story in enumerate(STORIES):
        # coloured tag, small caps, with a square bullet
        d.rectangle([margin, y + 4, margin + 12, y + 16],
                    fill=story["colour"])
        d.text((margin + 20, y), story["tag"], font=tag_font,
               fill=story["colour"], anchor="la")
        y += 28
        # bold headline, one line (checked to fit inside the margins)
        head_w = d.textlength(story["headline"], font=head_font)
        assert head_w <= text_w, f"headline too wide: {story['headline']}"
        d.text((margin, y), story["headline"], font=head_font,
               fill=INK, anchor="la")
        y += 38
        # summary, wrapped to at most two lines
        lines = wrap(d, story["summary"], body_font, text_w)
        assert len(lines) <= 2, f"summary too long: {story['summary']}"
        for line in lines:
            d.text((margin, y), line, font=body_font, fill=(52, 52, 52),
                   anchor="la")
            y += 26
        if i < len(STORIES) - 1:
            y += 6
            d.line([margin, y, W - margin, y], fill=RULE, width=1)
            y += 10

    # --- Footer strip: ALSO TODAY ------------------------------------
    foot_top = y + 4
    d.rectangle([0, foot_top, W, H], fill=FOOT_BG)
    d.line([0, foot_top, W, foot_top], fill=NAVY, width=3)
    label_font = font(BOLD, 24)
    item_font = font(REG, 20)
    d.text((margin, foot_top + 10), "ALSO TODAY", font=label_font,
           fill=RED, anchor="la")
    # one item per line, full width, each kept to a single line
    yy = foot_top + 46
    for item in ALSO_TODAY:
        text = "\u2022  " + item
        assert d.textlength(text, font=item_font) <= text_w, \
            f"footer item too wide: {item}"
        d.text((margin, yy), text, font=item_font, fill=INK, anchor="la")
        yy += 26

    return img


def main():
    img = draw_page()
    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    with open(OUT, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]} {size} bytes")
    print(f"sha256 {digest}")


if __name__ == "__main__":
    main()
