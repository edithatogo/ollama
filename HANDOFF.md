# LFM2-ColBERT-350M Integration — Handoff Document

## Current State

Two C++ changes have been committed and pushed to `edithatogo/ollama` on branch `feat/lfm2-embed-output-norm`:

### Change 1: Tensor Name Fix (PR #16195)
- **File**: `llama/llama.cpp/src/llama-model.cpp`
- **Change**: Line 6284: `LLM_TENSOR_OUTPUT_NORM` → `LLM_TENSOR_OUTPUT_NORM_LFM2`
- **Purpose**: The LFM2 GGUF model stores its output norm tensor as `token_embd_norm.weight`. The llama.cpp loading code was looking for `output_norm.weight`. The `LLM_TENSOR_OUTPUT_NORM_LFM2` enum already existed (mapped to `"token_embd_norm"`) but was never wired up.
- **Verification**: Error changed from `missing tensor 'output_norm'` → `done_getting_tensors: expected 149, got 148`
- **Status**: PR https://github.com/ollama/ollama/pull/16195 — OPEN, awaiting review

### Change 2: DENSE_2_OUT Added to Expected List
- **File**: `llama/llama.cpp/src/llama-arch.cpp`
- **Change**: Added `LLM_TENSOR_DENSE_2_OUT` to the LFM2 architecture's expected tensor list
- **Purpose**: The ColBERT model has a late interaction head projection tensor `dense_2.weight` that is not in the standard LFM2 expected tensor list. This causes `done_getting_tensors: expected 149, got 148`
- **Note**: `LLM_TENSOR_DENSE_2_OUT` already maps to `"dense_2"` and is used by other architectures (e.g., `GEMMA_EMBEDDING`)
- **Status**: Committed to fork, NOT yet submitted as a separate PR

## Repository Structure

```
/Users/doughnut/GitHub/ollama/
  ├── .git/
  ├── llama/llama.cpp/src/
  │   ├── llama-model.cpp      # Modified (tensor name fix)
  │   └── llama-arch.cpp       # Modified (DENSE_2_OUT addition)
  └── HANDOFF.md               # This file
```

## Build Artifacts

| File | Path | Size | Description |
|------|------|------|-------------|
| Custom binary | `/tmp/ollama-final` | 70.8 MB | Built with both fixes, `go build -a` |
| Plan document | `/tmp/plan.md` | 3.5 KB | Original plan |

## Downloaded Model

| File | Path | Size | Notes |
|------|------|------|-------|
| Q4_K_M GGUF | `blobs/sha256-6a969ec2c18a...` | 228 MB | All 149 tensors, has `dense_2.weight` |
| ollama model name | `hf.co/LiquidAI/LFM2-ColBERT-350M-GGUF:Q4_K_M` | 228 MB | Pulled from HuggingFace |

## Remaining Issues

### 1. `pooling_type` missing from Q4_K_M
- The quantized GGUF model lacks `lfm2.pooling_type = 1` metadata
- Without this, ollama reports: `"this model does not support embeddings"`
- The Python `gguf` library's `GGUFWriter.add_tensor_info()` doesn't support quantized tensor types (Q4_K, Q6_K, etc.)
- **Solution**: Binary-patch the Q4_K_M GGUF file to insert a KV pair for `lfm2.pooling_type = 1` (uint32) in the KV section, OR use the F16 version which already has pooling_type

### 2. F16 model file corrupted
- The original F16 GGUF (`sha256-42d1f438...`) was corrupted during GGUF patching attempts
- The repaired version has 148 tensors (missing `dense_2.weight`) and produces NaN embeddings
- The corrupted file also has broken data offsets for the first tensor

### 3. Build system nuance
- `go build` compiles C++ via CGo (llama.go + all .cpp files in `llama/llama.cpp/src/`)
- `go build -a` must be used to force recompilation of C++ files when they change
- `go clean -cache` may be needed before `-a` for a truly clean build
- On macOS, the Go binary also links against Metal/GPU libraries

### 4. Memory pressure
- The M1 Max with 32GB RAM is under memory pressure with multiple apps running
- Ollama server processes may get SIGKILL'd by the OOM killer
- Close other applications before testing

## How to Test

```bash
# 1. Build from source (if needed)
cd /Users/doughnut/GitHub/ollama
go clean -cache
go build -a -o /tmp/ollama-new .

# 2. Kill existing ollama and start custom build
kill -9 $(lsof -ti:11434) 2>/dev/null
/tmp/ollama-new serve &

# 3. Test embedding
curl http://localhost:11434/api/embed -d '{
  "model": "hf.co/LiquidAI/LFM2-ColBERT-350M-GGUF:Q4_K_M",
  "input": "Hello world"
}'
```

## Key Files to Edit Next

1. **To fix pooling_type**: Binary-patch the Q4_K_M GGUF to add `lfm2.pooling_type = 1`
   - Or use `gguf-new-metadata` to copy + Python to insert KV pair
   - The GGUF format: header(24) → KV pairs → TI entries → tensor data

2. **To add `dense_2.weight` forward pass**: Add the corresponding forward pass code in LFM2 model
   - Currently in `model/models/lfm2/model.go` (Go-side, not needed for C++ runner)
   - For C++ runner: add the tensor to the expected list in `llama-arch.cpp` (ALREADY DONE)

## Contact / Upstream

- PR #16195: https://github.com/ollama/ollama/pull/16195
- Fork: `edithatogo/ollama` on branch `feat/lfm2-embed-output-norm`
- Upstream llama.cpp: https://github.com/ggml-org/llama.cpp (vendored at commit ec98e2002)
