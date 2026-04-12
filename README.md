# OliveTheory

Half of 988 Suicide Hotline callers hang up before reaching a counselor. We think the right hold music -- chosen with actual neuroscience, not vibes -- could change that.

## What's going on

When someone calls 988 and gets put on hold, they're making a continuous decision: stay or hang up. At some point the pain of waiting wins and they leave. This is escape motivation -- the brain's process for deciding to terminate an aversive situation.

This isn't hand-wavy. There's a real computational literature on how the brain makes this kind of decision. Millner et al. (2018) formalized escape vs. avoidance using RL+DDM. Mobbs mapped the neural switch from deliberative patience to reactive flight. Doré showed how entrapment -- basically the psychological state of a suicidal caller -- degrades the brain's ability to override the impulse to bail.

So the pieces exist in the literature. What doesn't exist is the connection: music features → brain response → escape motivation. That's what this project is trying to build.

## The goal

Find a fully computational, mechanistically grounded pipeline from **music features** (including emotion) to **physiological signal** (brain activity) to **escape motivation** (hang-up propensity). Every link in that chain needs to be backed by existing research (with ideally mechanistic reasoning), and every step needs to be validated -- not assumed.

## Research Plan

See **[context/researchplan.md](context/researchplan.md)** for the full methodology.

**Pipeline**: Audio → TRIBE v2 (predicted brain activation) → Escape motivation measurement → Hold music recommendations

**Three components**:
1. **Audio → Brain**: TRIBE v2 + subcortical extension (training a new output head for NAcc, amygdala, caudate, thalamus)
2. **Brain → Escape Motivation**: Validated via Muller (temporal fatigue dynamics) and Dombrovski (attempter physiology), measured via Pedersen (approach-avoidance DDM) and CEMP (cortical escape motivation profile)
3. **Music → Features**: Acoustic feature extraction correlated with escape motivation scores → actionable specifications for hold music

**Current status**: TRIBE v2 cortical predictions validated — real music produces 2-6x stronger signal in escape-relevant regions than synthetic tones. Temporal dynamics match Muller's fatigue model. Subcortical head training in progress.

## What's here

```
tribev2/              # TRIBE v2 brain encoding model (facebookresearch, local dep)
directions/           # Research directions with living READMEs
context/              # Research plan, experiment writeups, model setup docs
experiments/          # Reusable benchmark scripts (Muller temporal dynamics)
papers/               # Reference papers and text extractions
external/MusER/       # MusER music emotion model (cloned)
bench.py              # GPU benchmarking
xai_cli.py            # Grok API -- search + reasoning
gemini_cli.py         # Gemini API -- deep research + long context
CLAUDE.md             # Research operating instructions
```

## References

- Pedersen et al. 2021 -- AAC-DDM, approach-avoidance in MDD ([paper](https://doi.org/10.1371/journal.pcbi.1008955))
- Millner et al. 2018 -- Escape vs. avoidance via RL+DDM
- Mobbs et al. 2020 -- Defensive hierarchy, vmPFC→PAG transition
- Müller et al. 2021 -- Recoverable/unrecoverable fatigue in effort-based choice (Nature Communications)
- Malhi et al. 2022 -- Entrapment neural correlates in suicide attempters (fMRI, Bipolar Disorders)
- Dombrovski et al. 2013 -- RL-based value signals in suicide attempters (fMRI, striatum/PFC)
- Gilbert & Allan 1998 -- Entrapment theory
- Tron & Fioresi 2024 -- Data Information Matrix for transfer learning ([paper](https://arxiv.org/abs/2409.07412))
- TRIBE v2 -- [paper](https://ai.meta.com/research/publications/a-foundation-model-of-vision-audition-and-language-for-in-silico-neuroscience/) / [code](https://github.com/facebookresearch/tribev2)
- MusER -- [paper](https://arxiv.org/abs/2312.10307) / [code](https://github.com/Tayjsl97/MusER)
