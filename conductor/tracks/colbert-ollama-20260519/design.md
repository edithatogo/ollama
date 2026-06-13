# Design Document — Mermaid Diagrams

## Current Design Scope

As of the June 14 refresh, the active upstream PR design surface is the Ollama converter and embedding documentation:

- LFM2-ColBERT conversion registration.
- SentenceTransformers `modules.json` parsing.
- nested safetensors discovery and tensor-name prefixing.
- dense projection metadata handling for ColBERT-style embedding heads.

The diagrams below document the earlier runtime/GGUF investigation and should be treated as historical/deferred context unless a new runtime track is opened.

## Architecture Overview

```mermaid
graph TB
    subgraph "Ollama Server"
        API["/api/embed"]
        SERVER[Server]
        SCHED[Scheduler]
    end

    subgraph "Runner (--ollama-engine)"
        GORUNNER[Go OllamaRunner]
        LLAMARUNNER[Go LlamaRunner]
    end

    subgraph "Model Loader (C++ via CGo)"
        LLAMA_GO[llama.go - CGo entry]
        LLAMA_MODEL[llama-model.cpp]
        LLAMA_ARCH[llama-arch.cpp]
        LLAMA_LOADER[llama-model-loader.cpp]
    end

    subgraph "GGUF File"
        METADATA[Metadata KV pairs]
        TI[Tensor Info entries]
        TENSORS[Tensor Data]
    end

    subgraph "GPU Backend"
        METAL[Metal GPU]
        GGML[GGML Library]
    end

    API --> SERVER
    SERVER --> SCHED
    SCHED --> GORUNNER
    SCHED --> LLAMARUNNER
    GORUNNER --> GGML
    LLAMARUNNER --> LLAMA_GO
    LLAMA_GO --> LLAMA_MODEL
    LLAMA_GO --> LLAMA_ARCH
    LLAMA_MODEL --> LLAMA_LOADER
    LLAMA_LOADER --> TENSORS
    GGML --> METAL
    LLAMA_ARCH --> METADATA
    LLAMA_ARCH --> TI
```

## Tensor Name Resolution Flow

```mermaid
sequenceDiagram
    participant Loader as llama-model-loader
    participant Model as llama-model.cpp
    participant Arch as llama-arch.cpp
    participant GGUF as GGUF File

    Model->>Arch: LLM_TN(arch)
    Arch-->>Model: tn = LLM_TN_IMPL(LLM_ARCH_LFM2)
    
    Model->>Loader: create_tensor(tn(LLM_TENSOR_OUTPUT_NORM_LFM2, "weight"), {1024})
    Note over Model: PR Fix: was LLM_TENSOR_OUTPUT_NORM
    
    Loader->>Arch: tn.tensor -> LLM_TENSOR_OUTPUT_NORM_LFM2
    Arch-->>Loader: name = "token_embd_norm"
    Note over Arch: Line 311: maps to "token_embd_norm"
    
    Loader->>Loader: tn.str() = "token_embd_norm.weight"
    Loader->>GGUF: get_tensor_meta("token_embd_norm.weight")
    GGUF-->>Loader: ✅ Found!
    
    Note over Loader: Previously: was looking for "output_norm.weight"\nwhich doesn't exist in LFM2 GGUF files
```

## Expected Tensor Validation Flow

```mermaid
sequenceDiagram
    participant Model as llama-model.cpp
    participant Arch as llama-arch.cpp
    participant Loader as llama-model-loader
    participant GGUF as GGUF File

    Model->>Arch: llm_get_tensor_names(LLM_ARCH_LFM2)
    Arch-->>Model: [ATTN_NORM, ATTN_Q, ..., OUTPUT_NORM_LFM2, DENSE_2_OUT, OUTPUT]
    Note over Arch: Line 2042: DENSE_2_OUT added for ColBERT

    loop For each tensor (i = 0..148)
        Model->>Loader: create_tensor(tn(tensor_i, suffix), shape)
        Loader->>GGUF: get_tensor_meta(name)
        GGUF-->>Loader: ✅ found or ❌ missing
    end

    Model->>Loader: done_getting_tensors()
    Note over Loader: Checks: n_created (149) == n_tensors (149)
    Loader-->>Model: ✅ Pass!
```

## GGUF Binary Structure (for Pooling Type Patching)

```mermaid
graph LR
    subgraph "GGUF File Layout"
        HDR[Header 24B]
        KV[KV Pairs]
        TI[Tensor Info]
        TD[Tensor Data]
    end

    subgraph "KV Pair to Insert"
        KL[key_len: 17]
        KEY["lfm2.pooling_type"]
        VT[type: 4 UINT32]
        VAL[value: 1 mean]
    end

    HDR --> KV
    KV --> TI
    TI --> TD
```

## Pooling Type Detection Flow

```mermaid
flowchart TD
    A[Load GGUF] --> B{Has lfm2.pooling_type?}
    B -->|Yes| C[Set arch = lfm2_embed]
    B -->|No| D[Set arch = lfm2]
    C --> E[Capabilities: embedding]
    D --> F[Capabilities: completion]
    E --> G[/api/embed available]
    F --> H[/api/embed returns error]
```

## ColBERT Per-Token Forward Pass (Proposed)

```mermaid
flowchart TD
    A[Input tokens] --> B[Token Embedding]
    B --> C[LFM2 Encoder Layers 0..15]
    C --> D[Output RMSNorm]
    D --> E{Hidden States: 1024 x n_tokens}
    E --> F[dense_2: Linear 1024→128]
    E --> G[Mean Pooling]
    F --> H[L2 Normalize per token]
    G --> I[L2 Normalize]
    H --> J[Per-token embeddings: 128 x n_tokens]
    I --> K[Pooled embedding: 1024]
    J --> L[ColBERT MaxSim Retrieval]
    K --> M[Standard Cosine Similarity]
```
