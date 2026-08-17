"""
SLURRY — Game Engine Detector, v1 (regime 1: real-time capture)
================================================================
Physical-plausibility axis. Identifies footage produced by a real-time
rendering engine (Unreal, Unity, etc.) by hunting the shortcut artifacts
an engine cannot avoid under frame-rate pressure.

Sub-detectors (per methodology paper §3):
  1. camera_motion      — impossibly smooth virtual-camera motion (spline vs. hand)
  2. taa_shimmer        — temporal anti-aliasing shimmer / edge flicker
  3. ssao_halo          — screen-space ambient-occlusion fringes at object edges
  4. lod_popping        — discrete detail jumps uncorrelated with motion
  5. ssr_dropout        — STUB in v1 (documented gap; needs reflection semantics)
Regime 2 (offline render) is a deliberate low-confidence murmur:
  6. noise_floor        — absence of sensor noise in flat regions

Output (fourfold, per spec): engine_probability 0-1, regime label,
confidence 0-1, itemized tells. A weak signal for the ensemble — never a verdict.

License: MIT (c) 2026 Jon Nealon / <verify>. Original work, no upstream code.
"""

from __future__ import annotations
import numpy as np
import cv2
from dataclasses import dataclass, field, asdict


# ----------------------------------------------------------------------
# Video I/O
# ----------------------------------------------------------------------

