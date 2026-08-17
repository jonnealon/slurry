# SLURRY
## A Protocol for the Multi-Axis Characterization of Synthetic and Suspect Media

**Jon Nealon** · \<verify\>
Version 1.0.0 — August 2026
License: CC BY 4.0 (document) · original module code: MIT
DOI: *(minted automatically by Zenodo on the v1.0.0 GitHub release)*

> **Status note:** release candidate — pending the author's final read-through before the v1.0.0 release is cut.

---

### Abstract

SLURRY is an open protocol for characterizing synthetic and suspect media. It does not produce verdicts. Given a media artifact and its required context — where it circulated, when, and what it claims — SLURRY runs an ensemble of independent modules across four measurement axes (biological signal, physical plausibility, contextual priors, and provenance) and reports findings, confidence, and inter-module disagreement, together with the evidentiary rules applied. Disagreement between modules is treated as information rather than noise. The protocol is aligned with the Berkeley Protocol on Digital Open Source Investigations: every artifact is hashed on intake, every analysis is logged by a registrar with tool versions and licenses, and every report separates observation from inference. SLURRY is designed for human-rights investigation, journalism, and research use; its modules are a mix of original instruments and audited open-source detectors, each carrying machine-readable license metadata that the protocol itself enforces against the analyst's declared intended use.

---

## 1. The problem: verdicts fail

The dominant form of synthetic-media detection is a score that collapses into a verdict — real or fake, human or AI. This form fails its users in four documented ways.

First, verdicts age silently. Detectors are trained against the generators of their training era; a February 2026 benchmark of sixteen detection methods found an average accuracy of 21% on images from a then-current generator, even as those same tools reported high accuracy on the generators of 2020. The user of a verdict has no way to see which era of the arms race their answer came from.

Second, verdicts fail in the wild. By the time suspect media reaches an analyst it has usually been recompressed, screenshotted, or re-encoded by platforms — and heavy compression degrades every pixel-level detector while also stripping the sensor traces that make real footage look real. Independent tests of deployed tools repeatedly show verdicts flipping on in-the-wild copies of confirmed fakes.

Third, verdicts injure. When a major newsletter platform deployed an accurate commercial AI-text detector in 2026, the immediate result was writers publicly defending their reputations against "an opaque metric" — a verdict with no inspectable reasoning, no account of mixed human-AI process, and no avenue of contest.

Fourth — and most fundamentally — a verdict answers the wrong question. In August 2026 a national newspaper's technology reviewer tested AI-image detectors against what he believed was an AI-generated photo of a San Francisco street sign; the detectors "failed" to flag it. A correction followed: the image was a real photograph of a physically staged hoax sign. The detectors were right; the *question* was wrong. Authentic media deployed under a false claim — the most common form of misleading content — is invisible to any instrument that only asks "was this made by AI?" The meaningful question is what an artifact *is* and what it *does* in an information environment, and that question cannot be answered from pixels alone.

SLURRY is a protocol built for the meaningful question.

## 2. Origins and philosophy

The name comes from wastewater treatment. A treatment plant does not extract contaminants with a single filter; it runs the stream through *stages* — screening, grit removal, settling, aeration, clarification — each binding a different class of material, with clean water emerging from the whole train rather than from any single step. An early version of this project took the metaphor literally (build a corpus of slop and let like bind to like); that proved intractable, but the metaphor matured with the method. The current architecture *is* a treatment train: a registrar, a rule set, and a sequence of specialized modules, each binding a different class of contaminant, with a finding that emerges from the ensemble. The retained insight: fight like with like — use the material's own properties against it.

The second commitment comes from remote sensing, the author's home field. The human eye is one narrow band; instruments read across the spectrum, and what the eye cannot access is precisely where the information lives. Expert visual inspection of synthetic media is now failing publicly — leading forensic experts have said on the record that they no longer trust their own eyes. SLURRY's response is to *sense rather than look*: noise statistics, color mathematics, frequency content, cardiac-band signal, attention dynamics — bands the eye was never built to access. And as synthesis grows more perfect, the visible artifacts vanish first; the protocol's instruments descend to lower and lower bands of the signal. The more perfect it looks, the deeper you go.

