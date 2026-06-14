# Implementation Plan: Per-Token MaxSim Runtime Support

## Phase 0: Track Boundary and Setup

- [x] Task: Split per-token MaxSim runtime support from the current Ollama conversion/docs PR
    - [x] Record that PR #16195 remains scoped to conversion/docs support.
    - [x] Record that `/api/embed` currently returns pooled vectors, not token-level MaxSim outputs.
    - [x] Keep runtime code changes out of this setup pass.
- [x] Task: Make the future runtime track granular enough to implement safely later
    - [x] Define scope and out-of-scope boundaries in `spec.md`.
    - [x] Define dependency gates in `metadata.json`.
    - [x] Break future implementation into API contract, backend capability, scoring boundary, validation, and docs phases.

## Phase 1: Runtime API Contract

- [ ] Task: Define token-level output shape
    - [ ] Specify tensor dimensions and batch layout.
    - [ ] Specify token alignment, token ids, and text-span metadata if exposed.
    - [ ] Specify padding, truncation, and attention-mask behavior.
    - [ ] Specify dtype and normalization behavior.
- [ ] Task: Define request controls
    - [ ] Decide whether token-level output is a new endpoint, new option, or model capability mode.
    - [ ] Preserve default pooled-vector behavior for existing `/api/embed` clients.
    - [ ] Define diagnostics for unsupported models or incompatible options.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Runtime API Contract' (Protocol in workflow.md)

## Phase 2: Backend Capability and Metadata

- [ ] Task: Define required GGUF/model metadata
    - [ ] Identify metadata that proves token-level output is available.
    - [ ] Identify metadata that proves MaxSim scoring is supported or deferred.
    - [ ] Define dense projection and normalization metadata requirements.
- [ ] Task: Align with native llama.cpp architecture track
    - [ ] Consume the native ColBERT architecture contract once available.
    - [ ] Avoid duplicating architecture decisions in the Ollama runtime layer.
    - [ ] Document any Ollama-specific adapter boundary.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Backend Capability and Metadata' (Protocol in workflow.md)

## Phase 3: MaxSim Scoring Boundary

- [ ] Task: Decide scoring ownership
    - [ ] Evaluate server-side MaxSim in Ollama.
    - [ ] Evaluate exposing token embeddings for client-side retrieval stacks.
    - [ ] Evaluate a hybrid path with explicit capability flags.
- [ ] Task: Define score semantics
    - [ ] Specify similarity metric, normalization assumptions, and mask handling.
    - [ ] Specify document/query role handling.
    - [ ] Specify batching behavior and memory limits.
- [ ] Task: Conductor - Automated Review and Checkpoint 'MaxSim Scoring Boundary' (Protocol in workflow.md)

## Phase 4: Implementation and Validation

- [ ] Task: Implement only after API and backend contracts are approved
    - [ ] Add runtime capability detection.
    - [ ] Add token-level output path or MaxSim path according to the contract.
    - [ ] Preserve pooled output behavior.
- [ ] Task: Add tests
    - [ ] Test successful token-level output.
    - [ ] Test unsupported model diagnostics.
    - [ ] Test pooled-output compatibility.
    - [ ] Test MaxSim parity if scoring is implemented server-side.
- [ ] Task: Add performance evidence
    - [ ] Benchmark memory and latency by sequence length.
    - [ ] Benchmark batch behavior.
    - [ ] Record guidance for practical retrieval workloads.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Implementation and Validation' (Protocol in workflow.md)

## Phase 5: Documentation and Publication

- [ ] Task: Document user-facing behavior
    - [ ] Explain pooled vectors versus token-level ColBERT retrieval.
    - [ ] Explain API options and capability detection.
    - [ ] Explain limitations and unsupported paths.
- [ ] Task: Update HF artifact notes if public validation changes
    - [ ] Keep GitHub as source of truth for code.
    - [ ] Keep HF docs-only unless license/provenance permits artifacts.
    - [ ] Record validation commands and exact commits.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Documentation and Publication' (Protocol in workflow.md)
