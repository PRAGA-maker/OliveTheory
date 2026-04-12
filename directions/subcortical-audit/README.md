# Subcortical Checkpoint Audit

## Purpose
Determine whether we can get subcortical predictions (amygdala, hippocampus, thalamus, and ideally PAG) from TRIBE v2 or an alternative.

## Motivation
The released checkpoint outputs 20,484 cortical vertices only. The paper describes a separate subcortical pathway predicting 8,802 voxels across 8 regions (Harvard-Oxford atlas): hippocampus, amygdala, thalamus, caudate, putamen, pallidum, accumbens, lateral ventricles. PAG is NOT in the paper's target set at all (it's too small/deep for the atlas used).

## Critical Context
- Mobbs' defensive hierarchy depends on vmPFC→PAG transition. Without PAG, we lose the reactive escape trigger.
- Amygdala is available in the paper's subcortical set but not in the released model.
- The paper's subcortical predictions were "two to three folds" lower than cortical anyway.
- Build args in checkpoint: `n_outputs=20484` — cortical only, confirmed.

## What Does Working Look Like?
Either: (a) find the subcortical checkpoint on HF/GitHub, load it, verify predictions, OR (b) determine it's not available and decide whether to retrain or accept cortical-only.

## Next Experiments
1. **[NOW] Check HF repo** for additional checkpoints (subcortical model, config variants)
2. **[NOW] Check GitHub issues/README** for subcortical model release plans
3. **[IF NOT FOUND] Assess retraining** from public data (HCP, NNDb have subcortical voxels)
4. **[FALLBACK] Accept cortical-only** and use Neurosynth/meta-analytic maps as subcortical proxy
