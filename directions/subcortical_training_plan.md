# Subcortical Training Plan for TRIBEv2

## Context for receiving agent

This document is a handoff from a prior analysis session. The user ("Praneel") is building a system to measure cortical escape motivation profiles (CEMP) from fMRI data, ultimately to optimize crisis hotline hold music. The core model is Meta's TRIBEv2 — a foundation model that predicts fMRI brain responses from multimodal stimuli (video, audio, text). The released checkpoint predicts **cortical surface only** (20,484 fsaverage5 vertices). Key subcortical regions needed for the research (NAcc, caudate, STN) are missing.

This plan covers: how to train a subcortical prediction head, what it costs, what gates exist at each stage, and what levers are available.

The user has two existing validation benchmarks from papers (Muller temporal dynamics, Dombrovski physiology) that test the cortical predictions. The subcortical train is a third leg that unlocks Pedersen 2021 DDM validation (NAcc avoidance bias, caudate drift rate, STN threshold).

---

## 1. The pretrained model we're starting from

| Component | Params | % of total | Role |
|---|---|---|---|
| Projectors (text/video/audio) | 4.2M | 2.4% | Map frozen LLaMA/V-JEPA2/Wav2Vec features to shared dim |
| Transformer encoder (8 layers, dim=1152) | 127.5M | 71.9% | Cross-modal temporal integration |
| Low-rank head (1152 -> 2048) | 2.4M | 1.3% | Bottleneck before subject prediction |
| Predictor (subject layers) | 42.0M | 23.7% | Per-subject linear map to 20,484 cortical vertices |
| Positional embedding | 1.2M | 0.7% | Temporal position |
| **Total** | **177.2M** | **100%** | |

Checkpoint: `facebook/tribev2` on HuggingFace (709 MB, fp32). Already downloaded locally.

Hardware available: RTX 4060 Laptop GPU (8GB VRAM), 32GB RAM, 16 CPU threads. CUDA 12.6 confirmed working. Inference benchmarked at ~2,700 TRs/s (fp32/fp16) at B=1, ~21,000 TRs/s at B=8 fp16.

---

## 2. The core question: representation quality

Before spending any compute on training, the critical unknown is:

**Does the frozen transformer backbone encode subcortical-relevant information?**

The backbone was trained to predict cortical surface activity. Cortex and subcortex are tightly coupled (cortico-striatal loops, thalamo-cortical projections, etc.), so the internal representations *should* contain subcortical signal — but this is an empirical question.

The cheapest way to answer it: fit a linear map from frozen features to subcortical voxels. This takes minutes, not hours. Everything else is optimization on top.

---

## 3. Stage 0: Linear probe on HCP data

### Why HCP

HCP movie-watching data (Van Essen et al., 2013) is ideal for this probe:
- **176 subjects, 7T scanner.** 7T gives ~2x SNR over 3T, critical for small deep structures like NAcc and STN.
- **Movie-watching = naturalistic stimuli.** Exactly the paradigm the encoder was trained on.
- **Public data.** Available on ConnectomeDB.
- **Clean OOD test.** HCP was in TRIBE's *test* set, not training. The backbone has never been trained to predict HCP subjects' brain data. If a linear probe works on HCP, the representations genuinely encode subcortical signal — it's not memorization.

### First test: Ridge regression

**Cost:** Minutes on CPU. $0.

**Setup:**
- Extract frozen 2048-dim features (output of `low_rank_head`) for HCP movie stimuli
- Get volumetric subcortical fMRI from the same subjects (Aseg parcellation, ~8,808 voxels)
- Fit ridge regression: 2048 dims → 8,808 voxels
- Use minimum 25 subjects for the first pass (plenty for ridge with 2048 features), hold out 5 for test
- Cross-validate to select ridge alpha

**Why all 8,808 voxels, not just targeted ROIs:** Ridge regression fits each voxel independently — there's no cross-voxel learning, so it costs the same whether you fit 2,000 or 8,808. You get per-ROI R-values for free. Run it on everything and inspect the ROIs you care about (NAcc, caudate, STN) plus everything else. If amygdala or thalamus lights up unexpectedly, that's free information.

