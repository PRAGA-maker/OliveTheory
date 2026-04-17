"""
Muller Temporal Dynamics Validation (Benchmark 1)

Tests whether TRIBE v2 predicted activation in fatigue-encoding regions
(cingulate, insula, MFG) shows temporal evolution consistent with
Muller 2021's fatigue accumulation model.

Prediction: Over a 5-minute audio sequence, predicted dACC/insula activation
should INCREASE over time (fatigue accumulation), and calming music should
show SLOWER increase than aversive music.
"""

import multiprocessing
import pathlib
import sys
import os
import time

if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath

import numpy as np
import soundfile as sf


def generate_5min_stimuli():
    """Generate 5-minute versions of calming and aversive audio."""
    SR = 16000
    DURATION = 300  # 5 minutes
    t = np.linspace(0, DURATION, SR * DURATION, endpoint=False)
    rng = np.random.default_rng(42)
    OUT = pathlib.Path("stimuli/temporal")
    OUT.mkdir(parents=True, exist_ok=True)

    def note_freq(midi):
        return 440.0 * 2 ** ((midi - 69) / 12)

    def synth_note(freq, t, harmonics=6, decay=0.3):
        signal = np.zeros_like(t)
        for h in range(1, harmonics + 1):
            signal += (1.0 / (h ** decay)) * np.sin(2 * np.pi * freq * h * t)
        return signal / harmonics

    # 1. CALMING: sustained Cmaj9 pad, very slow evolution
    freqs = [note_freq(n) for n in [48, 52, 55, 59, 62]]
    calming = np.zeros_like(t, dtype=np.float32)
    for f in freqs:
        calming += synth_note(f, t, harmonics=8, decay=0.5).astype(np.float32)
    env = np.clip(t / 5.0, 0, 1) * np.clip((DURATION - t) / 3.0, 0, 1)
    calming = (calming * env * 0.02).astype(np.float32)

    # 2. AVERSIVE: dissonant, irregular, escalating tension
    anx_freqs = [note_freq(n) for n in [48, 49, 54, 60, 61]]
    aversive = np.zeros_like(t, dtype=np.float32)
    for f in anx_freqs:
        aversive += synth_note(f, t, harmonics=6, decay=0.3).astype(np.float32)
    # Escalating amplitude modulation (gets more irregular over time)
    am_rate = 0.3 + 2.0 * (t / DURATION)  # AM frequency increases over time
    am = 0.5 + 0.5 * np.sin(2 * np.pi * am_rate * t)
    aversive = (aversive * am * env * 0.02).astype(np.float32)

    # 3. HOLD MUSIC: repeating pleasant loop, constant over time
    chords = [
        [note_freq(n) for n in [48, 52, 55]],  # C
        [note_freq(n) for n in [45, 48, 52]],  # Am
        [note_freq(n) for n in [41, 45, 48]],  # F
        [note_freq(n) for n in [43, 47, 50]],  # G
    ]
    beat_dur = 60.0 / 72  # 72 BPM
    chord_dur = 4 * beat_dur
    hold = np.zeros_like(t, dtype=np.float32)
    for i in range(int(DURATION / chord_dur) + 1):
        chord_freqs = chords[i % len(chords)]
        start = i * chord_dur
        end = min(start + chord_dur, DURATION)
        mask = (t >= start) & (t < end)
        local_t = t[mask] - start
        chord_env = np.clip(local_t / 0.3, 0, 1) * np.clip(
            (chord_dur - local_t) / 0.3, 0, 1
        )
        for f in chord_freqs:
            hold[mask] += (
                chord_env * synth_note(f, local_t, harmonics=6, decay=0.4)
            ).astype(np.float32)
    hold = (hold * env * 0.015).astype(np.float32)

    # Normalize RMS
    target_rms = 0.04
    for name, audio in [
        ("calming_5min", calming),
        ("aversive_5min", aversive),
        ("hold_5min", hold),
    ]:
        rms = np.sqrt(np.mean(audio**2))
        if rms > 0:
            audio = (audio * target_rms / rms).astype(np.float32)
        sf.write(str(OUT / f"{name}.wav"), audio, SR)
        print(f"  {name}: {len(audio)/SR:.0f}s, RMS={np.sqrt(np.mean(audio**2)):.4f}")

    return OUT


