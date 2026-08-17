# SLURRY Case Report — Template v0.1
*\<verify\> · 2026-08-17 · the per-artifact evidentiary memo; co-design target with Berkeley HRC*

Format rules: findings, confidence, and disagreement — never a verdict. Observations (what instruments measured) are strictly separated from inferences (what an analyst concludes). Every module result sits beside its provenance card. Anything requiring human judgment is flagged, not resolved. The report is generated from the registrar's log and is reproducible from it.

---

## Template

```
SLURRY CASE REPORT
Report ID · date generated · protocol version · rule set applied (and why — from intended use)

1. INTAKE RECORD
   Artifact: filename · media type · duration/dimensions · SHA-256 hash · intake timestamp
   Preservation: original stored unmodified at [ref]; working copies derived; hash re-verified [time]
   Context as entered (verbatim):
     platform of origin · date first seen · sharing chain · claim being made ·
     subject/event · case · jurisdiction · intended use
   Completeness: [fields provided / fields missing → analyses degraded or skipped as a result]

2. RULE SET & MODULE ELIGIBILITY (license gate output)
   Rule set selected: [e.g., human-rights investigation — Berkeley-Protocol-aligned defaults]
   Modules run: [list] · Modules withheld by license gate: [list + license reason]
   Modules skipped as uninformative for this artifact: [list + reason, e.g., "no audio track"]

3. CONTEXT CONDITIONING (stated before results, because it shapes their weight)
   e.g., "Platform = WhatsApp forward: ≥2 re-encodes assumed; pixel-forensic
   modules down-weighted; noise-based tells expect degradation; provenance
   metadata expected absent regardless of origin."

4. FINDINGS — one block per module
   ┌ Module name · version · [native/adopted]
   │ Provenance card: method · paper · training-data era · license · known limitations
   │ OBSERVATION: scores/maps/tells exactly as returned (figures attached: heatmaps,
   │   spectra, amplified clips — the inspectable evidence)
   │ Module confidence: [0–1] and why (signal quality, artifact suitability)
   └ Caveats triggered for THIS artifact: [e.g., "compression below reliable range"]

5. DISAGREEMENT MATRIX
   Modules × modules table of directional agreement; narrative reading of the
   structure (e.g., "physical-plausibility modules raise; context modules lower;
   consistent with heavily-processed authentic footage — see §6.2").
   Disagreement is reported as evidence, not reconciled.

6. SYNTHESIS
   6.1 OBSERVATIONS (aggregate): what the instruments measured, axis by axis.
   6.2 INFERENCES (analyst): interpretations consistent/inconsistent with the
       observations, each tied to the observations it rests on. Alternative
       explanations stated. NO verdict language.
   6.3 CHARACTERIZATION SUMMARY: 3–5 sentences an editor/legal reviewer can quote,
       in findings+confidence+disagreement form.

7. HUMAN-JUDGMENT FLAGS
   Numbered list of what the protocol cannot decide: domain knowledge needed
   (e.g., naval historian), claim-verification legwork, source contact, etc.

8. REGISTRAR EXTRACT
   Ordered analysis sequence with timestamps · module versions · licenses ·
   intermediate-result hashes · report generation hash. Full log exportable: [ref]

Prepared under SLURRY v[x] · This report characterizes; it does not adjudicate.
```

---

## Filled mock example (hypothetical artifact, illustrative values)

**SLURRY CASE REPORT** · SR-2026-0817-001 · generated 2026-08-17 · SLURRY v1.0-draft · Rule set: *human-rights investigation (Berkeley-Protocol-aligned defaults)* — selected by intended use "NGO documentation, possible legal annex"

**1. INTAKE RECORD.** Artifact `naval_strike_clip.mp4`, video 34 s, 720×1280. SHA-256 `9f3a…c41e`, intake 2026-08-17 14:02 UTC; original preserved; hash re-verified at report generation. Context (verbatim): *Platform: X, via Telegram forward · First seen: 2026-08-15 · Chain: Telegram channel → X repost (~2.1M views) · Claim: "Iranian missile destroys US destroyer, Strait of Hormuz, Aug 14" · Subject: Iran–US naval conflict · Case: [redacted] · Jurisdiction: US · Intended use: NGO documentation.* Completeness: all required fields present.

**2. RULE SET & ELIGIBILITY.** Modules run: Camera Physics v1.2, Game Engine Detector v1.0, Composite Detection v1.1, Platform Propensity v0.9, Trend v0.1-spec (manual), Provenance Reader v0.3, DualDataAlignment (adopted, Apache-2.0), TruFor (adopted, GRIP-UNINA NC — **eligible under this rule set**; would be withheld under commercial use). Skipped: Biosignal, RawNet2-Vocoder, AVAD (no faces; no original audio track survives re-encode).