**Gate:** R > 0 for target ROIs. Even R = 0.02 is a go — the paper's own subcortical scores (Fig 2B) ranged 0.02-0.14 with a *trained* head. A linear probe hitting > 0 means the signal exists and downstream training will amplify it.

**Params to search if R ~ 0 on first attempt:**
- **Alpha (regularization strength):** Log-space search from 1e-2 to 1e6. Subcortical BOLD is noisier than cortical — the optimal alpha may be much higher than you'd expect.
- **Temporal lag:** Subcortical hemodynamic responses can be slower/shifted relative to cortical. Try lagging the target fMRI by 0, 1, 2, 3 TRs relative to the features. The default offset in their pipeline is 5 TRs but this was tuned for cortex.
- **Feature source:** Try the raw 1152-dim encoder output (before `low_rank_head`) instead of the 2048-dim post-bottleneck features. The bottleneck was optimized for cortical prediction and may have discarded subcortical-relevant dimensions.
- **Subject pooling:** Try fitting per-subject models (more data per regression) vs. pooled across subjects (more generalization). Per-subject may work better for subcortical given high inter-subject variability in deep structures.

### If ridge doesn't work: alternative linear methods

Each of these has different assumptions. If ridge fails, the failure mode tells you which to try next.

| Method | Assumption | When to try | Cost |
|---|---|---|---|
| **Lasso (L1)** | Signal is sparse — only a few encoder dims map to each subcortical voxel | If ridge R ~ 0 but you suspect the signal is concentrated in a handful of dimensions (not spread across all 2048) | Minutes |
| **Elastic Net** | Mix of sparse and distributed signal | If both ridge and lasso give weak but nonzero R — captures both modes | Minutes |
| **Partial Least Squares (PLS)** | Shared low-dimensional structure between features and targets | If you suspect the encoder→subcortical mapping lives in a low-rank subspace. PLS explicitly finds this. Good when target dimensionality (8,808) >> useful feature dims | Minutes |
| **Canonical Correlation Analysis (CCA)** | Looking for maximally correlated subspaces | If PLS shows some structure but you want to find the specific feature/voxel subspaces that co-vary. Can reveal which encoder dims carry subcortical info | Minutes |
| **Group-regularized ridge** | Subcortical voxels within the same anatomical structure share regression weights | If per-voxel ridge is too noisy but there's signal at the ROI level. Uses anatomical priors — neighboring voxels in NAcc should have similar mappings. This has support in the subcortical literature: structures like striatum have smooth topographic organization | Minutes-hours |

**Diagnostic between methods:** If ridge R ~ 0 and lasso R > 0, the signal is sparse. If PLS R > 0 but ridge R ~ 0, the features need dimensionality reduction before mapping. If nothing works, the frozen features may genuinely not encode subcortical information, and you need to unfreeze the backbone (skip to Stage 2b).

### If linear doesn't work: nonlinear approaches

Still cheap. Still on frozen features. The question is whether the encoder→subcortical mapping has nonlinear structure.

| Method | What it captures | Cost | Notes |
|---|---|---|---|
| **Kernel ridge (RBF)** | Smooth nonlinear mapping without explicit architecture | Minutes-hours | Just ridge in a lifted feature space. Gamma parameter needs tuning. If this works and linear doesn't, the mapping is nonlinear but smooth |
| **2-layer MLP (2048→512→N_targets)** | Interactions between encoder dimensions that linear methods miss | ~1 hour GPU | Add dropout (0.3-0.5), train with early stopping. If this works and linear doesn't, there are meaningful feature interactions. This is still a probe, not the full training pipeline |
| **Random forest / gradient boosting** | Non-smooth, threshold-based mappings | Minutes (per voxel, slow for 8,808) | Fit on a few target ROIs only. Useful as a diagnostic — if tree methods work, the mapping is nonlinear and potentially non-smooth |

