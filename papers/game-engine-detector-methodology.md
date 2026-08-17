# Game Engine Detector — Methodology Paper
*SLURRY module methodology · v2 (supersedes handoff §3 draft v1) · \<verify\> · 2026-08-12*

| Provenance | |
|---|---|
| Module | Game Engine Detector |
| Axis | physical plausibility |
| Author | \<verify\> (native — original code, no upstream) |
| License | to be declared (open-source-leaning per protocol notes §7.4) |
| Code | **v1 implemented** (`game-engine-detector-v1.py`; Colab notebook): regime 1 live, SSR stubbed, regime 2 murmur |
| Paper | v2 — written against the real code; §6 citations verified 2026-08-12 |
| Training data | none — analytic method, no learned components |

## §1 — Purpose and Axis

The Game Engine Detector operates on the physical-plausibility axis, alongside the Camera Physics module. Its job is to identify footage produced by a real-time rendering engine such as Unreal or Unity. It targets a category of synthetic media the other modules systematically miss: content that is fully synthetic — no camera ever recorded it — yet was not produced by a generative-AI pipeline. Because game engines are engineered on decades of physically-based rendering, such footage can satisfy the Camera Physics module's expectations and pass undetected. This module closes that specific gap, and it is positioned not as a mode of Camera Physics but as its complement and cross-check: where Camera Physics asks whether footage obeys real optics, this module asks whether it obeys them in the particular, over-clean ways an engine does. Fused, the two would fight; separate, they cross-check. That is the ensemble working.

## §2 — Inputs and Outputs

**Input:** a video artifact (≥12 frames; ≥10 s at ≥15 fps recommended).

**Output, fourfold:** an engine-origin probability (0–1); a regime label — *real-time capture*, *possible offline render (low confidence)*, or *no engine signal detected*; a confidence score reflecting data and signal quality; and an itemized list of which specific tells fired, each with its measured values. Emitted as registrar-ready JSON.

As with every SLURRY module, the output is a weak signal contributing to the ensemble, not a standalone verdict, and its disagreement with other modules is itself reported as information.

## §3 — Methodology and Mechanism

The key inversion (unchanged from draft v1): **regime 1 detects the presence of engine shortcuts; regime 2 detects the absence of reality's messiness** — the same logic as the Biosignal module, detection by what should be there and isn't. v1 implements regime 1 in full and regime 2 as a deliberate murmur.

**Sub-detector 1 — camera-motion analysis** (`camera_motion_score`). Global translation is tracked per frame-pair by phase correlation, then analyzed in windowed spectra (median across windows, robust to pan/stop nonstationarity). Two disjoint bands carry the signal: the **hand-tremor band (2–8 Hz)**, where physical camera support lives and virtual cameras are silent, and the **near-Nyquist band (≥0.45·fps)**, where TAA's frame-alternating projection jitter lives — a positive engine cue no hand can produce. Engine evidence is either spline-like motion (low tremor and low-passed-jerk smoothness) or strong Nyquist-rate jitter. Static shots are declared uninformative rather than scored.

**Sub-detector 2 — TAA shimmer** (`taa_shimmer_score`). The discriminator is *detrended temporal alternation*: the second temporal difference of a pixel affected by frame-alternating jitter flips sign nearly every frame (alternation → 1.0), while stochastic sensor noise is statistically capped near 0.73 (MA(2) sign statistics) and compression pulls it lower; camera pan is a trend and cancels in the second difference. The metric is the fraction of amplitude-gated edge pixels with alternation > 0.9, contrasted against flat regions, computed per window with the strongest window winning — so mixed pan/hold gameplay stays readable.

**Sub-detector 3 — SSAO halo fringes** (`ssao_halo_score`). Screen-space ambient occlusion hugs object edges with a thin, scene-wide uniform dark band; real contact shadows are irregular and local. Measured as the near-band (2–6 px) to far-band (8–16 px) luminance ratio around strong edges on low-motion frames, with cross-frame consistency required.

**Sub-detector 4 — LOD popping** (`lod_popping_score`). Level-of-detail swaps produce step-changes in block-wise sharpness (Laplacian variance) uncorrelated with local motion. Jumps are z-scored against each block's own fluctuation distribution (MAD), so sensor-noise jitter cannot masquerade as popping; events require z > 8 in low-motion, textured blocks.

**Sub-detector 5 — SSR dropout: STUB.** Detecting screen-space-reflection dropout requires identifying reflective surfaces and their sources — semantic machinery outside v1 scope. Carried as an explicit zero-confidence entry so the ensemble knows it was not tested.

**Regime-2 murmur — noise floor** (`noise_floor_score`). High-pass residual in flat regions: real capture carries shot/read noise; clean renders carry (near) none. Capped at low confidence by design, because heavy recompression strips real footage's noise too (§5.3).

