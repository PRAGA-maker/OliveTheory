"""
Subcortical Ridge Regression Probe (Stage 0)

Tests whether TRIBE v2's frozen internal representations contain subcortical
information. The pretrained model predicts 20,484 cortical vertices from
audio/video/text. We extract its frozen 2048-dim latent features (output of
low_rank_head) and fit a ridge regression to predict subcortical fMRI voxels
from HCP movie-watching data.

Rationale: The backbone was trained on cortical targets only, but cortex and
subcortex are tightly coupled (cortico-striatal loops, thalamo-cortical
projections). If the frozen features encode any subcortical signal, even a
simple linear probe should recover it. Per the training plan, R > 0 for target
ROIs is a go signal — the paper's own subcortical scores ranged 0.02-0.14 with
a *trained* head.

HCP is ideal: 176 subjects, 7T (2x SNR for deep structures), movie-watching
(matches TRIBE's training paradigm), and it was in TRIBE's *test* set — so any
signal found is genuine, not memorization.

Diagnostics (from subcortical_training_plan.md):
  - Temporal lag: subcortical hemodynamic responses may be shifted relative to
    cortical. Try 0-3 TR lags on the target fMRI.
  - Feature source: try pre-bottleneck (1152-dim encoder output) vs.
    post-bottleneck (2048-dim low_rank_head output). The bottleneck was
    optimized for cortical prediction and may discard subcortical dimensions.
  - Alpha search: log-spaced 1e-2 to 1e6. Subcortical BOLD is noisier than
    cortical — optimal alpha may be much higher than expected.

Usage:
    1. Set DATA_DIR below to the path containing HCP CIFTI dtseries files.
    2. Set CKPT_DIR to the pretrained TRIBE v2 checkpoint directory.
    3. Run: python experiments/subcortical_probe.py

Outputs: outputs/subcortical_probe_results.npz
"""

import multiprocessing
import os
import pathlib
import sys
import time
import logging

# -- Windows compatibility --
if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath

import numpy as np
import torch
from pathlib import Path
from scipy.stats import pearsonr
from sklearn.linear_model import RidgeCV

# ---------------------------------------------------------------------------
# Configuration — fill these in once data is downloaded
# ---------------------------------------------------------------------------

# Path to HCP movie-watching CIFTI dtseries files.
# Expected structure: DATA_DIR/{subject_id}/MNINonLinear/Results/tfMRI_MOVIE{n}_7T_AP/
#                     tfMRI_MOVIE{n}_7T_AP_Atlas_MSMAll.dtseries.nii
DATA_DIR = Path("data/HCP_movie")

# Pretrained TRIBE v2 checkpoint directory (contains config.yaml + best.ckpt).
CKPT_DIR = "cache/models--facebook--tribev2/snapshots/f894e783020944dcd96e5568550afe2aa9743f9f"

# HCP movie stimulus audio files, aligned to the fMRI runs.
# Expected structure: STIM_DIR/MOVIE{n}_7T.wav
STIM_DIR = Path("data/HCP_stimuli")

# Subjects to use. Use a subset for the initial probe; expand later.
# First N_TRAIN for fitting, last N_TEST for held-out evaluation.
SUBJECT_IDS = [
    "100610", "102311", "102816", "104416", "105923",
    "108323", "109123", "111312", "111514", "114823",
    "115017", "115825", "116726", "118225", "125525",
    "126426", "128935", "130114", "130518", "131217",
    "131722", "132118", "134627", "134829", "135124",
    "137128", "140117", "144226", "145834", "146129",
]
N_TRAIN = 25
N_TEST = 5

# Temporal lags to try (in TRs). Subcortical hemodynamics may be shifted.
TEMPORAL_LAGS = [0, 1, 2, 3]

# Ridge alpha search space (log-spaced). Subcortical BOLD is noisy,
# so we search up to very high regularization.
RIDGE_ALPHAS = np.logspace(-2, 6, 50)

# Random seed for reproducibility.
SEED = 42

# ---------------------------------------------------------------------------
# Harvard-Oxford subcortical ROI definitions
# ---------------------------------------------------------------------------