**3. CONTEXT CONDITIONING.** Telegram→X chain implies ≥2 platform re-encodes: sensor-noise and provenance-metadata absence carries **no evidential weight**; pixel-forensic confidences capped accordingly. Claim date two days before first-seen date: recirculation check mandatory (§7.2).

**4. FINDINGS (abridged for the mock).**
- **Game Engine Detector v1.0** *(native; analytic, no training data; author \<verify\>)* — OBSERVATION: engine_probability 0.87, regime "real-time capture"; tells: nyquist_jitter 0.94, LOD pop events 12, hand-tremor 0.03 with smoothness 0.81. Confidence 0.72. Caveat: SSAO tell unvalidated on real footage; excluded from weight.
- **Camera Physics v1.2** *(native)* — OBSERVATION: noise floor near zero; chromatic aberration absent; spectral falloff sharper than lens MTF envelope. Confidence 0.4 (capped: compression can produce two of three). *Cross-check note: pattern equally consistent with clean render — see disagreement reading.*
- **TruFor** *(adopted; CVPR 2023; trained pre-2023 manipulation corpora; NC license logged)* — OBSERVATION: integrity score 0.44 (ambiguous); localization map: no coherent splice region; confidence map low over water surfaces (known weakness). Confidence 0.35.
- **DualDataAlignment** *(adopted; NeurIPS 2025; diffusion-era training)* — OBSERVATION: AI-generation score 0.22 (low). Confidence 0.5. *Provenance-card note: trained on generative-AI imagery; game-engine renders are out-of-distribution — a low score here does NOT contradict the engine finding.*
- **Platform Propensity v0.9** — OBSERVATION: X-2022+ propensity 0.80/spreadability 0.92; Telegram-2018+ propensity 0.80. Confidence 0.6 (sources per module memo).
- **Trend (manual, spec procedure)** — OBSERVATION: "Strait of Hormuz" search interest peaked 2026-08-13; artifact surfaced within 48 h of peak; visual-semantic match to trend topic high. Conjunction satisfied. Confidence 0.5 (retrospective feed only).
- **Provenance Reader v0.3** — OBSERVATION: no C2PA manifest; EXIF stripped. **Weight: none** (expected after platform transit — see §3).

**5. DISAGREEMENT MATRIX (reading).** The instructive disagreement is DualDataAlignment (low AI-generation score) versus Game Engine Detector (high engine score): the artifact appears *not* diffusion-generated **and** *not* camera-captured. This pattern is jointly consistent with real-time-rendered footage — a category the adopted AI-image detectors were never trained to see. TruFor's ambiguity is consistent: no splice, because nothing was composited. Context modules raise prior; physical modules split exactly along the training-era lines their provenance cards predict.

**6. SYNTHESIS.** *Observations:* strong real-time-render tells; no diffusion-generation signal; no splice localization; circulation profile matches high-velocity trend-adjacent amplification on high-propensity platforms; provenance channels empty but uninformative. *Inferences:* the observations are most consistent with **video-game footage presented as authentic conflict imagery** (cf. the documented War Thunder/Arma 3 laundering pattern, 2022–2026); they are inconsistent with an in-camera original and weakly inconsistent with diffusion synthesis. Alternative not excluded: heavily processed authentic footage with stabilization applied (would require §7.1 to resolve). *Characterization summary:* "Instrumental analysis characterizes this clip as bearing strong indicators of real-time game-engine rendering and no indicators of camera origin or diffusion-model generation, circulating in a pattern typical of trend-driven synthetic amplification. Confidence is moderate and rests principally on temporal rendering artifacts; module disagreement follows each instrument's documented training limits. No verdict is asserted; see human-judgment flags."

**7. HUMAN-JUDGMENT FLAGS.** (1) Domain identification of depicted vessels against claimed order of battle (specialist knowledge — cf. the Amsterdam corpus precedent). (2) Reverse-search the clip against pre-2026-08-14 postings; the claim/first-seen gap suggests possible recirculated fake. (3) If evidentiary use advances: obtain least-compressed available copy and re-run.

**8. REGISTRAR EXTRACT.** 14:02:11 intake+hash → 14:02:40 gate (8 eligible, 3 skipped, TruFor NC-eligibility logged) → 14:03–14:11 module sequence as ordered above (versions + per-result hashes logged) → 14:12 report generated, hash `77b0…19d3`. Full log: `SR-2026-0817-001.registrar.json`.

*Prepared under SLURRY v1.0-draft. This report characterizes; it does not adjudicate.*
