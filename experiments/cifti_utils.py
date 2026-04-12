"""Utilities for extracting subcortical voxel data from HCP CIFTI files.

CIFTI grayordinate files (.dtseries.nii) combine cortical surface vertices and
subcortical volume voxels in a single data matrix. This module provides
functions to isolate subcortical voxels, group them by ROI, and compute
ROI-level mean timeseries for downstream ridge regression probes.

Requires: nibabel >= 4.0
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple, Union

import numpy as np

try:
    import nibabel as nib
    from nibabel.cifti2 import BrainModelAxis
except ImportError:
    raise ImportError(
        "nibabel is required for CIFTI support. Install it with:\n"
        "  uv add nibabel\n"
        "or:\n"
        "  pip install nibabel>=4.0"
    )

# ---------------------------------------------------------------------------
# CIFTI structure names that correspond to subcortical grey-matter voxels.
# These are the structures present in HCP grayordinate files (91k or 170k).
# Cortex left/right are surface-based and excluded here.
# ---------------------------------------------------------------------------
SUBCORTICAL_STRUCTURES: Tuple[str, ...] = (
    "CIFTI_STRUCTURE_ACCUMBENS_LEFT",
    "CIFTI_STRUCTURE_ACCUMBENS_RIGHT",
    "CIFTI_STRUCTURE_AMYGDALA_LEFT",
    "CIFTI_STRUCTURE_AMYGDALA_RIGHT",
    "CIFTI_STRUCTURE_BRAIN_STEM",
    "CIFTI_STRUCTURE_CAUDATE_LEFT",
    "CIFTI_STRUCTURE_CAUDATE_RIGHT",
    "CIFTI_STRUCTURE_CEREBELLUM_LEFT",
    "CIFTI_STRUCTURE_CEREBELLUM_RIGHT",
    "CIFTI_STRUCTURE_DIENCEPHALON_VENTRAL_LEFT",
    "CIFTI_STRUCTURE_DIENCEPHALON_VENTRAL_RIGHT",
    "CIFTI_STRUCTURE_HIPPOCAMPUS_LEFT",
    "CIFTI_STRUCTURE_HIPPOCAMPUS_RIGHT",
    "CIFTI_STRUCTURE_PALLIDUM_LEFT",
    "CIFTI_STRUCTURE_PALLIDUM_RIGHT",
    "CIFTI_STRUCTURE_PUTAMEN_LEFT",
    "CIFTI_STRUCTURE_PUTAMEN_RIGHT",
    "CIFTI_STRUCTURE_THALAMUS_LEFT",
    "CIFTI_STRUCTURE_THALAMUS_RIGHT",
)

# Mapping from CIFTI structure names to canonical ROI labels used by
# get_subcortical_roi_masks(). Each key is a human-readable ROI name;
# the value is the list of CIFTI structure names that belong to it.
_ROI_TO_CIFTI: Dict[str, Tuple[str, ...]] = {
    "accumbens_left": ("CIFTI_STRUCTURE_ACCUMBENS_LEFT",),
    "accumbens_right": ("CIFTI_STRUCTURE_ACCUMBENS_RIGHT",),
    "amygdala_left": ("CIFTI_STRUCTURE_AMYGDALA_LEFT",),
    "amygdala_right": ("CIFTI_STRUCTURE_AMYGDALA_RIGHT",),
    "brain_stem": ("CIFTI_STRUCTURE_BRAIN_STEM",),
    "caudate_left": ("CIFTI_STRUCTURE_CAUDATE_LEFT",),
    "caudate_right": ("CIFTI_STRUCTURE_CAUDATE_RIGHT",),
    "cerebellum_left": ("CIFTI_STRUCTURE_CEREBELLUM_LEFT",),
    "cerebellum_right": ("CIFTI_STRUCTURE_CEREBELLUM_RIGHT",),
    "diencephalon_ventral_left": ("CIFTI_STRUCTURE_DIENCEPHALON_VENTRAL_LEFT",),
    "diencephalon_ventral_right": ("CIFTI_STRUCTURE_DIENCEPHALON_VENTRAL_RIGHT",),
    "hippocampus_left": ("CIFTI_STRUCTURE_HIPPOCAMPUS_LEFT",),
    "hippocampus_right": ("CIFTI_STRUCTURE_HIPPOCAMPUS_RIGHT",),
    "pallidum_left": ("CIFTI_STRUCTURE_PALLIDUM_LEFT",),
    "pallidum_right": ("CIFTI_STRUCTURE_PALLIDUM_RIGHT",),
    "putamen_left": ("CIFTI_STRUCTURE_PUTAMEN_LEFT",),
    "putamen_right": ("CIFTI_STRUCTURE_PUTAMEN_RIGHT",),
    "thalamus_left": ("CIFTI_STRUCTURE_THALAMUS_LEFT",),
    "thalamus_right": ("CIFTI_STRUCTURE_THALAMUS_RIGHT",),
}


def load_cifti_subcortical(
    cifti_path: Union[str, Path],
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """Load a CIFTI dtseries file and extract subcortical voxel timeseries.

    Parameters
    ----------
    cifti_path : str or Path
        Path to a .dtseries.nii CIFTI file.

    Returns
    -------
    timeseries : np.ndarray, shape (n_timepoints, n_subcortical_voxels)
        The BOLD timeseries for subcortical voxels only. Voxels are ordered
        by their appearance along the brain-model axis (i.e. the order in
        which CIFTI stores them).
    structure_labels : dict[str, np.ndarray]
        Mapping from CIFTI structure name (e.g. ``"CIFTI_STRUCTURE_HIPPOCAMPUS_LEFT"``)
        to an integer array of column indices into ``timeseries`` for that
        structure. Only structures actually present in the file are included.
    """
    cifti_path = Path(cifti_path)
    if not cifti_path.exists():
        raise FileNotFoundError(f"CIFTI file not found: {cifti_path}")

    img = nib.load(str(cifti_path))
    data = img.get_fdata()  # shape: (n_timepoints, n_grayordinates)

    # The brain-model axis is axis 1 for dtseries files (axis 0 is time/series).
    brain_model_axis = img.header.get_axis(1)
    if not isinstance(brain_model_axis, BrainModelAxis):
        raise ValueError(
            f"Expected a BrainModelAxis on axis 1, got {type(brain_model_axis).__name__}. "
            "Is this a .dtseries.nii file?"
        )

    # Collect subcortical slices. iter_structures yields:
    #   (cifti_structure_name: str, data_slice: slice, sub_axis: BrainModelAxis)
    subcortical_indices: list[int] = []
    structure_labels: Dict[str, np.ndarray] = {}

    for struct_name, data_slice, _sub_axis in brain_model_axis.iter_structures():
        if struct_name not in SUBCORTICAL_STRUCTURES:
            continue

        # Convert the slice to explicit indices relative to the full grayordinate axis
        indices = np.arange(data_slice.start, data_slice.stop or brain_model_axis.size)
        # Remap to 0-based positions in the output subcortical array
        offset = len(subcortical_indices)
        structure_labels[struct_name] = np.arange(offset, offset + len(indices))
        subcortical_indices.extend(indices.tolist())

    if not subcortical_indices:
        raise ValueError(
            "No subcortical structures found in the CIFTI file. "
            "The file may contain only cortical surface data."
        )

    timeseries = data[:, subcortical_indices]
    return timeseries, structure_labels


def get_subcortical_roi_masks(
    structure_labels: Dict[str, np.ndarray],
) -> Dict[str, np.ndarray]:
    """Create boolean ROI masks over the subcortical voxel dimension.

    Groups voxels by region (left/right kept separate):
    hippocampus, amygdala, thalamus, caudate, putamen, pallidum, accumbens,
    brain-stem, cerebellum, diencephalon-ventral.

    Parameters
    ----------
    structure_labels : dict[str, np.ndarray]
        As returned by :func:`load_cifti_subcortical`. Maps CIFTI structure
        names to index arrays.

    Returns
    -------
    roi_masks : dict[str, np.ndarray]
        Mapping from ROI name (e.g. ``"hippocampus_left"``) to a boolean mask
        of shape ``(n_subcortical_voxels,)``. Only ROIs that actually have
        voxels in ``structure_labels`` are included.
    """
    # Total number of subcortical voxels
    n_voxels = sum(len(idx) for idx in structure_labels.values())

    roi_masks: Dict[str, np.ndarray] = {}
    for roi_name, cifti_names in _ROI_TO_CIFTI.items():
        mask = np.zeros(n_voxels, dtype=bool)
        has_any = False
        for cifti_name in cifti_names:
            if cifti_name in structure_labels:
                mask[structure_labels[cifti_name]] = True
                has_any = True
        if has_any:
            roi_masks[roi_name] = mask

    return roi_masks


def compute_roi_means(
    timeseries: np.ndarray,
    roi_masks: Dict[str, np.ndarray],
) -> Dict[str, np.ndarray]:
    """Compute mean timeseries within each ROI.

    Parameters
    ----------
    timeseries : np.ndarray, shape (n_timepoints, n_subcortical_voxels)
        Subcortical voxel timeseries as returned by :func:`load_cifti_subcortical`.
    roi_masks : dict[str, np.ndarray]
        Boolean masks as returned by :func:`get_subcortical_roi_masks`.

    Returns
    -------
    roi_means : dict[str, np.ndarray]
        Mapping from ROI name to mean timeseries of shape ``(n_timepoints,)``.
    """
    roi_means: Dict[str, np.ndarray] = {}
    for roi_name, mask in roi_masks.items():
        if mask.sum() == 0:
            continue
        roi_means[roi_name] = timeseries[:, mask].mean(axis=1)
    return roi_means


# ---------------------------------------------------------------------------
# Quick summary helper
# ---------------------------------------------------------------------------

def summarize_subcortical(
    structure_labels: Dict[str, np.ndarray],
) -> str:
    """Return a human-readable summary of subcortical voxel counts per structure.

    Parameters
    ----------
    structure_labels : dict[str, np.ndarray]
        As returned by :func:`load_cifti_subcortical`.

    Returns
    -------
    summary : str
    """
    lines = ["Subcortical structures:"]
    total = 0
    for name, indices in sorted(structure_labels.items()):
        n = len(indices)
        total += n
        # Strip the CIFTI_STRUCTURE_ prefix for readability
        short = name.replace("CIFTI_STRUCTURE_", "").lower()
        lines.append(f"  {short:40s} {n:5d} voxels")
    lines.append(f"  {'TOTAL':40s} {total:5d} voxels")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    # Default placeholder -- override with a real path as a CLI argument
    default_path = (
        "/data/hcp/7T_movie/"
        "sub-100610/MNINonLinear/Results/tfMRI_MOVIE1_7T_AP/"
        "tfMRI_MOVIE1_7T_AP_Atlas_MSMAll_hp2000_clean.dtseries.nii"
    )
    cifti_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    print(f"Loading CIFTI file: {cifti_path}")
    timeseries, structure_labels = load_cifti_subcortical(cifti_path)
    print(f"Timeseries shape: {timeseries.shape}")
    print()
    print(summarize_subcortical(structure_labels))

    roi_masks = get_subcortical_roi_masks(structure_labels)
    print(f"\nROI masks ({len(roi_masks)} regions):")
    for name, mask in sorted(roi_masks.items()):
        print(f"  {name:40s} {mask.sum():5d} voxels")

    roi_means = compute_roi_means(timeseries, roi_masks)
    print(f"\nROI mean timeseries ({len(roi_means)} regions):")
    for name, ts in sorted(roi_means.items()):
        print(f"  {name:40s} shape={ts.shape}  "
              f"mean={ts.mean():.4f}  std={ts.std():.4f}")
