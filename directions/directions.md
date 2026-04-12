# Research Directions — Master Index

Living document. Update as directions mature, merge, or die.

## Active Directions

### a1. ft-tribe-music/
**Pitch**: Fine-tune TRIBE v2 on music-specific fMRI data to lift PFC sensitivity from rank 67→usable.
**Status**: TESTING — running real music through base model to establish baseline before FT.
**Key question**: Is the weak PFC signal a model limitation or a stimulus limitation? (synthetic tones vs. real music)
**Dependencies**: Subcortical audit (a2) determines if we also need subcortical FT.
**Datasets**: ds000145 (Music of 7Ts, 7T), ds000171 (emotional music + depression), ds003720 (GTZAN-fMRI)
**Blocking risk**: If TRIBE v2 architecture fundamentally can't propagate audio signal to PFC, FT won't help.

### a2. subcortical-audit/
**Pitch**: The released checkpoint is cortical-only (20,484 vertices). Paper describes subcortical pathway (8,802 voxels). Find it or build it.
**Status**: RESOLVED — no pre-trained subcortical checkpoint exists. Training config exists in code (`run_subcortical.py`) but requires retraining. Decision: accept cortical-only for now. vmPFC/dACC/OFC/insula are cortical and available. PAG is brainstem, probably too deep even for the subcortical model.
**Key question**: ~~Does the subcortical checkpoint exist?~~ → No. Proceed cortical-only.
**Dependencies**: None.
**Blocking risk**: LOW — critical escape regions (vmPFC, dACC, OFC, anterior insula) are all cortical.

### a3. ft-tribe-embeddings/
**Pitch**: Replace Wav2Vec-Bert with CLAP or music-specific embeddings to get better emotion-relevant audio features into TRIBE v2's input.
**Status**: IDEA — Ciferri et al. 2025 showed CLAP→fMRI encoding gets IFG. Casey 2017 showed chromagram features predict OFC.
**Key question**: Can we swap the audio extractor in TRIBE v2 without retraining the whole model? (Likely no — but CLAP→ridge regression as a parallel path is cheap.)
**Dependencies**: ft-tribe-music results inform whether embeddings are the bottleneck.
**Blocking risk**: Low. CLAP ridge regression is a fallback regardless.

### a4. construct-mapping/
**Pitch**: "Escape motivation" isn't a canonical construct. Map the taxonomy: entrapment (Gilbert & Allan), escape (Millner RL+DDM), defensive flight (Mobbs), fatigue-driven quitting (Muller). Pick measurable proxies, don't over-define.
**Status**: RULER IDENTIFIED — Muller 2021 fatigue model is the best available. Maps RF→RCZp, UF→RCZa/MFG/insula, SV→VS/SFG. Parameters need behavioral fitting but REGION SIGNALS can serve as proxies from predicted fMRI. Operational definition drafted in pointers/.
**Key question**: ~~Which construct?~~ → Muller fatigue model. Now: does TRIBE v2 have enough signal in RCZp/RCZa for this to work?
**Dependencies**: ft-tribe-music results (do real music stimuli differentiate fatigue-encoding regions?)
**Blocking risk**: Low — this is a framing choice that's now made. Awaiting empirical validation.

### b. muser-recon/
**Pitch**: MusER decomposes symbolic music into emotion-relevant features (tempo, pitch, velocity, chord). Assess SOTA, coverage, and whether it's useful as the "feature language" for hotline recommendations.
**Status**: CLONED to external/MusER/. Needs benchmarking.
**Key question**: Does MusER's VQ-VAE codebook cover the kind of music we'd use (ambient, calming, hold music) or just piano pop?
**Dependencies**: Independent. Can run anytime.
**Blocking risk**: Low. MusER is a nice-to-have for the recommendation layer, not the core bridge.

## Parked / Watch

- **DIM (Tron & Fioresi 2024)**: Quantify domain gap between TRIBE v2's training audio and our target stimuli. Useful but slow. Run after fast tests indicate viability.
- **Crisis FT**: Fine-tune on ds002320 (dynamic threat) or ds005237 (transdiagnostic + C-SSRS). Depends on whether base model shows any escape-relevant signal first.
- **CLAP parallel path**: Build a simple CLAP→ridge regression→fMRI pipeline as TRIBE v2 alternative. Cheap fallback if FT path dies.

## Dead / Abandoned

(none yet)

## Decision Log

| Date | Decision | Reasoning |
|------|----------|-----------|
| 2026-04-11 | Replaced phantom citations (Dore 2023, Goldfarb 2020) | Grok confirmed non-existent. Replaced with Malhi 2022, Muller 2021, Dombrovski 2013. |
| 2026-04-11 | Synthetic sensitivity test shows PFC rank 67-69 | dACC/vmPFC near-flat for synthetic tones. vlPFC/OFC rank 15. Need real music test. |
| 2026-04-11 | Released checkpoint is cortical-only | n_outputs=20484. Subcortical pathway not in public model. Training config exists but no pre-trained weights. |
| 2026-04-11 | Adopted Muller 2021 fatigue model as "ruler" | RF/UF brain signals (RCZp, RCZa, MFG) as proxy for quit propensity. Parameters need behavior, but region signals work from predicted fMRI. |
| 2026-04-11 | MusER/EMOPIA coverage is narrow | Piano pop only. Won't generalize to ambient/hold music. Use MIRtoolbox features directly instead. |
| 2026-04-12 | Real music pressure test PASSED | 2-6x PFC improvement over synthetic. Insula rank 26, OFC rank 23, dACC rank 49, vmPFC rank 59. Model is viable. |
| 2026-04-12 | Pedersen AAC-DDM is mostly subcortical | 3/4 brain regions (NAcc, STN, caudate) unavailable. pgACC drift-rate is the only cortical component. |
| 2026-04-12 | Measurement framework: CEMP | Cortical Escape Motivation Profile. Pattern-based measure across insula/dACC/vmPFC/OFC. Validated via Muller (temporal) + Dombrovski (physiology). Applied via activation pattern, not fitted DDM. |