Two metaphors, one argument: audit the method, not the expert.

## 3. The protocol in one view

SLURRY accepts a media artifact **plus required context** — the intake refuses context-free submissions by design — and produces a **characterization**: findings, confidence, and disagreement, under named evidentiary rules, with a complete custody and analysis log. The pipeline:

**INTAKE** (context + media; hash on entry) → **PROTOCOL** (context selects the rule set; license gate filters eligible modules) → **MODULES** (the ensemble runs; each module returns a weak signal with its own confidence) → **REGISTRAR** (logs everything, threaded through every step) → **REPORT** (findings · confidence · disagreement · rules applied).

Three properties distinguish this from every deployed detection tool the author has audited:

1. **Characterization, not verdict.** Modules are individually fallible weak signals; false positives are expected (conflict-zone footage sheds its sensor signatures; heavily recompressed real video looks render-clean). Reliability is emergent from the ensemble and is *surfaced through disagreement*. Disagreement is not resolved away — it is reported, because a detector trained on 2020 generators disagreeing with one trained on 2025 generators is itself evidence about the artifact.
2. **Context is data, not decoration.** The intake's context fields do two jobs: they select the governing rule set (a report destined for a newsroom, an NGO, or a court operates under different evidentiary standards), and they feed the context-axis modules directly as analysis input. The claim field determines what "fake" would even mean for the artifact — routing a false-caption case toward circulation analysis rather than futile pixel forensics.
3. **Custody as architecture.** The registrar is not an audit afterthought; it is a parallel channel from intake to report. Analysis says what we think; custody proves how we know and that nothing was touched.

## 4. Architecture

**4.1 The Intake.** Structured entry of the artifact and its context: platform of origin, date first seen, sharing chain, the claim being made, subject and event, case, jurisdiction, and intended use. The file is hashed and timestamped on entry; the original is preserved untouched. Required context is a designed friction: it filters out the oracle use-pattern that produces uninterpretable verdicts, and it is the protocol's implementation of the Berkeley Protocol's source-analysis leg. Context also conditions interpretation mechanically — platform identity implies compression history, which determines which signal modules deserve weight, and the report says so.

**4.2 The Protocol layer (the rule set).** Two sequential functions. It **filters**: every module carries structured, machine-readable license metadata, and the declared intended use gates which modules are eligible (a non-commercial-licensed detector is available to a human-rights investigation and withheld from commercial deployment; the gate records both the inclusion and the exclusion). Then it **orchestrates** the surviving modules under the rule set the context selected. License is thus both a front-door gating condition and a back-door registrar record.

**4.3 The Modules.** Two provenances, two orientations. *Native modules* are original instruments built within the protocol; *adopted modules* are audited open-source research detectors, containerized with their upstream licenses intact. *Signal modules* read the artifact (the technical-analysis leg); *context modules* read the world around it (the source- and content-analysis legs). Every module ships with a **provenance card**: paper, method, training-data era, license, code status, and known limitations. Surfacing the training era is a protocol principle, not a courtesy — the age of a detector's worldview is part of the finding.

**4.4 The Registrar.** Logs six things per artifact: hash on intake; module set; module versions; license per module; the ordered sequence of analyses; and intermediate results. The registrar's log is exportable and is what makes a report defensible after the fact.

**4.5 The Reports.** Two product classes. The **Case Report** is the per-artifact evidentiary memo: context as entered, preservation record, every module's result beside its provenance card, the disagreement matrix, observations separated from inferences, explicit flags for human judgment, and the rules applied. The **Corpus Study** is the aggregate research product: many artifacts through the same engine to study patterns — disagreement structures, circulation dynamics, the temporal relationship between platform attention and synthetic amplification. A byproduct of both is the registrar's audit trail.

## 5. The module system

