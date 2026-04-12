# OliveTheory

Half of 988 Suicide Hotline callers hang up before reaching a counselor. We're building a computational framework to predict and prevent that.

## Quick Start

1. **Clone** — `git clone https://github.com/PRAGA-maker/OliveTheory.git`
2. **Add keys** — copy `.env.example` to `.env` and fill in your API keys
3. **Go** — `uv sync && claude`

## The Problem

A person calls 988. They're put on hold. At some point, the subjective cost of waiting exceeds the discounted value of reaching a counselor -- and they hang up. This is escape motivation: the computational decision to terminate an ongoing aversive state.

This isn't abstract. Millner et al. (2018) formalized escape vs. avoidance via RL+DDM, showing escape as a starting-point bias (w_escape) toward the "go" boundary. The neural substrates are mapped: ventral anterior insula (psychological pain signal), dACC/MCC (effort cost / urgency), vmPFC (persistence value / future discounting), PAG (reactive escape execution). In entrapment states -- which describe suicidal callers well (Gilbert & Allan, 1998) -- vAI hyperactivates while vAI-SFG connectivity degrades, meaning top-down control over the escape impulse fails.

The question: can we computationally model this decision process and intervene with targeted acoustic stimuli (hold music) to shift the decision boundary toward persistence?

## The Approach

### 1. Computational Phenotype of Abandonment

Model hang-up as an RLDDM process:
```
Hang-up probability(t) = f(Escape Urgency - Persistence Value)

Parameters:
  w_escape     — starting-point bias toward hang-up (vAI activation)
  v_drift      — evidence accumulation rate
  alpha_neg    — learning rate for "waiting is futile" (dACC-striatal)
  k_loss       — loss aversion amplifier (anterior insula; elevated in attempters)
  UF           — unrecoverable fatigue accumulation (MFG/RCZa)
```

### 2. fMRI Encoding → Brain Response Prediction

This is where TRIBE v2 comes in. It predicts whole-brain fMRI responses from audio/video/text stimuli, trained on 1000+ hours across 720 subjects. We can use it to predict how a given person's brain responds to specific acoustic stimuli -- without putting them in a scanner during a crisis.

### 3. Music Emotion Decomposition → Targeted Intervention

MusER decomposes music into emotion-disentangled elements (pitch, velocity, tempo, chord → valence/arousal). If we can map which musical elements drive activity in which escape-relevant brain regions (vmPFC, vAI, dACC), we can design hold music that:
- **Upregulates vmPFC** (increase persistence value / patience)
- **Downregulates vAI** (reduce psychological pain signal)
- **Restores vAI-SFG connectivity** (top-down control over escape impulse)

### 4. The Bridge

TRIBE v2 and MusER were never designed to talk to each other. The bridge:
- Movie soundtracks already contain music that TRIBE v2 learned brain responses to
- Demucs source-separates the music → basic-pitch transcribes to MIDI → MidiTok tokenizes to MusER's input format
- MusER's 7 disentangled element subspaces can then be correlated with TRIBE v2's per-region brain predictions
- This tells us: which musical features predict which brain region activity

## Constraint Relaxation

The full target (predicting hang-up in actively suicidal callers) requires phased validation:

1. **Phase 1 — Proof of concept** (acute stress, non-clinical): Induce entrapment via unsolvable task. Validate RLDDM w_escape predicts quitting behavior.
2. **Phase 2 — Clinical validation** (suicidal ideators, non-acute): Demonstrate vAI-SFG connectivity predicts persistence in effort-based tasks.
3. **Phase 3 — Target population** (attempters / actively suicidal): Acoustic intervention modulates PAG/vmPFC transition per Mobbs defensive-distance model.

## Directions to Examine

1. **MusER ↔ TRIBE v2 bridge** — Which musical elements predict which brain regions? Domain validation (are movie soundtracks in-distribution for MusER?), temporal alignment, RSA.
2. **Escape motivation parameterization** — Can we extract RLDDM parameters from TRIBE v2's predicted brain responses? Map w_escape to vAI activation patterns.
3. **Acoustic intervention design** — Which acoustic features (tempo, dissonance, predictability) drive vmPFC activation in high-entrapment phenotypes?
4. **MVT framing** — Model hang-up as optimal patch-leaving (Marginal Value Theorem). Individual leaving thresholds, switching costs, average reward rate.

## Key References

- **Escape/Avoidance Computation**: Millner et al. 2018; Fontanesi et al. 2019
- **Pain-Avoidance Learning**: Oba et al. 2024
- **Loss Aversion in Attempters**: Liu et al. 2022
- **Entrapment Theory**: Gilbert & Allan 1998; DeLisle & Williams 2012
- **Entrapment Neural Signature**: Doré et al. 2023
- **Persistence/Quit Decision**: Goldfarb et al. 2020; Shen et al. 2015
- **Defensive Hierarchy**: Mobbs et al. 2020
- **fMRI Neurofeedback**: Olson et al. 2024; Misaki et al. 2023
- **TRIBE v2**: [Paper](https://ai.meta.com/research/publications/a-foundation-model-of-vision-audition-and-language-for-in-silico-neuroscience/) | [Code](https://github.com/facebookresearch/tribev2)
- **MusER**: [Paper](https://arxiv.org/abs/2312.10307) | [Code](https://github.com/Tayjsl97/MusER)

## Structure

```
.
├── CLAUDE.md              # Research operating instructions
├── .claude/               # Claude settings (permissions)
├── .env.example           # API key template (copy to .env)
├── xai_cli.py             # Grok API CLI (think + web search)
├── gemini_cli.py          # Gemini API CLI (think + deep research)
├── papers/                # Reference papers
│   ├── tribev2.pdf        # TRIBE v2 paper (27 pages)
│   └── tribev2.txt        # Text extraction
├── tribev2/               # TRIBE v2 source (local dep)
├── bench.py               # GPU benchmarking
├── outputs/               # Research outputs (gitignored)
└── pyproject.toml         # Project config (uv)
```
