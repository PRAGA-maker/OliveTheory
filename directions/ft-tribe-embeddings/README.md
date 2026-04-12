# Alternative Audio Embeddings for Brain Encoding

## Purpose
Test whether replacing TRIBE v2's Wav2Vec-Bert audio features with emotion-aware embeddings (CLAP, MusicLM, chromagram) improves PFC prediction.

## Motivation
Wav2Vec-Bert was trained on speech — it captures phonemic/prosodic structure well but may not encode the timbral/harmonic features that drive emotional responses to music. CLAP (Contrastive Language-Audio Pretraining) maps audio to a joint audio-language space that captures semantic/emotional content.

## Critical Context
- Ciferri et al. 2025: CLAP→ridge regression→fMRI gets bilateral STG + IFG. Open source.
- Casey et al. 2017: Simple chromagram/melodic features predict OFC at 7T.
- TRIBE v2's audio extractor is FROZEN during FT — swapping it means either:
  (a) Retrain TRIBE v2 from scratch with new embeddings (expensive, needs Meta's data pipeline)
  (b) Build a parallel ridge regression path: CLAP embeddings → fMRI voxels (cheap, 1 day)
- Option (b) is the pragmatic path. TRIBE v2 for auditory cortex, CLAP ridge for PFC.

## What Does Working Look Like?
A simple script: audio → CLAP embeddings → ridge regression → predicted PFC activation. Trained on ds000145 or ds003720 (GTZAN-fMRI). If PFC predictions are meaningful, this becomes our "PFC bridge" independent of TRIBE v2.

## Next Experiments
1. **[BLOCKED BY ft-tribe-music]** First see if base TRIBE v2 with real music gives adequate PFC signal
2. **[IF NOT] Download Ciferri repos** and reproduce their CLAP→fMRI pipeline
3. **[THEN] Test on music stimuli** that matter for our use case
