#!/usr/bin/env python3
"""Prepare five additional Long-20 source/output pairs for the project page."""
from __future__ import annotations

import subprocess
from pathlib import Path


PAGE = Path(__file__).resolve().parent
WORKSPACE = PAGE.parents[1]
PROJECT = WORKSPACE / "project/wan_dub"
INPUTS = PROJECT / "paper/long_video/external_inputs"
OUTPUTS = (
    PROJECT
    / "causal/experiments/r2a_ema200_ode_dmd_20261008/long_windowed_long20"
)
ASSETS = PAGE / "assets/paper/long/examples"
FFMPEG = PROJECT / "bench/bin/ffmpeg"
PAIRS = (3, 5, 6, 11, 18)


def run(*args: object) -> None:
    subprocess.run(
        [str(FFMPEG), "-loglevel", "error", "-y", "-nostdin", *map(str, args)],
        check=True,
    )


def transcode_video(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    run(
        "-i", source,
        "-t", 60,
        "-map", "0:v:0",
        "-an",
        "-vf", "scale='min(512,iw)':-2",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", 29,
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        destination,
    )


def transcode_audio(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    run(
        "-i", source,
        "-t", 60,
        "-vn",
        "-ac", 1,
        "-ar", 16000,
        "-c:a", "libmp3lame",
        "-b:a", "96k",
        destination,
    )


def main() -> None:
    for pair in PAIRS:
        name = f"pair{pair:02d}"
        source = INPUTS / name / "video.mp4"
        audio = INPUTS / name / "audio_cross.wav"
        output = OUTPUTS / f"{name}_60s.mp4"
        for path in (source, audio, output):
            if not path.is_file():
                raise FileNotFoundError(path)
        transcode_video(source, ASSETS / f"{name}_source.mp4")
        transcode_video(output, ASSETS / f"{name}_causaldub.mp4")
        transcode_audio(audio, ASSETS / f"{name}_replacement.mp3")
        print(name)


if __name__ == "__main__":
    main()
