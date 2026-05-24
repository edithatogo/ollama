# Implementation Plan: Native ColBERT Embedding Support

## Parallelization Strategy

This plan uses **3 parallel streams** with **3 dependency levels**:

```
Stream A: llama.cpp Backend  ─┐
                              ├──► Level 2: Integration ◄── Stream C: Docs/Release
Stream B: Ollama API ─────────┘
                              └── Stream C starts at Level 1 (parallel with A & B)
```

---

## Level 1: Foundation (Fully Parallel — All 3 Streams) 🚀

### Stream A1: llama.cpp Architecture Analysis
- [x] Task: Study existing embedding models (nomic-bert, all-MiniLM)
- [x] Task: Analyze GGUF metadata keys for embedding models
- [x] Task: Inspect LFM2-ColBERT-350M metadata and module forward components
- [x] Task: Document ColBERT-specific changes needed for llama.cpp

### Stream B1: Ollama Embed API Analysis
- [x] Task: Trace /api/embed endpoint through Ollama Go code
- [x] Task: Identify model registration path for new architectures
- [x] Task: Study Modelfile embedding model configuration
- [x] Task: Document integration points between Ollama and llama.cpp

### Stream C1: Custom mem0 Embedder (ALREADY COMPLETE) ✅
- [x] Task: Build custom ColBERT embedder via transformers
- [x] Task: Test mean-pooled embeddings (1024-dim verified)
- [x] Task: Benchmark inference on M1 Max MPS

---

## Level 2: Implementation (Parallel Streams A & B, C starts early tasks)

### Stream A2: llama.cpp ColBERT Implementation
- [x] Task: Add ColBERT model type to GGUF model loader
    - [x] Parallel sub-task 1: Register LFM2 ColBERT-compatible model config support
    - [x] Parallel sub-task 2: Add GGUF metadata keys for ColBERT dense projection
    - [x] Parallel sub-task 3: Implement ColBERT-compatible LFM2 model loader
- [x] Task: Implement embedding output mode
    - [x] Parallel sub-task 1: Add mean-pooling of last hidden state
    - [x] Parallel sub-task 2: Support normalized/un-normalized output
    - [x] Parallel sub-task 3: Add embedding dimension reporting through dense projection metadata
- [x] Task: Scope MaxSim late-interaction to retrieval-layer API design rather than `/api/embed`

### Stream B2: Ollama API Integration
- [x] Task: Register ColBERT model in Ollama model registry
- [x] Task: Wire up llama.cpp backend for ColBERT
- [x] Task: Implement Modelfile support for ColBERT architecture
- [x] Task: Implement /api/embed handler for ColBERT output format

### Stream C2: GGUF Conversion & Early Prep
- [x] Task: Create GGUF conversion support for ColBERT models
- [x] Task: Validate converted model output shape through Ollama `/api/embed`
- [x] Task: Write issue reports for ollama/ollama and ggml-org/llama.cpp

---

## Level 3: Integration & Testing (Sequential, A then B)

### Stream A3: llama.cpp Testing
- [x] Task: Test ColBERT model loading end-to-end
- [x] Task: Confirm embedding output dimensions against dense projection metadata
- [ ] Task: Performance benchmarks on M1 Max
- [ ] Task: Submit PR to ggml-org/llama.cpp

### Stream B3: Ollama Testing (Depends on A3)
- [x] Task: End-to-end test: local safetensors create → Ollama `/api/embed`
- [x] Task: Integration test with existing embedding models
- [ ] Task: Submit PR to ollama/ollama

### Stream C3: Release & Documentation
- [ ] Task: Upload GGUF version to HuggingFace
- [x] Task: Create Ollama Modelfile for LFM2-ColBERT-350M
- [x] Task: Write community usage documentation
- [ ] Task: Announce with benchmarks comparison vs nomic-embed-text

## Completion Notes
- Local implementation supports `Lfm2Model` conversion, SentenceTransformers/PyLate dense module metadata, nested dense safetensors, `lfm2_embed`, and dense-2-only llama.cpp embedding projection.
- Metadata check passed against `LiquidAI/LFM2-ColBERT-350M`: config uses `Lfm2Model`, `1_Dense/config.json` reports `1024 -> 128`, and `1_Dense/model.safetensors` contains `linear.weight`.
- Real-model validation passed: local `ollama create lfm2-colbert-local -f ...` converted the downloaded safetensors checkpoint to GGUF; `ollama show --verbose` reported `lfm2.dense_2_feat_out = 128`, `pooling_type = 1`, `dense_2.weight [1024 128]`, and embedding capability.
- End-to-end embedding passed: `/api/embed` returned two 128-dimensional vectors for `lfm2-colbert-local`.
- Local validation passed: targeted conversion/parser/cmd/model/server/llama tests, `go build -o ./ollama .`, and CPU CMake build.
- Remaining unchecked release tasks are external distribution steps: benchmark publication, PR submission, GGUF upload, and announcement.
