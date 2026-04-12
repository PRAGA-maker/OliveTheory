# EMOPIA / MusER Coverage Assessment

## EMOPIA Dataset
- 1,087 clips from 387 songs, ~11 hours
- Piano pop ONLY (Japanese anime, K-pop, Western pop covers, movie soundtracks — all solo piano)
- Russell valence-arousal quadrants: Q1 happy (250), Q2 anxious (265), Q3 sad (253), Q4 calm (310)
- Major keys skew to high-valence, minor to low-valence
- No tempo statistics published

## Generalization to ambient/hold music: POOR
- Domain shift: piano solo vs. synth pads/drones
- Rhythm mismatch: pop beats vs. arrhythmic/steady pulses  
- Structure mismatch: verse-chorus pop vs. evolving ambient textures
- Instrumentation: single piano vs. multi-timbral

## Better alternatives for broader music-emotion coverage
| Dataset | Size | Why |
|---------|------|-----|
| DEAM | 2k clips, multi-genre | Continuous V-A, per-second annotations |
| MTG-Jamendo | 18k clips, 87 genres | Broad genre coverage |
| XMIDI | 108k MIDI, wide genres | Symbolic, 100x larger |
| Music4all | 109k clips | Massive, diverse |

## Verdict
MusER trained on EMOPIA won't generalize to hold music out of the box. 
Options: (a) retrain on broader dataset (DEAM, XMIDI), (b) use simpler
MIRtoolbox features directly (tempo, spectral centroid, roughness, mode),
(c) use MusER architecture but retrain on ambient/hold music MIDI.

Option (b) is probably the right one for now — we don't need disentangled
latent space, we need "what features correlate with the brain regions we care about."
