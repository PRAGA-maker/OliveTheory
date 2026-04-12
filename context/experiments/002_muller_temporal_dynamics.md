# Experiment 002: Muller Temporal Dynamics Validation

**Date**: 2026-04-12
**Duration**: ~45 min (3 stimuli x 5 min each)
**Status**: DIRECTIONALLY CONSISTENT — signs match Muller's predictions

## A. Motivation

Muller 2021 shows that fatigue-encoding brain regions (RCZp, RCZa, MFG, insula) have
NEGATIVE covariance with fatigue state: higher fatigue → lower BOLD activity. If TRIBE v2's
temporal predictions are valid, we should see:
- Aversive audio → decreasing cingulate/insula/MFG over time (fatigue accumulating)
- Calming audio → stable or increasing activation (fatigue not accumulating)
- Hold music → somewhere in between

## B. Design

Three 5-minute (300-second) synthetic stimuli, RMS-normalized:
- **calming_5min**: Cmaj9 spread voicing pad with slow attack
- **aversive_5min**: Dissonant minor 2nd/tritone cluster with escalating AM modulation
- **hold_5min**: I-vi-IV-V chord progression at 72 BPM, steady

300 predicted TRs per stimulus (1 Hz). Split into early/mid/late thirds (100 TRs each).

## C. Key Results

### Temporal trends in Muller fatigue regions (late minus early activation)

```
Region                  Role                   Aversive    Calming      Hold
dACC (RCZa-adj)        conflict/escape          -0.012     +0.062     +0.014
anterior MCC (RCZp)    recoverable fatigue      -0.071     +0.163     +0.009
posterior MCC           posterior cingulate      -0.049     +0.122     -0.003
MFG/dlPFC              unrecoverable fatigue    -0.036     +0.102     +0.005
ant. insula (circ)     aversive salience        -0.029     +0.100     +0.015
ant. insula (short)    salience network         -0.044     +0.112     +0.009
vmPFC                  value integration        +0.006     +0.016     +0.003
OFC/vlPFC              emotion regulation       +0.006     +0.069     -0.000
```

### Linear slopes (x1000 for readability)

```
Region                  Role                   Aversive    Calming      Hold
dACC                   RCZa-adjacent            -0.050     +0.285     +0.059
anterior MCC           RCZp-adjacent            -0.331     +0.713     +0.017
posterior MCC          posterior                 -0.219     +0.546     -0.017
MFG                    UF region                -0.149     +0.466     +0.022
ant. insula            interoception            -0.131     +0.449     +0.065
insula (short)         salience                 -0.208     +0.486     +0.022
vmPFC                  value                    +0.030     +0.072     +0.015
OFC                    regulation               +0.042     +0.319     +0.027
```

## D. Interpretation

### The signs are CORRECT.

In Muller's framework, fatigue regions show **negative** covariance with fatigue:
- Higher fatigue → LOWER activation (more suppression)
- Lower fatigue → HIGHER activation (less suppression)

Our results:
- **Aversive audio → all fatigue regions DECREASE over time** (slopes -0.05 to -0.33)
  → Consistent with fatigue ACCUMULATING (more suppression over time)
- **Calming audio → all fatigue regions INCREASE over time** (slopes +0.28 to +0.71)
  → Consistent with fatigue NOT accumulating / dissipating (less suppression)
- **Hold music → flat** (slopes -0.02 to +0.07)
  → Consistent with neutral/low fatigue effect

vmPFC (value region) shows the SMALLEST trends — consistent with Muller, where
vmPFC encodes subjective value, not fatigue directly.

### The magnitudes are DIFFERENTIATED.

The calming-vs-aversive gap in anterior MCC (the closest proxy for RCZp):
- Calming: +0.163 (increasing)
- Aversive: -0.071 (decreasing)
- **Gap: 0.234** — a large difference in temporal trajectory

This means: over 5 minutes, the model predicts a DIVERGING cingulate response.
Calming music → cingulate activation increases (less fatigue). Aversive music →
cingulate activation decreases (more fatigue). This is exactly the temporal
dynamics that would predict different hang-up latencies.

## E. Caveats

1. **These are PREDICTED fMRI, not real fMRI.** The temporal dynamics could be artifacts
   of TRIBE v2's 100-second context window, not genuine neural adaptation.
2. **Stimuli are synthetic.** The calming pad has a slow attack that could drive the
   increasing trend independently of any "fatigue" mechanism.
3. **N=1 per condition.** No statistical power. This is a plausibility check, not proof.
4. **Muller's model is about EFFORT, not audio.** The mapping from physical effort
   fatigue to audio aversion fatigue is an analogy, not a validated equivalence.

## F. Verdict

**The Muller benchmark is directionally passed.** TRIBE v2 predicts temporal dynamics
in fatigue-encoding regions that match the expected direction: aversive audio →
increasing fatigue (decreasing activation), calming audio → decreasing fatigue
(increasing activation). Hold music is approximately neutral.

This doesn't prove the model accurately simulates fatigue dynamics. It demonstrates
that the model's temporal predictions in escape-relevant regions are AT LEAST
consistent with the framework we're using.

**Next**: Repeat with real music clips to rule out synthetic-stimulus artifacts.
Then run against actual fMRI temporal data (ds000113/studyforrest) to calibrate.
