#!/usr/bin/env python3
"""Paste 16 of 20 CausalDub-Bench gallery cases into their native frames."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np


PAGE = Path(__file__).resolve().parent
WORKSPACE = PAGE.parents[1]
WAN_DUB = WORKSPACE / "project/wan_dub"
BENCH = WAN_DUB / "bench"
MANIFEST = PAGE / "selection_manifest.json"
FFMPEG = BENCH / "bin" / "ffmpeg"
KEEP_CROPPED = {"case_05", "case_10", "case_15", "case_20"}
FRAMES = 81
FPS = 24


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mux_frames(
    frames: list[np.ndarray], audio: Path, destination: Path
) -> tuple[int, int]:
    height, width = frames[0].shape[:2]
    command = [
        str(FFMPEG),
        "-loglevel",
        "error",
        "-y",
        "-nostdin",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-s",
        f"{width}x{height}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-i",
        str(audio),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "24",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "96k",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-shortest",
        "-movflags",
        "+faststart",
        str(destination),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    for frame in frames:
        process.stdin.write(np.ascontiguousarray(frame).tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {destination}")
    return width, height


def add_audio(video: Path, audio: Path) -> None:
    temporary = video.with_name(f"{video.stem}.with_audio.mp4")
    subprocess.run(
        [
            str(FFMPEG),
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-shortest",
            "-movflags",
            "+faststart",
            str(temporary),
        ],
        check=True,
    )
    temporary.replace(video)


def read_native_frames(video: Path, start: int) -> list[np.ndarray]:
    capture = cv2.VideoCapture(str(video))
    capture.set(cv2.CAP_PROP_POS_FRAMES, start)
    frames = []
    for _ in range(FRAMES):
        ok, frame = capture.read()
        if not ok:
            break
        frames.append(frame)
    capture.release()
    if len(frames) != FRAMES:
        raise RuntimeError(f"Expected {FRAMES} frames from {video}, got {len(frames)}")
    return frames


def paste_frames(
    native: list[np.ndarray],
    generated: Path,
    crop_box: list[int],
    mask_path: Path,
) -> list[np.ndarray]:
    x0, y0, side = crop_box
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise FileNotFoundError(mask_path)
    alpha = cv2.GaussianBlur(mask, (0, 0), 12)
    alpha = cv2.resize(alpha, (side, side), interpolation=cv2.INTER_LINEAR)
    alpha = alpha.astype(np.float32)[:, :, None] / 255.0

    capture = cv2.VideoCapture(str(generated))
    pasted = []
    for frame in native:
        ok, crop = capture.read()
        if not ok:
            break
        crop = cv2.resize(crop, (side, side), interpolation=cv2.INTER_CUBIC)
        region = frame[y0 : y0 + side, x0 : x0 + side]
        blended = np.rint(
            region.astype(np.float32) * (1.0 - alpha)
            + crop.astype(np.float32) * alpha
        ).clip(0, 255).astype(np.uint8)
        output = frame.copy()
        output[y0 : y0 + side, x0 : x0 + side] = blended
        pasted.append(output)
    capture.release()
    if len(pasted) != FRAMES:
        raise RuntimeError(f"Expected {FRAMES} generated frames from {generated}")
    return pasted


def main() -> None:
    data = json.loads(MANIFEST.read_text())
    s00 = {
        row["id"]: row
        for row in read_jsonl(WAN_DUB / "data/manifest/s00_manifest.jsonl")
    }
    selected_keys = {case["key"] for case in data["cases"]}
    s02 = {}
    for path in sorted((WAN_DUB / "data/manifest/s02").glob("shard_*.jsonl")):
        for row in read_jsonl(path):
            if row.get("clip_id") in selected_keys:
                s02[row["clip_id"]] = row
    bench_items = {
        row["key"]: row
        for row in read_jsonl(BENCH / "data/causaldub/items.jsonl")
    }

    for case in data["cases"]:
        key = case["key"]
        item = bench_items[key]
        destination = PAGE / f"assets/{case['case']}"
        if case["case"] in KEEP_CROPPED:
            case["presentation"] = "crop"
            case.pop("native_resolution", None)
            add_audio(destination / "source.mp4", Path(item["audio_same"]))
            case["source_sha256"] = sha256(destination / "source.mp4")
            continue
        clip = s02[key]
        source_row = s00[clip["id"]]
        native = read_native_frames(Path(source_row["video_path"]), clip["start"])
        clip_dir = WAN_DUB / "data/clips" / clip["dir"]

        width, height = mux_frames(
            native, Path(item["audio_same"]), destination / "source.mp4"
        )
        for setting, audio_key in (("same", "audio_same"), ("cross", "audio_cross")):
            generated = BENCH / f"out/causaldub/r2a_dmd2/{key}__{setting}.mp4"
            pasted = paste_frames(
                native, generated, clip["crop_box"], clip_dir / "mask.png"
            )
            mux_frames(pasted, Path(item[audio_key]), destination / f"{setting}.mp4")

        middle = native[len(native) // 2]
        cv2.imwrite(
            str(PAGE / case["thumbnail"]),
            middle,
            [cv2.IMWRITE_JPEG_QUALITY, 90],
        )
        case["presentation"] = "native"
        case["native_resolution"] = [width, height]
        case["source_sha256"] = sha256(destination / "source.mp4")
        case["same_sha256"] = sha256(destination / "same.mp4")
        case["cross_sha256"] = sha256(destination / "cross.mp4")
        print(case["case"], key, f"{width}x{height}")

    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
