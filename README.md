# OliveTheory

Research workspace for bridging music emotion to brain activity.

## Quick Start

1. **Clone** — `git clone https://github.com/PRAGA-maker/OliveTheory.git`
2. **Add keys** — copy `.env.example` to `.env` and fill in your API keys
3. **Go** — `uv sync && claude`

## What This Is

TRIBE v2 (Meta/FAIR) predicts fMRI brain activity from movie audio. MusER (Ji et al.) decomposes symbolic music into emotion-disentangled latent spaces. Neither was designed to talk to the other. This repo is figuring out whether and how they can.

## The Suspicion

> Movie soundtracks contain music. TRIBE v2 already learned brain responses to that music (it trained on 1000+ hours of fMRI from people watching movies, listening to podcasts). MusER can decompose the emotional structure of music into interpretable elements (pitch, velocity, tempo, chord, duration, beat → valence/arousal). If we align these two over the same movie audio, we should be able to ask: **which musical elements predict activity in which brain regions?**
>
> "Velocity predicts amygdala" or "tempo aligns with motor cortex" would be a neuroscience finding — derived from existing models, no new fMRI data needed.
>
> The key insight is that the audio soundtracks decompose well — they already have music baked in (scores, soundtrack, incidental music across 100+ hours of content). Demucs can source-separate it, basic-pitch can MIDI-transcribe it, and then we're in MusER's input space.

## The Gap

The models don't share a representation space. Connecting them means:

- **Domain validation**: Does MusER's model (trained on piano pop) generalize to movie soundtrack music? Compare CP token distributions (pitch, velocity, tempo, etc.) against EMOPIA baseline. If distributions diverge, the bridge doesn't hold.
- **Transcription pipeline**: Movie audio → Demucs (source separation) → basic-pitch/MT3 (MIDI transcription) → MidiTok (CP tokenization). Each step introduces noise.
- **Temporal alignment**: MusER emotion latents and TRIBE v2 brain predictions need to be aligned in time over the same movie segments. Granularity matters.
- **Statistical test**: RSA? Element-wise regression? Something else? Needs to be simple, defensible, and produce a real finding — not just a correlation.

The methodology needs to anneal. The pieces are here; the question is what the cleanest, most defensible version looks like.

## Directions to Examine

1. **Distribution match test** — Are movie soundtracks in-domain for MusER? (Wasserstein distance on CP token distributions vs EMOPIA baseline)
2. **MusER latent coherence** — Does MusER's VQ-VAE produce meaningful emotion clusters on out-of-sample movie music? (Silhouette Coefficient)
3. **The bridge itself** — RSA between MusER's 7 disentangled element subspaces and TRIBE v2's predicted brain activity per region. Element-level decomposition is what makes this publishable.
4. **Controls** — Music-heavy vs dialogue-only segments (positive), visual cortex vs auditory (negative), permutation null (shuffle time alignment)

## Implementation Notes

- **CLI Tools:** `xai_cli.py` (Grok — cheap, fast, great for search) and `gemini_cli.py` (Gemini — long context, deep research)
- **Browser:** Chrome MCP tools for interactive paper reading and web research
- **Dependency mgmt:** `uv`
- **Agent protocol:** See `CLAUDE.md` for the research operating manual
- **Python:** 3.14 on this machine. torch + CUDA works. basic-pitch/demucs/fast_transformers need a 3.11 env.

## Structure

```
.
├── CLAUDE.md              # Research operating instructions
├── .claude/               # Claude settings (permissions, etc.)
├── .env.example           # API key template (copy to .env)
├── xai_cli.py             # Grok API CLI (think + web search)
├── gemini_cli.py          # Gemini API CLI (think + deep research)
├── papers/                # Reference papers and text extractions
│   ├── tribev2.pdf        # TRIBE v2 paper (full 27 pages)
│   └── tribev2.txt        # Text extraction of above
├── tribev2/               # TRIBE v2 source (facebookresearch, local dep)
├── bench.py               # GPU benchmarking script
├── outputs/               # Auto-generated research outputs (gitignored)
└── pyproject.toml         # Project config (uv)
```

## Key References

- **TRIBE v2**: [Paper](https://ai.meta.com/research/publications/a-foundation-model-of-vision-audition-and-language-for-in-silico-neuroscience/) | [Code](https://github.com/facebookresearch/tribev2) | [Weights](https://huggingface.co/facebook/tribev2)
- **MusER**: [Paper](https://arxiv.org/abs/2312.10307) | [Code](https://github.com/Tayjsl97/MusER) | [Checkpoints](https://huggingface.co/TaylorJi/MusER)
- **EMOPIA**: [Dataset](https://annahung31.github.io/EMOPIA/) (1,087 piano clips with valence-arousal labels)
- **MidiTok**: [Docs](https://miditok.readthedocs.io/) (Compound Word tokenization)
- **Demucs**: [Code](https://github.com/facebookresearch/demucs) (Meta's source separation)
