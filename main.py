#!/usr/bin/env python3
"""Place the 19 November 2026 front page where make.fun expects it.

The artwork (entry.png) is drawn ahead of time by draw.py and sits in
this same directory. This entrypoint only moves a copy of it into the
output directory the grader provides, so the run stays fast, offline
and deterministic.

Only the standard library is used. The output directory is created if
it does not exist yet; it is never deleted, because the grader mounts
it and removing it would break the run.
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run() -> Path:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)

    source = ROOT / "entry.png"
    if not source.is_file():
        raise SystemExit("entry.png not found next to main.py; run draw.py first")

    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise SystemExit("copied entry.png has the wrong size")
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return target


if __name__ == "__main__":
    run()
