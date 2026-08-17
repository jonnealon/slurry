# SLURRY — Adopted Open-Source Modules: Audited Shortlist
*\<verify\> · audited 2026-08-08 from the Deep-o-Meter live model set (37 models); formalized 2026-08-14*

Candidates for third-party modules to slot alongside the six originals, per handoff §1. Each entry is provenance-card-ready. Repos were audited for license, weights availability, inference ease, and maintenance (via GitHub pages; stars/dates as of Aug 2026).

## Tier 1 — adopt first

| Module | Modality | License | Why |
|---|---|---|---|
| **DualDataAlignment** | Image | Apache-2.0 | Current frontier (NeurIPS 2025 Spotlight; DINOv2 ViT-L/14 + LoRA). HuggingFace checkpoints, dedicated inference folder, actively maintained (commits Feb–Mar 2026). Permissive license keeps SLURRY's options open. [repo](https://github.com/roy-ch/Dual-Data-Alignment) |
| **HiFi_IFDL** | Image | MIT | The evidence-friendly one: clean Python API — `detect()` and `localize()` — returning forgery-localization masks an investigator can inspect. Key for the Berkeley HRC context. [repo](https://github.com/CHELSEA234/HiFi_IFDL) |
| **RawNet2-Vocoder** | Audio | MIT | Vocoder-artifact detection (generalizes across TTS pipelines; gestures at attribution). Single-file `eval.py`, weights shipped. UB Media Forensic Lab's own code — integration doubles as a collaboration signal. [repo](https://github.com/csun22/Synthetic-Voice-Detection-Vocoder-Artifacts) |

## Tier 2 — strong seconds

| Module | Modality | License | Notes |
|---|---|---|---|
| **AIDE** | Image | MIT | ICLR 2025; hybrid multi-expert features — a genuinely *different* feature family from DualDataAlignment, so disagreement between them is informative. Weights provided. [repo](https://github.com/shilinyan99/AIDE) |
| **NPR** | Image | **NONE — unresolved** | Lightweight, weights + HF demo; up-sampling-artifact method (third distinct feature family). No license file = all-rights-reserved by default; cannot redistribute until resolved. Gate accordingly. [repo](https://github.com/chuangchuangtan/NPR-DeepfakeDetection) |
| **UniversalFakeDetect (CLIP-ViT)** | Image | MIT | Cheapest to run (linear head on frozen CLIP). Script needs light adaptation for single images. [repo](https://github.com/Yuheng-Li/UniversalFakeDetect) |
| **AVAD** | Video (audio-visual) | MIT | Self-supervised audio-visual sync anomaly; single-video `detect.py`. The most conceptually interesting for video slop beyond face-forgery. [repo](https://github.com/cfeng16/audio-visual-forensics) |

## With caveats

- **DeepfakeBench** — 36 detectors in one framework, Docker support, 1,000+ stars. **CC BY-NC** and benchmarking-oriented: treat as a *comparison instrument*, not SLURRY's engine. [repo](https://github.com/SCLBD/DeepfakeBench)
- **Effort** — ICML 2025 oral, good single-image `demo.py`, weights. **CC BY-NC.** [repo](https://github.com/YZY-stack/Effort-AIGI-Detection)
- **AVSRDD (2025)** — no code released; the Deep-o-Meter "Code" link literally reads "TBD."

## Proposed starting ensemble (v1)

**Images:** DualDataAlignment + AIDE + NPR — three distinct feature families (foundation-model semantics / hybrid experts / up-sampling artifacts), which is what makes their disagreement meaningful rather than redundant. **Localization:** HiFi_IFDL (heatmaps for the Case Report). **Audio:** RawNet2-Vocoder. All MIT/Apache except NPR's gap.

## Post-audit updates (Aug 2026)

1. **License gating** (handoff §7.1) handles the CC BY-NC and no-license cases structurally: modules carry machine-readable license metadata; the protocol filters by declared intended use rather than excluding outright.
2. **Text modality:** Pangram (closed, $20/mo, API; near-perfect on text per NYT 8/13/26 + UChicago) could be the first *commercial* adopted module behind the gate. The open/auditable text-detection lane remains unoccupied.
3. **New module candidate — multi-modal provenance:** C2PA/Content Credentials reader for images + text-watermark checks (Anthropic announced Claude text watermarking Aug 2026; others expected to follow). Cheap, open, and nobody has it yet.
4. Related audits in this project: `slurry-evm-ip-memo.md` (Biosignal IP), `deep-o-meter-analysis-for-slurry.md` (full 37-model landscape), `slurry-context.md` (orientation).

---

# Directory 2 — the ImageWhisperer-named pool (audited 2026-08-14)

ImageWhisperer's benchmarks page names its underlying models; auditing that pool surfaced four permissively-licensed candidates the Buffalo directory doesn't list, plus one framework find.

## New Tier 1 candidates

| Module | Modality | License | Why |
|---|---|---|---|
| **Community Forensics (CommFor)** | Image | MIT | CVPR 2025 (Park & Owens). Trained on **thousands of generators** — the generator-diversity philosophy as a training strategy (this is ImageWhisperer's "Generator Diversity Check"). Weights on HuggingFace (`OwensLab/commfor-model-384`, 21.8M-param ViT-S — small and cheap). Inference is notebook-shaped but simple. [repo](https://github.com/JeongsooP/Community-Forensics) |
| **SPAI** | Image | Apache-2.0 | CVPR 2025 (MeVer/CERTH). **Spectral learning**, any-resolution — yet another distinct feature family. CLI inference (`spai infer`), <8GB VRAM. Weights via Google Drive. [repo](https://github.com/mever-team/spai) |
| **IMDLBenCo** (framework) | Image localization | **CC-BY-4.0 — attribution only, commercial OK** | NeurIPS 2024 D&B Spotlight. Pip-installable (`pip install imdlbenco`), packages IML-ViT + Mesorch + SparseViT + more with checkpoints and inference tooling; actively maintained (commits Aug 2026). **The permissively-licensed counterpart to DeepfakeBench** — a framework SLURRY can actually build on, not just compare against. [repo](https://github.com/scu-zjz/IMDLBenCo) |

## New Tier 2

| Module | Modality | License | Notes |
|---|---|---|---|
| **IML-ViT** | Image localization | MIT | Pixel-level manipulation masks; Colab/notebook demo; 309★. Direct competitor/complement to HiFi in the localization slot; also included in IMDLBenCo. [repo](https://github.com/SunnyHaze/IML-ViT) |
| **SparseViT** | Image localization | CC-BY-4.0 | AAAI 2025; ~70-line test script (needs trivial adaptation for GT-free images). [repo](https://github.com/scu-zjz/SparseViT) |
| **ClipDet** | Image | Apache-2.0 | GRIP-UNINA's CLIP-based detector (CVPRW 2024) — their one permissive repo; weights committed in-repo via LFS; quiet since Nov 2024. [repo](https://github.com/grip-unina/ClipBased-SyntheticImageDetection) |

## License-gated (non-commercial only — eligible via the gate for HR/research intended use)

- **TruFor** (GRIP-UNINA custom NC license: "only for informational and nonprofit purposes"): best-in-class output shape — pixel localization map + **confidence map** + whole-image score per artifact, Docker-first, weights auto-fetched, maintained through May 2025. Its map+confidence+score triple matches SLURRY's findings+confidence philosophy exactly. [repo](https://github.com/grip-unina/TruFor)
- **B-Free** (same GRIP NC license): CVPR 2025 bias-free detection, DINOv2-based, single-image script, actively maintained (Jan 2026). Score only. [repo](https://github.com/grip-unina/B-Free)

## Special case — Camera Physics axis

- **PerspectiveFields** (UMich/Adobe, CVPR 2023 Highlight): per-pixel up-vector + latitude fields with a defined discrepancy metric for compositing checks — a direct machine complement to the native Camera Physics module's vanishing-point/perspective ideas. **Adobe Research license: noncommercial AND no redistribution** — cannot be bundled; at most an optional, user-fetched dependency, documented as such in the gate. [repo](https://github.com/jinlinyi/PerspectiveFields)

## Revised v1 ensemble (supersedes the ensemble above)

**Images — AI-generation:** **DualDataAlignment + Community Forensics + SPAI** — three distinct philosophies (foundation-model alignment / generator-diversity training / spectral learning) with **fully clean licenses** (Apache/MIT/Apache). This retires the NPR license problem from the critical path; NPR and AIDE become optional fourth/fifth opinions, ClipDet a cheap alternate. **Localization:** HiFi_IFDL (MIT) and/or IMDLBenCo's IML-ViT — with TruFor added behind the NC gate for human-rights casework, where its confidence map earns its keep. **Audio:** RawNet2-Vocoder unchanged. **Multimodal:** AVAD unchanged.

**Directory lesson:** Buffalo and ImageWhisperer each surfaced permissive gems the other missed (Buffalo: DualDataAlignment, AIDE; ImageWhisperer's pool: CommFor, SPAI, ClipDet, IMDLBenCo). Two directories beat one; a periodic re-audit of both is cheap.
