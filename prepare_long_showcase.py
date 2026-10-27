#!/usr/bin/env python3
"""Prepare five additional Long-20 source/output pairs for the project page."""
from __future__ import annotations

import json
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


def probe_size(source: Path) -> tuple[int, int]:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "json", str(source),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    stream = json.loads(result.stdout)["streams"][0]
    return int(stream["width"]), int(stream["height"])


def transcode_source(concat_list: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    run(
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-t", 60,
        "-map", "0:v:0",
        "-map", "0:a:0?",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", 29,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "96k",
        "-ac", 1,
        "-movflags", "+faststart",
        destination,
    )


def transcode_output(
    source: Path, replacement_audio: Path, size: tuple[int, int], destination: Path
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    width, height = size
    run(
        "-i", source,
        "-i", replacement_audio,
        "-t", 60,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-vf", f"scale={width}:{height}",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", 29,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "96k",
        "-ac", 1,
        "-ar", 16000,
        "-shortest",
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
        source_list = INPUTS / name / "source.concat.txt"
        audio = INPUTS / name / "audio_cross.wav"
        output = OUTPUTS / f"{name}_60s.mp4"
        for path in (source, source_list, audio, output):
            if not path.is_file():
                raise FileNotFoundError(path)
        size = probe_size(source)
        transcode_source(source_list, ASSETS / f"{name}_source.mp4")
        transcode_output(
            output, audio, size, ASSETS / f"{name}_causaldub.mp4"
        )
        transcode_audio(audio, ASSETS / f"{name}_replacement.mp3")
        print(name, f"{size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
