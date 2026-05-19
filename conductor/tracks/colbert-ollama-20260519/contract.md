# Interface Contracts

## Contract C-01: Tensor Name Resolution

### Provider: llama.cpp model loader (`llama-model.cpp`)
### Consumer: GGUF file (LFM2 architecture models)

```
Preconditions:
  - GGUF file has architecture "lfm2"
  - GGUF file contains tensor "token_embd_norm.weight"

Postconditions:
  - output_norm tensor is loaded from GGUF as "token_embd_norm.weight"
  - model->output_norm is non-null

Invariants:
  - LLM_TENSOR_OUTPUT_NORM_LFM2 maps to "token_embd_norm" (verified in llama-arch.cpp:311)
  - LLM_TENSOR_OUTPUT_NORM_LFM2 is in LFM2 expected tensor list (llama-arch.cpp:2041)
  - create_tensor() uses LLM_TENSOR_OUTPUT_NORM_LFM2 for LFM2 arch (llama-model.cpp:6284)
```

## Contract C-02: Expected Tensor Count

### Provider: llama.cpp architecture definition (`llama-arch.cpp`)
### Consumer: Model loader (`llama-model.cpp`)

```
Preconditions:
  - LFM2 architecture is selected (general.architecture == "lfm2")
  - GGUF file has 149 tensors

Postconditions:
  - done_getting_tensors() passes (n_created == n_tensors == 149)
  - All expected tensors are loaded

Invariants:
  - LFM2 expected tensor list includes: ATTN_NORM, ATTN_Q/K/V/OUT, ATTN_K/Q_NORM,
    FFN_DOWN/GATE/NORM/UP, SHORTCONV_CONV/INPROJ/OUTPROJ, 
    TOKEN_EMBD, OUTPUT_NORM_LFM2, OUTPUT, DENSE_2_OUT
  - Total: 18 per-layer tensors × variable layers + embedding + output_norm + output + dense_2 = 149
```

## Contract C-03: Embedding API Response

### Provider: Ollama server (`server/routes.go`)
### Consumer: API clients (mem0, CLI tools, etc.)

```
Request:
  POST /api/embed
  {
    "model": "lfm2-colbert:latest",
    "input": "Hello world"
  }

Response (contract):
  HTTP 200
  {
    "model": "lfm2-colbert:latest",
    "embeddings": [[float32 x 1024]],     // Pooled (current)
    "prompt_eval_count": integer
  }

Extended Response (proposed for ColBERT):
  HTTP 200
  {
    "model": "lfm2-colbert:latest",
    "embeddings": [[float32 x 128]],       // Per-token, after dense_2 + L2 norm
    "embedding_type": "colbert",           // Indicates per-token format
    "token_count": integer,
    "prompt_eval_count": integer
  }
```

## Contract C-04: Build System

### Provider: Go build (`go build`)
### Consumer: Developer

```
Preconditions:
  - Go 1.26.3+, C++17 compiler, Xcode CLI tools
  - CGO_ENABLED=1 (implicit on macOS)

Command:
  go build -a -o /tmp/ollama-final .

Postconditions:
  - Binary at /tmp/ollama-final is ~70.8 MB
  - Contains compiled C++ code via CGo (llama.go)
  - All .cpp files in llama/llama.cpp/src/ are compiled

Environment:
  PATH="/opt/homebrew/bin:$PATH"
  GOPATH=/Users/doughnut/go
  GOMODCACHE=/Users/doughnut/go/pkg/mod
```

## Contract C-05: GGUF Metadata (Pooling Type)

### Provider: GGUF file
### Consumer: Ollama model detector

```
Required for embedding capability:
  KEY: "lfm2.pooling_type"   (or "bert.pooling_type" for BERT models)
  TYPE: UINT32
  VALUE: 1 (mean pooling)

Without this key:
  Ollama treats model as "completion" only
  /api/embed returns: "this model does not support embeddings"

With this key:
  Ollama adds "_embed" to architecture name
  Model appears with capabilities: ["embedding"]
```
