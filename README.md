# slurry
slurry is a system for the slopiverse


SLURRY 1.0
Synthetic Likelihood Using Residual and Real-world Yield
A Multi-Axis Epistemic Risk Protocol for Synthetic Media Environments

Jon Nealon — Documentary filmmaker, investigative journalist, MS GIS candidate, University at Albany


The Central Claim
Existing deepfake detection frameworks produce binary verdicts on individual artifacts — real or fake, pass or fail. SLURRY rejects this forensic paradigm.

Slop is not an artifact property. It is an ecological condition.

Content that contaminates epistemic environments regardless of how it was produced. The question is not "was this made by AI?" but "what does this content do to an information environment, and what does it carry ideologically?"

The wastewater treatment metaphor is generative: wastewater treatment doesn't ask whether a contaminant is natural or synthetic. It asks what it carries, what it does to the system it enters, and what remains after processing. SLURRY applies this logic to synthetic media — characterizing content by what it carries and what it does, not where it came from.


Four Measurement Axes
Axis 1 — Biological Signal
Eulerian Video Magnification (EVM) / rPPG

Detects periodic color variation in the heartbeat frequency band (0.83–2.5 Hz). Real human faces encode cardiac signal in pixel structure — blood moving through capillary beds produces subtle, spatially coherent color oscillation.

Key metric: spatial mean heartbeat-band power — more robust than aggregate SNR, which can be fooled by noise peaks. A real face shows high spatial mean power concentrated in anatomically expected regions. Fully synthetic video shows near-absent spatial power.

Empirical finding (June 24, 2026): Face-swap deepfakes inherit the cardiac pulse of the source actor — 2.9× separation in spatial mean power between real video and fully synthetic (D-ID) video.
Axis 2 — Physical Plausibility
Spectral & Sensor Forensics

Real cameras leave measurable physical traces: PRNU sensor noise, chromatic lens aberration, Bayer filter color channel statistics, characteristic frequency spectra. AI-generated content approximates the appearance of these traces but is not constrained by optics or physics.

Four sub-probes:

PRNU noise residual (structured spatial correlation)
2D FFT fingerprinting (GAN/diffusion grid artifacts)
Chromatic aberration analysis (lens physics)
Bayer color channel statistics (sensor physics)
Axis 3 — Subject Prior
Taxonomy + Dynamic Trend Signal

Some subjects systematically attract synthetic manipulation because of their epistemic utility — capacity to polarize, suppress, incite, or manufacture consent. A scored 20-category taxonomy encodes:

Base prior: documented manipulation rate by category
Emotional arousal: intensity of audience response
Political valence: ideological loading
Vessel risk: probability content is used as an emotional carrier for ideological payload

Critical insight: cute/wholesome content has low base prior but high vessel risk — it lowers epistemic guard and smuggles ideological payload. The Springfield pets case (AI-generated images of immigrants eating pets, amplified in a presidential debate) is the paradigm case.

Dynamic trend amplifier: live feed from Google Trends, Reddit, and Wikipedia pageview velocity modulates the static prior. What trends on platforms today is the raw material the sloposphere synthesizes tomorrow — trending data is a leading indicator of where synthetic manipulation will concentrate next.
Axis 4 — Context Signals
Platform, Account, Timing, Virality

Platform risk (Telegram > X > Facebook > YouTube)
Account age (new accounts = elevated risk)
Post velocity (bot-like behavior)
First-hour virality (coordinated amplification signature)
Election proximity (0–60 day window = elevated risk)


The Equation
P(slop | content) = f [ P(slop | signal) × P(slop | subject) × P(slop | context) ]

Composite score weighted by evidence strength. Not a binary verdict — a characterization profile.

The composite is Bayesian-flavored: when evidence is weak or unavailable for an axis, the score weights toward the base rate rather than making a strong claim. Each axis contributes independently; the composite is more robust than any single probe.


Empirical Findings — June 24, 2026
First real-world test run on three video types:

Video Type
SNR
Spatial Mean Power
Spatial Pattern
Real (FaceForensics++)
0.1188 @ 60 BPM
0.1952
Coherent, anatomical
Face-swap deepfake (FF++)
0.1140 @ 60 BPM
0.1990
Similar, slightly diffuse
D-ID fully synthetic
0.1916* @ 89 BPM
0.0670
Absent — near-black map


* Noise peak, not biological signal — spectral shape is diffuse with no harmonic structure

Finding 1: Face-swap deepfakes inherit the biological cardiac signal of the source actor. The face is replaced; the pulse is not. Single-axis rPPG detection cannot distinguish face-swap deepfakes from real video.

Finding 2: Spatial coherence of biological signal differs between real and face-swap video even when aggregate amplitude is similar — the deepfake shows slightly more diffuse spatial distribution, suggesting the inherited signal lacks the precise vascular anatomy of the source.

Finding 3: Fully synthetic video (D-ID talking head) shows 2.9× separation in spatial mean heartbeat-band power from real video. The spatial heatmap is near-black — effectively absent biological signal.

