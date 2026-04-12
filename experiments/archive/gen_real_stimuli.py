"""
Generate musically richer stimuli for the TRIBE v2 pressure test.

These aren't just sine waves — they use additive synthesis with harmonics,
amplitude modulation, reverb-like effects, and musical progressions to
approximate real music more closely while staying fully reproducible.
"""

import numpy as np
import soundfile as sf
from pathlib import Path
import os

SR = 16000
DURATION = 30
t = np.linspace(0, DURATION, SR * DURATION, endpoint=False)
rng = np.random.default_rng(42)

OUT = Path("stimuli/real")
OUT.mkdir(parents=True, exist_ok=True)


def note_freq(midi_note):
    return 440.0 * 2 ** ((midi_note - 69) / 12)


def synth_note(freq, t, harmonics=6, decay=0.3):
    """Additive synthesis with harmonic rolloff."""
    signal = np.zeros_like(t)
    for h in range(1, harmonics + 1):
        amp = 1.0 / (h ** decay)
        signal += amp * np.sin(2 * np.pi * freq * h * t)
    return signal / harmonics


def soft_pad(freqs, t, attack=2.0, release=1.0):
    """Soft ambient pad from multiple frequencies with slow attack."""
    signal = np.zeros_like(t)
    for f in freqs:
        signal += synth_note(f, t, harmonics=8, decay=0.5)
    # Envelope
    env = np.clip(t / attack, 0, 1) * np.clip((DURATION - t) / release, 0, 1)
    return (signal * env * 0.15).astype(np.float32)


def chord_progression(chords, beats_per_chord, bpm, t):
    """Simple chord progression with crossfade."""
    beat_dur = 60.0 / bpm
    chord_dur = beats_per_chord * beat_dur
    signal = np.zeros_like(t)
    for i, chord_freqs in enumerate(chords):
        start = i * chord_dur
        end = start + chord_dur
        mask = (t >= start) & (t < end)
        # Crossfade
        local_t = t[mask] - start
        env = np.clip(local_t / 0.5, 0, 1) * np.clip((chord_dur - local_t) / 0.5, 0, 1)
        for f in chord_freqs:
            signal[mask] += env * synth_note(f, local_t, harmonics=6, decay=0.4)
    return signal


stimuli = {}

# 1. CALMING AMBIENT PAD — C major 7 spread voicing, very slow
# C3, E3, G3, B3, D4 — Cmaj9 voicing
calming_freqs = [note_freq(n) for n in [48, 52, 55, 59, 62]]
stimuli["calming_pad"] = soft_pad(calming_freqs, t, attack=3.0)

# 2. ANXIOUS DISSONANT TEXTURE — minor 2nds, tritone, irregular AM
anx_freqs = [note_freq(n) for n in [48, 49, 54, 60, 61]]  # C3, Db3, Gb3, C4, Db4
anx_base = soft_pad(anx_freqs, t, attack=0.5)
# Add irregular amplitude modulation (anxiety = unpredictability)
am = 0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t) * np.sin(2 * np.pi * 1.7 * t)
stimuli["anxious_texture"] = (anx_base * am).astype(np.float32)

# 3. GENTLE CHORD PROGRESSION — I-vi-IV-V in C major, 60 BPM
# Cmaj, Am, Fmaj, Gmaj — each 4 beats at 60bpm = 4s per chord
chords_gentle = [
    [note_freq(n) for n in [48, 52, 55]],  # C
    [note_freq(n) for n in [45, 48, 52]],  # Am
    [note_freq(n) for n in [41, 45, 48]],  # F
    [note_freq(n) for n in [43, 47, 50]],  # G
] * 2  # repeat to fill ~32s
prog = chord_progression(chords_gentle, 4, 60, t)
stimuli["gentle_progression"] = (prog * 0.12).astype(np.float32)

# 4. TENSE PROGRESSION — diminished chords, faster, 100 BPM
chords_tense = [
    [note_freq(n) for n in [48, 51, 54]],  # Cdim
    [note_freq(n) for n in [49, 52, 55]],  # Dbdim
    [note_freq(n) for n in [50, 53, 56]],  # Ddim
    [note_freq(n) for n in [51, 54, 57]],  # Ebdim
] * 3
prog_tense = chord_progression(chords_tense, 2, 100, t)
# Add tremolo
tremolo = 0.7 + 0.3 * np.sin(2 * np.pi * 5 * t)
stimuli["tense_progression"] = (prog_tense * tremolo * 0.12).astype(np.float32)

# 5. TYPICAL HOLD MUSIC — major key, moderate tempo (80 BPM), simple melody + pad
# Pad: C major
hold_pad = soft_pad([note_freq(n) for n in [48, 52, 55]], t, attack=2.0) * 0.5
# Simple melody: pentatonic, quarter notes at 80 BPM
melody_notes = [60, 62, 64, 67, 69, 67, 64, 62] * 5  # C pentatonic
beat_dur = 60.0 / 80
melody_signal = np.zeros_like(t)
for i, note in enumerate(melody_notes):
    start = i * beat_dur
    end = start + beat_dur
    mask = (t >= start) & (t < end)
    local_t = t[mask] - start
    env = np.clip(local_t / 0.05, 0, 1) * np.exp(-local_t * 2)
    melody_signal[mask] += env * synth_note(note_freq(note), local_t, harmonics=4, decay=0.6)
stimuli["hold_music"] = (hold_pad + melody_signal * 0.08).astype(np.float32)

# 6. NATURE AMBIENCE APPROXIMATION — filtered noise + low drone
# Pink-ish noise (rolled off high freq)
white = rng.standard_normal(len(t)).astype(np.float32)
# Simple low-pass via cumulative average (crude but effective for test)
from scipy.signal import butter, sosfilt
sos = butter(4, 2000, btype='low', fs=SR, output='sos')
pink_ish = sosfilt(sos, white) * 0.15
# Low drone
drone = 0.08 * np.sin(2 * np.pi * 80 * t)
stimuli["nature_ambience"] = (pink_ish + drone).astype(np.float32)

# Normalize all to same RMS
target_rms = 0.05
for name in stimuli:
    s = stimuli[name]
    rms = np.sqrt(np.mean(s ** 2))
    if rms > 0:
        stimuli[name] = (s * target_rms / rms).astype(np.float32)

for name, audio in stimuli.items():
    sf.write(str(OUT / f"{name}.wav"), audio, SR)
    print(f"  {name}: {len(audio)/SR:.1f}s, RMS={np.sqrt(np.mean(audio**2)):.4f}")

print(f"\nGenerated {len(stimuli)} stimuli in {OUT}/")