**Combiner.** Confidence-weighted regime-1 evidence (weights: motion 0.35, shimmer 0.30, LOD 0.20, halo 0.15); strong regime-1 signal yields a high-confidence engine call; only a faint regime-2 murmur yields a low-confidence "possible offline render" flag deferred to the ensemble.

**Validation to date.** On the synthetic direction-of-effect harness (engine caricature: spline pan + hold, zero noise, alternating jitter, painted rims, one LOD pop; camera caricature: same scene with 2–12 Hz tremor and sensor noise): engine clip → P(engine) 0.945, regime "real-time capture," with motion, shimmer, and LOD tells at maximum; camera clip → P(engine) 0.0, all tells zero, no false positives. The halo tell is validated in logic but not yet against real engine footage (§5.5). These are unit tests, not benchmarks; threshold calibration against real gameplay/handheld pairs is the next task. One implementation finding worth recording: `cv2.phaseCorrelate` windows its inputs in place — pass copies, or every downstream detector reads corrupted frames.

## §4 — Grounding and Sources

1. **Real-time rendering literature** on temporal anti-aliasing and screen-space techniques and their characteristic artifacts: Yang, Liu & Salvi, "A Survey of Temporal Antialiasing Techniques," *Computer Graphics Forum* 39(2), 2020, doi:10.1111/cgf.14018 (documents jitter/ghosting/disocclusion artifacts and the shortcut regime).
2. **Sensor-noise forensics** grounding the regime-2 murmur: Lukáš, Fridrich & Goljan, "Digital Camera Identification from Sensor Pattern Noise," *IEEE Trans. Information Forensics and Security* 1(2), 2006, doi:10.1109/TIFS.2006.873602.
3. **Frequency-domain discrimination** of synthetic vs. optical imagery: Corvi et al., "On the Detection of Synthetic Images Generated by Diffusion Models," ICASSP 2023 (adjacent grounding; the render case differs from the generative case but shares the too-clean-spectrum logic).

## §5 — Known Limitations

1. **The offline-render case is genuinely hard.** Sub-detector 2 is deliberately low-confidence; a polished offline render converges with the general photoreal-CGI problem.
2. **Post-processing attack surface.** Added film grain, fake chromatic aberration, camera shake, and recompression mask engine tells — though such tampering may leave second-order fingerprints. The engine vendors are not the adversary; the launderer is.
3. **False-positive convergence.** Heavily recompressed real footage sheds its own sensor signatures and resembles a clean render. Conflict-zone footage is a specific risk — exactly the material this module will most often meet.
4. **Asymmetric reliability.** Strong on real-time gameplay capture, explicitly humble on offline renders; v1 scopes to the former and documents the latter as a gap.
5. **Halo tell unvalidated on real footage.** The synthetic harness validates three of four regime-1 tells; `ssao_halo` needs real engine footage.
6. **v1 thresholds are priors, not calibration.** All decision thresholds were set on synthetic clips; calibration requires a gameplay/handheld paired corpus, which existing deepfake datasets do not provide.

## §6 — Motivating Context

The module addresses a stable, recurring vector in conflict misinformation: realistic military and vehicle game footage laundered into fake war clips.

**Primary, firsthand evidence.** From the DMI Amsterdam corpus of Iran-war Twitter posts: a photoreal naval-battle clip that resembled a real engagement and would pass a camera-physics check, later identified as **World of Warships** footage. Its danger lay in its sobriety — historically accurate warship models that clear the untrained eye; the giveaway resided in specialist domain knowledge most viewers lack. (Firsthand; no external source required. Note: no *externally documented* WoW incident was found in verification — the documented family below is Arma 3 / War Thunder / DCS.)

**Corroborating documented family (verified 2026-08-12; full citations in the verification memo).** The pattern recurs across titles, conflicts, and years: the "Ghost of Kyiv" DCS World clip (PolitiFact, Feb 2022); the Arma 3 Ukraine-war wave that forced Bohemia Interactive's public statement — "we are certainly not pleased that it can be mistaken for real-life combat footage and used as war propaganda" (Nov 2022; Euronews, Jan 2023); Arma 3 as a fake Houthi strike on the USS Eisenhower (CBS, Jun 2024); Arma 3 in India–Pakistan misinformation (Full Fact, May 2025); War Thunder clips in the June 2025 Israel–Iran war, one requiring an IDF denial; and in the **March 2026 Iran war**, an AFP-debunked War Thunder clip presented as an Iranian attack on a US warship — reposted by **the Governor of Texas** with ~7.3M views before deletion, a clip already debunked by Reuters in 2024 under a different conflict's caption. Recycled across three conflicts, endorsed by a sitting governor: game-engine slop is not an anomaly but a repeat pattern with a laundering lifecycle. That is the core justification for this module — and for building regime 1 first, since every incident in the family is real-time-rendered gameplay, not offline cinematics.
