"""Regenerate animated GIF CB thumbs with ffmpeg two-pass shared palette.
Uses imageio_ffmpeg's bundled binary (no system install).
Recipe from prior Max Mustard CB fix: height<=400, 10fps, 128 colors, Bayer dither.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parent.parent / "Img" / "Content Posts" / "Genies"

JOBS = [
    (ROOT / "Doll" / "HaraARAnimBaked.gif", ROOT / "Doll" / "HaraARAnimBaked_CB.gif"),
    (ROOT / "Doll" / "Hara_FinalShapes_01.gif", ROOT / "Doll" / "Hara_FinalShapes_01_CB.gif"),
    (ROOT / "Doll" / "sample_02.gif", ROOT / "Doll" / "sample_02_CB.gif"),
    (ROOT / "AnimTest_01.gif", ROOT / "AnimTest_01_CB.gif"),
    (ROOT / "final main.gif", ROOT / "final main_CB.gif"),
]

VF = (
    "fps=10,"
    "scale=-2:'min(400,ih)':flags=lanczos,"
    "split[s0][s1];"
    "[s0]palettegen=max_colors=128:stats_mode=diff[p];"
    "[s1][p]paletteuse=dither=bayer:bayer_scale=3"
)


def main() -> None:
    print("ffmpeg:", FF)
    for src, dst in JOBS:
        if not src.is_file():
            print("missing", src)
            continue
        cmd = [
            FF,
            "-y",
            "-i",
            str(src),
            "-filter_complex",
            VF,
            "-gifflags",
            "-offsetting",
            str(dst),
        ]
        print("encoding", src.name, "...")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("FAIL", src.name)
            print(r.stderr[-1000:])
            continue
        print(
            f"OK {dst.name}: {dst.stat().st_size / 1024 / 1024:.2f}MB "
            f"(src {src.stat().st_size / 1024 / 1024:.2f}MB)"
        )


if __name__ == "__main__":
    main()
