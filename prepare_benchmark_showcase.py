#!/usr/bin/env python3
"""Build the reproducible 4-benchmark × 6-example comparison showcase."""
from __future__ import annotations

import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cv2
import numpy as np


PAGE = Path(__file__).resolve().parent
PROJECT = PAGE.parent
BENCH = PROJECT / "bench"
ASSET_DIRNAME = "benchmark_showcase_v4"
ASSETS = PAGE / "assets/paper" / ASSET_DIRNAME
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

FROZEN_TOP6 = {
    "hdtf": [
        ("Radio52", 1.091),
        ("KevinMcCarthy0", 0.845),
        ("DebFischer1", 0.695),
        ("RobPortman", 0.597),
        ("OlympiaSnowe", 0.441),
        ("DianeBlack0", 0.365),
    ],
    "vox2": [
        ("id03347_FKY5V8wmX5k_00046", 0.821),
        ("id00817_cBrdF4D2zJc_00314", 0.599),
        ("id01509_V6ZrSPkix8Y_00184", 0.503),
        ("id08701_z8t-KFSoYLI_00469", 0.486),
        ("id02057_m5IXuletN8Y_00352", 0.471),
        ("id07494_1A8ZDo11tzY_00010", 0.468),
    ],
    "talkvid": [
        ("videovideo8351_PvPwzmobAJw-scene11-scene5", 1.409),
        ("videovideokUUhJtbrIwU-scene57-scene7", 1.395),
        ("videovideof6sSM6vhWTE-scene21-scene17", 1.264),
        ("videovideoB8WTvLo3dsU-scene17-scene4", 1.243),
        ("videovideoSqqPLqjEA0I-scene70-scene2", 1.107),
        ("videovideo6-198fR9Sxo-scene61-scene2", 1.102),
    ],
    "causaldub": [
        ("qwen35_talking_020329_000", 1.647),
        ("qwen35_talking_080085_000", 1.393),
        ("qwen35_talking_076239_000", 1.293),
        ("qwen35_talking_027616_000", 1.251),
        ("qwen35_talking_040818_000", 1.121),
        ("qwen35_talking_008288_000", 1.094),
    ],
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def middle_frame_sharpness(path: Path) -> float:
    capture = cv2.VideoCapture(str(path))
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.set(cv2.CAP_PROP_POS_FRAMES, max(0, frames // 2))
    ok, image = capture.read()
    capture.release()
    if not ok:
        raise RuntimeError(f"cannot decode source frame: {path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def zscore(values: list[float]) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    return (array - array.mean()) / (array.std() + 1e-8)


def common_candidates(directory: str, wav2lip: str) -> list[tuple[float, dict]]:
    items = read_jsonl(BENCH / "data" / directory / "items.jsonl")
    methods = (wav2lip, "latentsync", "lipforcing_14b_fix", OURS)
    rows = []
    for item in items:
        key = item["key"]
        outputs = [
            BENCH / "out" / directory / method / f"{key}__cross.mp4"
            for method in methods
        ]
        metric_paths = [
            BENCH / "metrics" / directory / method / f"{key}__{setting}.json"
            for method in methods
            for setting in ("same", "cross")
        ]
        if not all(path.is_file() for path in outputs + metric_paths):
            continue
        all_metrics = [json.loads(path.read_text()) for path in metric_paths]
        if any(metric.get("sync_fail") for metric in all_metrics):
            continue
        same = json.loads(
            (BENCH / "metrics" / directory / OURS / f"{key}__same.json").read_text()
        )
        cross = json.loads(
            (BENCH / "metrics" / directory / OURS / f"{key}__cross.json").read_text()
        )
        required_same = ("lse_c", "lse_d", "ssim", "psnr", "lmd")
        if not all(isinstance(same.get(field), (int, float)) for field in required_same):
            continue
        if not all(isinstance(cross.get(field), (int, float)) for field in ("lse_c", "lse_d")):
            continue
        try:
            sharpness = middle_frame_sharpness(Path(item["video"]))
        except RuntimeError:
            continue
        rows.append(
            {
                "item": item,
                "same": same,
                "cross": cross,
                "sharpness": sharpness,
            }
        )
    if len(rows) < 6:
        raise RuntimeError(f"{directory}: only {len(rows)} complete common candidates")
    fields = {
        "cross_c": [row["cross"]["lse_c"] for row in rows],
        "cross_d": [row["cross"]["lse_d"] for row in rows],
        "same_c": [row["same"]["lse_c"] for row in rows],
        "ssim": [row["same"]["ssim"] for row in rows],
        "psnr": [row["same"]["psnr"] for row in rows],
        "lmd": [row["same"]["lmd"] for row in rows],
        "sharpness": [row["sharpness"] for row in rows],
    }
    normalized = {name: zscore(values) for name, values in fields.items()}
    for index, row in enumerate(rows):
        row["quality_score"] = float(
            0.32 * normalized["cross_c"][index]
            - 0.18 * normalized["cross_d"][index]
            + 0.12 * normalized["same_c"][index]
            + 0.17 * normalized["ssim"][index]
            + 0.08 * normalized["psnr"][index]
            - 0.05 * normalized["lmd"][index]
            + 0.08 * normalized["sharpness"][index]
            - 0.04 * abs(row["cross"].get("offset", 0))
        )
    rows.sort(key=lambda row: (-row["quality_score"], row["item"]["key"]))
    return [(row["quality_score"], row["item"]) for row in rows[:6]]


def frozen_candidates(directory: str, wav2lip: str) -> list[tuple[float, dict]]:
    items = {
        item["key"]: item
        for item in read_jsonl(BENCH / "data" / directory / "items.jsonl")
    }
    methods = (wav2lip, "latentsync", "lipforcing_14b_fix", OURS)
    selected = []
    for key, quality_score in FROZEN_TOP6[directory]:
        required = [
            BENCH / "out" / directory / method / f"{key}__cross.mp4"
            for method in methods
        ] + [
            BENCH / "metrics" / directory / method / f"{key}__{setting}.json"
            for method in methods
            for setting in ("same", "cross")
        ]
        if key not in items or not all(path.is_file() for path in required):
            raise RuntimeError(f"{directory}/{key}: frozen selection is incomplete")
        if any(json.loads(path.read_text()).get("sync_fail") for path in required[4:]):
            raise RuntimeError(f"{directory}/{key}: frozen selection has a metric failure")
        selected.append((quality_score, items[key]))
    return selected


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
            "-map",
            "0:v:0",
            "-map",
            "0:a:0?",
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
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-ac",
            "1",
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
        for rank, (quality_score, item) in enumerate(
            frozen_candidates(directory, wav2lip), 1
        ):
            key = item["key"]
            stem = f"{directory}_{rank:02d}"
            relative_root = Path("assets/paper") / ASSET_DIRNAME / stem
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
            aligned_audio = relative_root / "causaldub.mp4"
            comparisons.append(
                {
                    "benchmark": benchmark,
                    "regime": config["regime"],
                    "title": f"{benchmark} · {key}",
                    "aspect": config["aspect"],
                    "audio": str(aligned_audio),
                    "description": (
                        f"Rank {rank} by the frozen CausalDub quality score "
                        f"({quality_score:.2f}) among the four-method scoreable intersection."
                    ),
                    "selection_rank": rank,
                    "key": key,
                    "quality_score": round(quality_score, 6),
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
                    "For each benchmark, restrict to the four-method same/cross scoreable "
                    "intersection, then select the top six by the frozen CausalDub quality "
                    "score from paper/select_showcase.py; ties are broken by key."
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
