# Per-Token MaxSim Runtime Support

## Overview

Define a future runtime track for ColBERT token-level embeddings and MaxSim-ready retrieval behavior. This is intentionally separate from the current Ollama LFM2-ColBERT conversion/docs PR, which only converts SentenceTransformers-style checkpoints and preserves dense projection metadata.

The current `/api/embed` behavior remains pooled-vector oriented. ColBERT late interaction requires token-level embeddings and MaxSim scoring semantics, so runtime support needs its own API, data-shape, validation, and performance contract before implementation.

## Scope

In scope for this future track:

- Runtime representation for token-level ColBERT embeddings.
- API or internal interface contract for exposing token-level embeddings, MaxSim-ready tensors, or server-side MaxSim scoring.
- Ownership decision for MaxSim scoring: Ollama API, llama.cpp backend, retrieval-layer client, or a hybrid boundary.
- Validation strategy against a trusted reference implementation.
- Performance and memory profiling for token-level output at realistic sequence lengths.
- Documentation explaining pooled vectors versus token-level late interaction.

Out of scope for this track:

- Current Ollama conversion/docs PR #16195.
- Native llama.cpp architecture work before its architecture contract is ready.
- Model weight redistribution or derived GGUF publication.
- Product-specific vector database or ranking UI implementation.
- Claiming ColBERT MaxSim support through `/api/embed` while it returns only one pooled vector per input.

## Functional Requirements

- [ ] Define a token-level embedding response shape, including token alignment, padding/truncation behavior, dtype, dimensions, and normalization semantics.
- [ ] Decide whether MaxSim scoring is computed server-side or left to the retrieval client.
- [ ] Define compatibility behavior for existing `/api/embed` clients.
- [ ] Define request controls for pooled output versus token-level output without breaking existing embedding calls.
- [ ] Define fail-closed diagnostics for models that lack token-level or MaxSim metadata.
- [ ] Add reference-output parity tests for token embeddings and MaxSim scores where supported.
- [ ] Add docs that clearly distinguish pooled semantic search from ColBERT late-interaction retrieval.

## Non-Functional Requirements

- Backward compatibility with existing embedding API behavior.
- Bounded memory behavior for long inputs and batches.
- Clear performance notes for token-level output, including output size and sequence-length sensitivity.
- License-safe fixtures and reproducible validation commands.
- No public support claim until the runtime API and parity tests exist.

## Acceptance Criteria

1. A runtime API contract defines how token-level embeddings or MaxSim-ready outputs are requested and returned.
2. Existing `/api/embed` pooled-vector behavior remains compatible.
3. MaxSim scoring ownership is documented and validated.
4. Reference parity tests cover token-level embeddings and MaxSim scores where the runtime supports them.
5. Unsupported combinations fail with actionable diagnostics.
6. Docs explain when to use pooled vectors versus token-level MaxSim retrieval.

## Current State

This is a granular future track. No runtime code changes are being implemented as part of the current Ollama conversion/docs PR.
