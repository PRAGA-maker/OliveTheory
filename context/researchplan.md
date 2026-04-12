# OliveTheory Research Plan

## 1. Motivation

Half of 988 Suicide Hotline callers hang up before reaching a counselor. During the hold period, the caller is making a continuous decision — stay or go — driven by a neural process we call escape motivation. The right hold music, chosen with computational neuroscience rather than intuition, could shift that decision.

This project builds a fully computational pipeline from **music audio** to **predicted brain response** to **escape motivation measurement** to **actionable hold music recommendations**. Every link is grounded in published neuroscience, every step is validated against empirical benchmarks.

## 2. Key Problems

**Problem 1: No existing tool connects music to escape-relevant brain activity.**
There are models that predict brain responses from audio (TRIBE v2, Kell 2018), and there are computational models of escape/quit decisions (Pedersen 2021, Muller 2021, Dombrovski 2013). Nobody has connected them. The bridge between "this music has these acoustic features" and "this music shifts the brain toward or away from escape" does not exist.

**Problem 2: We can't scan people in crisis.**
Ethical constraints prevent putting suicidal callers in an fMRI scanner. So we need a way to *predict* brain responses (from audio alone) and *validate* those predictions against known physiology of crisis states (from published fMRI studies of depression and suicide attempters).

**Problem 3: "Escape motivation" is not a single construct.**
The literature fragments into: entrapment (Gilbert & Allan), Pavlovian escape bias (Millner), defensive flight (Mobbs), fatigue-driven quitting (Muller), value-based decision-making (Dombrovski), approach-avoidance conflict (Pedersen). We need to pick measurable proxies without collapsing distinct mechanisms.

## 3. Solution Architecture

Three components, each solving one part of the pipeline:

### Component A: Audio → Brain (TRIBE v2 + Subcortical Extension)

**What**: Meta's TRIBE v2 foundation model predicts whole-brain fMRI from audio. We extend it with a subcortical prediction head to access amygdala, NAcc, caudate, thalamus — regions critical for escape motivation.

**Why TRIBE v2 over alternatives**: It's the only model that predicts whole-brain fMRI from raw audio at cortical resolution. Narrow-scope models (Kell 2018, Ciferri CLAP-based) predict auditory cortex only. Casey 2017 showed music features predict OFC at 7T, but that was ridge regression on one dataset, not a generalizable model. TRIBE v2 is the foundation we build on.

**What we validated**: Real music produces 2-6x stronger differentiation in escape-relevant cortical regions (dACC, vmPFC, OFC, anterior insula) compared to synthetic tones. The model is viable. Temporal dynamics over 5-minute sequences match Muller's fatigue accumulation predictions: aversive audio → increasing cingulate/insula suppression, calming audio → the opposite.

**What's missing**: The released checkpoint is cortical-only (20,484 vertices). Subcortical regions (NAcc, amygdala, caudate) require training a new output head. Plan: freeze the pretrained encoder, train a linear head on HCP 7T subcortical data. Staged approach (ridge probe → trained head → optional backbone fine-tune) with clear gates at each step. See `directions/subcortical_training_plan.md`.

### Component B: Brain → Escape Motivation Measurement

**What**: A two-layer measurement framework that validates the instrument (can we trust the predictions?) and then uses it to measure escape motivation (what does the music do?).

**Layer 1 — Validation benchmarks** (prove the instrument works):

| Benchmark | What it tests | Regions | Status |
|-----------|--------------|---------|--------|
| **Muller 2021** (fatigue dynamics) | Do predicted cingulate/insula signals evolve over time like real fatigue? | RCZp, RCZa, MFG, insula — all cortical | **PASSED** — directionally consistent |
| **Dombrovski 2013** (attempter physiology) | Does the model predict vmPFC/insula patterns consistent with suicide attempter neuroscience? | vmPFC, insula (cortical), ventral striatum (needs subcortical) | Partially testable now, fully with subcortical |

**Layer 2 — Decision measurement** (measure escape motivation):

| Framework | What it measures | Regions | Status |
|-----------|-----------------|---------|--------|
| **Pedersen 2021** (AAC-DDM) | Approach vs. avoidance bias, drift rate, decision threshold | NAcc, pgACC, STN, caudate — mostly subcortical | Blocked until subcortical head trained |
| **CEMP** (Cortical Escape Motivation Profile) | Activation pattern across escape-relevant cortical regions | Insula, dACC, vmPFC, OFC — all cortical | Available now as interim measure |

