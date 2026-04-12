"""
Pressure test: Real (musically rich) stimuli through TRIBE v2.
Tests whether the weak PFC signal from synthetic tones was a stimulus
limitation vs. a model limitation.
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


def main():
    from tribev2 import TribeModel
    from tribev2.demo_utils import get_audio_and_text_events
    import pandas as pd
    from numpy.linalg import norm
    from nilearn import datasets

    CKPT_DIR = "cache/models--facebook--tribev2/snapshots/f894e783020944dcd96e5568550afe2aa9743f9f"
    STIMULI_DIR = pathlib.Path("stimuli/real")

    # Load model
    print("Loading TRIBE v2...")
    model = TribeModel.from_pretrained(CKPT_DIR, cache_folder="./cache")
    print("Loaded.\n")

    # Load parcellation
    destrieux = datasets.fetch_atlas_surf_destrieux()
    labels_lh = destrieux["map_left"]
    labels_rh = destrieux["map_right"]
    label_names = [
        l.decode() if isinstance(l, bytes) else l for l in destrieux["labels"]
    ]
    all_labels = np.concatenate([labels_lh, labels_rh])

    # Escape-relevant regions
    escape_regions = {
        "G_and_S_cingul-Ant": "dACC",
        "G_front_sup": "mPFC/SFG",
        "G_front_inf-Orbital": "vlPFC/OFC",
        "G_rectus": "vmPFC",
        "G_orbital": "OFC",
        "S_circular_insula_ant": "ant. insula",
        "G_insular_short": "ant. insula (short)",
        "G_temp_sup-Lateral": "aud. cortex (ctrl)",
        "S_temporal_sup": "STS (ctrl)",
    }

    # Run inference
    stim_files = sorted(STIMULI_DIR.glob("*.wav"))
    results = {}
    for f in stim_files:
        name = f.stem
        print(f"Processing: {name}...")
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
            print(f"  {preds.shape}, {time.perf_counter()-t0:.1f}s")
            results[name] = preds
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    if not results:
        print("No results!")
        sys.exit(1)

    names = list(results.keys())
    mean_preds = {n: results[n].mean(axis=0) for n in names}

    # --- Region-level analysis ---
    print(f"\n{'='*90}")
    print("  ESCAPE-RELEVANT REGION ACTIVATIONS (real music)")
    print(f"{'='*90}")
    header = f"  {'Region':<25} {'Role':<18}" + "".join(f"{n:>14}" for n in names)
    print(header)
    print("  " + "-" * (25 + 18 + 14 * len(names)))

    region_data = {}
    for atlas_name, role in escape_regions.items():
        mask = np.zeros(len(all_labels), dtype=bool)
        for i, rn in enumerate(label_names):
            if rn == atlas_name:
                mask |= all_labels == i
        if mask.sum() > 0:
            vals = [mean_preds[n][mask].mean() for n in names]
            var = np.var(vals)
            region_data[atlas_name] = {"role": role, "vals": vals, "var": var}
            val_str = "".join(f"{v:>14.4f}" for v in vals)
            print(f"  {atlas_name:<25} {role:<18}{val_str}")

    # --- Discriminability comparison with synthetic test ---
    print(f"\n{'='*90}")
    print("  DISCRIMINABILITY: Real music vs. Synthetic tones")
    print(f"{'='*90}")

    # Load synthetic results for comparison
    try:
        synth = np.load("outputs/sensitivity_test_results.npz", allow_pickle=True)
        synth_names = list(synth["stimulus_names"])
        synth_preds = {n: synth[f"pred_{n}"].mean(axis=0) for n in synth_names}
        synth_var = np.stack([synth_preds[n] for n in synth_names]).var(axis=0)

        real_all = np.stack([mean_preds[n] for n in names])
        real_var = real_all.var(axis=0)

        print(f"\n  {'Region':<25} {'Role':<18} {'Synth Var':>12} {'Real Var':>12} {'Ratio':>8}")
        print("  " + "-" * 75)
        for atlas_name, role in escape_regions.items():
            mask = np.zeros(len(all_labels), dtype=bool)
            for i, rn in enumerate(label_names):
                if rn == atlas_name:
                    mask |= all_labels == i
            if mask.sum() > 0:
                sv = synth_var[mask].mean()
                rv = real_var[mask].mean()
                ratio = rv / (sv + 1e-10)
                marker = " ***" if ratio > 2 else " *" if ratio > 1.5 else ""
                print(f"  {atlas_name:<25} {role:<18} {sv:>12.6f} {rv:>12.6f} {ratio:>7.1f}x{marker}")
    except FileNotFoundError:
        print("  (synthetic results not found for comparison)")

    # Pairwise cosine distances
    print(f"\n{'='*90}")
    print("  Pairwise cosine distances")
    print(f"{'='*90}")
    header = f"  {'':>20}" + "".join(f"{n:>16}" for n in names)
    print(header)
    for n1 in names:
        row = f"  {n1:>20}"
        for n2 in names:
            v1, v2 = mean_preds[n1], mean_preds[n2]
            cos_d = 1 - np.dot(v1, v2) / (norm(v1) * norm(v2) + 1e-8)
            row += f"{cos_d:>16.4f}"
        print(row)

    # Overall vertex variance
    all_preds = np.stack([mean_preds[n] for n in names])
    vertex_var = all_preds.var(axis=0)

    # Region ranking
    region_vars = {}
    for i, rname in enumerate(label_names):
        mask = all_labels == i
        if mask.sum() > 0:
            region_vars[rname] = vertex_var[mask].mean()
    sorted_regions = sorted(region_vars.items(), key=lambda x: x[1], reverse=True)

    print(f"\n{'='*90}")
    print("  Escape-region RANKS (of {0} regions)".format(len(sorted_regions)))
    print(f"{'='*90}")
    for atlas_name, role in escape_regions.items():
        rank = next(
            (i + 1 for i, (rn, _) in enumerate(sorted_regions) if rn == atlas_name),
            None,
        )
        var = region_vars.get(atlas_name, 0)
        print(f"  {atlas_name:<30} {role:<18} rank {rank:>3} (var={var:.6f})")

    # Save
    os.makedirs("outputs", exist_ok=True)
    np.savez(
        "outputs/real_music_results.npz",
        **{f"pred_{n}": results[n] for n in names},
        stimulus_names=np.array(names),
    )
    print(f"\nSaved to outputs/real_music_results.npz")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
