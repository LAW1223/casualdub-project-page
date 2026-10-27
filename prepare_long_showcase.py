#!/usr/bin/env python3
"""Prepare five additional Long-20 source/output pairs for the project page."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


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
SIZE = 512
CROP_SCALE = 1.8
LM_NOSE_BOTTOM = 2
LM_CHEEK_R = 234
LM_CHEEK_L = 454
LM_CHIN = 152
LM_FOREHEAD = 10


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


def sampled_landmarks(source: Path) -> tuple[np.ndarray, int, int]:
    capture = cv2.VideoCapture(str(source))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    landmarks = []
    with mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as detector:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            result = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if result.multi_face_landmarks:
                faces = [
                    np.array(
                        [
                            (point.x * width, point.y * height)
                            for point in face.landmark[:468]
                        ],
                        dtype=np.float32,
                    )
                    for face in result.multi_face_landmarks
                ]
                landmarks.append(max(faces, key=lambda points: np.ptp(points[:, 1])))
    capture.release()
    if not landmarks:
        raise RuntimeError(f"No face landmarks found in {source}")
    return np.stack(landmarks), height, width


def paste_geometry(source: Path) -> tuple[int, tuple[int, int, int], np.ndarray]:
    landmarks, height, width = sampled_landmarks(source)
    face = np.nanmedian(
        np.maximum(
            np.ptp(landmarks[:, :, 0], axis=1),
            np.ptp(landmarks[:, :, 1], axis=1),
        )
    )
    pad = max(0, int(np.ceil((face * CROP_SCALE - min(height, width)) / 2)) + 1)
    points = landmarks + pad
    padded_height, padded_width = height + 2 * pad, width + 2 * pad
    center_x = (np.nanmin(points[:, :, 0]) + np.nanmax(points[:, :, 0])) / 2
    center_y = (np.nanmin(points[:, :, 1]) + np.nanmax(points[:, :, 1])) / 2
    side = int(min(face * CROP_SCALE, padded_height, padded_width))
    x0 = int(np.clip(center_x - side / 2, 0, padded_width - side))
    y0 = int(np.clip(center_y - side / 2, 0, padded_height - side))
    scale = SIZE / side
    face_height = np.nanmedian(
        points[:, LM_CHIN, 1] - points[:, LM_FOREHEAD, 1]
    )
    top = np.nanmin(points[:, LM_NOSE_BOTTOM, 1])
    bottom = np.nanmax(points[:, LM_CHIN, 1]) + 0.1 * face_height
    left = np.nanmin(points[:, LM_CHEEK_R, 0])
    right = np.nanmax(points[:, LM_CHEEK_L, 0])
    (mask_left, mask_top), (mask_right, mask_bottom) = (
        (
            np.array([[left, top], [right, bottom]]) - np.array([x0, y0])
        )
        * scale
    ).round().astype(int)
    mask = np.zeros((SIZE, SIZE), dtype=np.uint8)
    mask[
        max(mask_top, 0) : min(mask_bottom, SIZE),
        max(mask_left, 0) : min(mask_right, SIZE),
    ] = 255
    alpha = cv2.GaussianBlur(mask, (0, 0), 15).astype(np.float32) / 255.0
    return pad, (x0, y0, side), alpha


def paste_back_output(
    source: Path, generated: Path, replacement_audio: Path, destination: Path
) -> tuple[int, int, tuple[int, int, int]]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    pad, (x0, y0, side), alpha_512 = paste_geometry(source)
    source_capture = cv2.VideoCapture(str(source))
    generated_capture = cv2.VideoCapture(str(generated))
    width = int(source_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(source_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    alpha = cv2.resize(alpha_512, (side, side), interpolation=cv2.INTER_LINEAR)[
        :, :, None
    ]
    command = [
        str(FFMPEG), "-loglevel", "error", "-y", "-nostdin",
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s", f"{width}x{height}",
        "-r", "25",
        "-i", "-",
        "-i", str(replacement_audio),
        "-t", "60",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "29",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "96k",
        "-ac", "1",
        "-ar", "16000",
        "-shortest",
        "-movflags", "+faststart",
        str(destination),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    frames = 0
    while frames < 1500:
        source_ok, source_frame = source_capture.read()
        generated_ok, generated_frame = generated_capture.read()
        if not source_ok or not generated_ok:
            break
        padded = (
            cv2.copyMakeBorder(
                source_frame, pad, pad, pad, pad, cv2.BORDER_REPLICATE
            )
            if pad
            else source_frame.copy()
        )
        generated_region = cv2.resize(
            generated_frame, (side, side), interpolation=cv2.INTER_CUBIC
        )
        source_region = padded[y0 : y0 + side, x0 : x0 + side]
        blended = np.rint(
            source_region.astype(np.float32) * (1.0 - alpha)
            + generated_region.astype(np.float32) * alpha
        ).clip(0, 255).astype(np.uint8)
        padded[y0 : y0 + side, x0 : x0 + side] = blended
        restored = padded[pad : pad + height, pad : pad + width] if pad else padded
        process.stdin.write(np.ascontiguousarray(restored).tobytes())
        frames += 1
    source_capture.release()
    generated_capture.release()
    process.stdin.close()
    if process.wait() != 0 or frames != 1500:
        raise RuntimeError(f"Paste-back failed for {source}: {frames} frames")
    return width, height, (x0 - pad, y0 - pad, side)


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
        width, height, box = paste_back_output(
            source, output, audio, ASSETS / f"{name}_causaldub.mp4"
        )
        transcode_audio(audio, ASSETS / f"{name}_replacement.mp3")
        if (width, height) != size:
            raise RuntimeError(f"Unexpected source size for {name}")
        print(name, f"{width}x{height}", f"box={box}")


if __name__ == "__main__":
    main()