The logic: Muller and Dombrovski tell us whether our predictions match known physiology (benchmarkable — we know the right answer). Once we trust the instrument, Pedersen tells us what the music actually does to the escape/approach decision (the question we care about).

**Why this ordering matters**: Pedersen's AAC-DDM is harder to benchmark directly (we don't have AAC task fMRI for our stimuli). But Muller and Dombrovski have published brain patterns we can compare against. If our model reproduces their known results, we have reason to trust it for the Pedersen measurement.

### Component C: Music → Features (Actionable Recommendations)

**What**: Decompose music into interpretable features (tempo, consonance, spectral profile, harmonic complexity) and correlate those features with the escape motivation measurement from Component B. The deliverable is: "hold music should have features X, Y, Z" — specific, backed by predicted brain activation.

**Why not MusER directly**: MusER's VQ-VAE was trained on piano pop (EMOPIA dataset). It won't generalize to ambient/hold music without retraining. Instead, we use acoustic features extracted directly from audio (MIRtoolbox-style: tempo, spectral centroid, roughness, mode, harmonic change) and correlate them with CEMP/Pedersen scores across a library of candidate music clips.

**The workflow**:
1. Curate a library of candidate hold music (N=50-100 clips, diverse styles)
2. Run each through TRIBE v2 → get predicted brain activation
3. Compute escape motivation score (CEMP or Pedersen once subcortical available)
4. Extract acoustic features from each clip
5. Regression: which features predict lower escape motivation?
6. Deliverable: "Optimal hold music has tempo 60-80 BPM, high consonance, low roughness, spectral centroid below X Hz"

**MusER's future role**: Once we know which features matter (from step 5), MusER (or a retrained variant) becomes useful for *generating* music that optimizes those features. But discovery comes first.

## 4. Why This Approach Over Alternatives

**Alternative 1: Skip the brain, just test music on callers directly.**
Pro: most direct. Con: massive sample sizes needed, ethical complexity, can't explain *why* something works, can't generalize to new music. Our approach provides mechanistic understanding that transfers.

**Alternative 2: Use emotion recognition models instead of brain encoding.**
Pro: simpler pipeline. Con: emotion labels are subjective and coarse ("calming" vs. "anxious" is not the same as "reduces escape motivation in the dACC"). We need physiological specificity, not self-report proxies.

**Alternative 3: Use a different brain encoding model.**
We evaluated all available options. TRIBE v2 is the only model that predicts whole-brain fMRI from raw audio at cortical resolution. Kell 2018 is auditory-cortex only. CLAP-based encoding (Ciferri 2025) gets IFG but not whole-brain. No model targets PFC/emotion regions from music specifically — this gap is exactly what our subcortical extension addresses.

## 5. Simulating Crisis Physiology

TRIBE v2 was trained on healthy adults. Crisis callers have altered PFC function, heightened insula reactivity, and blunted striatal reward signals. How do we bridge this gap?

**Approach: Constraint relaxation ladder + fine-tuning (mandatory, not optional)**

We fine-tune TRIBE v2 toward crisis physiology. This is part of the core pipeline, not an enhancement. Even if the fine-tuned model benchmarks similarly to the base model, we use it as the production model as long as: (a) all base functionality is preserved (no catastrophic forgetting), and (b) calibration checks confirm the model is simulating crisis-adjacent brain patterns correctly (Dombrovski vmPFC/striatal offsets, Muller fatigue dynamics).

```
Healthy (original TRIBE v2 training)
  → Fine-tune on stress/threat data (ds002320: dynamic threat-of-shock)
    → Fine-tune on depression data (ds000171: emotional music + MDD)
      → Select SI+ subjects from ds005237 (transdiagnostic, C-SSRS scores)
        → [Active crisis: no data — ethical wall]
```

Each step produces a model variant whose predictions are closer to crisis physiology. The gap between "suicidal ideation" and "active 988 caller" cannot be bridged empirically — but the direction of change is characterized by the literature (more PFC suppression, more insula activation, blunted reward signals).

