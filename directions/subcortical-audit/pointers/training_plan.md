# Subcortical Head Training — Concrete Plan

## The Idea
The pretrained TRIBE v2 encoder (127M params) already learned excellent audio→brain
representations. Those same latent representations contain subcortical-relevant
information. We just need to learn the LINEAR MAPPING from latent → subcortical voxels.

## Architecture Recap
```
Audio → Wav2Vec-Bert → [FROZEN transformer encoder] → 2048-dim latent → [NEW linear head] → 8,808 subcortical voxels
```

We replace ONLY the last layer. Everything else stays pretrained.

## What We Need

### 1. Training targets: Subcortical fMRI voxels
- Source: HCP 7T movie-watching data (176 subjects, publicly available)
  - Already in TRIBE v2's TEST set, so stimuli are known
  - Volumetric MNI-registered data available from HCP
- Extraction: `MaskProjector(mask="subcortical", resolution=2)` → Harvard-Oxford atlas → 8,808 voxels
- Also viable: Wen2017 (3 subjects, smallest/simplest, MNI data included)

### 2. Latent representations from pretrained model
- Run the pretrained TRIBE v2 on the SAME stimuli used in HCP
- Extract the 2048-dim output of `low_rank_head` (before the cortical predictor)
- This is the "brain encoding" latent space — already trained

### 3. Training procedure
Option A (simplest): Ridge regression
- X: latent reps (n_timepoints, 2048)
- Y: subcortical voxels (n_timepoints, 8808)
- Fit with sklearn `RidgeCV` or similar
- No GPU needed for this step
- Minutes to train

Option B (better): Re-initialize subject block + predictor, freeze encoder, train 1 epoch
- This is exactly what TRIBE v2's fine-tuning does (paper Section 5.4)
- Uses low-rank SVD factorization (rank 128) for the new subject block
- 1 epoch, same optimizer settings
- GPU needed but small job (~20M trainable params)
- Hours to train

## Estimated Timeline

| Step | Time | Blocker? |
|------|------|----------|
| Download HCP movie data | 1-2 hours | Need HCP account (free, requires agreement) |
| Extract subcortical voxels | 30 min | nibabel + neuralset, straightforward |
| Extract audio features | 1-2 hours | Already cached if same stimuli |
| Run pretrained encoder → latent reps | 30 min | Just forward pass, no training |
| Train subcortical head (Ridge) | 5 min | Literally sklearn |
| Train subcortical head (1-epoch FT) | 2-4 hours | GPU, small model |
| Validate predictions | 30 min | Sanity check |

**Total: 1-2 days including data download.**

## Alternative: Wen2017 (fastest proof of concept)
- Only 3 subjects, ~3 hours of video
- MNI-registered volumetric data likely included in download
- Fastest to get running — proves the concept before scaling to HCP
- Limitation: small sample, video-only (no audio in Wen2017!)
  → Actually this is a problem — Wen2017 has NO audio, so the audio pathway
  wouldn't contribute. HCP or BoldMoments (which have audio) are better.

## Recommended Path
1. Get HCP data access (free academic agreement)
2. Download the 7T movie-watching subset (one movie, 176 subjects)
3. Extract subcortical voxels
4. Run pretrained encoder on HCP stimuli → latent reps
5. Train ridge regression first (5 min) → validate
6. If ridge works, do 1-epoch FT for better performance
7. Package as `subcortical_head.pt` alongside the original `best.ckpt`

## What This Gets Us
- Predicted activation in: hippocampus, amygdala, thalamus, caudate, putamen,
  pallidum, NAcc, lateral ventricles
- Enables: full Pedersen AAC-DDM (NAcc approach-bias), Dombrovski (ventral striatum PE),
  Mobbs (amygdala threat)
- Does NOT get us: PAG (not in Harvard-Oxford atlas)
