#!/usr/bin/env python3
"""Render terminal-like screenshots from recorded command output."""
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BG = (18, 18, 18)
FG = (230, 230, 230)
ACCENT = (120, 200, 120)
PROMPT = (80, 180, 255)
PAD_X = 24
PAD_Y = 20
LINE_H = 22


def wrap_line(line: str, width: int) -> list[str]:
    if not line:
        return [""]
    if len(line) <= width:
        return [line]
    return textwrap.wrap(line, width=width, replace_whitespace=False, drop_whitespace=False) or [""]


def render(text: str, out: Path, title: str, cols: int = 110) -> None:
    font = ImageFont.truetype(FONT_PATH, 14)
    raw_lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines: list[str] = []
    for line in raw_lines:
        lines.extend(wrap_line(line.rstrip("\n"), cols))
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if not lines:
        lines = [""]

    width = PAD_X * 2 + cols * 8
    height = PAD_Y * 2 + 36 + len(lines) * LINE_H
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, width, 32), fill=(40, 40, 40))
    draw.ellipse((12, 10, 22, 20), fill=(255, 95, 86))
    draw.ellipse((30, 10, 40, 20), fill=(255, 189, 46))
    draw.ellipse((48, 10, 58, 20), fill=(39, 201, 63))
    draw.text((76, 8), title, font=font, fill=(210, 210, 210))

    y = 44
    for line in lines:
        color = FG
        if line.startswith("$ ") or line.startswith("ivan@") or line.startswith("# "):
            color = PROMPT
        elif line.startswith("==="):
            color = ACCENT
        draw.text((PAD_X, y), line, font=font, fill=color)
        y += LINE_H

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("--title", default="terminal")
    args = parser.parse_args()
    text = Path(args.infile).read_text(encoding="utf-8", errors="replace")
    render(text, Path(args.outfile), args.title)


if __name__ == "__main__":
    main()
