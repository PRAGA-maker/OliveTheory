# Real Music Pressure Test — Status

**Started**: 2026-04-12 ~01:00
**Status**: RUNNING (3 of 6 stimuli completed as of 01:15)

## Stimuli (musically richer than synthetic test)
1. calming_pad — Cmaj9 spread voicing, slow 3s attack (DONE)
2. anxious_texture — minor 2nds + tritone + irregular AM (DONE)
3. gentle_progression — I-vi-IV-V in C major, 60 BPM (PROCESSING)
4. tense_progression — diminished chords, 100 BPM, tremolo (PENDING)
5. hold_music — C major pad + pentatonic melody, 80 BPM (PENDING)
6. nature_ambience — pink noise + 80Hz drone (PENDING)

## What we're looking for
Compare PFC region variance (real music) vs. PFC region variance (synthetic tones).
Key regions: dACC (rank 69 synthetic), vmPFC (rank 67), vlPFC/OFC (rank 15),
anterior insula (rank 56), MFG (rank 45).

**Hypothesis**: Real music with harmonic structure should produce stronger PFC
differentiation than synthetic sine waves. The warm_chord stimulus (most "musical"
of the synthetic set) already showed the strongest PFC response.

## Bottleneck
Wav2Vec-Bert feature extraction runs mostly on CPU (~12.9GB RAM).
Each new 30s clip takes ~5-8 min. Features are cached after first extraction.
