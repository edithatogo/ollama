# LFM2-ColBERT-350M Integration - Handoff Document

## Current State

The current upstream code-review branch is `edithatogo/ollama:feat/lfm2-embed-output-norm`.

Current pushed head:

- `1f4302ef4a65b6927242771249682ad4f014816d`
- Rebasing note: branch was rebased onto `ollama/ollama@12e04379c` on 2026-06-14 and force-pushed with lease.
- Local safety branch before rebase: `backup/feat-lfm2-embed-output-norm-pre-rebase`
- Local safety branch before June 14 rebase: `backup/feat-lfm2-embed-output-norm-pre-rebase-20260614`
- Post-rebase validation comment: https://github.com/ollama/ollama/pull/16195#issuecomment-4698915854
- PR body was updated on 2026-06-14 to match the current one-commit conversion/docs diff and remove stale runtime-file claims.

Upstream Ollama PR:

- https://github.com/ollama/ollama/pull/16195
- Title: `lfm2: support ColBERT embedding models`
- State: open
- Reviewer artifact note: https://github.com/ollama/ollama/pull/16195#issuecomment-4527936929

The PR now covers the broader LFM2/ColBERT conversion and runtime path, not just the original two C++ tensor-loading fixes.

It includes:

- LFM2 embedding model registration for `lfm2_embed` and `lfm2moe_embed`
- SentenceTransformers `modules.json` parsing for pooling, normalization, and dense projection metadata
- nested safetensors discovery and tensor-name prefixing for module subdirectories such as `1_Dense/model.safetensors`
- upload path preservation for directory-structured model inputs
- optional LFM2 dense projection loading/application for ColBERT-style embedding heads
- documentation for LFM2-ColBERT embedding behavior

The original low-level fixes were:

### Change 1: Tensor Name Fix
- **File**: `llama/llama.cpp/src/llama-model.cpp`
- **Change**: Line 6284: `LLM_TENSOR_OUTPUT_NORM` → `LLM_TENSOR_OUTPUT_NORM_LFM2`
- **Purpose**: The LFM2 GGUF model stores its output norm tensor as `token_embd_norm.weight`. The llama.cpp loading code was looking for `output_norm.weight`. The `LLM_TENSOR_OUTPUT_NORM_LFM2` enum already existed (mapped to `"token_embd_norm"`) but was never wired up.
- **Verification**: Error changed from `missing tensor 'output_norm'` → `done_getting_tensors: expected 149, got 148`
- **Status**: included in PR https://github.com/ollama/ollama/pull/16195

### Change 2: DENSE_2_OUT Added to Expected List
- **File**: `llama/llama.cpp/src/llama-arch.cpp`
- **Change**: Added `LLM_TENSOR_DENSE_2_OUT` to the LFM2 architecture's expected tensor list
- **Purpose**: The ColBERT model has a late interaction head projection tensor `dense_2.weight` that is not in the standard LFM2 expected tensor list. This causes `done_getting_tensors: expected 149, got 148`
- **Note**: `LLM_TENSOR_DENSE_2_OUT` already maps to `"dense_2"` and is used by other architectures (e.g., `GEMMA_EMBEDDING`)
- **Status**: included in PR https://github.com/ollama/ollama/pull/16195

## Repository Structure

```
/Volumes/PortableSSD/GitHub/ollama/
  ├── .git/
  ├── llama/llama.cpp/src/
  ├── cmd/
  ├── convert/
  ├── docs/
  ├── model/models/lfm2/
  └── parser/

/Volumes/PortableSSD/GitHub/ollama-conductor-handoff/
  ├── HANDOFF.md
  └── conductor/
```

The active upstream PR branch should stay focused on code and docs intended for Ollama review. Conductor planning material is kept separately on `edithatogo/ollama:conductor/colbert-handoff`.

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
cd /Volumes/PortableSSD/GitHub/ollama
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

Current validation already run for the upstream PR branch:

```bash
go test -count=1 ./cmd ./convert ./parser ./model/models/lfm2 ./llama
find . -name '*.go' \
  -not -path './app/*' \
  -not -path './integration/*' \
  -not -path './.git/*' \
  -exec dirname {} \; | sort -u | sed 's#^\./#./#' | xargs go test -count=1
```

