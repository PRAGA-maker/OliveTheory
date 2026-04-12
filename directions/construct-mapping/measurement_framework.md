# Measurement Framework: Escape Motivation from Audio

## The Problem
We want to measure: "How does music X vs. music Y affect a 988 caller's propensity to hang up?"

We can't put callers in a scanner. We CAN predict brain activation from audio using TRIBE v2 and measure whether that predicted activation matches patterns known to promote escape vs. persistence.

## The Measure: Cortical Escape Motivation Profile (CEMP)

The primary measurement is a **predicted activation pattern** across escape-relevant cortical regions, not a single scalar. For a given audio stimulus, TRIBE v2 predicts activation in:

| Region | Role in escape | Interpretation | Direction |
|--------|---------------|----------------|-----------|
| Anterior insula (short gyri) | Aversive salience | "How bad does this feel?" | High → escape |
| Anterior insula (circular) | Interoceptive awareness | "Am I distressed?" | High → escape |
| dACC (G_and_S_cingul-Ant) | Conflict monitoring | "Should I stay or go?" | High → conflict |
| vmPFC (G_rectus) | Value integration / safety | "Is staying worth it?" | Low → escape |
| vlPFC/OFC | Emotion regulation | "Can I manage this?" | Low → escape |
| pgACC (anterior cingulate) | Reward-aversion drift | "Is the reward of waiting winning?" | Approach-favoring drift → persist |

**Escape-promoting pattern**: High insula + high dACC + low vmPFC + low OFC
**Persistence-promoting pattern**: Low insula + positive vmPFC + low dACC + stable OFC

Music that shifts the pattern toward persistence is predicted to reduce hang-up probability.

## Validation Layer: "Can We Trust the Instrument?"

Before using CEMP to evaluate hold music, we benchmark against known physiology.

### Benchmark 1: Muller Fatigue Dynamics (ALL CORTICAL — most falsifiable)

**What Muller showed**: During sustained effort, RCZp (cingulate) encodes recoverable fatigue, RCZa + MFG + insula encode unrecoverable fatigue. Fatigue accumulates → SV drops → quit.

**Our test**: Feed TRIBE v2 a 5-minute audio sequence. Does predicted dACC/insula activation change over time? Does it follow the pattern of accumulating fatigue (initial stability → gradual increase)? Does calming music show slower accumulation than aversive music?

**Regions needed**: dACC, MFG, insula — ALL cortical, ALL available (rank 49, 45, 26 respectively).

**Pass criterion**: Temporal dynamics of predicted cingulate/insula activation differentiate calming vs. aversive audio AND show increasing activation over time (fatigue accumulation).

### Benchmark 2: Dombrovski Attempter Physiology (PARTIALLY TESTABLE)

**What Dombrovski showed**: Suicide attempters have blunted ventral striatal prediction errors and reduced vmPFC value signals. Under crisis, this makes escape look relatively more attractive.

**Our test**: Can we detect vmPFC value differences across audio conditions? Does our model predict that aversive audio produces lower vmPFC activation (paralleling reduced value integration)?

**Regions needed**: vmPFC (rank 59, weak but available), insula (rank 26, strong). Ventral striatum NOT available.

**Pass criterion**: vmPFC shows condition-dependent activation consistent with value integration theory. We already see this: nature ambience → positive vmPFC (+0.009), tense music → negative vmPFC (-0.043).

**Limitation**: Cannot test striatal PE component. Document this gap.

### Benchmark 3: Pedersen pgACC Drift Rate (PARTIALLY TESTABLE)

**What Pedersen showed**: pgACC modulates drift rate (reward vs. aversion sensitivity) in approach-avoidance decisions. In MDD, this contributes to reduced approach tendency.

**Our test**: Does pgACC (anterior cingulate) activation differentiate music conditions in a way consistent with drift-rate modulation? Music with more reward-associated features (tonal, consonant, predictable) should produce different pgACC patterns than aversive music.

**Regions needed**: pgACC (maps to dACC/anterior cingulate — rank 49, available). NAcc, STN, caudate NOT available.

**Pass criterion**: pgACC activation pattern is interpretable as drift-rate modulation.

## Decision Layer: "What Should the Hold Music Be?"

Once benchmarks pass, CEMP becomes a validated instrument. We use it to:

1. **Screen candidate hold music**: Run N audio clips through TRIBE v2, compute CEMP for each
2. **Rank by persistence-promoting pattern**: Lower insula, higher vmPFC, lower dACC → better hold music
3. **Identify musical features driving the pattern**: Correlate CEMP scores with acoustic features (tempo, spectral centroid, consonance, etc.) — this is where MIRtoolbox or MusER-style decomposition becomes useful
4. **Generate specific recommendations**: "Hold music should have tempo in range X, harmonic structure Y, spectral profile Z" — backed by predicted brain activation, not vibes

## What This Framework Does NOT Cover

1. **Active escape impulse** (Millner's Pavlovian bias): We measure predicted activation states, not action tendencies. The model tells us which music produces escape-favoring brain patterns, not which music a distressed person would behaviorally react to.

2. **Subcortical dynamics** (NAcc, PAG, amygdala): Blocked by cortical-only checkpoint. If subcortical model becomes available (GitHub Issue #23), the framework expands to include Pedersen's full parameter set and Dombrovski's striatal PE.

3. **Individual differences**: TRIBE v2's unseen-subject mode predicts group-average activation. Crisis callers are not average — they have altered PFC function (entrapment literature). Fine-tuning on depression fMRI data (ds000171) could address this.

4. **Real-time dynamics**: This framework evaluates static audio clips. The 988 scenario involves dynamic state evolution over minutes. Benchmark 1 (Muller temporal dynamics) partially addresses this.

## Implementation Priority

1. **[NOW] Muller temporal dynamics test** — longest audio sequences, measure dACC/insula temporal evolution
2. **[NEXT] Formalize CEMP scoring** — define the index mathematically (weighted combination of region activations)
3. **[THEN] Run candidate hold music through CEMP** — screen real music clips
4. **[LATER] Fine-tune on ds000113 (music fMRI)** to improve PFC sensitivity
5. **[IF AVAILABLE] Extend to subcortical** with released checkpoint