**Benchmark at every step**: Rerun Muller temporal dynamics test after each FT step. Verify: (a) escape-region sensitivity is preserved or improved (no catastrophic forgetting), (b) predictions shift in the direction predicted by the crisis literature (reduced vmPFC, elevated insula). The base model serves as the healthy comparison — the FT model is what we actually use.

**Validation**: The Dombrovski/Muller benchmarks serve double duty: they validate the instrument AND they confirm the FT moved predictions in the expected direction. If depression-tuned predictions show reduced vmPFC (matching Dombrovski) and accelerated cingulate fatigue (matching Muller), the adaptation is working and we use the FT model for all downstream measurements.

## 6. Problems That Emerge and Our Approach

| Problem | Where it surfaces | Approach |
|---------|-------------------|----------|
| Subcortical predictions missing | Pedersen requires NAcc, STN | Train output head on HCP data (staged, with gates) |
| Model trained on healthy subjects | Crisis callers have altered PFC function | Validate via Dombrovski benchmarks; FT on depression fMRI (ds000171) |
| Synthetic stimuli ≠ real music | Our tests used generated audio | Repeat all experiments with real music clips before drawing conclusions |
| Muller is about effort, not crisis | Fatigue model not validated in suicidal populations | Use as temporal dynamics benchmark only; Pedersen is the decision measure |
| Can't scan callers | No ground truth for crisis physiology | Constraint relaxation: validate on healthy → depression → suicide attempter literature |
| MusER too narrow for hold music | EMOPIA covers piano pop only | Use raw acoustic features; MusER becomes relevant only for generation |

## 7. Methodology

### Phase 1: Validate the Instrument (current)
- [x] Sensitivity test: does TRIBE v2 differentiate audio in escape-relevant regions? **YES (2-6x improvement with real music)**
- [x] Temporal dynamics: do predictions show Muller-consistent fatigue patterns? **YES (directionally consistent)**
- [ ] Subcortical probe: does frozen encoder contain subcortical signal? (Ridge regression on HCP, ~30 min)
- [ ] Subcortical head training (if probe positive): train output head, validate per-ROI R
- [ ] Dombrovski benchmark: vmPFC/insula/striatal patterns across conditions
- [ ] Retest all benchmarks after subcortical training (catastrophic forgetting check)

### Phase 2: Build the Measurement
- [ ] Formalize CEMP scoring function (weighted combination of region activations)
- [ ] Extend CEMP with subcortical components once head is trained
- [ ] Test Pedersen AAC-DDM parameter extraction from predicted subcortical activations
- [ ] Validate: does music that scores "low escape" differ systematically from "high escape" music?

### Phase 3: Generate Recommendations
- [ ] Curate candidate hold music library (50-100 clips)
- [ ] Run full pipeline: audio → TRIBE v2 → escape motivation score
- [ ] Extract acoustic features, correlate with escape scores
- [ ] Identify feature ranges that minimize escape motivation
- [ ] Deliverable: evidence-based hold music specification

### Phase 4: Validate Externally (stretch)
- [ ] Fine-tune on depression fMRI data (ds000171) to simulate crisis-adjacent physiology
- [ ] Test whether music recommendations transfer across healthy → depressed predictions

## 8. References

- Pedersen et al. 2021 — AAC-DDM, approach-avoidance in MDD (PLOS Comp Bio)
- Muller et al. 2021 — Recoverable/unrecoverable fatigue (Nature Communications)
- Dombrovski et al. 2013 — RL value signals in suicide attempters (JAMA Psychiatry)
- Millner et al. 2018 — Escape vs. avoidance via RL+DDM (J Cogn Neurosci)
- Mobbs et al. 2020 — Defensive hierarchy, vmPFC→PAG transition (Trends Cogn Sci)
- Malhi et al. 2022 — Entrapment neural correlates (Bipolar Disorders)
- Gilbert & Allan 1998 — Entrapment theory
- Casey 2017 — Music of the 7Ts, OFC encoding from music features (Frontiers Psychology)
- TRIBE v2 (d'Ascoli et al. 2026) — Foundation model for brain encoding
- MusER (Ji & Yang 2024) — Musical element-based regularization (AAAI)
- Ciferri et al. 2025 — CLAP-based fMRI encoding