**5.1 Native modules (six).** *Biosignal* — Eulerian video magnification of cardiac-band signal; an independent reimplementation of the published method (audited; original expression), with the analysis emphasis on *spatial* pulse coherence in light of 2025 findings that face-swaps inherit their source's global heartbeat. *Camera Physics* — does the artifact obey real optics: noise floor, chromatic aberration, color-channel statistics, spectral falloff. *Composite Detection* — a seam-finder: video presenting as one continuous take that is actually spliced, with localization. *Trend* — a context razor scoring the conjunction of semantic resemblance to a recently peaked topic and temporal proximity to that peak; operationalizes the protocol's central testable hypothesis, that high-attention topics attract synthetic amplification within 24–72 hours. *Platform Propensity* — a time-indexed prior over platforms with separate propensity and spreadability dimensions. *Game Engine Detector* — identifies real-time-rendered footage (a third category: fully synthetic yet not generative-AI), motivated by the documented, recurring laundering of war-game footage into conflict misinformation; version 1 targets the shortcut artifacts real-time rendering cannot avoid. Each native module has a methodology paper in a fixed six-section house format whose final section is always *known limitations*.

**5.2 Adopted modules.** An audited starting ensemble, chosen for *diversity of detection philosophy* — foundation-model feature alignment, generator-diversity training, and spectral learning for images; manipulation localization with inspectable heatmaps; vocoder-artifact analysis for audio; audio-visual synchrony for video — because disagreement between methods that share a philosophy is redundancy, while disagreement between methods that do not is evidence. All primary adopted modules carry permissive licenses; stronger non-commercially-licensed instruments are integrated *behind the license gate* for eligible uses. The full audited shortlist, with licenses and repositories, is published alongside this document.

**5.3 What the protocol deliberately lacks.** No text-authorship detection (the capable tools are closed and verdict-shaped; the open lane is acknowledged as unoccupied). No aesthetic-quality judgment. No harm assessment — SLURRY characterizes artifacts, and hands its characterizations to frameworks that assess impact.

## 6. Relation to existing work

