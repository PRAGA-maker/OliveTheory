"""
Sensitivity test: Does TRIBE v2's audio pathway produce meaningfully
different predictions in escape-relevant brain regions for different
types of audio stimuli?

Generates synthetic stimuli, runs TRIBE v2 inference (audio-only),
extracts ROI activations, and tests discriminability.
"""

import multiprocessing
import pathlib
import sys
import os
import time

# Windows PosixPath fix
if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath

import numpy as np
import soundfile as sf
import torch


def main():
    # -------------------------------------------------------------------
    # 1. Generate synthetic stimuli
    # -------------------------------------------------------------------
    STIMULI_DIR = pathlib.Path("stimuli")
    STIMULI_DIR.mkdir(exist_ok=True)

    SR = 16000  # Wav2Vec-Bert expects 16kHz
    DURATION = 30  # seconds

    rng = np.random.default_rng(42)
    t = np.linspace(0, DURATION, SR * DURATION, endpoint=False)

    stimuli = {}

    # Silence
    stimuli["silence"] = np.zeros_like(t, dtype=np.float32)

    # White noise (arousing / aversive)
    stimuli["noise"] = (rng.standard_normal(len(t)) * 0.3).astype(np.float32)

    # Pure tone 440Hz (neutral auditory baseline)
    stimuli["tone_440hz"] = (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

    # Low calming drone (100Hz + 150Hz harmony)
    stimuli["calm_drone"] = (
        0.2 * np.sin(2 * np.pi * 100 * t) + 0.15 * np.sin(2 * np.pi * 150 * t)
    ).astype(np.float32)

    # Anxious pulsing noise (3Hz AM modulated noise)
    envelope = np.abs(np.sin(2 * np.pi * 3 * t))
    stimuli["anxious_pulse"] = (
        envelope * rng.standard_normal(len(t)) * 0.3
    ).astype(np.float32)

    # Slow warm chord (C major: 261, 329, 392 Hz with slow fade-in)
    fade = np.clip(t / 5.0, 0, 1)  # 5s fade-in
    stimuli["warm_chord"] = (
        fade
        * (
            0.15 * np.sin(2 * np.pi * 261.6 * t)
            + 0.12 * np.sin(2 * np.pi * 329.6 * t)
            + 0.10 * np.sin(2 * np.pi * 392.0 * t)
        )
    ).astype(np.float32)

    for name, audio in stimuli.items():
        sf.write(str(STIMULI_DIR / f"{name}.wav"), audio, SR)
    print(f"Generated {len(stimuli)} stimuli in {STIMULI_DIR}/")

    # -------------------------------------------------------------------
    # 2. Load TRIBE v2
    # -------------------------------------------------------------------
    from tribev2 import TribeModel
    from tribev2.demo_utils import get_audio_and_text_events
    import pandas as pd

    CKPT_DIR = "cache/models--facebook--tribev2/snapshots/f894e783020944dcd96e5568550afe2aa9743f9f"

    print(f"\nLoading TRIBE v2 from {CKPT_DIR}...")
    t0 = time.perf_counter()
    model = TribeModel.from_pretrained(CKPT_DIR, cache_folder="./cache")
    print(f"Loaded in {time.perf_counter() - t0:.1f}s")

    # -------------------------------------------------------------------
    # 3. Run inference on each stimulus (audio-only)
    # -------------------------------------------------------------------
    results = {}

    for name in stimuli:
        audio_path = str(STIMULI_DIR / f"{name}.wav")
        print(f"\nProcessing: {name}...")

        event = {
            "type": "Audio",
            "filepath": os.path.abspath(audio_path),
            "start": 0,
            "timeline": "default",
            "subject": "default",
        }
        try:
            events = get_audio_and_text_events(
                pd.DataFrame([event]), audio_only=True
            )
            t0 = time.perf_counter()
            preds, segments = model.predict(events, verbose=False)
            elapsed = time.perf_counter() - t0
            print(f"  Shape: {preds.shape}, {elapsed:.2f}s")
            results[name] = preds
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback

            traceback.print_exc()

    if not results:
        print("\nNo results! Pipeline failed.")
        sys.exit(1)

    # -------------------------------------------------------------------
    # 4. Analyze
    # -------------------------------------------------------------------
    from numpy.linalg import norm

    print("\n" + "=" * 70)
    print("  RESULTS: Global activation statistics")
    print("=" * 70)
    print(
        f"  {'Stimulus':<20} {'Mean':>10} {'Std':>10} "
        f"{'Min':>10} {'Max':>10} {'Shape':>15}"
    )
    print(f"  {'-'*20} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*15}")

    for name, preds in results.items():
        mean_pred = preds.mean(axis=0)
        print(
            f"  {name:<20} {mean_pred.mean():>10.4f} {mean_pred.std():>10.4f} "
            f"{mean_pred.min():>10.4f} {mean_pred.max():>10.4f} "
            f"{str(preds.shape):>15}"
        )

    # Pairwise cosine distances
    names = list(results.keys())
    mean_preds = {name: results[name].mean(axis=0) for name in names}

    print(f"\n{'='*70}")
    print("  Pairwise cosine distances between conditions")
    print(f"{'='*70}")

    header = f"  {'':>20}" + "".join(f"{n:>15}" for n in names)
    print(header)
    for n1 in names:
        row = f"  {n1:>20}"
        for n2 in names:
            v1, v2 = mean_preds[n1], mean_preds[n2]
            cos_sim = np.dot(v1, v2) / (norm(v1) * norm(v2) + 1e-8)
            row += f"{1 - cos_sim:>15.4f}"
        print(row)

    # Most discriminative vertices
    all_mean_preds = np.stack([mean_preds[n] for n in names])
    vertex_variance = all_mean_preds.var(axis=0)

    print(f"\n{'='*70}")
    print("  Top 20 discriminative vertices (highest cross-condition variance)")
    print(f"{'='*70}")

    top_idx = np.argsort(vertex_variance)[-20:][::-1]
    print(
        f"  {'Vertex':>8} {'Variance':>10}  "
        + "  ".join(f"{n:>12}" for n in names)
    )
    for idx in top_idx:
        vals = "  ".join(
            f"{all_mean_preds[i, idx]:>12.4f}" for i in range(len(names))
        )
        print(f"  {idx:>8} {vertex_variance[idx]:>10.6f}  {vals}")

    # Discriminability summary
    mean_inter_dist = 0
    count = 0
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            v1, v2 = mean_preds[names[i]], mean_preds[names[j]]
            mean_inter_dist += norm(v1 - v2)
            count += 1
    mean_inter_dist /= count

    mean_intra_var = np.mean([results[n].var(axis=0).mean() for n in names])

    print(f"\n{'='*70}")
    print("  DISCRIMINABILITY SUMMARY")
    print(f"{'='*70}")
    print(f"  Mean inter-condition L2 distance: {mean_inter_dist:.6f}")
    print(f"  Mean intra-condition variance:    {mean_intra_var:.6f}")
    ratio = mean_inter_dist / (mean_intra_var + 1e-8)
    print(f"  Ratio (signal/noise):             {ratio:.2f}")
    n_discriminative = (vertex_variance > 1e-6).sum()
    print(
        f"  Total vertices with var > 1e-6:   "
        f"{n_discriminative} / {len(vertex_variance)}"
    )

    # Save
    os.makedirs("outputs", exist_ok=True)
    np.savez(
        "outputs/sensitivity_test_results.npz",
        **{f"pred_{name}": preds for name, preds in results.items()},
        vertex_variance=vertex_variance,
        stimulus_names=np.array(names),
    )
    print(f"\nSaved to outputs/sensitivity_test_results.npz")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
