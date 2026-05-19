# Product: LFM2-ColBERT-350M Native Ollama Support

## Vision
Make LFM2-ColBERT-350M a first-class embedding model in ollama, enabling state-of-the-art late interaction retrieval on local hardware.

## Target Users
- Developers building local RAG pipelines
- AI coding agents (Codex, Cline, Claude, Aider) using mem0 for memory
- Anyone needing SOTA multilingual retrieval without cloud APIs

## Success Criteria
1. `ollama run hf.co/LiquidAI/LFM2-ColBERT-350M-GGUF` loads without errors
2. `/api/embed` returns valid 1024-dim pooled embeddings (or per-token embeddings for ColBERT)
3. Model works on Apple Silicon (M1 Max, 32GB) without OOM
4. Fixes accepted upstream in ollama/ollama and ggml-org/llama.cpp
