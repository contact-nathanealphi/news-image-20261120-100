#!/usr/bin/env python3
"""Copy the bundled front page into the harness output directory.

The image is pre-rendered (see tools/render.py) and shipped in this
repository, so this program only moves bytes: it reads no input, calls no
network, and every run writes exactly the same file.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "assets" / "entry.png"
OUT_NAME = "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, out_dir / OUT_NAME)
    return 0


if __name__ == "__main__":
    sys.exit(main())