**If nonlinear probes also fail:** The frozen backbone likely does not encode subcortical information. Proceed directly to Stage 2b (unfreeze backbone). This is still not a dead end — it just means the backbone needs adaptation, which is expected given it was only trained on cortical targets.

---

## 4. Stage 1: Trained head, full subcortical, frozen backbone

**Cost:** ~5 hours on RTX 4060. $0.

**Prerequisite:** Stage 0 showed R > 0 for at least some subcortical ROIs.

**What:**
- Freeze entire backbone (127.5M params)
- Replace cortical predictor with subcortical predictor targeting all 8,808 voxels
- low_rank_head: 1152 → 128 (SVD initialization from existing weights)
- Predictor: 128 → 8,808 subcortical voxels
- Train with Muon optimizer, cosine schedule, fp32 (bf16 OK for exploratory sweeps only)
- 3 epochs on 1x data (HCP + original training studies if subcortical volumetric data is available)
- ~13,500 steps, batch=8

**Why full 8,808 and not targeted ROIs:** Unlike ridge (which fits each voxel independently), the trained head uses a shared r=128 bottleneck. This means the model is forced to find low-rank structure across all subcortical regions. Emergence between regions happens through this shared bottleneck — if NAcc and caudate share a latent dimension (they're both striatal, connected via the same dopaminergic circuits), the model can exploit that. Training on just 3 ROIs throws away this cross-region structure.

Think of it as: the bottleneck is 128-dimensional. With 8,808 target voxels, the model must find ~128 "subcortical eigenmodes." With only 2,000 targeted voxels, you get fewer constraints on what those eigenmodes look like, and they might not generalize to other structures you'll want later.

**Trainable params:** ~1.3M (128 × 1152 + 128 × 8808 = 147K + 1.1M). Training memory: ~700 MB total (dominated by frozen backbone).

**Data adequacy:** 1x data = ~3.6M timepoints, params = 1.3M. Ratio ~3:1. Reasonable for a constrained linear map — not as overdetermined as the targeted case, but the shared bottleneck acts as strong regularization.

**Gate:** Compare per-ROI R to the Stage 0 linear probe. The trained head should improve on ridge because: (a) the shared bottleneck finds cross-region structure, (b) end-to-end optimization through the bottleneck beats two-stage SVD + regression. If R doesn't improve, the bottleneck rank might be wrong (try r=256 or r=512) or the architecture isn't helping and you should just use the linear probe.

---

## 5. Stage 2a: Head-only, 2x data, 5 epochs

**Cost:** ~16 hours on RTX 4060. $0. Or $11 on A100.

**Prerequisite:** Stage 1 showed meaningful improvement over Stage 0.

**What:** Same as Stage 1 but with 2x data and 5 epochs. Need to find datasets that we would like to add, data that we think would be relevant to the task we are optimizing for.
- 5 epochs = Chinchilla-optimal (~18:1 data:param at 2x data) + 10% bake-in + 2x instability buffer (for crashes, or a cold-end to ensure we train for enough time as-needed.)
- 45,000 total steps
- This is the maximum useful compute for a frozen-backbone head train. Beyond this, returns are flat.

**Gate:** R improves over Stage 1. If the improvement from 1x→2x data is < 5% relative, the head has saturated and more data won't help. The lever to pull next is the backbone, not the data.

---

## 6. Stage 2b: Unfreeze backbone, 1 epoch fine-tune

**Cost:** ~16 hours on RTX 4060. $0. Or $53 on A100 with 5x data.

**Prerequisite:** Stage 0 showed weak/no signal (go here directly) OR Stages 1/2a have plateaued.

**What:** Unfreeze all 177M params. Fine-tune for 1 epoch (matching the paper's fine-tuning protocol). Use the head from Stage 1/2a as initialization.
- All params trainable
- 1 epoch on available data
- Lower learning rate (1e-5 or 5e-5) to avoid catastrophic forgetting of cortical representations
- This is where the backbone adapts its internal representations to better encode subcortical structure

**Memory:** ~3 GB mixed precision. Fits on 8GB GPU.

**Gate:** Subcortical R improves meaningfully over Stage 2a. Also verify that cortical R hasn't degraded (the backbone must still predict cortex well for the Muller/Dombrovski benchmarks).

**Risk:** Catastrophic forgetting of cortical representations. Mitigate by: (a) low LR, (b) saving the pre-fine-tune checkpoint, (c) monitoring cortical R alongside subcortical R during training.

---

## 7. Stage 3: Full training with 2x data (nuclear option)

**Cost:** ~10 days on RTX 4060. $0. Or $240 on A100.

**Prerequisite:** Only if Stages 0-2b all show the backbone representations are fundamentally inadequate.

**What:** Train the full 177M model from scratch (or from pretrained init) on 2x data for 15 epochs with subcortical targets (or combined cortical + subcortical = ~29K targets).
- All params trainable from epoch 1
- 15 epochs, 9,000 steps/epoch = 135,000 total steps
- Muon + cosine schedule + fp32

**Gate:** Only reach this stage if Stages 1-2b all show the backbone representations are fundamentally inadequate for subcortical prediction. This is unlikely — the paper reports above-chance subcortical encoding with their existing architecture.

---

## 8. Available levers

### Precision
- **fp32**: Native training precision of released checkpoint. **Use this for any final/production training run.** The model is small enough that fp32 fits easily — don't sacrifice precision to save a few hours when the total is already cheap.
- **bf16 mixed precision**: 2-3x faster at higher batch sizes. Fine for cheap exploratory runs, hyperparameter sweeps, and directional checks (e.g., "does r=256 help?"). But only if the results aren't wildly different from fp32 — if bf16 introduces noticeable quality degradation, drop it entirely and just eat the extra time.
- **fp16**: Avoid for training. Numerically less stable than bf16 (no exponent headroom). OK for inference only.

### Data volume
- **1x** (~1,000h, 720 subjects, 4 studies): What they trained on. Already adequate for head training.
- **2x** (~2,000h): Adds subject diversity. Helps most if unfreezing backbone. For head-only, diminishing returns.
- **5x+**: Only justified for full retraining from scratch. Not cost-effective for head training.
- Key datasets: HCP (already ideal — 176 subjects, 7T), OpenNeuro ds000171 (music+depression), ds002320 (dynamic threat), CNeuroMod, BoldMoments.

### Training duration (epochs/steps)
- **Ridge probe**: No epochs, single fit, minutes.
- **3 epochs**: Conservative head training. Probably sufficient for convergence.
- **5 epochs**: Chinchilla-optimal + buffer. Maximum useful for head training.
- **1 epoch (fine-tune)**: For backbone unfreezing. Paper's protocol.
- **15 epochs**: Full training from scratch. Only for Stage 3.

### Model size (head params)
- **1.3M** (full subcortical, r=128): Recommended. Shared bottleneck enables cross-region emergence.
- **0.4M** (targeted ROIs, r=128): Cheaper but loses cross-region structure. Only if you're sure you don't need emergence.
- **6.5M+** (r=2048): Full-rank head. More capacity but the bottleneck is representation quality, not head capacity.

### Bottleneck rank (r)
- **r=128**: Paper's fine-tuning default. Good balance of capacity vs. regularization.
- **r=64**: Stronger compression. Forces the model to find fewer, more fundamental eigenmodes. Try if r=128 overfits.
- **r=256 or r=512**: More capacity. Try if r=128 underfits (Stage 1 R doesn't improve over linear probe).

### Frozen vs. fine-tune vs. full retrain
- **Frozen backbone + head only**: Cheapest. Tests whether existing representations suffice. Always do this first.
- **Fine-tune (unfreeze 1 epoch)**: Lets backbone adapt to subcortical targets. Low risk with low LR. Second step.
- **Full retrain**: Nuclear option. Only if representations are fundamentally inadequate. Days, not hours.

### Target selection
- **Full subcortical (8,808 voxels)**: Recommended for trained head (shared bottleneck enables emergence). Also run this for the linear probe — it's free.
- **Targeted (NAcc, caudate, STN, ~2K voxels)**: Useful as a diagnostic lens (inspect these ROIs from the full-subcortical model) but don't train on these alone unless you're certain cross-region structure doesn't help.
- **Cortical + subcortical (~29K targets)**: One unified model. Consider for Stage 3.

### Optimizer
- **Adam (their choice)**: Safe, well-understood. No weight decay in their config (questionable).
- **Muon (user preference)**: Faster convergence for small models. Recommended.
- **AdamW**: Adam + weight decay. Minimal change from their setup, strict improvement.

---

## 9. Pareto optimality and the representation quality ceiling

The staged plan is designed to find the Pareto frontier between compute and quality:

```
Quality (R)
  ^
  |                              * Stage 3 (full retrain, 10d)
  |                         * Stage 2b (unfreeze, 16h)
  |                   * Stage 2a (head 2x data, 16h)
  |              * Stage 1 (trained head, 5h)
  |         * Stage 0 nonlinear (MLP probe, 1h)
  |      * Stage 0 linear (ridge, 30 min)
  |
  +-------------------------------------------------> Compute
```

At each stage, the go/no-go gate asks: "Did quality improve enough to justify the next step?" If the curve is flattening, stop.

**The cheapest test (Stage 0 ridge, 30 min) tells you 80% of what you need to know.** If the linear probe shows zero subcortical signal in the frozen features, nothing downstream will fix that without unfreezing the backbone. If it shows R > 0, the remaining stages are optimization.

The representation quality ceiling is set by the backbone. Stages 0-2a all share the same ceiling — they just approach it with different head architectures. Stage 2b (unfreezing) raises the ceiling itself but risks catastrophic forgetting. Stage 3 resets the ceiling entirely.

### Existing benchmarks (for context)

- **Muller benchmark**: Temporal dynamics of predicted cingulate/insula/MFG activation vs. known fatigue accumulation patterns. All cortical, directly testable with released model.
- **Dombrovski benchmark**: Different vmPFC/insula patterns for stimuli affecting depressed vs. healthy populations. Partially testable (cortical regions available, striatum not).
- **Pedersen benchmark** (unlocked by this plan): NAcc avoidance bias, caudate drift rate, STN threshold. The most diagnostically important one (NAcc AUC=0.68 for MDD). Requires subcortical predictions.

---

## 10. Technical implementation notes

The codebase already has most of what's needed:

- `main.py:435-464`: `freeze_backbone=True` + `resize_subject_layer=True` implements head-only training with SVD initialization
- `grids/run_subcortical.py`: Grid config for subcortical training using `MaskProjector` with subcortical mask
- `model.py:139-141`: `low_rank_head` parameter controls bottleneck rank

What needs to be built/changed:
1. **Stage 0 probe script**: Standalone. Extract frozen 2048-dim features for HCP stimuli, load volumetric subcortical fMRI, fit ridge/lasso/PLS/MLP, report per-ROI R.
2. Swap `SurfaceProjector(mesh='fsaverage5')` for `MaskProjector(mask='subcortical')` in data config
3. Point at fMRI data with volumetric (not surface-projected) subcortical coverage
4. Replace Adam with Muon in optimizer config
5. Add bf16 precision flag to trainer config

The user considers Meta's training implementation suboptimal — plan to rewrite the training loop using a modern, community-standard engine (plain PyTorch + Muon, or a lightweight framework) rather than building on their neuraltrain/exca/neuralset dependency stack.

### On HCP as the probe dataset

HCP was in TRIBE's **test** set, not training (Table 1 in the paper). The backbone has never been trained to predict HCP subjects' brain data. This makes HCP a clean out-of-distribution test: if a linear probe from frozen features to subcortical voxels works on held-out HCP data, we know the representations genuinely encode subcortical signal, not memorization. 176 subjects at 7T with movie-watching stimuli — this is the best available data for this probe.
