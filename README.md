# OliveTheory

Half of 988 Suicide Hotline callers hang up before reaching a counselor. We think the right hold music -- chosen with actual neuroscience, not vibes -- could change that.

## Setup

```bash
cp .env.example .env   # add your XAI_API_KEY and GEMINI_API_KEY
uv sync && claude
```

## What's going on

When someone calls 988 and gets put on hold, they're making a continuous decision: stay or hang up. At some point the pain of waiting wins and they leave. This is escape motivation -- the brain's process for deciding to terminate an aversive situation.

This isn't hand-wavy. There's a real computational literature on how the brain makes this kind of decision: reinforcement learning models that track how quickly someone learns "waiting is futile," drift-diffusion models that measure how biased someone is toward quitting before they even start, and fMRI work showing which regions encode the cost of staying vs. the value of what you're waiting for. Millner et al. (2018) formalized escape vs. avoidance in exactly this framework. Mobbs mapped the neural switch from deliberative patience to reactive flight. Doré showed how entrapment -- which is basically the psychological state of a suicidal caller -- degrades the brain's ability to override the impulse to bail.

So the pieces exist. What doesn't exist is anyone connecting them to the actual problem: what is happening in someone's brain during hold music, and can we pick music that makes them more likely to stay?

## What we need to figure out

**Measuring escape motivation from a physiological signal.** We need a way to estimate how close someone is to hanging up -- ideally from something we can actually observe or predict, not something that requires putting a crisis caller in a scanner. The mechanistic literature gives us candidates (vAI activation, dACC effort-cost signals, vmPFC persistence), but we need to figure out how to get from "these brain regions do this" to "we can predict hang-up probability from an audio response model."

**Whether brain encoding models generalize to this.** TRIBE v2 (Meta) can predict fMRI brain activity from audio. It was trained on people watching movies and listening to podcasts -- not people in crisis on hold. But Wav2Vec-BERT (its audio backbone) is general-purpose, and the model demonstrates zero-shot generalization to novel tasks. The question is whether its predictions are meaningful enough in this context to be useful.

**How to decompose music into the features that matter.** If we're going to design hold music that targets specific neural responses, we need to know which musical features drive which brain responses. MusER (Ji et al.) decomposes symbolic music into emotion-relevant elements -- pitch, velocity, tempo, chord -- and maps them to valence/arousal. The question is whether these decompositions, aligned temporally with TRIBE v2's brain predictions over the same audio, actually tell us anything real. "Velocity dynamics predict amygdala activation" would be a finding. "Everything correlates a little" would not.

**Relaxing constraints to make progress.** The target population (actively suicidal, on hold) is about as hard as it gets for research. The existing literature suggests a ladder: start with stressed non-clinical populations, validate in suicidal ideators, then move to the target. Each step needs to carry the computational framework forward, not just be a separate study.

## Intuitions & guidelines

- The RLDDM framework (reinforcement learning + drift-diffusion) is the right computational language for this. It gives us mechanistically grounded parameters that map to specific neural substrates and predict specific behaviors (quit timing, persistence).
- Music is the intervention because it's the only thing we control during the hold. But "music" is too vague -- we need to think in terms of specific acoustic features driving specific neural targets (vmPFC upregulation for persistence, vAI downregulation for pain reduction).
- The movie soundtrack angle is real: TRIBE v2's training data has 100+ hours of audio with music baked in. That music is the bridge between "what does this sound do to a brain" and "what musical features drove that response."
- Every claim needs a citation. Every mechanism needs prior fMRI evidence. This isn't speculative -- it's connecting established results in a new configuration.
- Be honest about what's a stretch and what's solid. The computational neuroscience of escape motivation is solid. The music-to-brain-region mapping is plausible but unvalidated. The application to crisis callers is the stretch goal.

## What's here

```
tribev2/          # TRIBE v2 brain encoding model (facebookresearch, local dep)
papers/           # Reference papers and text extractions
bench.py          # GPU benchmarking
xai_cli.py        # Grok API -- search + reasoning
gemini_cli.py     # Gemini API -- deep research + long context
CLAUDE.md         # Research operating instructions
```

## Key references

- Millner et al. 2018 -- Escape vs. avoidance via RL+DDM
- Mobbs et al. 2020 -- Defensive hierarchy, vmPFC→PAG transition
- Doré et al. 2023 -- Entrapment neural signature (vAI-SFG connectivity)
- Goldfarb et al. 2020 -- Persistence/quit decisions, unrecoverable fatigue
- Gilbert & Allan 1998 -- Entrapment theory
- TRIBE v2 -- [paper](https://ai.meta.com/research/publications/a-foundation-model-of-vision-audition-and-language-for-in-silico-neuroscience/) / [code](https://github.com/facebookresearch/tribev2)
- MusER -- [paper](https://arxiv.org/abs/2312.10307) / [code](https://github.com/Tayjsl97/MusER)
