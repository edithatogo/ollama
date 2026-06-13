# Ollama Tracks Overview

## Active Tracks

| Track ID | Name | Status | Priority | Progress |
|----------|------|--------|----------|----------|
| `colbert-ollama-20260519` | LFM2-ColBERT-350M Integration | In upstream review | P0-MUST | Current PR ready; runtime experiments deferred |

## Track: colbert-ollama-20260519

LFM2-ColBERT-350M Ollama conversion support with:
- LFM2 embedding model conversion registration
- SentenceTransformers `modules.json` parsing
- nested safetensors discovery and tensor-name prefixing
- dense projection metadata support for ColBERT-style heads
- embedding documentation

The older tensor-loading, GGUF metadata patching, and per-token runtime experiments are retained in the track documents as historical/deferred context.

**Quick links:**
- [Index](tracks/colbert-ollama-20260519/index.md)
- [Requirements](tracks/colbert-ollama-20260519/requirements.md)
- [Design](tracks/colbert-ollama-20260519/design.md)
- [Contracts](tracks/colbert-ollama-20260519/contract.md)
- [Plan](tracks/colbert-ollama-20260519/plan.md)
- [Spec](tracks/colbert-ollama-20260519/spec.md)
- [Metadata](tracks/colbert-ollama-20260519/metadata.json)
