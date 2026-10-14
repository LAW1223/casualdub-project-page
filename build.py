#!/usr/bin/env python3
"""Build the CausalDub project page (static GitHub Pages site)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "selection_manifest.json").read_text())

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CausalDub — Two-Step Causal Lip Editing</title>
<meta name="description" content="CausalDub distills a full-context lip editor into a two-step block-causal model with one audio branch per block.">
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

.table-wrap{overflow:auto;border-radius:14px;border:1px solid var(--line)}
table{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff;min-width:720px}
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
.cross video{outline:2px solid var(--accent);outline-offset:-2px}
.audio{margin-top:8px;width:100%}

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
  .case-head{grid-template-columns:auto 1fr}
  .metrics{grid-column:1/-1;justify-content:flex-start}
  .grid{grid-template-columns:1fr}
  button.sync{margin-left:0}
  .nav-links{display:none}
}
</style>
</head>
<body>
<nav><div class="wrap nav-inner">
  <a class="brand" href="#">CausalDub</a>
  <div class="nav-links">
    <a href="#abstract">Abstract</a>
    <a href="#method">Method</a>
    <a href="#results">Results</a>
    <a href="#videos">Videos</a>
    <a href="#cite">Cite</a>
  </div>
</div></nav>

<header class="hero"><div class="wrap">
  <div class="eyebrow">CVPR 2027 · Anonymous submission</div>
  <p class="hero-brand">CausalDub</p>
  <h2>Full-context lip editing, distilled into two causal steps.</h2>
  <p class="lead">
    Edit only the mouth of a source video to follow replacement speech—while preserving
    identity, pose, expression, lighting, and non-mouth motion—with two denoising
    evaluations and one audio branch per causal block.
  </p>
  <div class="cta">
    <a class="btn btn-primary" href="#videos">Watch results</a>
    <a class="btn btn-ghost" href="#results">See numbers</a>
    <a class="btn btn-ghost" href="#cite">BibTeX</a>
  </div>
  <div class="hero-visual">
    <img src="media/teaser.jpg" alt="CausalDub teaser: source, same-audio, and cross-audio results across seven cases" width="2200" height="1016">
  </div>
  <p class="caption">Seven frozen cases (English A–D, Chinese E–G): source articulation, same-audio reconstruction, and replacement-speech edit. Mouth insets highlight lip response.</p>

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
      Source-video lip editing must follow replacement speech while preserving the source
      video’s identity, pose, expression, lighting, and non-mouth motion. We compress a strong
      full-context editor into a block-causal model with two denoising evaluations and one
      audio branch per block. The construction adapts the editor to causal generation,
      regresses two-step trajectories from the guided causal parent, and applies guided
      distribution matching with an appearance-retention anchor. On held-out CausalDub-Bench
      the student reaches 8.681 cross Sync-C, non-inferior to its 48-step teacher (8.718)
      and above every external method (best 7.575). SyncNet-independent lip-reading WER and
      audio-shift calibration support that the gain is not a SyncNet artifact.
    </p>
  </div>
</div></section>

<section id="method"><div class="wrap">
  <h3>Method</h3>
  <p class="section-lead">A full-context teacher is adapted to causal generation, used to supervise two-step trajectories, then refined with guided distribution matching and retention.</p>
  <div class="two">
    <div class="panel">
      <img src="media/framework.jpg" alt="CausalDub framework overview">
      <p class="caption">Block-causal student: two denoising evaluations, one audio branch, bounded history.</p>
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
</div></section>

<section id="results"><div class="wrap">
  <h3>Results</h3>
  <p class="section-lead">Cross-audio lip sync and visual quality on public benchmarks. FPS is single-H20 marginal throughput of the full public pipeline.</p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Method</th><th>NFE</th><th>FPS↑</th>
          <th>HDTF Sync-C↑</th><th>HDTF Sync-D↓</th><th>HDTF FVD↓</th>
          <th>CDB Sync-C↑</th><th>CDB FVD↓</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Wav2Lip</td><td>1</td><td>5.2</td><td>8.782</td><td>6.972</td><td>129.51</td><td>—</td><td>—</td></tr>
        <tr><td>LatentSync 1.6</td><td>20</td><td>2.2</td><td>8.160</td><td>7.035</td><td>28.05</td><td>—</td><td>—</td></tr>
        <tr><td>Lip Forcing</td><td>—</td><td>2.4</td><td>—</td><td>—</td><td>—</td><td>5.192</td><td>15.78</td></tr>
        <tr><td>Teacher (ours, 48-NFE)</td><td>48</td><td>—</td><td>9.422</td><td>6.127</td><td>27.49</td><td>8.718</td><td>15.23</td></tr>
        <tr class="ours"><td>CausalDub</td><td>2</td><td>6.3</td><td>10.001</td><td>6.062</td><td>30.89</td><td>8.681</td><td>17.35</td></tr>
      </tbody>
    </table>
  </div>
  <p class="note">CDB = CausalDub-Bench-256 (held-out identities, English + Chinese). Full tables, VoxCeleb2 / TalkVid, WER, and ablations are in the paper and supplementary.</p>
  <div class="panel" style="margin-top:18px">
    <img src="media/pareto.jpg" alt="Sync vs efficiency Pareto plot">
    <p class="caption">Synchronization–efficiency trade-off. CausalDub sits at high Sync-C with 2 NFE.</p>
  </div>
  <div class="panel" style="margin-top:18px">
    <img src="media/comparison.jpg" alt="Qualitative cross-audio comparison against baselines">
    <p class="caption">Cross-audio comparison on the first HDTF item. All methods receive the same source and replacement waveform.</p>
  </div>
</div></section>

<section id="videos"><div class="wrap">
  <h3>Video showcase</h3>
  <p class="section-lead">
    Twenty frozen, source-disjoint CausalDub-Bench examples (10 English / 10 Chinese),
    selected by a reproducible sync + reconstruction gate and visual farthest-point sampling—not a hand-picked top-20.
    Each case shows source, same-audio reconstruction, and replacement-speech edit.
  </p>
  <div class="toolbar">
    <button class="filter active" data-lang="all">All 20</button>
    <button class="filter" data-lang="en">English</button>
    <button class="filter" data-lang="zh">Chinese</button>
    <button class="ghost" id="mute">Unmute videos</button>
    <button class="sync" id="play">Play visible videos</button>
  </div>
  <main id="cases"></main>
</div></section>

<section id="cite"><div class="wrap">
  <h3>Cite</h3>
  <p class="section-lead">BibTeX will be updated when the preprint is released. Placeholder for the anonymous submission:</p>
  <div class="bib" id="bib">@inproceedings{causaldub2027,
  title     = {CausalDub: Distilling Full-Context Lip Editing into a Two-Step Causal Model},
  author    = {Anonymous},
  booktitle = {CVPR},
  year      = {2027}
}</div>
</div></section>

<footer><div class="wrap">
  CausalDub project page · results showcase for an anonymous CVPR submission.
  Videos and metrics are frozen from the paper’s CausalDub-Bench protocol.
  Lip-editing technology can be misused; use only with consent and provenance watermarking.
</div></footer>

<script>
const DATA = __DATA__;
const root = document.getElementById('cases');
let muted = true;
function esc(x){
  return String(x||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function render(lang='all'){
  root.innerHTML='';
  DATA.cases.filter(x=>lang==='all'||x.lang===lang).forEach(x=>{
    const m=x.metrics;
    const el=document.createElement('section');
    el.className='case';
    el.innerHTML=`<div class="case-head"><div class="number">${String(x.rank).padStart(2,'0')}</div><div><div class="title">${esc(x.lang.toUpperCase())} · ${esc(x.age_group)} · ${esc(x.gender_group)}</div><div class="prompt" title="${esc(x.prompt)}">${esc(x.prompt)}</div></div><div class="metrics"><div class="metric"><b>${m.cross_sync_c.toFixed(2)}</b>Cross Sync-C</div><div class="metric"><b>${m.same_ssim.toFixed(3)}</b>Same SSIM</div><div class="metric"><b>${m.cross_sync_d.toFixed(2)}</b>Cross Sync-D</div></div></div><div class="grid"><div class="cell"><div class="label">Source <small>original</small></div><video muted loop playsinline preload="metadata" src="${x.files.source}"></video></div><div class="cell"><div class="label">Same audio <small>reconstruction</small></div><video muted loop playsinline preload="metadata" src="${x.files.same}"></video><audio class="audio" controls preload="none" src="${x.files.audio_same}"></audio></div><div class="cell cross"><div class="label">Replacement <small>CausalDub</small></div><video muted loop playsinline preload="metadata" src="${x.files.cross}"></video><audio class="audio" controls preload="none" src="${x.files.audio_cross}"></audio></div></div>`;
    root.appendChild(el);
  });
}
document.querySelectorAll('.filter').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.filter').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
  render(b.dataset.lang);
});
document.getElementById('mute').onclick=()=>{
  muted=!muted;
  document.querySelectorAll('video').forEach(v=>v.muted=muted);
  document.getElementById('mute').textContent=muted?'Unmute videos':'Mute videos';
};
document.getElementById('play').onclick=()=>document.querySelectorAll('#cases video').forEach(v=>{
  v.currentTime=0; v.play().catch(()=>{});
});
render();
</script>
</body>
</html>
'''


def main() -> None:
    html = HTML.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
    (ROOT / "index.html").write_text(html)
    print(ROOT / "index.html")


if __name__ == "__main__":
    main()