def load_video(path: str, max_frames: int = 300, max_side: int = 640):
    """Load frames as float32 grayscale + color, downscaled for speed.
    Returns (gray[T,H,W] in 0..1, color[T,H,W,3] uint8, fps)."""
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise IOError(f"cannot open {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    grays, colors = [], []
    while len(grays) < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        h, w = frame.shape[:2]
        s = max_side / max(h, w)
        if s < 1.0:
            frame = cv2.resize(frame, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
        colors.append(frame)
        grays.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0)
    cap.release()
    if len(grays) < 12:
        raise ValueError(f"too few frames ({len(grays)}) — need >= 12")
    return np.stack(grays), np.stack(colors), float(fps)


# ----------------------------------------------------------------------
# Sub-detector 1 — camera-motion smoothness
# A handheld or rig-mounted physical camera carries tremor (~2-12 Hz) and
# jerk irregularity. A virtual camera on a spline (or mouse-flick aim) is
# either unnaturally smooth or shows discontinuous snaps with zero tremor.
# ----------------------------------------------------------------------

def global_motion_track(gray: np.ndarray) -> np.ndarray:
    """Per-frame global translation via phase correlation. Returns [T-1, 2]."""
    T = gray.shape[0]
    win = cv2.createHanningWindow((gray.shape[2], gray.shape[1]), cv2.CV_32F)
    shifts = []
    for t in range(T - 1):
        # NB: cv2.phaseCorrelate applies the window to its inputs IN PLACE —
        # pass copies or every downstream detector sees corrupted frames.
        (dx, dy), _ = cv2.phaseCorrelate(gray[t].copy(), gray[t + 1].copy(), win)
        shifts.append((dx, dy))
    return np.array(shifts, dtype=np.float32)


def camera_motion_score(gray: np.ndarray, fps: float) -> dict:
    sh = global_motion_track(gray)
    mag = np.linalg.norm(sh, axis=1)
    moving = mag > 0.05                       # frames with real camera motion
    frac_moving = float(moving.mean())
    if frac_moving < 0.15:
        # static shot: motion analysis uninformative
        return {"score": 0.0, "confidence": 0.2, "detail": "camera mostly static — motion tell uninformative",
                "tremor_power": None, "smoothness": None}
    sig = sh - sh.mean(axis=0, keepdims=True)
    n = sig.shape[0]
    # windowed spectra (nonstationary motion: pans, stops, snaps) — median across
    # windows resists leakage from pan/stop transitions
    win_len = max(24, int(2 * fps))
    tremors, jitters = [], []
    for w0 in range(0, max(1, n - win_len + 1), win_len // 2):
        seg = sig[w0:w0 + win_len]
        if seg.shape[0] < 16:
            continue
        seg = seg - seg.mean(axis=0, keepdims=True)
        hann = np.hanning(seg.shape[0])[:, None]
        freqs = np.fft.rfftfreq(seg.shape[0], d=1.0 / fps)
        spec = np.abs(np.fft.rfft(seg * hann, axis=0)).sum(axis=1)
        total = spec[1:].sum() + 1e-9
        hand_band = (freqs >= 2.0) & (freqs <= min(8.0, 0.35 * fps))
        nyq_band = freqs >= 0.45 * fps
        tremors.append(spec[hand_band].sum() / total)
        jitters.append(spec[nyq_band].sum() / total)
    tremor = float(np.median(tremors)) if tremors else 0.5   # hands: substantial; splines: tiny
    taa_jitter = float(np.max(jitters)) if jitters else 0.0  # frame-alternating jitter: engine cue
    # smoothness: normalized jerk of the LOW-PASSED trajectory (ignore alternation)
    if n >= 8:
        k = max(3, int(fps / 8) | 1)
        kern = np.ones(k, np.float32) / k
        lp = np.stack([np.convolve(sig[:, i], kern, mode="valid") for i in range(2)], axis=1)
        jerk = np.diff(lp, n=2, axis=0)
        smooth = float(1.0 / (1.0 + (np.linalg.norm(jerk, axis=1).mean() / (mag.mean() + 1e-6))))
    else:
        smooth = 0.5
    # engine-like = (low hand-tremor AND smooth) OR strong frame-alternating jitter
    spline_like = np.clip((0.12 - tremor) / 0.12, 0, 1) * np.clip((smooth - 0.6) / 0.35, 0, 1)
    score = float(np.clip(max(spline_like, np.clip((taa_jitter - 0.35) / 0.4, 0, 1)), 0, 1))
    conf = float(np.clip(frac_moving * 1.5, 0.3, 0.9))
    return {"score": score, "confidence": conf,
            "detail": f"hand_tremor={tremor:.3f}, nyquist_jitter={taa_jitter:.3f}, smoothness={smooth:.3f}, moving_frac={frac_moving:.2f}",
            "tremor_power": tremor, "smoothness": smooth}


# ----------------------------------------------------------------------
# Sub-detector 2 — TAA shimmer / edge flicker
# TAA under motion produces sub-pixel sign-alternating luminance jitter
# concentrated on fine, high-contrast edges. Optical capture does not:
# its edge noise is broadband sensor noise, spatially unstructured.
# We measure: fraction of edge pixels whose temporal difference series
# alternates sign at a rate far above the noise expectation.
# ----------------------------------------------------------------------

def taa_shimmer_score(gray: np.ndarray, shifts: np.ndarray = None, win_len: int = 40) -> dict:
    """Detrended temporal alternation on edges, windowed.
    TAA jitter/shimmer is deterministic and frame-alternating: the SECOND
    temporal difference of an affected pixel flips sign nearly every frame
    (alternation -> 1.0). Sensor noise is stochastic (~0.73 by MA(2)
    statistics, lower after compression). Camera pan is a trend, removed by
    the second difference. Windowing keeps mixed pan/hold clips readable:
    the tell is scored per window and the strongest window wins.
    """
    T = gray.shape[0]
    best = {"edge": 0.0, "flat": 0.0, "ratio": 0.0, "npx": 0}
    for w0 in range(0, max(1, T - win_len + 1), max(1, win_len // 2)):
        g = gray[w0:w0 + win_len]
        if g.shape[0] < 16:
            continue
        d2 = np.diff(g, n=2, axis=0)
        s2 = np.sign(d2)
        alt = (s2[:-1] * s2[1:] < 0).mean(axis=0)
        med = np.median(g, axis=0)
        edges = cv2.Sobel(med, cv2.CV_32F, 1, 0) ** 2 + cv2.Sobel(med, cv2.CV_32F, 0, 1) ** 2
        edge_mask = edges > np.percentile(edges, 90)
        flat_mask = edges <= np.percentile(edges, 50)
        amp = np.abs(d2).mean(axis=0)
        amp_gate = amp > np.median(amp[flat_mask]) * 2.0 + 1e-4
        npx = int((edge_mask & amp_gate).sum())
        if npx < 50 or flat_mask.sum() < 50:
            continue
        e = float((alt[edge_mask & amp_gate] > 0.9).mean())
        f = float((alt[flat_mask] > 0.9).mean())
        if e > best["edge"]:
            best = {"edge": e, "flat": f, "ratio": e / (f + 1e-3), "npx": npx}
    score = float(np.clip((best["edge"] - 0.04) / 0.20, 0, 1) *
                  np.clip((best["ratio"] - 2.0) / 6.0, 0, 1))
    conf = float(np.clip(best["npx"] / 2000.0, 0.3, 0.85))
    return {"score": score, "confidence": conf,
            "detail": (f"edge_alt90={best['edge']:.3f}, flat_alt90={best['flat']:.3f}, "
                       f"ratio={best['ratio']:.2f}, gated_edge_px={best['npx']} (best window)")}


# ----------------------------------------------------------------------
# Sub-detector 3 — SSAO halo fringes
# Screen-space AO produces a thin uniform dark band hugging object edges.
# Real contact shadows are irregular and scene-dependent. We measure the
# systematic darkening of the 2-6 px band around strong edges relative to
# the 8-16 px band, aggregated over frames. Uniformity across the whole
# image is the tell — real shadows are not everywhere.
# ----------------------------------------------------------------------

def ssao_halo_score(gray: np.ndarray, sample: int = 12) -> dict:
    # prefer low-motion frames: halos are crisp when the camera rests
    d = np.abs(np.diff(gray, axis=0)).mean(axis=(1, 2))
    order = np.argsort(np.concatenate([[d[0]], d]))
    idx = order[:min(sample, gray.shape[0])]
    ratios = []
    for t in idx:
        f = gray[t]
        e = cv2.Canny((f * 255).astype(np.uint8), 60, 140) > 0
        if e.sum() < 200:
            continue
        near = cv2.dilate(e.astype(np.uint8), np.ones((5, 5), np.uint8), iterations=1).astype(bool) & ~e
        far_ring = cv2.dilate(e.astype(np.uint8), np.ones((13, 13), np.uint8), iterations=1).astype(bool)
        far = far_ring & ~cv2.dilate(e.astype(np.uint8), np.ones((9, 9), np.uint8), iterations=1).astype(bool)
        if near.sum() < 200 or far.sum() < 200:
            continue
        ratios.append(float(np.median(f[near]) / (np.median(f[far]) + 1e-6)))
    if not ratios:
        return {"score": 0.0, "confidence": 0.2, "detail": "insufficient edges for halo analysis"}
    r = float(np.mean(ratios))
    consistency = float(1.0 - np.std(ratios))
    # engine tell: near-band systematically darker (r < ~0.97) AND uniform across frames
    score = float(np.clip((0.985 - r) / 0.06, 0, 1) * np.clip((consistency - 0.9) / 0.1, 0, 1))
    return {"score": score, "confidence": 0.55,
            "detail": f"near/far luminance ratio={r:.3f}, frame_consistency={consistency:.3f}"}


# ----------------------------------------------------------------------
# Sub-detector 4 — LOD popping
# Level-of-detail swaps create step-changes in local sharpness that are
# not accompanied by proportional local motion. We track block-wise
# Laplacian variance over time and count discrete jumps in blocks whose
# content is otherwise static.
# ----------------------------------------------------------------------

def lod_popping_score(gray: np.ndarray, block: int = 40) -> dict:
    T, H, W = gray.shape
    bh, bw = H // block, W // block
    if bh < 2 or bw < 2:
        return {"score": 0.0, "confidence": 0.2, "detail": "frame too small for block analysis"}
    sharp = np.zeros((T, bh, bw), np.float32)
    motion = np.zeros((T - 1, bh, bw), np.float32)
    for t in range(T):
        lap = cv2.Laplacian(gray[t], cv2.CV_32F)
        for i in range(bh):
            for j in range(bw):
                sharp[t, i, j] = lap[i*block:(i+1)*block, j*block:(j+1)*block].var()
    d = np.abs(np.diff(gray, axis=0))
    for t in range(T - 1):
        for i in range(bh):
            for j in range(bw):
                motion[t, i, j] = d[t, i*block:(i+1)*block, j*block:(j+1)*block].mean()
    ds = np.abs(np.diff(sharp, axis=0))                       # sharpness jumps
    # z-score each jump against that block's own typical fluctuation (MAD),
    # so continuous sensor-noise jitter does not read as popping
    mad = np.median(ds, axis=0) + 1e-7
    z = ds / (1.4826 * mad[None])
    base = np.median(sharp, axis=0) + 1e-6
    static = motion < np.percentile(motion, 60)               # low-motion blocks
    pops = (z > 8.0) & static & (base[None] > np.percentile(base, 40))
    pop_events = int(pops.sum())
    pop_rate = float(pops.mean())
    score = float(np.clip(pop_events / 6.0, 0, 1))
    return {"score": score, "confidence": 0.5,
            "detail": f"pop_events={pop_events}, pop_rate={pop_rate:.5f} (z>8 sharpness steps in static blocks)"}


# ----------------------------------------------------------------------
# Sub-detector 5 — SSR dropout (STUB, v1)
# Detecting screen-space-reflection dropout requires identifying reflective
# surfaces and tracking their sources — semantic machinery out of v1 scope.
# Kept as an explicit documented gap so the ensemble knows it wasn't tested.
# ----------------------------------------------------------------------

def ssr_dropout_score(gray: np.ndarray) -> dict:
    return {"score": 0.0, "confidence": 0.0,
            "detail": "STUB — not implemented in v1 (needs reflection semantics); documented gap"}


# ----------------------------------------------------------------------
# Regime 2 murmur — sensor-noise floor (absence of reality's messiness)
# Real capture carries shot/read noise visible as high-frequency residual
# in flat regions. A clean render has (near) none, or synthetic grain that
# is spatially uniform. Low-confidence by design (heavy compression also
# strips noise — false-positive convergence, see limitations §5.3).
# ----------------------------------------------------------------------

def noise_floor_score(gray: np.ndarray, sample: int = 10) -> dict:
    idx = np.linspace(0, gray.shape[0] - 1, min(sample, gray.shape[0])).astype(int)
    noise_levels = []
    for t in idx:
        f = gray[t]
        hp = f - cv2.GaussianBlur(f, (0, 0), 1.2)
        grad = cv2.Sobel(f, cv2.CV_32F, 1, 0) ** 2 + cv2.Sobel(f, cv2.CV_32F, 0, 1) ** 2
        flat = grad <= np.percentile(grad, 30)
        if flat.sum() > 500:
            noise_levels.append(float(hp[flat].std()))
    if not noise_levels:
        return {"score": 0.0, "confidence": 0.1, "detail": "no flat regions found"}
    nl = float(np.mean(noise_levels))
    # typical real capture flat-region HP std (post-compression) >~ 0.004..0.02
    score = float(np.clip((0.0035 - nl) / 0.0030, 0, 1))
    return {"score": score, "confidence": 0.35,
            "detail": f"flat-region noise std={nl:.5f} (renders: near zero; cameras: higher)"}


# ----------------------------------------------------------------------
# Combiner — fourfold output
# ----------------------------------------------------------------------

WEIGHTS_R1 = {"camera_motion": 0.35, "taa_shimmer": 0.30, "ssao_halo": 0.15, "lod_popping": 0.20}

@dataclass
class GEDResult:
    engine_probability: float
    regime: str
    confidence: float
    tells: list = field(default_factory=list)
    sub_results: dict = field(default_factory=dict)
    module: str = "Game Engine Detector v1"
    axis: str = "physical-plausibility"
    note: str = ("Weak signal for the SLURRY ensemble — not a standalone verdict. "
                 "Disagreement with other modules is itself information.")
    def to_dict(self):
        return asdict(self)


def run_game_engine_detector(path: str, max_frames: int = 300) -> GEDResult:
    gray, _color, fps = load_video(path, max_frames=max_frames)
    shifts = global_motion_track(gray)
    subs = {
        "camera_motion": camera_motion_score(gray, fps),
        "taa_shimmer": taa_shimmer_score(gray, shifts=shifts),
        "ssao_halo": ssao_halo_score(gray),
        "lod_popping": lod_popping_score(gray),
        "ssr_dropout": ssr_dropout_score(gray),
        "noise_floor_r2": noise_floor_score(gray),
    }
    # regime-1 evidence: confidence-weighted mean of the implemented tells
    num = sum(WEIGHTS_R1[k] * subs[k]["score"] * subs[k]["confidence"] for k in WEIGHTS_R1)
    den = sum(WEIGHTS_R1[k] * subs[k]["confidence"] for k in WEIGHTS_R1) + 1e-9
    r1 = num / den
    r1_conf = den / sum(WEIGHTS_R1.values())
    r2 = subs["noise_floor_r2"]["score"] * subs["noise_floor_r2"]["confidence"]

    tells = [f"{k}: {v['detail']}" for k, v in subs.items() if v["score"] > 0.35 and v["confidence"] > 0.25]
    if r1 >= 0.45:
        regime, prob, conf = "real-time capture", float(0.5 + 0.5 * r1), float(np.clip(r1_conf, 0.3, 0.9))
    elif r2 >= 0.25:
        regime, prob, conf = "possible offline render (low confidence)", float(0.4 + 0.4 * r2), 0.25
        t2 = "noise_floor_r2: " + subs["noise_floor_r2"]["detail"]
        if t2 not in tells:
            tells.append(t2)
    else:
        regime, prob, conf = "no engine signal detected", float(0.25 * r1 + 0.15 * r2), float(np.clip(r1_conf * 0.8, 0.2, 0.7))
    return GEDResult(engine_probability=round(prob, 3), regime=regime,
                     confidence=round(conf, 3), tells=tells,
                     sub_results={k: {kk: vv for kk, vv in v.items() if kk in ("score", "confidence", "detail")}
                                  for k, v in subs.items()})
