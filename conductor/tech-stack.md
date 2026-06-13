# Tech Stack

## Core Dependencies
| Component | Version | Source |
|-----------|---------|--------|
| ollama | `ollama/ollama@12e04379c` plus PR branch `feat/lfm2-embed-output-norm` | edithatogo/ollama |
| llama.cpp / runtime backend | Managed by current upstream Ollama tree | ollama/ollama |
| ggml | Vendored with ollama | ggml-org/ggml |
| Go | 1.26.3 | Homebrew |
| CMake | 4.3.2 | Homebrew |
| Python gguf | 0.19.0 | PyPI |

## Target Hardware
- Apple M1 Max, 32GB RAM, macOS 26.3.1
- Metal GPU backend (Apple M1 Max GPU)

## Build System
- Current PR validation uses Go package tests for conversion and parser code.
- The June 14 PR shape is conversion/docs-only and does not modify vendored runtime files.
- Older CGo/runtime build notes are retained in the handoff as historical local-experiment context.

## Key Files Modified
| File | Change | Track |
|------|--------|-------|
| `convert/convert_lfm2.go` | LFM2-ColBERT conversion support | Current PR |
| `convert/convert_lfm2_test.go` | conversion regression coverage | Current PR |
| `convert/reader_safetensors.go` | nested safetensors path handling | Current PR |
| `convert/convert_embeddinggemma.go` | nested dense-module compatibility | Current PR |
| `docs/capabilities/embeddings.mdx` | embedding capability docs | Current PR |
