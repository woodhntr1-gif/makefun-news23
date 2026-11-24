#!/usr/bin/env python3
"""Entry point for the 23 November 2026 news image.

The finished front page is rendered at build time by render.py and
stored in this repository as entry.png. At run time this script does
nothing but copy that file, byte for byte, into the output directory
the harness provides. There is no drawing, no font handling, no
network access and no randomness here, so every run writes exactly
the same bytes.
"""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def destination() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = Path(out_dir) / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def main() -> None:
    target = destination()
    shutil.copyfile(SOURCE, target)
    print(f"copied {SOURCE} -> {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
