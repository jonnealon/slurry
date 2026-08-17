# SLURRY

**An open protocol for the multi-axis characterization of synthetic and suspect media.**
*Findings, confidence, and disagreement — never a verdict.*

by Jon Nealon · \<verify\> · [Protocol document (DOI)](#) · License: see [Licensing](#licensing)

---

SLURRY takes a media artifact **plus its required context** (platform, date, sharing chain, the claim being made, intended use) and runs it through an ensemble of independent modules across four axes — **biological signal, physical plausibility, contextual priors, and provenance** — then reports what each instrument measured, how confident it was, and where the instruments disagree. Disagreement is reported as evidence, not resolved away: a detector trained on 2020's generators disagreeing with one trained on 2025's is itself a finding.

The protocol is aligned with the [Berkeley Protocol on Digital Open Source Investigations](https://humanrights.berkeley.edu): artifacts are hashed on intake, every analysis is logged by a registrar (tool versions, licenses, sequence, intermediate results), and reports separate observation from inference. Built for human-rights investigation, journalism, and research. **Local-first:** sensitive material never needs to transit a third-party API.

## Why not a verdict?

Verdicts age silently (detectors carry their training era's blind spots), fail on platform-recompressed copies, injure people via unappealable opaque scores, and answer the wrong question — the most common misleading media is *authentic footage under a false claim*, invisible to any tool that only asks "was this made by AI?" SLURRY asks what an artifact **is** and what it **does** in an information environment. The full argument is in the [protocol document](#).

## Modules

**Native** (original instruments; each with a methodology paper ending in *Known Limitations*):

| Module | Axis | Status |
|---|---|---|
| Biosignal (EVM, spatial pulse coherence) | biological | code + paper |
| Camera Physics | physical plausibility | code + paper |
| Composite Detection (seam-finder) | physical plausibility | code + paper |
| Game Engine Detector (v1: real-time regime) | physical plausibility | code + paper |
| Trend (attention-conjunction razor) | context | spec + paper |
| Platform Propensity (time-indexed) | context | prototype + memo |

**Adopted** (audited open-source detectors, containerized, upstream licenses intact — chosen for *diversity of detection philosophy* so disagreement is informative): DualDataAlignment · Community Forensics · SPAI (image generation, three distinct philosophies) · HiFi_IFDL / IML-ViT (manipulation localization with inspectable heatmaps) · RawNet2-Vocoder (audio) · AVAD (audio-visual sync) · plus license-gated instruments (e.g., TruFor) available only for eligible intended uses. Full audit: [`docs/adopted-modules-shortlist.md`](#).

Every module carries a **provenance card** — method, paper, training-data era, license, known limitations — surfaced in every report, because the age of a detector's worldview is part of the finding.

## The license gate

Modules declare machine-readable license metadata. At intake you declare an intended use; the protocol **filters** eligible modules before it **orchestrates** them, and the registrar logs both inclusions and exclusions. Non-commercial research instruments stay usable for human-rights work without contaminating other deployments.

## Quickstart

```bash
# reference implementation — under construction
git clone https://github.com/<org>/slurry && cd slurry
# [placeholder: docker compose up · slurry intake <file> --context context.yaml · slurry report]
```

Until then: the Game Engine Detector runs standalone as a [Colab notebook](#), and each adopted module's audit entry links its upstream inference instructions.

## Outputs

**Case Report** — per-artifact evidentiary memo: intake record, rule set, per-module findings beside provenance cards, disagreement matrix, observation/inference separation, human-judgment flags, registrar extract. [Template + worked example](#). **Corpus Study** — the same engine over many artifacts, for research on disagreement structure and circulation dynamics.

## Licensing

- Protocol document, templates, papers: **CC BY 4.0** ([LICENSE-DOCS.md](LICENSE-DOCS.md))
- Native module code: **MIT** ([LICENSE](LICENSE))
- Adopted modules: **retain their upstream licenses**, enforced by the gate. Note: the Biosignal module's method is subject to US patents (expiring 2032–33); non-commercial research use is covered by the rights-holder's covenant. See [`docs/ip-notes.md`](#).

## Status & roadmap

v1.0-draft. Honest ledger: ensemble thresholds are priors, not calibrations (a platform-degraded paired corpus is the top empirical need); the integration rubric is a weighted evidence framework, not a probability model; offline renders and text authorship are documented gaps. Roadmap: engine scaffold (Docker-per-module + registrar) → v1 ensemble wiring → calibration corpus → first Corpus Study.

## Citing

> Nealon, J. (2026). *SLURRY: A Protocol for the Multi-Axis Characterization of Synthetic and Suspect Media* (v1.0). \<verify\>. DOI: [10.5281/zenodo.21986995](https://doi.org/10.5281/zenodo.21986995)

Contributions welcome once the engine scaffold lands — especially modules with honest provenance cards. This project characterizes; it does not adjudicate.
