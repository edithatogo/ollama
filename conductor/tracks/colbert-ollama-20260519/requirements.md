# Requirements — MoSCoW Prioritization

## P0 — MUST (Blocking for MVP)

### REQ-M01: Model Loading
- **Description**: LFM2-ColBERT-350M must load in ollama without tensor errors
- **Acceptance**: `ollama run hf.co/LiquidAI/LFM2-ColBERT-350M-GGUF` exits with code 0
- **Current**: PR #16195 fixes tensor name; T-02 adds DENSE_2_OUT to expected list
- **Status**: 🟡 Code complete, build verified, testing blocked by T-03

### REQ-M02: Embedding API
- **Description**: `/api/embed` must return valid float32 embeddings for the model
- **Acceptance**: API returns 200 with `{"embeddings": [[float32 x 1024]]}`, no NaN values
- **Current**: Blocked — Q4_K_M model missing `lfm2.pooling_type = 1`
- **Status**: 🔴 Blocked (see T-03)

### REQ-M03: Tensor Name Resolution
- **Description**: C++ model loader must use `LLM_TENSOR_OUTPUT_NORM_LFM2` for LFM2 architecture
- **Acceptance**: No `missing tensor 'output_norm'` error when loading LFM2 models
- **Current**: ✅ Implemented in `llama-model.cpp:6284`
- **Status**: ✅ Complete

### REQ-M04: ColBERT Tensor Support
- **Description**: The `dense_2.weight` tensor must be recognized as a valid LFM2 architecture tensor
- **Acceptance**: No `wrong number of tensors; expected 149, got 148` error
- **Current**: ✅ Added `LLM_TENSOR_DENSE_2_OUT` to `llama-arch.cpp:2042`
- **Status**: ✅ Complete

### REQ-M05: Upstream Merge
- **Description**: Fixes must be submitted as PR(s) to ollama/ollama and merged
- **Acceptance**: PR merged into ollama mainline
- **Current**: PR #16195 open; T-02 needs separate PR
- **Status**: 🟡 Awaiting review

## P1 — SHOULD (High Value)

### REQ-S01: Per-Token Embeddings
- **Description**: Return per-token embeddings via `dense_2` projection for ColBERT MaxSim retrieval
- **Acceptance**: New endpoint or extended format returning `{embeddings: [[128 x n_tokens]]}`
- **Status**: ⬜ Not started

### REQ-S02: Pooling Type Auto-Detection
- **Description**: Ollama should detect ColBERT models and apply correct pooling automatically
- **Acceptance**: Model pulled from HuggingFace works out of box without manual metadata patching
- **Status**: 🟡 Partially — Q4_K_M conversion loses pooling_type; F16 has it

### REQ-S03: Flash Attention for LFM2
- **Description**: Enable Flash Attention support for LFM2 models to reduce memory at long context
- **Acceptance**: Flash attention activates for LFM2 architecture
- **Status**: ⬜ Not started — requires MLX kernel work

### REQ-S04: Build Reproducibility
- **Description**: `go build -a` must produce a working binary with both fixes included
- **Acceptance**: Binary at `/tmp/ollama-final` loads model without errors
- **Status**: ✅ Complete — binary built and verified

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