Post-rebase focused validation passed on 2026-05-24:

```bash
go test -count=1 ./cmd ./convert ./parser ./model/models/lfm2 ./llama
```

Post-June-14 focused validation passed:

```bash
go test -count=1 ./cmd ./convert ./parser
```

Post-rebase broad non-app package sweep also passed on 2026-05-24:

```bash
find . -name '*.go' \
  -not -path './app/*' \
  -not -path './integration/*' \
  -not -path './.git/*' \
  -exec dirname {} \; | sort -u | sed 's#^\./#./#' | xargs go test -count=1
```

Post-June-14 broad non-app package sweep also passed with the same command.

## Hugging Face Artifact Track

Public documentation-only Hugging Face repo:

- https://huggingface.co/edithatogo/ollama-colbert-local-artifacts
- Current HF commit: `421e4a3002e372ecd029cff2628c4618c6925da7`
- Visibility: public
- Gated: false
- Files: `.gitattributes`, `README.md`, `artifact-manifest.md`, `github-links.md`

No model weights, GGUF files, or generated binaries were uploaded.

The HF docs link was also added as a reviewer-facing comment on the Ollama PR:

- https://github.com/ollama/ollama/pull/16195#issuecomment-4527936929

Purpose:

- Keep GitHub as the source of truth for code, PRs, branches, and review.
- Use Hugging Face as the model-facing artifact index, provenance log, and future publication surface.
- Record candidate artifacts and block third-party or derived model uploads until license/provenance checks are complete.

Current source metadata checks:

| Source model | Metadata snapshot | Decision |
| --- | --- | --- |
| `LiquidAI/LFM2-ColBERT-350M` | public, ungated, `license:other`, sha `0c31032e995fe698f3ddd74f0ddb566cfd3d4d5a` | Reference only; no weights or derived GGUF uploaded. |
| `microsoft/bitnet-b1.58-2B-4T` | public, ungated, `license:mit`, sha `04c3b9ad9361b824064a1f25ea60a8be9599b127` | Reference only; no weights or derived GGUF uploaded. |

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
- Handoff branch: `edithatogo/ollama` on branch `conductor/colbert-handoff`
- Hugging Face docs repo: https://huggingface.co/edithatogo/ollama-colbert-local-artifacts
- Upstream llama.cpp: https://github.com/ggml-org/llama.cpp (vendored at commit ec98e2002)

## Local Branch Hygiene

Current repo checkouts on `/Volumes/PortableSSD/GitHub`:

| Checkout | Branch | State |
| --- | --- | --- |
| `ollama` | `feat/lfm2-embed-output-norm` | Clean; pushed to `fork/feat/lfm2-embed-output-norm` at `1f4302ef4`; rebased onto current `origin/main`; upstream PR #16195 open and mergeable. |
| `ollama-conductor-handoff` | `conductor/colbert-handoff` | Clean; pushed to `fork/conductor/colbert-handoff`; contains Conductor tracks and HF docs. |
| `BitNet` | `local-bitnet-runner-wrapper` | Clean; points at the two fork-only local runner commits and is pushed to `fork/local-bitnet-runner-wrapper`. Local `main` has been restored to track `origin/main`. |
| `BitNet-ignore-pr` | `ignore-generated-kernel-headers` | Clean; pushed to `fork/ignore-generated-kernel-headers`; upstream PR #563 open. |

The BitNet wrapper commits are preserved on `local-bitnet-runner-wrapper`; use that branch for local runner work.

BitNet PR branch freshness check on 2026-05-24:

- `ignore-generated-kernel-headers` is based on current `microsoft/BitNet:main`
- Branch is one commit ahead of `origin/main`
- PR #563 is open and mergeable
- `license/cla` check is passing

Local branch upstreams are configured to the pushed fork branches:

- `ollama:feat/lfm2-embed-output-norm` tracks `fork/feat/lfm2-embed-output-norm`
- `ollama-conductor-handoff:conductor/colbert-handoff` tracks `fork/conductor/colbert-handoff`
- `BitNet:local-bitnet-runner-wrapper` tracks `fork/local-bitnet-runner-wrapper`
- `BitNet-ignore-pr:ignore-generated-kernel-headers` tracks `fork/ignore-generated-kernel-headers`
