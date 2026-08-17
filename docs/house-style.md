# SLURRY House Style — Module Methodology Papers
### The six-section template (formalized from the Platform Propensity memo, per handoff item 3)

*\<verify\> · v1.0 · 2026-08-12*

Every SLURRY module gets one methodology paper in this shape. The exemplar is the Platform Propensity memo; the Game Engine Detector paper (handoff §3) is the second instance. Target length ~700–1,400 words. Plain declarative prose; no marketing language; limitations stated as flatly as capabilities.

## The six sections

**§1 — Purpose and Axis.** What the module detects, which axis it operates on (biological / physical plausibility / context), what gap it fills relative to the other modules, and how it relates to its nearest neighbor module (complement, cross-check, inverse). One paragraph.

**§2 — Inputs and Outputs.** Input: the artifact type and any required context fields. Output: enumerated, typed, bounded (e.g., probability 0–1, label, confidence 0–1, itemized tells). Always close with the ensemble sentence: the output is a weak signal contributing to the ensemble, not a standalone verdict, and its disagreement with other modules is itself reported as information.

**§3 — Methodology and Mechanism.** How it actually works: sub-detectors, features, decision logic, combiner. Written against the real code where code exists — name the actual functions and parameters, not idealized ones. Where the module has regimes or modes, state which are implemented and which are stubs.

**§4 — Grounding and Sources.** The literatures and named studies the mechanism rests on, with full citations. Any claim not confirmed against a source carries an explicit `[VERIFY]` flag. A paper with unresolved `[VERIFY]` flags is a draft, not a release.

**§5 — Known Limitations.** Numbered list. Include at minimum: false-positive modes (what real content will trip it), attack surface (how an adversary defeats it), reliability asymmetries (where it is strong vs. deliberately humble), and data/collection biases. The fairness trap belongs here when relevant.

**§6 — Motivating Context.** Why the module exists: the real-world cases that justify it. Firsthand evidence (e.g., the Amsterdam corpus) is identified as such and needs no external source; external incidents carry citations. Close by stating the pattern the cases establish.

## Conventions

- **Flags:** `[VERIFY]` = generated from recall, unconfirmed. `[FINDING]` = confirmed this session, source noted. `[PLACEHOLDER]` = name or value known to be provisional. `[PENDING TASK]` = work item, not a fact.
- **Provenance card** (front-matter of every module paper): module name; axis; author (native: \<verify\> / adopted: upstream project); license, structured and machine-readable; code status (exists / prototype / spec-only); paper status; training-data era where applicable.
- **The ensemble principle, verbatim where needed:** modules are individually fallible weak signals; false positives are expected; reliability is emergent from the ensemble and surfaced through disagreement; disagreement is not noise to be resolved — it is information, and itself a finding. Output is findings + confidence + disagreement, never a verdict.
- **Verdict language ban:** module papers do not use "real/fake verdict," "detects fakes," or "Protocol-compliant." Say "characterizes," "raises/lowers slop probability," "Protocol-aligned."
- **Naming:** modules are nouns, not acronyms, where possible (Biosignal, Camera Physics, Composite Detection, Trend, Platform Propensity, Game Engine Detector).
