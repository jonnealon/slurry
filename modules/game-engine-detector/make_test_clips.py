"""Synthetic sanity clips for the Game Engine Detector.
'engine.mp4'  — spline-smooth pan, zero sensor noise, TAA-like edge jitter,
                SSAO-like dark rims, one LOD pop event.
'camera.mp4'  — same scene, handheld tremor, per-frame sensor noise,
                no alternating edge jitter, no rims, no pops.
These are caricatures for unit-testing direction-of-effect, not benchmarks.
"""
import numpy as np, cv2

H, W, T, FPS = 360, 640, 240, 30.0
rng = np.random.default_rng(7)

def scene(pop=False):
    """Static world image, larger than the viewport for panning."""
    world = np.full((H + 200, W + 400), 0.55, np.float32)
    # buildings / blocks with strong edges
    boxes = [(60, 120, 300, 260, 0.25), (350, 60, 520, 300, 0.75), (600, 180, 760, 380, 0.35),
             (820, 90, 960, 320, 0.65), (150, 320, 700, 420, 0.45)]
    for x0, y0, x1, y1, v in boxes:
        world[y0:y1, x0:x1] = v
    # fine geometry: fence lines (aliasing-prone)
    for x in range(80, W + 380, 9):
        world[430:520, x:x+2] = 0.2
    if pop:
        pass
    return world

def ssao_rims(img):
    e = cv2.Canny((img * 255).astype(np.uint8), 60, 140) > 0
    near = cv2.dilate(e.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    out = img.copy()
    out[near & ~e] *= 0.75
    return out

def render(engine: bool, path: str):
    world = scene()
    vw = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"FFV1"), FPS, (W, H), isColor=False)
    vw.set(cv2.VIDEOWRITER_PROP_QUALITY, 96)
    # camera path: smooth spline for engine; tremor added for camera
    tt = np.clip(np.linspace(0, 1 / 0.6, T), 0, 1)       # pan for 60%, hold for 40%
    base_x = 40 + 300 * (3 * tt**2 - 2 * tt**3)          # smoothstep pan
    base_y = 60 + 30 * np.sin(2 * np.pi * tt * 0.5)
    if not engine:
        # handheld tremor: band-limited random walk, 2-12 Hz
        n = rng.standard_normal((T, 2))
        from scipy.signal import butter, filtfilt
        b, a = butter(2, [2 / (FPS/2), 12 / (FPS/2)], btype="band")
        trem = filtfilt(b, a, n, axis=0) * 2.2
        drift = np.cumsum(rng.standard_normal((T, 2)) * 0.25, axis=0)
        base_x = base_x + trem[:, 0] + drift[:, 0]
        base_y = base_y + trem[:, 1] + drift[:, 1]
    for t in range(T):
        w = world.copy()
        if engine and t == 150:                            # LOD pop: fence detail appears
            for x in range(80, W + 380, 9):
                w[430:520, x:x+4] = 0.15                   # thicker/sharper geometry
        if engine and t > 150:
            for x in range(80, W + 380, 9):
                w[430:520, x:x+4] = 0.15
        M = np.float32([[1, 0, -base_x[t]], [0, 1, -base_y[t]]])
        frame = cv2.warpAffine(w, M, (W, H), flags=cv2.INTER_LINEAR)
        if engine:
            frame = ssao_rims(frame)
            # TAA-like alternating sub-pixel edge jitter
            jit = 0.35 if t % 2 == 0 else -0.35
            Mj = np.float32([[1, 0, jit], [0, 1, 0]])
            frame = 0.5 * frame + 0.5 * cv2.warpAffine(frame, Mj, (W, H), flags=cv2.INTER_LINEAR)
        else:
            frame = frame + rng.standard_normal((H, W)).astype(np.float32) * 0.025  # sensor noise
        vw.write((np.clip(frame, 0, 1) * 255).astype(np.uint8))
    vw.release()
    print("wrote", path)

render(True, "/home/claude/work/ged/engine.avi")
render(False, "/home/claude/work/ged/camera.avi")
