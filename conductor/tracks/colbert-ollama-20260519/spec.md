# Technical Specification

## File Changes

### 1. `llama/llama.cpp/src/llama-model.cpp` (Line 6284)

```cpp
// BEFORE (bug):
output_norm = create_tensor(tn(LLM_TENSOR_OUTPUT_NORM, "weight"), {n_embd}, 0);

// AFTER (fix):
output_norm = create_tensor(tn(LLM_TENSOR_OUTPUT_NORM_LFM2, "weight"), {n_embd}, 0);
```

### 2. `llama/llama.cpp/src/llama-arch.cpp` (Line 2042)

```cpp
// ADDED to LLM_ARCH_LFM2 expected tensors:
LLM_TENSOR_DENSE_2_OUT,  // ColBERT late interaction head projection
```

## Tensor Mapping

| Tensor Name in GGUF | LLM Tensor Enum | Notes |
|---------------------|-----------------|-------|
| `token_embd_norm.weight` | `LLM_TENSOR_OUTPUT_NORM_LFM2` | Fix: was incorrectly `LLM_TENSOR_OUTPUT_NORM` |
| `dense_2.weight` | `LLM_TENSOR_DENSE_2_OUT` | ColBERT-specific, added to expected list |
| `output.weight` | `LLM_TENSOR_OUTPUT` | Shared with `token_embd.weight` via tie_embedding |

## Model Architecture (LFM2-ColBERT-350M)

| Parameter | Value |
|-----------|-------|
| Architecture | `lfm2` (GGUF metadata) |
| Parameters | 353,453,824 (353M) |
| Layers | 16 (blk.0..blk.15) |
| Embedding dim | 1024 |
| FFN dim | 4608 |
| Attention heads | 16 (with 8 KV heads on attention layers) |
| ShortConv l_cache | 3 |
| Vocab size | 64,402 |
| Context length | 128,000 |
| Rope freq base | 1,000,000 |
| ColBERT output dim | 128 (via dense_2) |
| Pooling type | 1 (mean) — required in GGUF |

## Layer Configuration

```
Layer 0:  ShortConv (dense FFN)
Layer 1:  ShortConv (dense FFN)
Layer 2:  Attention (dense FFN)
Layer 3:  ShortConv (dense FFN)
Layer 4:  ShortConv (dense FFN)
Layer 5:  Attention (dense FFN)
Layer 6:  ShortConv (dense FFN)
Layer 7:  ShortConv (dense FFN)
Layer 8:  Attention (dense FFN)
Layer 9:  ShortConv (dense FFN)
Layer 10: Attention (dense FFN)
Layer 11: ShortConv (dense FFN)
Layer 12: Attention (dense FFN)
Layer 13: ShortConv (dense FFN)
Layer 14: Attention (dense FFN)
Layer 15: ShortConv (dense FFN)
```

## Pooling Type Values (GGUF)

| Value | Name | Usage |
|-------|------|-------|
| 0 | None | Text generation (default) |
| 1 | Mean | Pooled embedding for retrieval |
| 2 | CLS | CLS token pooling |

## ColBERT Forward Pass (Proposed)

```
Input: token_ids [n_tokens]

1. Token Embedding: token_ids → embeds [n_tokens, 1024]
2. Position Encoding: add position embeddings
3. LFM2 Encoder: 16 layers of (ShortConv | Attention) + FFN
4. Output Norm: RMSNorm(hidden) → normalized [n_tokens, 1024]
5. Pooling (if not ColBERT): Mean(hidden) → [1024]
6. ColBERT projection (if ColBERT): dense_2(hidden) → [n_tokens, 128]
7. L2 Normalize: per-token or per-vector

Output (pooled):  [1024] float32 embedding vector
Output (ColBERT): [n_tokens, 128] float32 per-token embeddings
```
