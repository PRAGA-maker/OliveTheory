# OliveTheory

Half of 988 Suicide Hotline callers hang up before reaching a counselor. We think the right hold music -- chosen with actual neuroscience, not vibes -- could change that.

## Setup

```bash
cp .env.example .env   # add your XAI_API_KEY and GEMINI_API_KEY
uv sync && claude
```

## What's going on

When someone calls 988 and gets put on hold, they're making a continuous decision: stay or hang up. At some point the pain of waiting wins and they leave. This is escape motivation -- the brain's process for deciding to terminate an aversive situation.

This isn't hand-wavy. There's a real computational literature on how the brain makes this kind of decision. Millner et al. (2018) formalized escape vs. avoidance using RL+DDM. Mobbs mapped the neural switch from deliberative patience to reactive flight. Doré showed how entrapment -- basically the psychological state of a suicidal caller -- degrades the brain's ability to override the impulse to bail.

So the pieces exist in the literature. What doesn't exist is the connection: music features → brain response → escape motivation. That's what this project is trying to build.

## The goal

Find a fully computational, mechanistically grounded pipeline from **music features** (including emotion) to **physiological signal** (brain activity) to **escape motivation** (hang-up propensity). Every link in that chain needs to be backed by existing research, and every step needs to be validated -- not assumed.

## Open questions

This is a research project, not an implementation project. The methodology has to be felt out on-the-fly. Here's where we are:

**Do we even have the right models?**
- TRIBE v2 (Meta) predicts fMRI from audio. But it was trained on people watching movies, not people in crisis. Is it the right tool, or do we need something else? Do we need foundation models at all, or is there a simpler path?
- MusER decomposes symbolic music into emotion-relevant features. But it was trained on piano pop (EMOPIA). Does its latent space cover the kind of music that would matter here?

**How do we test fitness-for-purpose?**
- Can we measure how well TRIBE v2 generalizes to our domain? Things like: how diverse is its training audio? Does its latent space cover the acoustic features we care about? Can we use tools from transfer learning -- e.g., the Data Information Matrix (Tron & Fioresi, 2024) to quantify distributional distance between TRIBE's training data and our target stimuli?
- Same for MusER: does its VQ-VAE codebook cover movie soundtrack music, or just piano? This is half engineering (run the comparison) and half research (figure out what the right comparison even is).

**Can we emulate a crisis state computationally?**
- We can't put suicidal callers in a scanner. Can we approximate? The entrapment literature (Gilbert & Allan, Doré et al.) describes specific neural signatures. Can we validate those signatures against TRIBE v2's predictions? Can we use constraint relaxation -- stressed → crisis → suicidal ideation → active suicidality -- to build a ladder?

**What's the right bridge between music features and brain regions?**
- MusER gives us disentangled musical elements (pitch, velocity, tempo, chord). TRIBE v2 gives us predicted brain activation per region. If we align them temporally over the same audio, what's the right statistical test? RSA? Regression? Something else?
- Is the bridge even through these two models, or is there a more direct path?

**What does "escape motivation" look like in a signal?**
- The RLDDM framework gives us computational parameters (drift rate, starting-point bias, learning rate for futility). These map to specific brain regions (vAI, dACC, vmPFC, PAG). But can we actually extract these from a predicted fMRI? Or do we need a different proxy?

## Guidelines

- **Fully computational.** No hand-coding features, no manual annotation, no "we think this sounds calming." Every step must be computable and reproducible.
- **Mechanistically grounded.** Every claim about what a brain region does or what a musical feature causes needs a citation to prior fMRI/neuroscience work that validates it.
- **Prove at every step.** Don't assume the bridge works -- test it. Don't assume the model generalizes -- measure it. Don't assume the decomposition is meaningful -- validate it.
- **Be honest about the gaps.** The computational neuroscience of escape motivation is solid. The music-to-brain-region mapping is plausible but unvalidated. The application to crisis callers is the stretch goal. Know which layer you're on.

## What's here

```
tribev2/          # TRIBE v2 brain encoding model (facebookresearch, local dep)
papers/           # Reference papers and text extractions
bench.py          # GPU benchmarking
xai_cli.py        # Grok API -- search + reasoning
gemini_cli.py     # Gemini API -- deep research + long context
CLAUDE.md         # Research operating instructions
```

## References

- Millner et al. 2018 -- Escape vs. avoidance via RL+DDM
- Mobbs et al. 2020 -- Defensive hierarchy, vmPFC→PAG transition
- Doré et al. 2023 -- Entrapment neural signature
- Goldfarb et al. 2020 -- Persistence/quit decisions, unrecoverable fatigue
- Gilbert & Allan 1998 -- Entrapment theory
- Tron & Fioresi 2024 -- Data Information Matrix for transfer learning ([paper](https://arxiv.org/abs/2409.07412))
- TRIBE v2 -- [paper](https://ai.meta.com/research/publications/a-foundation-model-of-vision-audition-and-language-for-in-silico-neuroscience/) / [code](https://github.com/facebookresearch/tribev2)
- MusER -- [paper](https://arxiv.org/abs/2312.10307) / [code](https://github.com/Tayjsl97/MusER)
