#!/usr/bin/env python3
"""Build the reproducible 4-benchmark × 6-example comparison showcase."""
from __future__ import annotations

import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


PAGE = Path(__file__).resolve().parent
PROJECT = PAGE.parent
BENCH = PROJECT / "bench"
ASSETS = PAGE / "assets/paper/benchmark_showcase"
MANIFEST = PAGE / "benchmark_showcase_manifest.json"
FFMPEG = BENCH / "bin/ffmpeg"
OURS = "r2a_dmd2"

BENCHMARKS = {
    "HDTF": {
        "directory": "hdtf",
        "regime": "Captured source",
        "aspect": "wide",
        "wav2lip": "wav2lip",
    },
    "VoxCeleb2": {
        "directory": "vox2",
        "regime": "Captured in the wild",
        "aspect": "square",
        "wav2lip": "wav2lip",
    },
    "TalkVid": {
        "directory": "talkvid",
        "regime": "Web source",
        "aspect": "wide",
        "wav2lip": "wav2lip_rf1",
    },
    "CausalDub-Bench": {
        "directory": "causaldub",
        "regime": "Generated source",
        "aspect": "square",
        "wav2lip": "wav2lip",
    },
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def common_candidates(directory: str, wav2lip: str) -> list[tuple[float, dict]]:
    items = read_jsonl(BENCH / "data" / directory / "items.jsonl")
    methods = (wav2lip, "latentsync", "lipforcing_14b_fix", OURS)
    candidates = []
    for item in items:
        key = item["key"]
        outputs = [BENCH / "out" / directory / method / f"{key}__cross.mp4" for method in methods]
        metric_path = BENCH / "metrics" / directory / OURS / f"{key}__cross.json"
        if not metric_path.is_file() or not all(path.is_file() for path in outputs):
            continue
        metric = json.loads(metric_path.read_text())
        if metric.get("sync_fail") or not isinstance(metric.get("lse_c"), (int, float)):
            continue
        candidates.append((float(metric["lse_c"]), item))
    candidates.sort(key=lambda row: (-row[0], row[1]["key"]))
    if len(candidates) < 6:
        raise RuntimeError(f"{directory}: only {len(candidates)} complete common candidates")
    return candidates[:6]


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def transcode_video(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and destination.stat().st_mtime >= source.stat().st_mtime:
        return
    run(
        [
            str(FFMPEG),
            "-loglevel",
            "error",
            "-y",
            "-nostdin",
            "-i",
            str(source),
            "-t",
            "5",
            "-an",
            "-vf",
            "scale='min(480,iw)':-2",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "27",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(destination),
        ]
    )


def transcode_audio(
    source: Path, destination: Path, duration: int = 5, force: bool = False
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if (
        not force
        and destination.is_file()
        and destination.stat().st_mtime >= source.stat().st_mtime
    ):
        return
    run(
        [
            str(FFMPEG),
            "-loglevel",
            "error",
            "-y",
            "-nostdin",
            "-i",
            str(source),
            "-t",
            str(duration),
            "-vn",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "96k",
            str(destination),
        ]
    )


def prepare_long_reference() -> None:
    manifest = json.loads((PROJECT / "paper/long_video/long_video_manifest.json").read_text())
    row = next(item for item in manifest["rows"] if item["pair_id"] == "long_14")
    output_root = PAGE / "assets/paper/long"
    output_root.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt") as handle:
        for clip in row["source_clips"]:
            handle.write(f"file '{clip['path']}'\n")
        handle.flush()
        run(
            [
                str(FFMPEG),
                "-loglevel",
                "error",
                "-y",
                "-nostdin",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                handle.name,
                "-t",
                "60",
                "-an",
                "-vf",
                "scale='min(480,iw)':-2",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "27",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(output_root / "source_pair14.mp4"),
            ]
        )
    transcode_audio(
        output_root / "source_reanchored_pair14.mp4",
        output_root / "replacement_audio_pair14_60s.mp3",
        duration=60,
        force=True,
    )


def prepare_job(job: tuple[str, Path, Path, float | None]) -> None:
    kind, source, destination, duration = job
    if kind == "video":
        transcode_video(source, destination)
    else:
        transcode_audio(source, destination, duration=duration or 5, force=True)


def main() -> None:
    comparisons = []
    jobs: list[tuple[str, Path, Path, float | None]] = []
    for benchmark, config in BENCHMARKS.items():
        directory = config["directory"]
        wav2lip = config["wav2lip"]
        for rank, (sync_c, item) in enumerate(common_candidates(directory, wav2lip), 1):
            key = item["key"]
            stem = f"{directory}_{rank:02d}"
            relative_root = Path("assets/paper/benchmark_showcase") / stem
            output_root = PAGE / relative_root
            sources = {
                "Reference video": Path(item["video"]),
                "Wav2Lip": BENCH / "out" / directory / wav2lip / f"{key}__cross.mp4",
                "LatentSync": BENCH / "out" / directory / "latentsync" / f"{key}__cross.mp4",
                "LipForcing-14B": BENCH / "out" / directory / "lipforcing_14b_fix" / f"{key}__cross.mp4",
                "CausalDub": BENCH / "out" / directory / OURS / f"{key}__cross.mp4",
            }
            items = []
            for label, source in sources.items():
                filename = (
                    "source.mp4"
                    if label == "Reference video"
                    else label.lower().replace("-", "").replace(" ", "_") + ".mp4"
                )
                destination = output_root / filename
                jobs.append(("video", source, destination, None))
                items.append({"label": label, "video": str(relative_root / filename)})
            audio_destination = output_root / "replacement_audio_v2.mp3"
            shared_duration = min(5.0, *(probe_duration(path) for path in sources.values()))
            jobs.append(
                ("audio", Path(item["audio_cross"]), audio_destination, shared_duration)
            )
            comparisons.append(
                {
                    "benchmark": benchmark,
                    "regime": config["regime"],
                    "title": f"{benchmark} · {key}",
                    "aspect": config["aspect"],
                    "audio": str(relative_root / audio_destination.name),
                    "description": (
                        f"Rank {rank} by CausalDub cross-audio Sync-C ({sync_c:.2f}) "
                        "among samples with complete outputs from all displayed methods."
                    ),
                    "selection_rank": rank,
                    "key": key,
                    "ours_cross_sync_c": round(sync_c, 4),
                    "items": items,
                }
            )

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(prepare_job, job) for job in jobs]
        for future in futures:
            future.result()

    MANIFEST.write_text(
        json.dumps(
            {
                "schema": 1,
                "selection": (
                    "For each benchmark, top six final-model cross-audio Sync-C values "
                    "among samples with complete Wav2Lip, LatentSync, LipForcing-14B, "
                    "and CausalDub outputs; ties broken by key."
                ),
                "comparisons": comparisons,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
    prepare_long_reference()
    print(f"Wrote {MANIFEST} with {len(comparisons)} matched examples and {len(jobs)} media files")


if __name__ == "__main__":
    main()
