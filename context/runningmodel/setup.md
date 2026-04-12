# Running TRIBE v2 -- Setup & Inference

## Prerequisites

- Python 3.11+
- CUDA-capable GPU (tested on RTX 4060 Laptop, 8GB VRAM)
- PyTorch 2.5+ with CUDA

## Install

```bash
uv sync                                              # installs from pyproject.toml
pip install neuralset==0.0.2 neuraltrain==0.0.2      # TRIBE v2's data/model framework (OSS, PyPI)
pip install x_transformers einops                     # transformer backbone deps
```

## Download checkpoint

```bash
python -c "from huggingface_hub import hf_hub_download; hf_hub_download('facebook/tribev2', 'best.ckpt', cache_dir='./cache')"
python -c "from huggingface_hub import hf_hub_download; hf_hub_download('facebook/tribev2', 'config.yaml', cache_dir='./cache')"
```

Checkpoint lands in `cache/models--facebook--tribev2/snapshots/<hash>/`.

## Windows PosixPath fix

The config.yaml was serialized on Linux with `pathlib.PosixPath`. On Windows, add this before any tribev2 imports:

```python
import pathlib, sys
if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath
```

Not needed on WSL/Linux.

## Load model (official pipeline)

```python
from tribev2 import TribeModel

CKPT_DIR = "cache/models--facebook--tribev2/snapshots/f894e783020944dcd96e5568550afe2aa9743f9f"
model = TribeModel.from_pretrained(CKPT_DIR, cache_folder="./cache")
# model._model is the FmriEncoderModel (177M params)
# model._model.device shows current device
```

## Run inference on audio

```python
events = model.get_events_dataframe(audio_path="path/to/audio.wav")
preds, segments = model.predict(events)
# preds: (n_segments, 20484) -- predicted fMRI for 20,484 cortical vertices
# segments: aligned time segments
```

## Run inference on video (includes audio extraction + transcription)

```python
events = model.get_events_dataframe(video_path="path/to/video.mp4")
preds, segments = model.predict(events)
```

## Audio-only mode (skip transcription)

```python
from tribev2.demo_utils import get_audio_and_text_events
import pandas as pd

event = {"type": "Audio", "filepath": "path/to/audio.wav", "start": 0,
         "timeline": "default", "subject": "default"}
events = get_audio_and_text_events(pd.DataFrame([event]), audio_only=True)
preds, segments = model.predict(events)
```

## Model architecture (from paper)

- **Audio**: Wav2Vec-Bert-2.0 -> 2Hz embeddings (1024-dim x 2 layers = 2048)
- **Video**: V-JEPA-2-Giant -> 2Hz embeddings (1280-dim x 2 layers = 2816 -- note: 1408 in paper, 1280 effective after averaging)
- **Text**: LLaMA-3.2-3B -> 2Hz word embeddings (2048-dim x 3 layers = 6144)
- Each modality projected to 384-dim, concatenated -> 1152-dim
- 8-layer transformer encoder (16 heads, head_dim=72)
- Low-rank head (2048) -> subject-conditioned linear -> 20,484 cortical vertices
- Separate subcortical pathway: 8,802 voxels (hippocampus, amygdala, thalamus, caudate, putamen, pallidum, accumbens, lateral ventricles)
- **Note**: PAG is NOT in the subcortical target set

## Benchmarks (RTX 4060 Laptop, 8GB VRAM)

| Config | fp32 (ms) | fp16 (ms) | Peak VRAM |
|--------|-----------|-----------|-----------|
| B=1, T=50 | 10.6 | ~5 | 714 MB |
| B=1, T=200 | 17.0 | ~9 | 744 MB |
| B=8, T=200 | 99.0 | ~50 | 1090 MB |

Plenty of headroom. No OOM risk.

## Output space

- 20,484 cortical vertices on fsaverage5 surface
- Can be parcellated using HCP Glasser atlas (360 regions) or Desikan-Killiany
- For our ROIs: use nilearn or HCP parcellation to extract vmPFC, dACC, anterior insula, amygdala (subcortical)

## Feature extractors required for full pipeline

The official pipeline runs frozen feature extractors:
- `facebook/w2v-bert-2.0` (Wav2Vec-Bert for audio)
- V-JEPA-2-Giant (video)
- LLaMA-3.2-3B (text)

These download on first use (~several GB each). For audio-only experiments, only Wav2Vec-Bert is needed.
