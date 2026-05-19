# Tech Stack

## Core Dependencies
| Component | Version | Source |
|-----------|---------|--------|
| ollama | v0.25.0-rc0 (branch `feat/lfm2-embed-output-norm`) | edithatogo/ollama |
| llama.cpp (vendored) | ec98e2002 | ggml-org/llama.cpp |
| ggml | Vendored with ollama | ggml-org/ggml |
| Go | 1.26.3 | Homebrew |
| CMake | 4.3.2 | Homebrew |
| Python gguf | 0.19.0 | PyPI |

## Target Hardware
- Apple M1 Max, 32GB RAM, macOS 26.3.1
- Metal GPU backend (Apple M1 Max GPU)

## Build System
- Go build with CGo for C++ compilation
- C++ files in `llama/llama.cpp/src/` compiled via CGo
- Metal GPU acceleration via GGML backend

## Key Files Modified
| File | Change | Track |
|------|--------|-------|
| `llama/llama.cpp/src/llama-model.cpp` | L6284: OUTPUT_NORM → OUTPUT_NORM_LFM2 | T-01 |
| `llama/llama.cpp/src/llama-arch.cpp` | Added DENSE_2_OUT to LFM2 expected list | T-02 |
