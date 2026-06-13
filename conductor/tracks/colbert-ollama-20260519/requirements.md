# Requirements — MoSCoW Prioritization

## Current Scope

As of the June 14 refresh, PR #16195 is scoped to LFM2-ColBERT conversion and documentation support. The older local runtime/GGUF requirements below are retained as historical/deferred context and are not blockers for the current upstream PR.

## P0 — MUST (Blocking for MVP)

### REQ-M00: Conversion Support
- **Description**: Ollama must convert LFM2-ColBERT style SentenceTransformers checkpoints with nested module safetensors.
- **Acceptance**: Conversion tests pass for LFM2 and nested dense-module safetensors handling.
- **Current**: Implemented in the current one-commit PR at `1f4302ef4a65b6927242771249682ad4f014816d`.
- **Status**: ✅ Complete / in upstream review

### REQ-M01: Model Loading
- **Description**: LFM2-ColBERT-350M must load in ollama without tensor errors
- **Acceptance**: `ollama run hf.co/LiquidAI/LFM2-ColBERT-350M-GGUF` exits with code 0
- **Current**: Historical runtime lane; not part of the current conversion/docs PR.
- **Status**: Deferred / separate track

### REQ-M02: Embedding API
- **Description**: `/api/embed` must return valid float32 embeddings for the model
- **Acceptance**: API returns 200 with `{"embeddings": [[float32 x 1024]]}`, no NaN values
- **Current**: Historical runtime lane; Q4_K_M metadata patching is deferred.
- **Status**: Deferred / separate track

### REQ-M03: Tensor Name Resolution
- **Description**: C++ model loader must use `LLM_TENSOR_OUTPUT_NORM_LFM2` for LFM2 architecture
- **Acceptance**: No `missing tensor 'output_norm'` error when loading LFM2 models
- **Current**: Historical runtime lane from the earlier branch shape.
- **Status**: Historical

### REQ-M04: ColBERT Tensor Support
- **Description**: The `dense_2.weight` tensor must be recognized as a valid LFM2 architecture tensor
- **Acceptance**: No `wrong number of tensors; expected 149, got 148` error
- **Current**: Historical runtime lane from the earlier branch shape.
- **Status**: Historical

### REQ-M05: Upstream Merge
- **Description**: Fixes must be submitted as PR(s) to ollama/ollama and merged
- **Acceptance**: PR merged into ollama mainline
- **Current**: PR #16195 open and mergeable; current head is focused on conversion/docs support.
- **Status**: In upstream review

## P1 — SHOULD (High Value)

### REQ-S01: Per-Token Embeddings
- **Description**: Return per-token embeddings via `dense_2` projection for ColBERT MaxSim retrieval
- **Acceptance**: New endpoint or extended format returning `{embeddings: [[128 x n_tokens]]}`
- **Status**: Deferred / separate track

### REQ-S02: Pooling Type Auto-Detection
- **Description**: Ollama should detect ColBERT models and apply correct pooling automatically
- **Acceptance**: Model pulled from HuggingFace works out of box without manual metadata patching
- **Status**: Deferred / separate track

### REQ-S03: Flash Attention for LFM2
- **Description**: Enable Flash Attention support for LFM2 models to reduce memory at long context
- **Acceptance**: Flash attention activates for LFM2 architecture
- **Status**: Deferred / separate track

### REQ-S04: Build Reproducibility
- **Description**: `go build -a` must produce a working binary with both fixes included
- **Acceptance**: Binary at `/tmp/ollama-final` loads model without errors
- **Status**: Historical; current PR validation uses Go package tests for conversion/parser code

## P2 — COULD (Nice to Have)

### REQ-C01: GGUF Metadata Standard for ColBERT
- **Description**: Define GGUF metadata keys for ColBERT-style multi-vector models
- **Acceptance**: Keys like `colbert.token_dim`, `colbert.output_tensor` recognized
- **Status**: ⬜ Not started — speculative

### REQ-C02: Benchmark Suite
- **Description**: Benchmarks comparing LFM2-ColBERT vs nomic-embed-text for retrieval accuracy
- **Acceptance**: Automated benchmark script in `conductor/benchmarks/`
- **Status**: ⬜ Not started

### REQ-C03: Docker/CI Pipeline
- **Description**: GitHub Actions workflow to build and test ollama with LFM2-ColBERT
- **Acceptance**: CI passes on PR
- **Status**: ⬜ Not started

## P3 — WON'T (Out of Scope)

### REQ-W01: Cloud Inference
- **Reason**: Ollama is local-first; cloud inference is orthogonal

### REQ-W02: Python SDK Changes
- **Reason**: Upstream ollama-python should handle new model types automatically

### REQ-W03: Windows ARM Support
- **Reason**: Focus on macOS/Apple Silicon for initial release
