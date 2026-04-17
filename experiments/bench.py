"""
Benchmark script for TRIBEv2 inference.
Tests CPU and GPU (if available), reports timing, memory, and whether you'll OOM.
"""

import gc
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn


# ---------------------------------------------------------------------------
# Minimal model reconstruction from checkpoint (no external deps needed)
# ---------------------------------------------------------------------------

class RMSNorm(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.g = nn.Parameter(torch.ones(1))
        self.dim = dim

    def forward(self, x):
        return x * self.g * (x.shape[-1] ** 0.5) / x.norm(dim=-1, keepdim=True).clamp(min=1e-8)


class RotaryEmbedding(nn.Module):
    def __init__(self, dim):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

    def forward(self, seq_len):
        t = torch.arange(seq_len, device=self.inv_freq.device).float()
        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        return torch.cat([freqs, freqs], dim=-1)


def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat([-x2, x1], dim=-1)


def apply_rotary(q, k, freqs):
    # q, k: (B, n_heads, T, head_dim), freqs: (T, head_dim)
    freqs = freqs[: q.shape[2]]
    cos = freqs.cos().unsqueeze(0).unsqueeze(0)  # (1, 1, T, head_dim)
    sin = freqs.sin().unsqueeze(0).unsqueeze(0)
    q = q * cos + rotate_half(q) * sin
    k = k * cos + rotate_half(k) * sin
    return q, k


class Attention(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.to_q = nn.Linear(dim, dim, bias=False)
        self.to_k = nn.Linear(dim, dim, bias=False)
        self.to_v = nn.Linear(dim, dim, bias=False)
        self.to_out = nn.Linear(dim, dim, bias=False)
        self.dim = dim
        self.head_dim = 72  # 1152 / 16 heads
        self.n_heads = dim // self.head_dim

    def forward(self, x, rotary_freqs=None):
        B, T, _ = x.shape
        q = self.to_q(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.to_k(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.to_v(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        if rotary_freqs is not None:
            q, k = apply_rotary(q, k, rotary_freqs)
        out = torch.nn.functional.scaled_dot_product_attention(q, k, v)
        out = out.transpose(1, 2).reshape(B, T, -1)
        return self.to_out(out)


class FeedForward(nn.Module):
    def __init__(self, dim, mult=4):
        super().__init__()
        # Match checkpoint structure: ff.0.0=Linear, ff.0.1=GELU (inside Sequential), ff.2=Linear
        self.ff = nn.Sequential(
            nn.Sequential(nn.Linear(dim, dim * mult), nn.GELU()),
            nn.Identity(),  # placeholder for dropout at index 1
            nn.Linear(dim * mult, dim),
        )

    def forward(self, x):
        return self.ff(x)


class ResidualScale(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.residual_scale = nn.Parameter(torch.ones(dim))

    def forward(self, x, residual):
        return x + residual * self.residual_scale


class TransformerBlock(nn.Module):
    def __init__(self, dim, block_type):
        super().__init__()
        # Checkpoint has norm as nn.Sequential(RMSNorm) → keys are norm.0.g
        self.norm = nn.Sequential(RMSNorm(dim))
        self.block_type = block_type
        if block_type == "attn":
            self.fn = Attention(dim)
        else:
            self.fn = FeedForward(dim)
        self.residual = ResidualScale(dim)

    def forward(self, x, rotary_freqs=None):
        normed = self.norm(x)
        if self.block_type == "attn":
            out = self.fn(normed, rotary_freqs)
        else:
            out = self.fn(normed)
        return self.residual(out, x)


class TribeEncoder(nn.Module):
    def __init__(self, dim=1152, depth=8):
        super().__init__()
        self.rotary = RotaryEmbedding(dim // (dim // 72))  # head_dim=72
        blocks = []
        for i in range(depth):
            blocks.append(TransformerBlock(dim, "attn"))
            blocks.append(TransformerBlock(dim, "ffn"))
        self.blocks = nn.ModuleList(blocks)
        self.final_norm = RMSNorm(dim)

    def forward(self, x):
        freqs = self.rotary(x.shape[1]).to(dtype=x.dtype, device=x.device)
        for block in self.blocks:
            if block.block_type == "attn":
                x = block(x, freqs)
            else:
                x = block(x)
        return self.final_norm(x)


class TribeModel(nn.Module):
    """Minimal TRIBEv2 model for benchmarking -- reconstructed from checkpoint."""

    def __init__(self):
        super().__init__()
        hidden = 1152

        # Projectors (linear layers for each modality)
        self.projectors = nn.ModuleDict({
            "text": nn.Linear(6144, 384),
            "video": nn.Linear(2816, 384),
            "audio": nn.Linear(2048, 384),
        })

        # Positional embedding
        self.time_pos_embed = nn.Parameter(torch.randn(1, 1024, hidden))

        # Transformer encoder
        self.encoder = TribeEncoder(dim=hidden, depth=8)

        # Low-rank head + subject predictor
        self.low_rank_head = nn.Linear(hidden, 2048, bias=False)
        self.predictor_weights = nn.Parameter(torch.randn(1, 2048, 20484))
        self.predictor_bias = nn.Parameter(torch.zeros(1, 20484))

        # Pooler
        self.pooler = nn.AdaptiveAvgPool1d(100)  # duration_trs=100

    def forward(self, text, video, audio):
        """Forward pass with raw feature tensors.

        Args:
            text:  (B, T, 6144) - LLaMA features (3 layers × 2048)
            video: (B, T, 2816) - V-JEPA2 features (2 layers × 1408)
            audio: (B, T, 2048) - Wav2Vec features (2 layers × 1024)
        """
        # Project each modality to hidden/3 = 384
        t = self.projectors["text"](text)
        v = self.projectors["video"](video)
        a = self.projectors["audio"](audio)

        # Concatenate → (B, T, 1152)
        x = torch.cat([t, v, a], dim=-1)

        # Add positional embedding
        x = x + self.time_pos_embed[:, :x.size(1)]

        # Transformer
        x = self.encoder(x)  # (B, T, 1152)

        # Low-rank head
        x = self.low_rank_head(x)  # (B, T, 2048)

        # Subject prediction (average subject)
        x = x.transpose(1, 2)  # (B, 2048, T)
        x = torch.einsum("bdt,sdo->bot", x, self.predictor_weights) + self.predictor_bias.unsqueeze(-1)

        # Pool to output timesteps
        x = self.pooler(x)  # (B, 20484, 100)

        return x


def load_model_from_checkpoint(ckpt_path):
    """Load weights from the HuggingFace checkpoint into our minimal model."""
    model = TribeModel()
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    sd = ckpt["state_dict"]

    # Map checkpoint keys → our model keys
    new_sd = {}
    for k, v in sd.items():
        # Strip "model." prefix
        k2 = k.replace("model.", "", 1)

        if k2 == "predictor.weights":
            new_sd["predictor_weights"] = v
        elif k2 == "predictor.bias":
            new_sd["predictor_bias"] = v
        elif k2.startswith("encoder.layers."):
            # Checkpoint: encoder.layers.{i}.{sub}.{rest}
            # Our model: encoder.blocks.{i}.{mapped_sub}.{rest}
            parts = k2.split(".")
            layer_idx = int(parts[2])
            sub_idx = int(parts[3])  # 0=norm, 1=fn, 2=residual
            rest = ".".join(parts[4:])

            if sub_idx == 0:
                new_sd[f"encoder.blocks.{layer_idx}.norm.{rest}"] = v
            elif sub_idx == 1:
                new_sd[f"encoder.blocks.{layer_idx}.fn.{rest}"] = v
            elif sub_idx == 2:
                new_sd[f"encoder.blocks.{layer_idx}.residual.{rest}"] = v
        elif k2.startswith("encoder.rotary_pos_emb."):
            rest = k2.replace("encoder.rotary_pos_emb.", "")
            new_sd[f"encoder.rotary.{rest}"] = v
        elif k2.startswith("encoder.final_norm."):
            rest = k2.replace("encoder.final_norm.", "")
            new_sd[f"encoder.final_norm.{rest}"] = v
        else:
            new_sd[k2] = v

    missing, unexpected = model.load_state_dict(new_sd, strict=False)
    if missing:
        print(f"  Warning: {len(missing)} missing keys")
    if unexpected:
        print(f"  Warning: {len(unexpected)} unexpected keys")
    return model


def estimate_memory(model, dtype):
    """Estimate model memory in MB."""
    param_bytes = sum(p.numel() * p.element_size() for p in model.parameters())
    return param_bytes / 1024 / 1024


def benchmark_device(model, device, dtype, seq_lens, batch_sizes, n_warmup=3, n_runs=10):
    """Run benchmark on a given device."""
    model = model.to(device=device, dtype=dtype)
    model.eval()

    results = []

    for batch_size in batch_sizes:
        for seq_len in seq_lens:
            label = f"B={batch_size}, T={seq_len}"

            # Create dummy inputs
            text = torch.randn(batch_size, seq_len, 6144, device=device, dtype=dtype)
            video = torch.randn(batch_size, seq_len, 2816, device=device, dtype=dtype)
            audio = torch.randn(batch_size, seq_len, 2048, device=device, dtype=dtype)

            try:
                if device.type == "cuda":
                    torch.cuda.reset_peak_memory_stats()

                # Warmup
                for _ in range(n_warmup):
                    with torch.no_grad():
                        _ = model(text, video, audio)
                    if device.type == "cuda":
                        torch.cuda.synchronize()

                # Timed runs
                times = []
                for _ in range(n_runs):
                    if device.type == "cuda":
                        torch.cuda.synchronize()
                    t0 = time.perf_counter()
                    with torch.no_grad():
                        out = model(text, video, audio)
                    if device.type == "cuda":
                        torch.cuda.synchronize()
                    times.append(time.perf_counter() - t0)

                avg_ms = sum(times) / len(times) * 1000
                std_ms = (sum((t * 1000 - avg_ms) ** 2 for t in times) / len(times)) ** 0.5

                if device.type == "cuda":
                    peak_mb = torch.cuda.max_memory_allocated() / 1024 / 1024
                else:
                    peak_mb = None

                results.append({
                    "label": label,
                    "avg_ms": avg_ms,
                    "std_ms": std_ms,
                    "peak_vram_mb": peak_mb,
                    "output_shape": list(out.shape),
                    "oom": False,
                })

            except torch.cuda.OutOfMemoryError:
                torch.cuda.empty_cache()
                gc.collect()
                results.append({
                    "label": label,
                    "avg_ms": None,
                    "std_ms": None,
                    "peak_vram_mb": None,
                    "output_shape": None,
                    "oom": True,
                })

            except RuntimeError as e:
                if "out of memory" in str(e).lower():
                    if device.type == "cuda":
                        torch.cuda.empty_cache()
                    gc.collect()
                    results.append({
                        "label": label,
                        "avg_ms": None,
                        "std_ms": None,
                        "peak_vram_mb": None,
                        "output_shape": None,
                        "oom": True,
                    })
                else:
                    raise

            # Cleanup
            del text, video, audio
            if device.type == "cuda":
                torch.cuda.empty_cache()
            gc.collect()

    return results


def print_results(device_name, results, model_mem_mb):
    print(f"\n{'='*70}")
    print(f"  {device_name}")
    print(f"  Model memory: {model_mem_mb:.0f} MB")
    print(f"{'='*70}")
    print(f"  {'Config':<20} {'Time (ms)':>12} {'Peak VRAM':>12} {'Output':>20} {'OOM':>5}")
    print(f"  {'-'*20} {'-'*12} {'-'*12} {'-'*20} {'-'*5}")
    for r in results:
        if r["oom"]:
            print(f"  {r['label']:<20} {'---':>12} {'---':>12} {'---':>20} {'YES':>5}")
        else:
            time_str = f"{r['avg_ms']:.1f} ± {r['std_ms']:.1f}"
            vram_str = f"{r['peak_vram_mb']:.0f} MB" if r["peak_vram_mb"] is not None else "n/a"
            out_str = str(r["output_shape"])
            print(f"  {r['label']:<20} {time_str:>12} {vram_str:>12} {out_str:>20} {'no':>5}")


def main():
    ckpt_path = Path("cache/models--facebook--tribev2/snapshots")
    ckpt_files = list(ckpt_path.rglob("best.ckpt"))
    if not ckpt_files:
        print("ERROR: best.ckpt not found in cache/. Download it first:")
        print('  python -c "from huggingface_hub import hf_hub_download; '
              "hf_hub_download('facebook/tribev2', 'best.ckpt', cache_dir='./cache')\"")
        sys.exit(1)
    ckpt_file = ckpt_files[0]

    print("=" * 70)
    print("  TRIBEv2 Inference Benchmark")
    print("=" * 70)

    # System info
    print(f"\n  System:")
    print(f"    PyTorch:  {torch.__version__}")
    print(f"    CUDA:     {torch.cuda.is_available()}", end="")
    if torch.cuda.is_available():
        print(f" ({torch.cuda.get_device_name(0)}, {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB)")
    else:
        print()
    import psutil
    print(f"    RAM:      {psutil.virtual_memory().total / 1024**3:.1f} GB "
          f"({psutil.virtual_memory().available / 1024**3:.1f} GB free)")

    # Load model
    print(f"\n  Loading checkpoint: {ckpt_file}")
    model = load_model_from_checkpoint(str(ckpt_file))
    total_params = sum(p.numel() for p in model.parameters())
    print(f"  Parameters: {total_params:,} ({total_params / 1e6:.1f}M)")

    # Test configs: (batch_size, seq_len)
    # seq_len=200 = 100 seconds at 2Hz (typical segment)
    # seq_len=100 = 50 seconds
    # seq_len=50  = 25 seconds
    batch_sizes = [1, 4, 8]
    seq_lens = [50, 100, 200]

    # --- GPU benchmark ---
    if torch.cuda.is_available():
        for dtype, dtype_name in [(torch.float32, "GPU fp32"), (torch.float16, "GPU fp16")]:
            model_gpu = load_model_from_checkpoint(str(ckpt_file))
            mem_mb = estimate_memory(model_gpu, dtype)
            results = benchmark_device(model_gpu, torch.device("cuda"), dtype, seq_lens, batch_sizes)
            print_results(dtype_name, results, mem_mb)
            del model_gpu
            torch.cuda.empty_cache()
            gc.collect()

    # --- CPU benchmark (fewer configs to save time) ---
    print("\n  Running CPU benchmark (subset of configs)...")
    cpu_batch_sizes = [1, 4]
    cpu_seq_lens = [50, 100]
    mem_mb = estimate_memory(model, torch.float32)
    results = benchmark_device(model, torch.device("cpu"), torch.float32, cpu_seq_lens, cpu_batch_sizes, n_warmup=1, n_runs=3)
    print_results("CPU fp32", results, mem_mb)

    # --- Summary ---
    print(f"\n{'='*70}")
    print("  SUMMARY")
    print(f"{'='*70}")
    if torch.cuda.is_available():
        vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
        model_fp16_mb = sum(p.numel() * 2 for p in model.parameters()) / 1024 / 1024
        model_fp32_mb = sum(p.numel() * 4 for p in model.parameters()) / 1024 / 1024
        print(f"  GPU VRAM:        {vram_gb:.1f} GB")
        print(f"  Model (fp32):    {model_fp32_mb:.0f} MB")
        print(f"  Model (fp16):    {model_fp16_mb:.0f} MB")
        print(f"  Headroom (fp16): ~{vram_gb * 1024 - model_fp16_mb:.0f} MB for activations")
        print()
        print("  Recommendation:")
        if vram_gb >= 6:
            print("    Use fp16 on GPU for fast inference.")
            print("    fp32 may OOM on larger batches/sequences.")
        else:
            print("    VRAM is tight. Use fp16, batch_size=1, short sequences.")
    else:
        print("  No GPU available. CPU-only inference will work but be slower.")
    print()


if __name__ == "__main__":
    main()
