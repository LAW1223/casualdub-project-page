# CausalDub Project Page

Static results page for **CausalDub: Replacement-Aware Video Dubbing for Diverse Sources**.

## View locally

```bash
python -m http.server 8000
```

Open [http://localhost:8000/](http://localhost:8000/).

## Contents

- `index.html` — project page (paper-matched abstract, method, results, and video evidence)
- `media/` — teaser, comparison, framework, Pareto figures
- `assets/case_XX/` — source / same / cross videos + audio
- `assets/paper/benchmark_showcase/` — four benchmarks × six matched multi-method examples
- `benchmark_showcase_manifest.json` — reproducible top-six common-output selections
- `thumbnails/` — preview frames
- `selection_manifest.json` — frozen showcase selection + metrics
- `prepare_benchmark_showcase.py` — regenerate compact comparison media and Long-20 inputs
- `prepare_gallery_pasteback.py` — paste 16 CausalDub-Bench cases into native frames
- `build.py` — regenerate `index.html` from the manifest

## GitHub Pages

This repo is intended to be served from the root of the `main` branch (GitHub Pages → Deploy from branch → `/`).
