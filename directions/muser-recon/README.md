# MusER Reconnaissance

## Purpose
Assess MusER's utility as the "feature language" for hold music recommendations. If the brain-encoding pipeline works, MusER tells us *which features* (tempo, pitch, velocity, chord) to optimize in the music that hotlines play.

## Motivation
The end goal isn't just "calming music reduces escape motivation" — it's "these specific musical parameters, in these ranges, produce the brain response we want." MusER decomposes symbolic music into disentangled elements with emotion labels.

## Critical Context
- MusER is a VQ-VAE trained on EMOPIA (piano pop dataset). Codebook coverage for ambient/hold music is unknown.
- I/O is MIDI/symbolic, not raw audio. Needs audio→MIDI transcription as preprocessing.
- Trained checkpoints available on HuggingFace (TaylorJi/MusER).
- AAAI 2024 paper. Moderate citation count.
- Cloned to external/MusER/.

## What Does Working Look Like?
Run MusER on MIDI transcriptions of candidate hold music. Inspect the latent space — do different emotional categories separate? Do the disentangled elements (tempo, harmony, etc.) make musical sense for our use case? If codebook is too narrow (piano pop only), this tool is limited.

## Next Experiments
1. **Check EMOPIA dataset** — what's the genre/tempo/key distribution? How far from hold music?
2. **Run VQ_explore.py** on a few MIDI files to visualize the latent space
3. **Assess audio→MIDI transcription** quality for ambient/hold music (likely lossy — flag if so)
4. **Decision**: useful feature language, or too narrow? If narrow, look at alternatives (e.g., MIRtoolbox features directly)
