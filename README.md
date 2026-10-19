# CausalDub Project Page

Static results page for **CausalDub: Guided Response Distillation for Causal Video Dubbing**.

## View locally

```bash
python -m http.server 8000
```

Open [http://localhost:8000/](http://localhost:8000/).

## Contents

- `index.html` — project page (abstract, method, results, 20-case video showcase)
- `media/` — teaser, comparison, framework, Pareto figures
- `assets/case_XX/` — source / same / cross videos + audio
- `thumbnails/` — preview frames
- `selection_manifest.json` — frozen showcase selection + metrics
- `build.py` — regenerate `index.html` from the manifest

## GitHub Pages

This repo is intended to be served from the root of the `main` branch (GitHub Pages → Deploy from branch → `/`).
