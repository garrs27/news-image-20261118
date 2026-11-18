#!/usr/bin/env python3
"""The World in One Image — Wednesday, 18 November 2026.

The entry image (entry.png, shipped in this repository) sums up the world
news of Wednesday, 18 November 2026 in one 1024x1024 picture: a masthead
naming the day, the seven-panel editorial collage from front-page.png, and
short headline captions for the day's seven biggest stories — Trump in
Manila for the Quad talks, Ukraine's strike on the Crimean Bridge, Iran's
drone attack on a US radar in Bahrain, Nvidia's revenue jump, a third day
of sliding stocks, the Canada-China trade deals, and Cyclone Akvan.

This program copies that image to the grader's output location:
MAKEFUN_OUTPUT_DIR/entry.png when the environment variable is set (the
local stand-in for /output), otherwise /output/entry.png.

Pure standard library, no network, no clock, no randomness: every run
writes exactly the bytes of the shipped entry.png.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   ->  writes out/entry.png
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.png")


def main():
    dest = output_path()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    size = os.path.getsize(dest)
    print(f"Wrote {dest} from {SOURCE} ({size} bytes)")


if __name__ == "__main__":
    main()