# The 8 bilateral structures from the Harvard-Oxford subcortical atlas,
# excluding cortex, white matter, brainstem, and background.
# These are the names as they appear in nilearn's fetch_atlas_harvard_oxford.
SUBCORTICAL_ROIS = {
    "Thalamus":            {"left": "Left Thalamus",            "right": "Right Thalamus"},
    "Caudate":             {"left": "Left Caudate",             "right": "Right Caudate"},
    "Putamen":             {"left": "Left Putamen",             "right": "Right Putamen"},
    "Pallidum":            {"left": "Left Pallidum",            "right": "Right Pallidum"},
    "Hippocampus":         {"left": "Left Hippocampus",         "right": "Right Hippocampus"},
    "Amygdala":            {"left": "Left Amygdala",            "right": "Right Amygdala"},
    "Accumbens":           {"left": "Left Accumbens",           "right": "Right Accumbens"},
    "Brain-Stem":          {"bilateral": "Brain-Stem"},
}

# For reporting — maps to functional relevance for the project.
ROI_ROLES = {
    "Thalamus":    "thalamo-cortical relay",
    "Caudate":     "drift rate (Pedersen DDM)",
    "Putamen":     "habit/motor",
    "Pallidum":    "output nucleus",
    "Hippocampus": "memory/context",
    "Amygdala":    "threat/salience",
    "Accumbens":   "avoidance bias (Pedersen DDM)",
    "Brain-Stem":  "arousal/PAG",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ===========================================================================
# Feature extraction from frozen TRIBE v2
# ===========================================================================

def load_tribe_model(ckpt_dir: str, device: str = "auto"):
    """Load pretrained TRIBE v2 model in eval mode.

    Returns the TribeModel wrapper (for event processing) and the raw
    FmriEncoderModel (for feature extraction hooks).
    """
    from context.tribev2 import TribeModel

    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    model = TribeModel.from_pretrained(ckpt_dir, cache_folder="./cache")
    log.info("Loaded TRIBE v2 on %s", device)
    return model


def extract_latent_features(
    tribe_model,
    audio_path: str,
    feature_source: str = "post_bottleneck",
) -> np.ndarray:
    """Extract frozen latent features from a TRIBE v2 model for a given audio file.

    Hooks into the model's forward pass to capture intermediate activations
    before the cortical predictor.

    Parameters
    ----------
    tribe_model : TribeModel
        Loaded TRIBE v2 model (from load_tribe_model).
    audio_path : str
        Path to the stimulus audio file.
    feature_source : str
        Which features to extract:
        - "post_bottleneck": 2048-dim output of low_rank_head (default).
        - "pre_bottleneck": 1152-dim output of the transformer encoder,
          before low_rank_head. May retain subcortical info that the
          cortical-optimized bottleneck discards.

    Returns
    -------
    features : np.ndarray
        Shape (n_TRs, feature_dim). Feature dim is 2048 for post_bottleneck
        or 1152 for pre_bottleneck.
    """
    import pandas as pd
    from context.tribev2.demo_utils import get_audio_and_text_events

    # Build events dataframe from audio file.
    event = {
        "type": "Audio",
        "filepath": str(Path(audio_path).resolve()),
        "start": 0,
        "timeline": "default",
        "subject": "default",
    }
    events = get_audio_and_text_events(pd.DataFrame([event]), audio_only=True)

    model = tribe_model._model
    device = model.device

    # --- Hook into the forward pass to capture latent features ---
    captured = {}

    def hook_post_bottleneck(module, input, output):
        """Capture output of low_rank_head: (B, T, 2048) transposed to (B, 2048, T)."""
        # low_rank_head is applied as: x = self.low_rank_head(x.transpose(1,2)).transpose(1,2)
        # The hook on nn.Linear captures output shape (B, T, 2048).
        captured["post_bottleneck"] = output.detach().cpu()

    def hook_pre_bottleneck(module, input, output):
        """Capture transformer encoder output: (B, T, 1152)."""
        captured["pre_bottleneck"] = output.detach().cpu()

    handles = []
    if feature_source == "post_bottleneck":
        if hasattr(model, "low_rank_head"):
            handles.append(model.low_rank_head.register_forward_hook(hook_post_bottleneck))
        else:
            raise ValueError(
                "Model has no low_rank_head. Set feature_source='pre_bottleneck'."
            )
    elif feature_source == "pre_bottleneck":
        handles.append(model.encoder.register_forward_hook(hook_pre_bottleneck))
    else:
        raise ValueError(f"Unknown feature_source: {feature_source!r}")

    # --- Run inference, collecting hooked features per batch ---
    from einops import rearrange
    from tqdm import tqdm

    loader = tribe_model.data.get_loaders(events=events, split_to_build="all")["all"]

    all_features = []
    all_keep_masks = []

    with torch.inference_mode():
        for batch in tqdm(loader, desc=f"Extracting {feature_source} features"):
            batch = batch.to(device)

            # Determine which TRs to keep (non-empty segments).
            batch_segments = []
            for segment in batch.segments:
                for t in np.arange(0, segment.duration - 1e-2, tribe_model.data.TR):
                    batch_segments.append(
                        segment.copy(offset=t, duration=tribe_model.data.TR)
                    )
            keep = np.array([len(s.ns_events) > 0 for s in batch_segments])

            # Forward pass triggers the hook.
            _ = model(batch)

            key = feature_source
            feats = captured[key]  # (B, T, D) or (B, D, T) depending on hook point

            if feature_source == "post_bottleneck":
                # Hook on nn.Linear captures (B, T, 2048). Rearrange to (B*T, D).
                feats = rearrange(feats, "b t d -> (b t) d")
            elif feature_source == "pre_bottleneck":
                # Encoder output is (B, T, 1152). Rearrange to (B*T, D).
                feats = rearrange(feats, "b t d -> (b t) d")

            feats = feats[keep].numpy()
            all_features.append(feats)

    # Clean up hooks.
    for h in handles:
        h.remove()

    features = np.concatenate(all_features, axis=0)
    log.info(
        "Extracted %s features: %d TRs x %d dims",
        feature_source, features.shape[0], features.shape[1],
    )
    return features


# ===========================================================================
# Loading subcortical fMRI from HCP CIFTI files
# ===========================================================================

def load_subcortical_from_cifti(cifti_path: str) -> tuple[np.ndarray, dict]:
    """Load subcortical voxel timeseries from an HCP CIFTI dtseries file.

    HCP CIFTI grayordinate files contain both cortical surface vertices and
    subcortical volume voxels in a single file. The brain model axis (axis 1)
    encodes which grayordinates are surface vs. volume and which anatomical
    structure each belongs to.

    Parameters
    ----------
    cifti_path : str
        Path to a .dtseries.nii CIFTI file.

    Returns
    -------
    subcortical_data : np.ndarray
        Shape (n_timepoints, n_subcortical_voxels). The subcortical voxel
        timeseries extracted from the CIFTI file.
    roi_map : dict
        Maps ROI name (str) -> array of voxel indices into subcortical_data.
        Keys match CIFTI brain structure names (e.g., "ACCUMBENS_LEFT").
    """
    import nibabel as nib

    img = nib.load(cifti_path)
    data = img.get_fdata()  # (n_timepoints, n_grayordinates)

    # The brain model axis tells us which grayordinates are subcortical.
    brain_axis = img.header.get_axis(1)

    subcortical_indices = []
    roi_map = {}
    current_idx = 0

    for name, slc, bm in brain_axis.iter_structures():
        struct_name = str(name)

        # Skip cortical surface structures.
        if "CORTEX" in struct_name:
            continue

        n_voxels = slc.stop - slc.start
        voxel_indices_in_subcortical = np.arange(current_idx, current_idx + n_voxels)
        roi_map[struct_name] = voxel_indices_in_subcortical
        subcortical_indices.extend(range(slc.start, slc.stop))
        current_idx += n_voxels

    subcortical_indices = np.array(subcortical_indices)
    subcortical_data = data[:, subcortical_indices]

    log.info(
        "Loaded CIFTI %s: %d timepoints, %d subcortical voxels, %d structures",
        Path(cifti_path).name,
        subcortical_data.shape[0],
        subcortical_data.shape[1],
        len(roi_map),
    )
    return subcortical_data, roi_map


def map_cifti_structures_to_rois(roi_map: dict) -> dict:
    """Map CIFTI brain structure names to our Harvard-Oxford ROI groupings.

    CIFTI structures have names like "CIFTI_STRUCTURE_ACCUMBENS_LEFT".
    We map these to our ROI dictionary for reporting.

    Parameters
    ----------
    roi_map : dict
        From load_subcortical_from_cifti. Keys are CIFTI structure names,
        values are arrays of voxel indices.

    Returns
    -------
    grouped : dict
        Maps our ROI names (e.g., "Accumbens") -> array of voxel indices.
        Left and right hemispheres are merged.
    """
    # Mapping from keywords in CIFTI structure names to our ROI names.
    cifti_to_roi = {
        "THALAMUS":    "Thalamus",
        "CAUDATE":     "Caudate",
        "PUTAMEN":     "Putamen",
        "PALLIDUM":    "Pallidum",
        "HIPPOCAMPUS": "Hippocampus",
        "AMYGDALA":    "Amygdala",
        "ACCUMBENS":   "Accumbens",
        "BRAIN_STEM":  "Brain-Stem",
        "BRAINSTEM":   "Brain-Stem",
    }

    grouped = {}
    for cifti_name, indices in roi_map.items():
        matched = False
        for keyword, roi_name in cifti_to_roi.items():
            if keyword in cifti_name.upper():
                if roi_name not in grouped:
                    grouped[roi_name] = []
                grouped[roi_name].append(indices)
                matched = True
                break
        if not matched:
            log.warning("Unmapped CIFTI structure: %s (%d voxels)", cifti_name, len(indices))

    # Concatenate left/right into single arrays.
    for roi_name in grouped:
        grouped[roi_name] = np.concatenate(grouped[roi_name])

    return grouped


def load_hcp_subject_data(
    subject_id: str,
    data_dir: Path,
    movie_runs: list[str] = None,
) -> tuple[np.ndarray, dict]:
    """Load and concatenate subcortical fMRI across movie runs for one subject.

    Parameters
    ----------
    subject_id : str
        HCP subject ID (e.g., "100610").
    data_dir : Path
        Root data directory.
    movie_runs : list[str] or None
        Which movie runs to load. Defaults to all 4 HCP 7T movie runs.

    Returns
    -------
    data : np.ndarray
        Shape (total_timepoints, n_subcortical_voxels).
    roi_map : dict
        ROI name -> voxel index array (from the first run; consistent across runs).
    """
    if movie_runs is None:
        movie_runs = ["MOVIE1_7T_AP", "MOVIE2_7T_PA", "MOVIE3_7T_PA", "MOVIE4_7T_AP"]

    all_data = []
    roi_map = None

    for run in movie_runs:
        cifti_path = (
            data_dir / subject_id / "MNINonLinear" / "Results"
            / f"tfMRI_{run}" / f"tfMRI_{run}_Atlas_MSMAll.dtseries.nii"
        )
        if not cifti_path.exists():
            log.warning("Missing: %s", cifti_path)
            continue

        run_data, run_roi_map = load_subcortical_from_cifti(str(cifti_path))
        all_data.append(run_data)
        if roi_map is None:
            roi_map = run_roi_map

    if not all_data:
        raise FileNotFoundError(f"No movie CIFTI files found for subject {subject_id}")

    data = np.concatenate(all_data, axis=0)
    return data, roi_map


# ===========================================================================
# Ridge regression probe
# ===========================================================================

def apply_temporal_lag(features: np.ndarray, targets: np.ndarray, lag: int):
    """Align features and targets with a temporal lag.

    A positive lag means the target fMRI is shifted forward — i.e., the model
    features at time t predict brain activity at time t+lag. This accounts for
    hemodynamic delay differences between cortical and subcortical regions.

    Parameters
    ----------
    features : np.ndarray
        Shape (T, D). Model latent features.
    targets : np.ndarray
        Shape (T, V). Subcortical fMRI voxels.
    lag : int
        Number of TRs to shift targets forward. 0 = no lag.

    Returns
    -------
    features_aligned : np.ndarray
        Shape (T - lag, D).
    targets_aligned : np.ndarray
        Shape (T - lag, V).
    """
    if lag == 0:
        return features, targets
    if lag < 0:
        raise ValueError("Lag must be non-negative")
    # Features at t predict targets at t+lag.
    return features[:-lag], targets[lag:]


def fit_ridge_probe(
    features_train: np.ndarray,
    targets_train: np.ndarray,
    features_test: np.ndarray,
    targets_test: np.ndarray,
    alphas: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fit RidgeCV from frozen features to subcortical voxels.

    Uses leave-one-out cross-validation (efficient for Ridge) to select alpha,
    then evaluates on held-out test data.

    Parameters
    ----------
    features_train, targets_train : np.ndarray
        Training data. Features: (T_train, D), targets: (T_train, V).
    features_test, targets_test : np.ndarray
        Test data. Features: (T_test, D), targets: (T_test, V).
    alphas : np.ndarray
        Regularization strengths to search.

    Returns
    -------
    r_per_voxel : np.ndarray
        Pearson R for each voxel on test data. Shape (V,).
    best_alpha : np.ndarray
        Selected alpha for each voxel (or single value). Shape depends on
        RidgeCV internals; returned for diagnostics.
    predictions : np.ndarray
        Predicted test targets. Shape (T_test, V).
    """
    log.info(
        "Fitting RidgeCV: train=%s -> %s, test=%s -> %s, %d alphas [%.1e, %.1e]",
        features_train.shape, targets_train.shape,
        features_test.shape, targets_test.shape,
        len(alphas), alphas.min(), alphas.max(),
    )

    # z-score features (important for ridge — puts all dimensions on equal footing).
    feat_mean = features_train.mean(axis=0)
    feat_std = features_train.std(axis=0)
    feat_std[feat_std == 0] = 1.0  # avoid division by zero for dead dimensions
    features_train = (features_train - feat_mean) / feat_std
    features_test = (features_test - feat_mean) / feat_std

    # z-score targets per voxel.
    tgt_mean = targets_train.mean(axis=0)
    tgt_std = targets_train.std(axis=0)
    tgt_std[tgt_std == 0] = 1.0
    targets_train = (targets_train - tgt_mean) / tgt_std
    targets_test_z = (targets_test - tgt_mean) / tgt_std

    t0 = time.perf_counter()
    ridge = RidgeCV(
        alphas=alphas,
        fit_intercept=True,
        scoring=None,  # default: efficient LOO for RidgeCV
        cv=None,  # None = efficient LOO
        alpha_per_target=False,  # single alpha for all voxels (faster, more stable)
    )
    ridge.fit(features_train, targets_train)
    elapsed = time.perf_counter() - t0
    log.info("Ridge fit took %.1fs. Best alpha: %.2e", elapsed, ridge.alpha_)

    # Predict on test set.
    predictions_z = ridge.predict(features_test)

    # Pearson R per voxel (on z-scored data — equivalent to raw correlation).
    n_voxels = targets_test_z.shape[1]
    r_per_voxel = np.zeros(n_voxels)
    for v in range(n_voxels):
        if targets_test_z[:, v].std() > 0 and predictions_z[:, v].std() > 0:
            r_per_voxel[v], _ = pearsonr(targets_test_z[:, v], predictions_z[:, v])
        else:
            r_per_voxel[v] = 0.0

    # Un-z-score predictions for downstream use.
    predictions = predictions_z * tgt_std + tgt_mean

    return r_per_voxel, np.array(ridge.alpha_), predictions


def compute_roi_results(
    r_per_voxel: np.ndarray,
    roi_grouped: dict,
) -> dict:
    """Aggregate per-voxel Pearson R into per-ROI statistics.

    Parameters
    ----------
    r_per_voxel : np.ndarray
        Pearson R for each subcortical voxel. Shape (V,).
    roi_grouped : dict
        From map_cifti_structures_to_rois. ROI name -> voxel index array.

    Returns
    -------
    results : dict
        Maps ROI name -> dict with keys: mean_r, median_r, max_r, n_voxels,
        frac_positive (fraction of voxels with R > 0).
    """
    results = {}
    for roi_name, indices in roi_grouped.items():
        roi_r = r_per_voxel[indices]
        results[roi_name] = {
            "mean_r": float(np.mean(roi_r)),
            "median_r": float(np.median(roi_r)),
            "max_r": float(np.max(roi_r)),
            "std_r": float(np.std(roi_r)),
            "n_voxels": len(indices),
            "frac_positive": float(np.mean(roi_r > 0)),
        }
    return results


# ===========================================================================
# Main experiment
# ===========================================================================

def main():
    np.random.seed(SEED)
    torch.manual_seed(SEED)

    # --- Validate paths ---
    if not Path(CKPT_DIR).exists():
        log.error("Checkpoint not found: %s", CKPT_DIR)
        log.error("Download with: TribeModel.from_pretrained('facebook/tribev2')")
        sys.exit(1)

    if not DATA_DIR.exists():
        log.error("HCP data directory not found: %s", DATA_DIR)
        log.error(
            "Download HCP 7T movie-watching data from ConnectomeDB and set DATA_DIR."
        )
        sys.exit(1)

    if not STIM_DIR.exists():
        log.error("Stimulus directory not found: %s", STIM_DIR)
        log.error("Place HCP movie stimulus audio files in %s", STIM_DIR)
        sys.exit(1)

    # --- Load model ---
    log.info("Loading TRIBE v2 from %s", CKPT_DIR)
    tribe_model = load_tribe_model(CKPT_DIR)

    # --- Extract features for each movie run ---
    # We extract features once and reuse across all lag/feature_source configs.
    feature_sources = ["post_bottleneck", "pre_bottleneck"]
    stim_features = {}

    movie_stim_files = sorted(STIM_DIR.glob("*.wav"))
    if not movie_stim_files:
        log.error("No .wav files found in %s", STIM_DIR)
        sys.exit(1)

    for source in feature_sources:
        stim_features[source] = {}
        for stim_file in movie_stim_files:
            log.info("Extracting %s features for %s", source, stim_file.name)
            feats = extract_latent_features(tribe_model, str(stim_file), source)
            stim_features[source][stim_file.stem] = feats

    # --- Load subcortical fMRI for each subject ---
    log.info("Loading subcortical fMRI for %d subjects", len(SUBJECT_IDS))
    subject_data = {}
    roi_map_global = None

    for sid in SUBJECT_IDS:
        try:
            data, roi_map = load_hcp_subject_data(sid, DATA_DIR)
            subject_data[sid] = data
            if roi_map_global is None:
                roi_map_global = roi_map
            log.info("  %s: %s", sid, data.shape)
        except FileNotFoundError as e:
            log.warning("  %s: skipped (%s)", sid, e)

    if len(subject_data) < N_TRAIN + N_TEST:
        log.error(
            "Need at least %d subjects, got %d. Check DATA_DIR and SUBJECT_IDS.",
            N_TRAIN + N_TEST, len(subject_data),
        )
        sys.exit(1)

    # Group CIFTI structures into our ROI definitions.
    roi_grouped = map_cifti_structures_to_rois(roi_map_global)
    log.info("ROI grouping: %s", {k: len(v) for k, v in roi_grouped.items()})

    # Split subjects into train/test.
    sids = list(subject_data.keys())
    train_sids = sids[:N_TRAIN]
    test_sids = sids[N_TRAIN : N_TRAIN + N_TEST]
    log.info("Train subjects: %d, Test subjects: %d", len(train_sids), len(test_sids))

    # --- Run probe across all configurations ---
    # Results indexed by (feature_source, lag).
    all_results = {}
    all_r_per_voxel = {}

    for source in feature_sources:
        for lag in TEMPORAL_LAGS:
            config_key = f"{source}_lag{lag}"
            log.info("=" * 70)
            log.info("Configuration: %s", config_key)
            log.info("=" * 70)

            # Concatenate features and targets across subjects and runs.
            # For each subject, align the stimulus features to their fMRI
            # (same stimuli for all subjects in HCP movie-watching).
            train_feats_all, train_tgts_all = [], []
            test_feats_all, test_tgts_all = [], []

            # Get the concatenated feature vector for all movie runs.
            run_features = []
            for stim_name in sorted(stim_features[source].keys()):
                run_features.append(stim_features[source][stim_name])
            concat_features = np.concatenate(run_features, axis=0)

            for sid in train_sids:
                tgts = subject_data[sid]
                feats = concat_features

                # Ensure temporal alignment: truncate to min length.
                min_t = min(feats.shape[0], tgts.shape[0])
                feats = feats[:min_t]
                tgts = tgts[:min_t]

                # Apply temporal lag.
                feats, tgts = apply_temporal_lag(feats, tgts, lag)

                train_feats_all.append(feats)
                train_tgts_all.append(tgts)

            for sid in test_sids:
                tgts = subject_data[sid]
                feats = concat_features

                min_t = min(feats.shape[0], tgts.shape[0])
                feats = feats[:min_t]
                tgts = tgts[:min_t]

                feats, tgts = apply_temporal_lag(feats, tgts, lag)

                test_feats_all.append(feats)
                test_tgts_all.append(tgts)

            train_feats = np.concatenate(train_feats_all, axis=0)
            train_tgts = np.concatenate(train_tgts_all, axis=0)
            test_feats = np.concatenate(test_feats_all, axis=0)
            test_tgts = np.concatenate(test_tgts_all, axis=0)

            log.info(
                "Train: %d TRs x %d features -> %d voxels",
                train_feats.shape[0], train_feats.shape[1], train_tgts.shape[1],
            )
            log.info(
                "Test: %d TRs x %d features -> %d voxels",
                test_feats.shape[0], test_feats.shape[1], test_tgts.shape[1],
            )

            # Fit ridge regression.
            r_per_voxel, best_alpha, predictions = fit_ridge_probe(
                train_feats, train_tgts, test_feats, test_tgts, RIDGE_ALPHAS,
            )

            roi_results = compute_roi_results(r_per_voxel, roi_grouped)
            all_results[config_key] = roi_results
            all_r_per_voxel[config_key] = r_per_voxel

            # Print ROI summary for this configuration.
            print(f"\n{'='*80}")
            print(f"  {config_key}  |  alpha={best_alpha:.2e}")
            print(f"{'='*80}")
            print(
                f"  {'ROI':<16} {'Role':<30} {'Mean R':>8} {'Med R':>8} "
                f"{'Max R':>8} {'%>0':>6} {'N vox':>7}"
            )
            print(f"  {'-'*16} {'-'*30} {'-'*8} {'-'*8} {'-'*8} {'-'*6} {'-'*7}")

            for roi_name in SUBCORTICAL_ROIS:
                if roi_name not in roi_results:
                    continue
                r = roi_results[roi_name]
                role = ROI_ROLES.get(roi_name, "")
                marker = " ***" if r["mean_r"] > 0 else ""
                print(
                    f"  {roi_name:<16} {role:<30} {r['mean_r']:>8.4f} "
                    f"{r['median_r']:>8.4f} {r['max_r']:>8.4f} "
                    f"{r['frac_positive']:>5.0%} {r['n_voxels']:>7d}{marker}"
                )

    # --- Summary: best configuration per ROI ---
    print(f"\n{'='*80}")
    print("  BEST CONFIGURATION PER ROI")
    print(f"{'='*80}")
    print(f"  {'ROI':<16} {'Best config':<30} {'Mean R':>8} {'Gate':>8}")
    print(f"  {'-'*16} {'-'*30} {'-'*8} {'-'*8}")

    for roi_name in SUBCORTICAL_ROIS:
        best_config = None
        best_r = -np.inf
        for config_key, roi_results in all_results.items():
            if roi_name in roi_results:
                r = roi_results[roi_name]["mean_r"]
                if r > best_r:
                    best_r = r
                    best_config = config_key
        if best_config is not None:
            gate = "GO" if best_r > 0 else "STOP"
            print(f"  {roi_name:<16} {best_config:<30} {best_r:>8.4f} {gate:>8}")

    # --- Save results ---
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "subcortical_probe_results.npz"

    save_dict = {
        "feature_sources": np.array(feature_sources),
        "temporal_lags": np.array(TEMPORAL_LAGS),
        "ridge_alphas": RIDGE_ALPHAS,
        "roi_names": np.array(list(SUBCORTICAL_ROIS.keys())),
        "train_subjects": np.array(train_sids),
        "test_subjects": np.array(test_sids),
    }

    # Save per-voxel R arrays and ROI results for each configuration.
    for config_key, r_per_voxel in all_r_per_voxel.items():
        save_dict[f"r_per_voxel__{config_key}"] = r_per_voxel
    for config_key, roi_results in all_results.items():
        for roi_name, metrics in roi_results.items():
            prefix = f"roi__{config_key}__{roi_name}"
            for metric_name, value in metrics.items():
                save_dict[f"{prefix}__{metric_name}"] = np.array(value)

    np.savez(str(out_path), **save_dict)
    log.info("Saved results to %s", out_path)

    # --- Final gate decision ---
    print(f"\n{'='*80}")
    print("  STAGE 0 GATE DECISION")
    print(f"{'='*80}")

    target_rois = ["Accumbens", "Caudate", "Thalamus"]
    any_go = False
    for roi_name in target_rois:
        best_r = -np.inf
        for config_key, roi_results in all_results.items():
            if roi_name in roi_results:
                best_r = max(best_r, roi_results[roi_name]["mean_r"])
        if best_r > 0:
            print(f"  {roi_name}: R={best_r:.4f} -> GO (signal exists)")
            any_go = True
        else:
            print(f"  {roi_name}: R={best_r:.4f} -> signal weak/absent")

    if any_go:
        print("\n  DECISION: Proceed to Stage 1 (trained head, frozen backbone)")
        print("  The frozen representations encode subcortical signal.")
    else:
        print("\n  DECISION: Try nonlinear probes (kernel ridge, 2-layer MLP)")
        print("  If those also fail -> proceed to Stage 2b (unfreeze backbone)")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