def main():
    from context.tribev2 import TribeModel
    from context.tribev2.demo_utils import get_audio_and_text_events
    import pandas as pd
    from nilearn import datasets

    print("Generating 5-minute stimuli...")
    stim_dir = generate_5min_stimuli()

    CKPT_DIR = "cache/models--facebook--tribev2/snapshots/f894e783020944dcd96e5568550afe2aa9743f9f"
    print("\nLoading TRIBE v2...")
    model = TribeModel.from_pretrained(CKPT_DIR, cache_folder="./cache")
    print("Loaded.")

    # Load atlas
    destrieux = datasets.fetch_atlas_surf_destrieux()
    labels_lh = destrieux["map_left"]
    labels_rh = destrieux["map_right"]
    label_names = [
        l.decode() if isinstance(l, bytes) else l for l in destrieux["labels"]
    ]
    all_labels = np.concatenate([labels_lh, labels_rh])

    # Muller-relevant regions
    muller_regions = {
        "G_and_S_cingul-Ant": "dACC (RCZa-adjacent)",
        "G_and_S_cingul-Mid-Ant": "anterior MCC (RCZp-adjacent)",
        "G_and_S_cingul-Mid-Post": "posterior MCC",
        "G_front_middle": "MFG/dlPFC (UF region)",
        "S_circular_insula_ant": "ant. insula",
        "G_insular_short": "ant. insula (short)",
        "G_rectus": "vmPFC (value)",
        "G_front_inf-Orbital": "vlPFC/OFC",
        "S_temporal_sup": "STS (auditory ctrl)",
    }

    # Build region masks
    region_masks = {}
    for atlas_name in muller_regions:
        mask = np.zeros(len(all_labels), dtype=bool)
        for i, rn in enumerate(label_names):
            if rn == atlas_name:
                mask |= all_labels == i
        if mask.sum() > 0:
            region_masks[atlas_name] = mask

    # Run inference and track temporal dynamics
    stim_files = sorted(stim_dir.glob("*.wav"))
    all_temporal = {}

    for f in stim_files:
        name = f.stem
        print(f"\nProcessing: {name} (5 min)...")
        event = {
            "type": "Audio",
            "filepath": str(f.resolve()),
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
            print(f"  {preds.shape}, {elapsed:.1f}s")

            # Extract per-TR activations for each region
            temporal = {}
            for atlas_name, mask in region_masks.items():
                # preds shape: (n_TRs, 20484)
                temporal[atlas_name] = preds[:, mask].mean(axis=1)
            all_temporal[name] = temporal

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    if not all_temporal:
        print("No results!")
        sys.exit(1)

    # Analysis
    print(f"\n{'='*90}")
    print("  TEMPORAL DYNAMICS: Muller Fatigue Benchmark")
    print(f"{'='*90}")

    names = list(all_temporal.keys())
    n_trs = min(len(all_temporal[n][list(region_masks.keys())[0]]) for n in names)

    # Split into time bins (early, mid, late)
    third = n_trs // 3
    bins = {
        "early (0-100s)": slice(0, third),
        "mid (100-200s)": slice(third, 2 * third),
        "late (200-300s)": slice(2 * third, n_trs),
    }

    print(f"\nTRs per stimulus: {n_trs}")
    print(f"Bin size: {third} TRs each")

    for atlas_name, role in muller_regions.items():
        if atlas_name not in region_masks:
            continue
        print(f"\n  {atlas_name} ({role}):")
        header = f"    {'Bin':<20}" + "".join(f"{n:>18}" for n in names)
        print(header)
        for bin_name, bin_slice in bins.items():
            row = f"    {bin_name:<20}"
            for stim_name in names:
                vals = all_temporal[stim_name][atlas_name][bin_slice]
                row += f"{vals.mean():>18.4f}"
            print(row)

        # Trend: late - early (positive = accumulation)
        row_trend = f"    {'TREND (late-early)':<20}"
        for stim_name in names:
            early_mean = all_temporal[stim_name][atlas_name][bins["early (0-100s)"]].mean()
            late_mean = all_temporal[stim_name][atlas_name][bins["late (200-300s)"]].mean()
            trend = late_mean - early_mean
            marker = " **" if abs(trend) > 0.005 else ""
            row_trend += f"{trend:>18.4f}{marker}"
        print(row_trend)

    # Linear regression for trend per region x stimulus
    print(f"\n{'='*90}")
    print("  LINEAR TREND (slope of activation over time)")
    print(f"{'='*90}")
    print(f"  {'Region':<30} {'Role':<22}" + "".join(f"{n:>18}" for n in names))

    from numpy.polynomial.polynomial import polyfit

    for atlas_name, role in muller_regions.items():
        if atlas_name not in region_masks:
            continue
        row = f"  {atlas_name:<30} {role:<22}"
        for stim_name in names:
            y = all_temporal[stim_name][atlas_name][:n_trs]
            x = np.arange(len(y))
            slope = polyfit(x, y, 1)[1]  # linear coefficient
            row += f"{slope*1000:>18.4f}"  # multiply by 1000 for readability
        print(row)
    print("  (slopes x1000 for readability)")

    # Save
    os.makedirs("outputs", exist_ok=True)
    save_dict = {}
    for stim_name in names:
        for atlas_name in region_masks:
            key = f"{stim_name}__{atlas_name}"
            save_dict[key] = all_temporal[stim_name][atlas_name]
    save_dict["stimulus_names"] = np.array(names)
    save_dict["region_names"] = np.array(list(region_masks.keys()))
    np.savez("outputs/temporal_dynamics_results.npz", **save_dict)
    print(f"\nSaved to outputs/temporal_dynamics_results.npz")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
