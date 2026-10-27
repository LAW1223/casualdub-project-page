#!/usr/bin/env python3
"""Build the CausalDub project page (static GitHub Pages site)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "selection_manifest.json").read_text())
EXTRA = json.loads((ROOT / "project_page_manifest.json").read_text())
SHOWCASE = json.loads((ROOT / "benchmark_showcase_manifest.json").read_text())
EXTRA["comparisons"] = SHOWCASE["comparisons"]

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CausalDub — Replacement-Aware Video Dubbing for Diverse Sources</title>
<meta name="description" content="CausalDub is a replacement-aware causal video-dubbing editor evaluated on captured, web, generated, and long-form sources.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,550;9..144,700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#132028;
  --muted:#5d6b73;
  --line:#d5dde1;
  --soft:#f3f6f5;
  --paper:#fbfcfc;
  --accent:#0f766e;
  --accent-2:#c45c26;
  --sky:#e7f1ef;
  --shadow:0 18px 50px rgba(19,32,40,.08);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;color:var(--ink);background:
    radial-gradient(1200px 500px at 10% -10%, #dcece8 0%, transparent 55%),
    radial-gradient(900px 420px at 90% 0%, #f3e7dc 0%, transparent 50%),
    var(--paper);
  font-family:Manrope,ui-sans-serif,system-ui,sans-serif;line-height:1.55;
}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px}
nav{
  position:sticky;top:0;z-index:40;backdrop-filter:blur(14px);
  background:rgba(251,252,252,.86);border-bottom:1px solid rgba(213,221,225,.85);
}
.nav-inner{display:flex;align-items:center;gap:18px;min-height:58px}
.brand{font-weight:800;letter-spacing:-.04em;font-size:18px;color:var(--ink);text-decoration:none}
.nav-links{display:flex;gap:16px;margin-left:auto;flex-wrap:wrap;font-size:14px;font-weight:600}
.nav-links a{color:var(--muted);text-decoration:none}
.nav-links a:hover{color:var(--ink)}
.menu-button{display:none;margin-left:auto;border-color:var(--line);background:#fff}

.hero{padding:56px 0 18px}
.eyebrow{
  display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:18px;
}
.hero-brand{
  font-family:Fraunces,Georgia,serif;font-size:clamp(52px,9vw,96px);line-height:.92;
  letter-spacing:-.045em;margin:0 0 16px;font-weight:700;
}
.hero h2{
  font-family:Fraunces,Georgia,serif;font-weight:550;font-size:clamp(22px,3.2vw,34px);
  line-height:1.2;letter-spacing:-.03em;max-width:18ch;margin:0 0 16px;
}
.lead{max-width:62ch;color:var(--muted);font-size:17px;margin:0 0 24px}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:34px}
.btn{
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  border-radius:999px;padding:11px 18px;font-weight:700;font-size:14px;
  border:1px solid var(--ink);text-decoration:none;transition:transform .15s ease, background .15s ease;
}
.btn:hover{transform:translateY(-1px);text-decoration:none}
.btn-primary{background:var(--ink);color:#fff}
.btn-ghost{background:transparent;color:var(--ink)}
.hero-visual{
  border-radius:18px;overflow:hidden;box-shadow:var(--shadow);
  border:1px solid rgba(19,32,40,.06);background:#111;
  animation:rise .7s ease both;
}
.hero-visual img{display:block;width:100%;height:auto}
.caption{font-size:13px;color:var(--muted);margin-top:10px}

.stats{
  display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;
  margin:36px 0 8px;
}
.stat{
  background:rgba(255,255,255,.72);border:1px solid var(--line);border-radius:16px;
  padding:16px 16px 14px;animation:rise .6s ease both;
}
.stat:nth-child(2){animation-delay:.05s}
.stat:nth-child(3){animation-delay:.1s}
.stat:nth-child(4){animation-delay:.15s}
.stat b{display:block;font-family:Fraunces,Georgia,serif;font-size:28px;letter-spacing:-.03em;line-height:1.1}
.stat span{display:block;color:var(--muted);font-size:12px;font-weight:600;margin-top:4px}

section{padding:54px 0 8px}
section h3{
  font-family:Fraunces,Georgia,serif;font-size:clamp(28px,4vw,40px);
  letter-spacing:-.035em;margin:0 0 12px;font-weight:700;
}
.section-lead{color:var(--muted);max-width:70ch;margin:0 0 22px}
.panel{
  background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;
  box-shadow:0 10px 30px rgba(19,32,40,.04);
}
.two{display:grid;grid-template-columns:1.1fr .9fr;gap:22px;align-items:start}
.panel img{width:100%;height:auto;border-radius:12px;display:block}
.bullets{margin:0;padding-left:18px}
.bullets li{margin:0 0 10px;color:var(--ink)}
.bullets li::marker{color:var(--accent)}

.table-wrap{overflow:auto;border-radius:14px;border:1px solid var(--line);box-shadow:inset -18px 0 18px -24px rgba(19,32,40,.65)}
table{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff;min-width:980px}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left}
th{background:var(--soft);font-size:12px;letter-spacing:.02em}
tr.ours td{background:#eef7f5;font-weight:700}
.note{font-size:12.5px;color:var(--muted);margin-top:10px}

.toolbar{
  position:sticky;top:58px;z-index:30;background:rgba(251,252,252,.94);
  backdrop-filter:blur(12px);border:1px solid var(--line);border-radius:999px;
  padding:8px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0 18px;
}
button{
  border:1px solid transparent;background:transparent;color:var(--ink);
  border-radius:999px;padding:8px 14px;font-weight:700;font-size:13px;cursor:pointer;
  font-family:inherit;
}
button.active,button.sync{background:var(--ink);color:#fff}
button.sync{margin-left:auto;background:var(--accent);border-color:var(--accent)}
button.ghost{border-color:var(--line);background:#fff}

.case{border-top:1px solid var(--line);padding:28px 0 36px}
.case-head{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:start;margin-bottom:14px}
.number{font-family:Fraunces,Georgia,serif;font-size:36px;font-weight:700;color:#b7c2c7;letter-spacing:-.04em}
.title{font-size:18px;font-weight:800;margin-bottom:4px}
.prompt{color:var(--muted);font-size:13.5px;line-height:1.45;max-width:80ch;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.metrics{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}
.metric{background:var(--soft);border-radius:10px;padding:7px 9px;font-size:11px;color:var(--muted)}
.metric b{display:block;font-size:15px;color:var(--accent);font-weight:800}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.cell{min-width:0}
.label{display:flex;justify-content:space-between;align-items:center;font-size:12.5px;font-weight:800;margin:0 2px 6px}
.label small{font-weight:500;color:var(--muted)}
video{width:100%;display:block;background:#111;aspect-ratio:1/1;object-fit:contain;border-radius:10px}
.grid.native video{aspect-ratio:7/4}
.cross video{outline:2px solid var(--accent);outline-offset:-2px}
.hint{font-size:12px;color:var(--muted);margin:0 0 14px}
.domain-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.domain-card,.evidence-card,.long-card{
  overflow:hidden;background:#fff;border:1px solid var(--line);border-radius:18px;
  box-shadow:0 10px 30px rgba(19,32,40,.04)
}
.card-copy{padding:20px 22px 16px}
.card-copy h4,.evidence-copy h4{font-family:Fraunces,Georgia,serif;font-size:24px;line-height:1.1;letter-spacing:-.025em;margin:0 0 7px}
.card-copy p,.evidence-copy p{margin:0;color:var(--muted);font-size:13.5px}
.tag{display:inline-block;color:var(--accent);font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px}
.media-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px;background:var(--line)}
.media-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.media-grid.four{grid-template-columns:repeat(4,minmax(0,1fr))}
.media-grid figure{min-width:0;margin:0;background:#fff}
.media-grid figcaption{padding:8px 11px 10px;color:var(--muted);font-size:11.5px;font-weight:700}
.media-grid.wide video{aspect-ratio:16/9}
.benchmark-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}
.benchmark-tabs button{border-color:var(--line);background:#fff}
.benchmark-tabs button.active{background:var(--ink);color:#fff;border-color:var(--ink)}
.comparison-list{display:grid;gap:18px}
.comparison-card{overflow:hidden;background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:0 10px 30px rgba(19,32,40,.04)}
.compare-controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:0 22px 18px}
.compare-controls audio{height:34px;max-width:280px}
.compare-body{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:2px;background:var(--line)}
.compare-body figure{margin:0;background:#fff;min-width:0}
.compare-body video{border-radius:0}
.compare-body.square video{aspect-ratio:1/1}
.compare-body.wide video{aspect-ratio:16/9}
.compare-body figcaption{padding:9px 11px 11px;color:var(--muted);font-size:11.5px;font-weight:800}
.compare-body figure:first-child{box-shadow:inset 0 3px 0 var(--accent-2)}
.sample-index{color:var(--muted);font-variant-numeric:tabular-nums}
.group-play{background:var(--ink);color:#fff}
.evidence-list{display:grid;gap:18px}
.evidence-card{display:block}
.evidence-copy{padding:28px;display:flex;flex-direction:column;justify-content:center}
.evidence-copy h4{font-size:28px;margin-bottom:12px}
.long-reference{display:grid;grid-template-columns:minmax(260px,.8fr) 1.2fr;gap:18px;margin-bottom:18px;align-items:center}
.long-reference figure{margin:0}
.long-input{padding:22px}
.long-input audio{width:100%;margin-top:10px}
.long-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.long-card figure{margin:0}
.long-card video{aspect-ratio:1/1;border-radius:0}
.long-card figcaption{padding:8px 12px 12px;color:var(--muted);font-size:11.5px;font-weight:700}
.long-card.failure{border-color:#e5c1a6}
.long-card.success{border-color:#9dccbd}
.long-controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 16px}
.long-controls audio{height:34px;max-width:320px}
.long-more-title{font-family:Fraunces,Georgia,serif;font-size:25px;margin:32px 0 7px}
.long-more-lead{color:var(--muted);font-size:13px;margin:0 0 16px}
.long-examples{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.long-example{padding:0;overflow:hidden}
.long-example-head{padding:18px 20px 12px}
.long-example-head h4{font-family:Fraunces,Georgia,serif;font-size:22px;margin:0 0 10px}
.long-example .compare-controls{padding:0}
.long-example .compare-controls audio{max-width:240px}
.long-example .media-grid video{aspect-ratio:1/1;border-radius:0}
.load-row{display:flex;justify-content:center;padding:18px 0 0}
.load-more{background:var(--ink);color:#fff;padding:11px 20px}
.limits{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;list-style:none;padding:0;margin:0}
.limits li{padding:18px;border-radius:12px;background:var(--soft);color:var(--muted);font-size:13px}

.bib{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px;
  white-space:pre-wrap;background:var(--soft);border-radius:12px;padding:16px;overflow:auto;
  border:1px solid var(--line);
}
footer{padding:40px 0 70px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);margin-top:40px}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@media(max-width:900px){
  .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
  .two{grid-template-columns:1fr}
  .domain-grid,.long-grid,.long-examples,.evidence-card{grid-template-columns:1fr}
  .media-grid.four,.compare-body,.long-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .long-reference{grid-template-columns:1fr}
  .limits{grid-template-columns:1fr}
  .case-head{grid-template-columns:auto 1fr}
  .metrics{grid-column:1/-1;justify-content:flex-start}
  .grid{grid-template-columns:1fr}
  button.sync{margin-left:0}
  .menu-button{display:inline-flex}
  .nav-links{display:none;position:absolute;top:58px;left:16px;right:16px;padding:14px;background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}
  .nav-links.open{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:560px){
  .wrap{padding:0 16px}
  .hero{padding-top:38px}
  .stats{grid-template-columns:1fr 1fr}
  .compare-body,.long-grid{grid-template-columns:1fr}
  .toolbar{position:static;border-radius:16px}
  table{font-size:12px}
}
</style>
</head>
<body>
<nav><div class="wrap nav-inner">
  <a class="brand" href="#">CausalDub</a>
  <button class="menu-button" id="menu" aria-expanded="false" aria-controls="nav-links">Sections</button>
  <div class="nav-links" id="nav-links">
    <a href="#abstract">Abstract</a>
    <a href="#method">Method</a>
    <a href="#results">Results</a>
    <a href="#comparisons">Baselines</a>
    <a href="#evidence">Ablations</a>
    <a href="#long">Long-20</a>
    <a href="#videos">Gallery</a>
    <a href="#cite">Cite</a>
  </div>
</div></nav>

<header class="hero"><div class="wrap">
  <div class="eyebrow">Source-video lip editing</div>
  <h1 class="hero-brand">CausalDub</h1>
  <h2>Replacement-aware video dubbing for diverse sources.</h2>
  <p class="lead">
    Preserve the recorded person, performance, and scene while transferring
    replacement-speech articulation to a two-evaluation causal editor.
  </p>
  <div class="cta">
    <a class="btn btn-primary" href="#comparisons">Compare methods</a>
    <a class="btn btn-ghost" href="#results">See numbers</a>
    <a class="btn btn-ghost" href="#cite">BibTeX</a>
  </div>
  <div class="hero-visual">
    <img src="media/teaser.jpg" alt="Replacement-speech editing comparison under matched source video and driving audio" width="1225" height="536">
  </div>
  <p class="caption">Replacement-speech editing with two-step causal generation. All methods receive the same source video and driving audio; mouth insets compare articulation under matched conditions.</p>

  <div class="stats">
    <div class="stat"><b>2</b><span>NFE per causal block</span></div>
    <div class="stat"><b>6.3</b><span>FPS full pipeline · single H20</span></div>
    <div class="stat"><b>10.001</b><span>HDTF cross Sync-C</span></div>
    <div class="stat"><b>8.681</b><span>CausalDub-Bench Sync-C</span></div>
  </div>
</div></header>

<section id="abstract"><div class="wrap">
  <h3>Abstract</h3>
  <div class="panel">
    <p style="margin:0;color:var(--ink)">
      Video dubbing replaces spoken content while preserving the person, performance,
      and scene of a source video. Existing systems are predominantly trained and
      evaluated on short, same-audio captured clips. This protocol creates three
      deployment mismatches: the recorded mouth is invalid supervision under replacement
      speech, captured clips do not represent web and generated sources, and short
      evaluations do not reveal long-execution instability. We introduce CausalDub,
      which first learns a full-context replacement response and then transfers it to a
      causal two-step editor. Its asymmetric supervision retains full reconstruction for
      same-audio samples but removes source-mouth targets under replacement audio while
      preserving valid non-mouth evidence. Guided causal adaptation and trajectory
      regression transfer the learned response into a two-evaluation autoregressive
      student. Distribution matching recovers compression-induced visual degradation,
      while source-reanchored windows bound generated-state propagation on long inputs.
      We also introduce CausalDub-Bench, comprising 256 source-disjoint generated videos
      with fixed replacement-audio pairs, and evaluate captured, web, generated, and
      60-second sources. Across four benchmarks, matched replacement-aware refinement
      improves cross-audio Sync-C by 0.954–1.653 with mixed FVD, and, among evaluated
      external methods, the final model attains the highest cross-audio Sync-C on every
      benchmark.
    </p>
  </div>
</div></section>

<section id="method"><div class="wrap">
  <h3>Method</h3>
  <p class="section-lead">The method separates source preservation from replacement-speech control, then transfers a guided parent response into a two-step causal student.</p>
  <div class="two">
    <div class="panel">
      <img src="media/architecture.png" alt="CausalDub causal editing architecture">
      <p class="caption">Masked source and reference preserve appearance; frame-local audio controls articulation; block-causal attention reads only committed generated history.</p>
    </div>
    <div class="panel">
      <ul class="bullets">
        <li><b>Causal adaptation</b> — convert the bidirectional editor so each block only sees past video state.</li>
        <li><b>Trajectory distillation</b> — regress a two-step initializer from the guided causal parent.</li>
        <li><b>Guided DMD + retention</b> — match the teacher distribution while anchoring non-mouth appearance.</li>
        <li><b>One-branch inference</b> — replacement speech at 2 NFE without a second classifier-free branch at test time.</li>
      </ul>
    </div>
  </div>
  <div class="panel" style="margin-top:18px">
    <img src="media/training.png" alt="CausalDub guided response distillation training procedure">
    <p class="caption">Counterfactual adaptation, matched trajectory regression, and guided distribution matching with retention. Auxiliary networks are removed at inference.</p>
  </div>
</div></section>

<section id="results"><div class="wrap">
  <h3>Results</h3>
  <p class="section-lead">Complete cross-audio summary across captured, web, and generated sources. Each cell is Sync-C↑ / FVD↓; results use each method’s scoreable subset, with coverage audited separately.</p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Method</th><th>NFE</th>
          <th>HDTF-30</th><th>VoxCeleb2-30</th><th>TalkVid-500</th><th>CDB-256</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Wav2Lip</td><td>1</td><td>8.782 / 129.51</td><td>7.800 / 71.73</td><td>6.750 / 111.19</td><td>6.922 / 98.62</td></tr>
        <tr><td>Diff2Lip</td><td>25</td><td>8.680 / 99.70</td><td>7.533 / 67.15</td><td>6.944 / 73.37</td><td>7.575 / 58.87</td></tr>
        <tr><td>LatentSync 1.6</td><td>20</td><td>8.160 / 28.05</td><td>6.239 / 28.89</td><td>6.860 / 59.27</td><td>7.544 / 46.77</td></tr>
        <tr><td>Lip Forcing</td><td>2</td><td>6.884 / 33.80</td><td>4.871 / 41.03</td><td>5.610 / 12.68</td><td>5.192 / 15.78</td></tr>
        <tr><td>Full-context teacher</td><td>30/30/48</td><td>9.422 / 27.49</td><td>7.382 / 39.11</td><td>7.663 / 8.51</td><td>8.718 / 15.23</td></tr>
        <tr class="ours"><td>CausalDub</td><td>2</td><td>10.001 / 30.89</td><td>8.549 / 53.25</td><td>7.713 / 13.37</td><td>8.681 / 17.35</td></tr>
      </tbody>
    </table>
  </div>
  <p class="note">Swipe horizontally on small screens. CDB is source-disjoint CausalDub-Bench. TalkVid success ranges from 402/500 to 500/500; its all-method common intersection has 308 items. CDB’s common intersection has 245 items. Full success counts, Sync-D, confidence intervals, WER/CER, and preservation metrics are reported in the paper.</p>
  <div class="panel" style="margin-top:18px">
    <img src="media/results.jpg" alt="Cross-audio synchronization versus distribution quality on four benchmarks">
    <p class="caption">Cross-audio synchronization versus distribution quality. CausalDub has the highest Sync-C on all four benchmarks; FVD shows the remaining visual-quality gap.</p>
  </div>
</div></section>

<section id="comparisons"><div class="wrap">
  <h3>Comparison with prior methods</h3>
  <p class="section-lead">Six matched examples from each of four benchmarks. Every row fixes both the reference video and replacement-speech input across methods; these examples complement—not replace—the frozen aggregate metrics above.</p>
  <div class="benchmark-tabs" id="benchmark-tabs"></div>
  <div class="comparison-list" id="comparison-list"></div>
</div></section>

<section id="evidence"><div class="wrap">
  <h3>Matched interventions</h3>
  <p class="section-lead">The page separates the source of replacement control from the role of few-step quality recovery.</p>
  <div class="evidence-list" id="evidence-list"></div>
</div></section>

<section id="long"><div class="wrap">
  <h3 id="long-title">Long-20</h3>
  <p class="section-lead" id="long-description"></p>
  <div class="long-reference panel">
    <div id="long-source"></div>
    <div class="long-input">
      <span class="tag">Shared inputs</span>
      <h4>Reference video + replacement speech</h4>
      <p class="hint">All four outputs below use this same visual reference and target audio.</p>
      <audio id="long-audio" controls preload="metadata"></audio>
      <div class="long-controls" style="margin-top:14px">
        <button class="group-play" data-group="long-grid">Play all from start</button>
        <button class="ghost group-pause" data-group="long-grid">Pause all</button>
      </div>
    </div>
  </div>
  <div class="long-grid" id="long-grid"></div>
  <h4 class="long-more-title">Five additional 60-second cases</h4>
  <p class="long-more-lead">For five of the six cases, the generated lower-face region is pasted back into the native Long-20 frames. References retain original speech; CausalDub outputs contain replacement speech. Pair 14 remains a 512-crop multi-method comparison.</p>
  <div class="long-examples" id="long-examples"></div>
</div></section>

<section id="videos"><div class="wrap">
  <h3>CausalDub-Bench gallery</h3>
  <p class="section-lead">
    Twenty frozen, source-disjoint CausalDub-Bench examples (10 English / 10 Chinese),
    selected by a reproducible sync + reconstruction gate and visual farthest-point sampling—not a hand-picked top-20.
    Each case shows source, same-audio reconstruction, and replacement-speech edit; 16 cases paste the edited region into native 1344×768 frames, while four retain the model's 512 crop.
  </p>
  <p class="hint">Six cases load initially. Clips autoplay muted when visible; unmuting one clip automatically mutes the others.</p>
  <div class="toolbar">
    <button class="filter active" data-lang="all">All</button>
    <button class="filter" data-lang="en">English</button>
    <button class="filter" data-lang="zh">Chinese</button>
    <button class="ghost" id="mute">Mute all</button>
    <button class="sync" id="play">Replay visible</button>
  </div>
  <main id="cases"></main>
  <div class="load-row"><button class="load-more" id="load-more">Load 6 more cases</button></div>
</div></section>

<section id="limits"><div class="wrap">
  <h3>Scope and limitations</h3>
  <ul class="limits" id="limitations"></ul>
</div></section>

<section id="cite"><div class="wrap">
  <h3>Cite</h3>
  <p class="section-lead">Please cite CausalDub as follows (update authors / venue when available):</p>
  <div class="bib" id="bib">@misc{causaldub,
  title        = {CausalDub: Guided Response Distillation for Causal Video Dubbing},
  howpublished = {Project page},
  note         = {https://law1223.github.io/casualdub-project-page/}
}</div>
</div></section>

<footer><div class="wrap">
  CausalDub project page · video results and benchmark numbers from CausalDub-Bench.
  Lip-editing technology can be misused; use only with consent and provenance watermarking.
</div></footer>

<script>
const DATA = __DATA__;
const EXTRA = __EXTRA__;
const root = document.getElementById('cases');
let io = null;
let activeLang = 'all';
let visibleCount = 6;
function esc(x){
  return String(x||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function media(src,label){
  if(!src) return '';
  return `<figure><video controls loop playsinline preload="metadata" aria-label="${esc(label)}" title="${esc(label)}" src="${esc(src)}"></video><figcaption>${esc(label)}</figcaption></figure>`;
}
const benchmarks=[...new Set(EXTRA.comparisons.map(x=>x.benchmark))];
let activeBenchmark=benchmarks[0];
const tabs=document.getElementById('benchmark-tabs');
tabs.innerHTML=benchmarks.map((x,i)=>`<button class="${i===0?'active':''}" data-benchmark="${esc(x)}">${esc(x)} · 6</button>`).join('');
function renderComparisons(){
  document.getElementById('comparison-list').innerHTML=EXTRA.comparisons.filter(x=>x.benchmark===activeBenchmark).map((x,i)=>
    `<article class="comparison-card" data-sync-card><div class="card-copy"><span class="tag">${esc(x.regime)} · <span class="sample-index">sample ${String(i+1).padStart(2,'0')}/06</span></span><h4>${esc(x.title)}</h4><p>${esc(x.description)}</p></div><div class="compare-controls"><button class="group-play">Play synchronized</button><button class="ghost group-pause">Pause</button><span class="hint" style="margin:0">Aligned replacement speech:</span><audio controls preload="metadata" src="${esc(x.audio)}"></audio></div><p class="hint" style="padding:0 22px;margin-top:-8px">Two modes: use synchronized playback for a shared audio clock, or play any video directly with its own audio. Starting one individual player pauses other audio.</p><div class="compare-body ${esc(x.aspect)}">${x.items.map(v=>media(v.video,v.label)).join('')}</div></article>`
  ).join('');
  wireComparisonControls();
  wireExclusiveAudio(document.getElementById('comparison-list'));
}
tabs.querySelectorAll('button').forEach(b=>b.onclick=()=>{
  tabs.querySelectorAll('button').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');activeBenchmark=b.dataset.benchmark;renderComparisons();
});
document.getElementById('evidence-list').innerHTML=EXTRA.ablations.map(x=>
  `<article class="evidence-card"><div class="evidence-copy"><span class="tag">${esc(x.eyebrow)}</span><h4>${esc(x.title)}</h4><p>${esc(x.description)}</p></div></article>`
).join('');
document.getElementById('long-title').textContent=EXTRA.long_form.title;
document.getElementById('long-description').textContent=EXTRA.long_form.description;
document.getElementById('long-audio').src=EXTRA.long_form.audio;
document.getElementById('long-source').innerHTML=media(EXTRA.long_form.source,'Reference video');
document.getElementById('long-grid').innerHTML=EXTRA.long_form.items.map(x=>
  `<article class="long-card ${esc(x.kind)}"><div class="card-copy"><span class="tag">${esc(x.note)}</span><h4>${esc(x.label)}</h4></div>${media(x.video,x.label)}</article>`
).join('');
document.getElementById('long-examples').innerHTML=EXTRA.long_form.additional_cases.map(x=>
  `<article class="long-example panel" data-sync-card>
    <div class="long-example-head">
      <span class="tag">Source-reanchored · 60 seconds</span>
      <h4>${esc(x.label)}</h4>
      <div class="compare-controls">
        <audio controls preload="metadata" src="${esc(x.audio)}"></audio>
        <button class="group-play">Play together</button>
        <button class="ghost group-pause">Pause</button>
      </div>
    </div>
    <div class="media-grid">
      ${media(x.source,'Reference video')}
      ${media(x.output,'CausalDub · replacement speech','replacement')}
    </div>
  </article>`
).join('');
document.getElementById('limitations').innerHTML=EXTRA.limitations.map(x=>`<li>${esc(x)}</li>`).join('');
let suppressExclusiveAudio=false;
function wireExclusiveAudio(scope=document){
  scope.querySelectorAll('video').forEach(v=>{
    if(v.dataset.audioWired) return;
    v.dataset.audioWired='1';
    v.addEventListener('play',()=>{
      if(activeSync||v.muted) return;
      document.querySelectorAll('video').forEach(other=>{if(other!==v) other.pause();});
      document.querySelectorAll('audio').forEach(a=>a.pause());
    });
    v.addEventListener('volumechange',()=>{
      if(suppressExclusiveAudio||v.muted) return;
      document.querySelectorAll('video').forEach(other=>{if(other!==v) other.muted=true;});
      document.querySelectorAll('audio').forEach(a=>a.pause());
    });
  });
  scope.querySelectorAll('audio').forEach(a=>{
    if(a.dataset.audioWired) return;
    a.dataset.audioWired='1';
    a.addEventListener('play',()=>{
      document.querySelectorAll('audio').forEach(other=>{if(other!==a) other.pause();});
      if(!activeSync) document.querySelectorAll('video').forEach(v=>v.pause());
    });
  });
}
let activeSync=null;
function stopActiveSync(reset=false){
  if(!activeSync) return;
  clearInterval(activeSync.timer);
  suppressExclusiveAudio=true;
  activeSync.videos.forEach((v,i)=>{
    v.pause();v.loop=true;v.muted=activeSync.mutedStates[i];
    if(reset)v.currentTime=0;
  });
  requestAnimationFrame(()=>{suppressExclusiveAudio=false;});
  activeSync.audio.pause();
  if(reset) activeSync.audio.currentTime=0;
  activeSync=null;
}
function playTogether(container,audio){
  stopActiveSync(false);
  const videos=[...container.querySelectorAll('video')];
  const mutedStates=videos.map(v=>v.muted);
  videos.forEach(v=>{v.pause();v.loop=false;v.currentTime=0;v.muted=true;});
  audio.currentTime=0;
  const align=()=>videos.forEach(v=>{
    if(Math.abs(v.currentTime-audio.currentTime)>.18) v.currentTime=Math.min(audio.currentTime,v.duration||audio.currentTime);
    if(!audio.paused && v.paused && !v.ended) v.play().catch(()=>{});
  });
  activeSync={videos,audio,mutedStates,timer:setInterval(align,250)};
  audio.onseeking=align;
  audio.onended=()=>stopActiveSync(true);
  audio.onpause=()=>{if(activeSync&&activeSync.audio===audio) videos.forEach(v=>v.pause());};
  videos.forEach(v=>v.play().catch(()=>{}));
  audio.play().catch(()=>stopActiveSync(false));
}
function pauseTogether(container,audio){
  if(activeSync&&activeSync.audio===audio) stopActiveSync(false);
  else{
    container.querySelectorAll('video').forEach(v=>v.pause());
    if(audio) audio.pause();
  }
}
function wireComparisonControls(){
  document.querySelectorAll('[data-sync-card]').forEach(card=>{
    const audio=card.querySelector('audio');
    card.querySelector('.group-play').onclick=()=>playTogether(card,audio);
    card.querySelector('.group-pause').onclick=()=>pauseTogether(card,audio);
  });
}
document.querySelector('#long .group-play').onclick=()=>playTogether(document.getElementById('long-grid'),document.getElementById('long-audio'));
document.querySelector('#long .group-pause').onclick=()=>pauseTogether(document.getElementById('long-grid'),document.getElementById('long-audio'));
function wireAutoplay(){
  if(io) io.disconnect();
  io = new IntersectionObserver((entries)=>{
    entries.forEach(en=>{
      const v = en.target;
      if(en.isIntersecting && en.intersectionRatio >= 0.35){
        v.play().catch(()=>{});
      }else{
        v.pause();
      }
    });
  }, {threshold:[0,0.35,0.7]});
  document.querySelectorAll('#cases video').forEach(v=>io.observe(v));
}
function render(reset=true){
  const filtered=DATA.cases.filter(x=>activeLang==='all'||x.lang===activeLang);
  const start=reset?0:root.children.length;
  if(reset) root.innerHTML='';
  filtered.slice(start,visibleCount).forEach(x=>{
    const m=x.metrics;
    const el=document.createElement('section');
    el.className='case';
    const vattrs=`controls muted autoplay loop playsinline preload="metadata"`;
    el.innerHTML=`<div class="case-head"><div class="number">${String(x.rank).padStart(2,'0')}</div><div><div class="title">${esc(x.lang.toUpperCase())} · ${esc(x.age_group)} · ${esc(x.gender_group)}</div><div class="prompt" title="${esc(x.prompt)}">${esc(x.prompt)}</div><div class="compare-controls" style="padding:10px 0 0"><span class="hint" style="margin:0">Replacement-speech input:</span><audio controls preload="metadata" src="${esc(x.files.audio_cross)}"></audio></div></div><div class="metrics"><div class="metric"><b>${m.cross_sync_c.toFixed(2)}</b>Cross Sync-C</div><div class="metric"><b>${m.same_ssim.toFixed(3)}</b>Same SSIM</div><div class="metric"><b>${m.cross_sync_d.toFixed(2)}</b>Cross Sync-D</div></div></div><div class="grid ${x.presentation==='native'?'native':''}"><div class="cell"><div class="label">Reference video <small>original</small></div><video ${vattrs} src="${x.files.source}"></video></div><div class="cell"><div class="label">Same audio <small>reconstruction</small></div><video ${vattrs} src="${x.files.same}"></video></div><div class="cell cross"><div class="label">Replacement <small>CausalDub</small></div><video ${vattrs} src="${x.files.cross}"></video></div></div>`;
    root.appendChild(el);
  });
  wireExclusiveAudio(root);
  wireAutoplay();
  const more=document.getElementById('load-more');
  const remaining=filtered.length-visibleCount;
  more.hidden=remaining<=0;
  more.textContent=remaining>0?`Load ${Math.min(6,remaining)} more cases`:'All cases loaded';
}
document.querySelectorAll('.filter').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.filter').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
  activeLang=b.dataset.lang;
  visibleCount=6;
  render(true);
});
document.getElementById('mute').onclick=()=>{
  document.querySelectorAll('video').forEach(v=>v.muted=true);
  document.querySelectorAll('audio').forEach(a=>a.pause());
};
document.getElementById('play').onclick=()=>document.querySelectorAll('#cases video').forEach(v=>{
  const r=v.getBoundingClientRect();
  const vis=r.top<window.innerHeight && r.bottom>0;
  if(vis){v.currentTime=0;v.play().catch(()=>{});}
});
document.getElementById('load-more').onclick=()=>{visibleCount+=6;render(false);};
const menu=document.getElementById('menu');
const navLinks=document.getElementById('nav-links');
menu.onclick=()=>{
  const open=navLinks.classList.toggle('open');
  menu.setAttribute('aria-expanded',String(open));
};
navLinks.querySelectorAll('a').forEach(a=>a.onclick=()=>{navLinks.classList.remove('open');menu.setAttribute('aria-expanded','false');});
wireExclusiveAudio();
renderComparisons();
render(true);
</script>
</body>
</html>
'''


def main() -> None:
    html = (
        HTML.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
        .replace("__EXTRA__", json.dumps(EXTRA, ensure_ascii=False))
    )
    (ROOT / "index.html").write_text(html)
    print(ROOT / "index.html")


if __name__ == "__main__":
    main()
