# Subcortical Audit Result (2026-04-11)

## Finding: No pre-trained subcortical model exists

**HuggingFace repo (facebook/tribev2)**: Only 5 files — best.ckpt (cortical, 20484 vertices), config.yaml, README, LICENSE, .gitattributes.

**But**: The codebase contains `tribev2/grids/run_subcortical.py` which is a TRAINING config for subcortical models. The HF README even documents: `python -m tribev2.grids.run_subcortical`.

## What the subcortical training does
- Changes target projection from cortical surface (fsaverage5, 20484 vertices) to subcortical mask (Harvard-Oxford atlas, ~8802 voxels)
- Uses `MaskProjector` with `mask="subcortical"` and `fwhm=6.0` (spatial smoothing)
- Same model architecture, same training data (Algonauts, Lahner, Lebel, Wen)
- Same feature extractors (frozen Wav2Vec-Bert, V-JEPA, LLaMA)

## Options
1. **Train ourselves** — we have the architecture and some public training data. HCP and NNDb are publicly available. But the full pipeline requires neuralset study configurations that may need customization.
2. **Monitor GitHub Issue #23** — already open requesting this checkpoint (https://github.com/facebookresearch/tribev2/issues/23, no response as of 2026-04-12)
3. **Accept cortical-only** — use Neurosynth meta-analytic maps as subcortical proxy, or use the fact that vmPFC and dACC (cortical regions) are available even if PAG (brainstem) isn't.

## Recommendation
Option 3 (accept cortical-only) for now. vmPFC, dACC, anterior insula, and OFC are all cortical and available. PAG is brainstem — even the paper's subcortical model probably doesn't predict it well (too small, too deep). Don't let the perfect subcortical model block progress on the cortical analysis.

If cortical escape-region results look promising, revisit option 1 later.