**Aggregation platforms** (the University at Buffalo's DeepFake-o-Meter, 37 models at audit) established the ensemble-of-open-detectors pattern and the honest presentation of multiple scores; SLURRY adds required context, rule-set selection, license gating, custody architecture, and disagreement-as-finding. **Commercial verification services** (image- and text-focused) demonstrate both the power of per-generator specialization and the costs of verdict form and closed method; SLURRY is their open, auditable, contestable counterpart. **The characterization turn in research** — most visibly the Columbia IGP convening report (2026), which declined to define slop and instead proposed analytic dimensions of *quality, scale, intent, deception, harm, and context/consent* — names the intellectual need this protocol answers: SLURRY is, to the author's knowledge, the first instrument that operationalizes such dimensions into per-artifact measurement. Its axes map onto the IGP dimensions directly (context/consent → intake; scale → corpus studies; deception → claim-aware routing; intent → context priors), and its gaps (harm, quality) are complementary rather than competitive. **The digital-methods tradition** (the Digital Methods Initiative, Amsterdam — within which this project's evidentiary-slop fieldwork was conducted, and whose 2026 summer school took slop as its theme) contributes the protocol's research sensibility: platforms as instruments, circulation as evidence, and the sprint as a working form. SLURRY's cousin SPLAT, developed in parallel at DMI 2026, heads toward forensic attribution; SLURRY is explicitly non-forensic, and the two remain separate by design.

## 7. The guiding documents

SLURRY is built *on* documents as much as on code. The founding-documents layer is not a bibliography; it is the load-bearing stratum of the architecture — the system diagram draws it as the bedrock beneath the processing chain, and the rule sets the protocol applies are derived from it. Four external standards, one internal cornerstone, and a distinct legal companion layer.

**7.1 External methodological standards.** Each contributes something specific and traceable to the architecture:

- **The Berkeley Protocol on Digital Open Source Investigations** (OHCHR & UC Berkeley Human Rights Center, 2020) is the primary foundation. Its three-legged verification framework maps directly onto the architecture — source analysis → the intake's context fields; technical analysis → the signal modules; content analysis → the claim-aware context modules — and its professional standards (documentation of method, minimization of bias, separation of observation from inference, chain of custody) are implemented by the registrar and the Case Report format rather than merely cited. SLURRY is **aligned with** the Berkeley Protocol, not "compliant with" it: compliance is a property of investigations and investigators, never of software.
- **The Leiden Guidelines on the Use of Digitally Derived Evidence** (2021) speak to where a characterization may ultimately travel: international criminal proceedings. They shape the Case Report's evidentiary form — preservation records, authentication trail, reproducibility from the registrar's log — so that a report generated for documentation does not have to be reconstructed if it is later needed as an annex.
- **The Verification Handbook for Disinformation and Media Manipulation** (ed. Silverman, 2020) carries the journalistic verification craft: the discipline of asking who published a thing, where it first appeared, and what it claims before asking what its pixels contain. The intake's required fields are this tradition rendered as a form, and the claim field's routing role descends from it.
- **The Amsterdam Matrix** (Torres et al.) contributes the contextual parameter set — twenty-three parameters in four families for situating an artifact in its investigative context. It is the leading candidate structure for the intake's context schema, and it carries the protocol's digital-methods lineage into the founding layer.

**7.2 The internal cornerstone.** *SLURRY: Origins and Philosophy* (§2 of this document is its summary) sits in the founding layer but is not an external standard: it records why the system is shaped the way it is — the treatment-train architecture, the remote-sensing commitment — so that future maintainers inherit reasons, not just structure.

**7.3 The legal companion layer.** The methodological documents above govern *how* investigation is conducted; a separate layer concerns *what the evidence ultimately serves* — the causes of action where characterized media may matter. These are deliberately kept out of the methodological block because they answer a different question and change on a different clock: following the U.S. Supreme Court's 2026 decision in *Cisco v. Doe*, which closed the Alien Tort Statute to new claims, this layer centers on the Torture Victim Protection Act, the trafficking statutes' civil provisions, and related accountability instruments. The layer is under development; its role in the protocol is already fixed, however — the intake's *jurisdiction* and *intended use* fields select rule sets whose evidentiary strictness derives from the frameworks the work may feed.

**7.4 A commitment that belongs here rather than in a footnote.** Sensitive material must be analyzable **locally**. Human-rights media can depict identifiable survivors, witnesses, and perpetrators; a protocol aligned with the documents above cannot require such material to transit third-party APIs. The reference implementation is self-hostable end to end.

## 8. Limitations and open problems

Stated in the same register the module papers use. The ensemble's thresholds are priors, not calibrations; a paired real/synthetic corpus reflecting *platform-degraded* conditions is the protocol's largest empirical need. The integration rubric that combines axes is a weighted evidence framework, not a probability model, and is presented as such. The subject-prior axis is deliberately unstaffed. Offline-rendered engine footage, humanized text, and aesthetic slop remain hard or out of scope. Detector staleness is mitigated by transparency (provenance cards) rather than solved. And the protocol's most distinctive claims — that disagreement structure is diagnostic, and that attention precedes synthetic amplification by 24–72 hours — are testable hypotheses that the Corpus Study product exists to test.

## 9. Versioning, citation, governance

This document is the canonical statement of the protocol; the author maintains the versioned record on GitHub, with each release archived on Zenodo under a version DOI and a concept DOI covering all versions. The document and templates are CC BY 4.0; original module code is MIT; adopted modules retain their upstream licenses, enforced by the protocol's license gate. The work is published under the author's personal authorship and the \<verify\> imprint; institutional collaborations will be named in future versions as agreements are established.

**Cite as:** Nealon, J. (2026). *SLURRY: A Protocol for the Multi-Axis Characterization of Synthetic and Suspect Media* (v1.0.0). \<verify\>. DOI: assigned at release (see repository CITATION.cff).

### Acknowledgments
This protocol grew out of fieldwork with the "OSINT and Evidentiary Slop" group at the Digital Methods Initiative Summer School 2026, University of Amsterdam, whose collective work first demonstrated the evidentiary-slop problem this protocol addresses. *(Author to review and extend before release.)*

### References
*(Verified citations from the project's verification memo and module papers — full reference list to be attached from those documents at deposit: Wu et al. 2012 (EVM); Lukáš, Fridrich & Goljan 2006 (PRNU); Yang, Liu & Salvi 2020 (TAA survey); the Berkeley Protocol (2020/2022); Leiden Guidelines (2021); Silverman, ed., Verification Handbook (2020); Weedon, François & Ponak, IGP report (2026); Fraunhofer HHI heartbeat findings (2025); the February 2026 cross-generator benchmark; platform-propensity sources per its memo.)*
