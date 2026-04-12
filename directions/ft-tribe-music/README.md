# Fine-Tune TRIBE v2 on Music fMRI Data

## Purpose
Improve TRIBE v2's audio→PFC predictions by fine-tuning on datasets where participants listened to music during fMRI scanning. The base model was trained on movie/podcast audio — FT on pure music should specialize the audio pathway for our use case.

## Motivation
Sensitivity test (2026-04-11) showed dACC rank 69/76, vmPFC rank 67/76 for synthetic audio. vlPFC/OFC at rank 15 is the bright spot. Casey et al. 2017 proved music features CAN predict OFC at 7T — so the mapping exists in biology, just not (yet) in our model.

## Critical Context
- TRIBE v2 FT is designed for this: paper shows single-epoch FT on new subjects → 2-4x improvement
- FT uses low-rank factorization (SVD, rank 128) for the subject block — memory efficient
- The question isn't "can we FT" but "does FT on music data lift PFC sensitivity specifically"
- Audio extractor (Wav2Vec-Bert) is frozen during FT — only the transformer + subject block are tuned

## What Does Working Look Like?
Run TRIBE v2 on real music → measure PFC activation variance → FT on ds000145 or ds000171 → re-measure. If PFC variance improves 3x+, this direction is alive. If flat, the bottleneck is in the frozen audio embeddings (→ pivot to a3/embeddings).

## Next Experiments
1. **[NOW] Real music baseline**: Download actual calming/anxious music, run through base model, compare PFC signal to synthetic test
2. **[NEXT] Download ds000145** (Music of the 7Ts) — check BIDS format, stimulus availability, compatibility with TRIBE v2 data pipeline
3. **[THEN] Single-epoch FT** on ds000145, re-run music sensitivity test, measure PFC improvement
4. **[IF WORKS] Extend to ds000171** (emotional music + depression cohort) for clinical-adjacent FT
