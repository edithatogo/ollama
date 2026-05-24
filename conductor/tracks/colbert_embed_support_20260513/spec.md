# Native ColBERT Embedding Model Support for Ollama

## Overview

Add native support for ColBERT architecture embedding models to the Ollama ecosystem. ColBERT (Contextualized Late Interaction over BERT) models use late-interaction scoring (MaxSim), which is fundamentally different from standard embedding models that produce single fixed-dimension vectors. This track implements the full pipeline: Ollama API support, llama.cpp GGUF backend, and a custom mem0 embedder.

## Repositories

- **ollama/ollama** - Go backend (API endpoint, model registry)
- **ggml-org/llama.cpp** - C++ inference backend (GGUF format, ColBERT architecture)
- **LiquidAI/LFM2-ColBERT-350M** - Target model to support

## Functional Requirements

### 1. llama.cpp ColBERT Support (Backend)
- [ ] Implement ColBERT architecture in llama.cpp (MaxSim late-interaction)
- [ ] Support GGUF quantization for ColBERT models
- [ ] Add embedding output mode (mean pooling / CLS token)
- [ ] Benchmark and optimize inference speed

### 2. Ollama Embed API Integration (Server)
- [ ] Register LFM2-ColBERT-350M in Ollama's model registry
- [ ] Expose `/api/embed` endpoint for ColBERT models
- [ ] Support standard embedding output (fixed-dimension vectors)
- [ ] Add documentation for ColBERT model support

### 3. Custom mem0 Embedder (Client)
- [ ] Test and validate mean-pooled embeddings from ColBERT model
- [ ] Integrate with mem0's HuggingFace embedder provider
- [ ] Benchmark embedding quality vs nomic-embed-text

## Non-Functional Requirements

- Must maintain backward compatibility with existing embedding models
- Embedding output must be compatible with vector databases (Qdrant, Chroma, etc.)
- Performance should be comparable to nomic-embed-text for standard use cases
- Documentation for model conversion and deployment

## Acceptance Criteria

1. `ollama run LFM2-ColBERT-350M` produces valid embeddings via `/api/embed`
2. Embeddings are compatible with mem0's Qdrant vector store
3. All existing embedding models continue to work unchanged
4. GGUF conversion scripts are provided for ColBERT models
5. PRs submitted to ollama/ollama and ggml-org/llama.cpp

## Out of Scope

- Training or fine-tuning ColBERT models
- Support for ColBERT vision/language multimodal models
- Cloud deployment infrastructure

## Progress Log

### 2026-05-14: Discovery
- llama.cpp already has `LLM_ARCH_LFM2` architecture support
- llama.cpp's `convert_hf_to_gguf.py` already has `LFM2ColBertModel` class (registered as `"Lfm2Model"`)
- ColBERT-specific tensors (`dense_2_out`) already defined in `llama_model_lfm2`
- Ollama auto-detects embedding capability from GGUF `pooling_type` key
- **Missing piece**: C++ graph builder doesn't use `dense_2_out` projection
- **Fixed**: Added 9-line patch to `lfm2.cpp` to apply `dense_2_out` and update `t_embd`
- **Fixed**: Added `pooling_type=MEAN` to `LFM2ColBertModel.set_gguf_parameters()`
- 🔨 **Building**: llama.cpp with patch to test embedding output
- ✅ **GGUF converted**: 707 MB, 149 tensors, recognized by Ollama as embedding model