Key methodological insight: Aggregate SNR is unreliable as a standalone discriminator. The D-ID video returned higher SNR (0.1916) than the real video (0.1188) due to a noise peak — but the spatial map immediately revealed the absence of structured biological signal. Spatial mean heartbeat-band power is the robust discriminator.


The Forensic Distinction
Forensic Paradigm (Farid et al.)
SLURRY
Works on slop artifact by artifact
Works through slop at population level
Binary real/fake verdict
Epistemic risk characterization profile
Reactive — detects after circulation
Anticipatory — trend signal as leading indicator
Fails to generalize across generators
Defined by function, not production method
Does not ask what content does or carries
Asks what content does and what it carries



Applications
Journalism & OSINT verification: Documented, reproducible methodology for conflict zone imagery and political content verification. Defensible in ways that "I looked at it and it seemed fake" is not.

Legal proceedings: Multi-axis probabilistic characterization suitable for expert evidence. Courts respond better to probabilistic characterization than binary claims — more defensible under cross-examination. Relevant to Take It Down Act enforcement, DEFIANCE Act civil litigation, and state electoral deepfake laws.

Platform compliance: Take It Down Act requires platforms to remove NCII within 48 hours of a valid request. SLURRY provides automated first-pass verification distinguishing genuine NCII from bad-faith takedown attempts.

Insurance underwriting: Deepfake fraud claims require verifiable authentication methodology. SLURRY's open, documented protocol satisfies the "reasonable governance" standard emerging in deepfake insurance coverage.

Election integrity: 46 US states have enacted deepfake legislation; EU AI Act Article 50 takes effect August 2026. SLURRY provides characterization infrastructure for enforcement.


Repository Structure
slurry/

├── README.md                          # This file

├── SLURRY_1_0_Framework.pdf           # One-page framework statement

├── preprint/

│   └── SLURRY_preprint_v1.pdf        # Full theoretical paper

├── notebook/

│   └── EVM_Slop_Detector.ipynb       # Full four-axis Colab notebook

├── data/

│   ├── gmf_catalog/                  # GMF Spitting Images documented cases

│   │   ├── gmf_spitting_images.json

│   │   └── slurry_intake_queue.json

│   └── README_data.md               # Data sources and access instructions

├── findings/

│   └── SLURRY_Preliminary_Findings_v3.pdf   # June 24 2026 test results

└── LICENSE                           # MIT License


Getting Started
Run in Google Colab (recommended)
Open colab.research.google.com
Upload notebook/EVM_Slop_Detector.ipynb
Run cells top to bottom — setup cells install all dependencies
Upload your test videos when prompted (Step 5)
Results include power spectrum, spatial heatmap, and composite SLURRY score
Requirements (local)
pip install opencv-python-headless scipy numpy matplotlib \

            trendspyg praw wikipedia-api requests pandas seaborn
Minimum video requirements
Format: MP4, AVI, MOV
Duration: 10+ seconds
Frame rate: 15+ fps
Content: frontal face, relatively stable framing
Resolution: 320×240 minimum (720p preferred)


Data Sources
Dataset
Access
Use in SLURRY
FaceForensics++
Free, Kaggle
Axis 1 calibration — face-swap pairs
DeepFakeFace
Free, HuggingFace
Axis 2 calibration — diffusion images
Deepfake-Eval-2024
Free, sign ToS
In-the-wild validation
WildDeepfake
Free, email request
Real-world deepfake pairs
GMF Spitting Images
Open
Political slop with epistemic context
TrueMedia.org
Free account
Current political slop



Citation
If you use SLURRY in your research, please cite:

@misc{nealon2026slurry,

  title={SLURRY: A Multi-Axis Epistemic Risk Protocol for Synthetic Media Environments},

  author={Nealon, Jon},

  year={2026},

  note={Preprint. GitHub: https://github.com/[your-handle]/slurry},

  institution={University at Albany, SUNY}

}


License
MIT License. The core protocol, notebook, and taxonomy are freely available for research, journalism, and public interest use.

Commercial applications (insurance underwriting, legal proceedings, platform compliance) are welcome — attribution required.


Contact
Jon Nealon [jnealon@gmail.com] University at Albany, MS GIS DMI Affiliated Scholar (pending) — Digital Methods Initiative, University of Amsterdam

SLURRY was developed in preparation for the DMI Summer School 2026, University of Amsterdam, theme: "Visual AI for internet research: On and beyond slop."


Acknowledgments
Theoretical foundation: Richard Rogers' digital methods tradition and the DMI Summer School 2026 theme. EVM methodology: Wu et al. SIGGRAPH 2012; Davis et al. SIGGRAPH 2014. rPPG detection context: Ciftci et al. FakeCatcher (IEEE TPAMI 2020). Political slop catalog: German Marshall Fund Spitting Images tracker. Deepfake-Eval-2024: TrueMedia.org and Camp.org.

