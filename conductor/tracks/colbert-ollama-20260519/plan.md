# Implementation Plan

## Phase 0: Foundation (✅ Complete)

### T-01: Tensor Name Fix
- [x] Add `LLM_TENSOR_OUTPUT_NORM_LFM2` to expected tensor list (already existed)
- [x] Change `create_tensor` call from `LLM_TENSOR_OUTPUT_NORM` to `LLM_TENSOR_OUTPUT_NORM_LFM2`
- [x] Verify: `llama-arch.cpp:311` maps to `"token_embd_norm"`
- [x] Build binary and verify error changes from `missing tensor 'output_norm'`
- [x] Submit PR #16195 to ollama/ollama

### T-02: DENSE_2_OUT Addition
- [x] Add `LLM_TENSOR_DENSE_2_OUT` to LFM2 expected list at `llama-arch.cpp:2042`
- [x] Commit and push to fork branch
- [ ] Submit as separate PR to ollama/ollama

## Phase 1: Model Loading (🟡 In Progress)

### T-03: Pooling Type Metadata
- [ ] Binary-patch Q4_K_M GGUF to insert `lfm2.pooling_type = 1`
- [ ] Alternative: Use gguf library with raw file I/O workaround
- [ ] Alternative: Download F16 model (already has pooling_type) and rename tensor only
- [ ] Verify model shows capabilities: ["embedding"]
- [ ] Test `/api/embed` returns valid embeddings

## Phase 2: SOTA Features (⬜ Not Started)

### T-04: ColBERT Per-Token Embeddings
- [ ] Add `dense_2` linear layer to LFM2 Go model struct
- [ ] Implement forward pass: hidden → dense_2 → L2 norm
- [ ] Add per-token embedding output path
- [ ] Extend `/api/embed` response format for multi-vector
- [ ] Test with MaxSim scoring (pylate or manual)

## Phase 3: Polish (⬜ Not Started)

### T-05: Upstream
- [ ] Submit DENSE_2_OUT addition as PR to ollama/ollama
- [ ] Consider PR to ggml-org/llama.cpp for both fixes
- [ ] Respond to PR #16195 review feedback

### T-06: Testing
- [ ] Automated test for LFM2 model loading
- [ ] Regression test for existing LFM2 text models
- [ ] Benchmark embeddings vs nomic-embed-text

## Dependencies

```mermaid
graph TD
    T01[T-01: Tensor Name Fix] --> T05[T-05: Upstream]
    T02[T-02: DENSE_2_OUT] --> T03[T-03: Pooling Type]
    T03 --> T06[T-06: Testing]
    T02 --> T04[T-04: ColBERT Per-Token]
    T04 --> T06
    T01 --> T03
```

## Timeline

| Phase | Started | Completed | Notes |
|-------|---------|-----------|-------|
| Phase 0 | 2026-05-14 | 2026-05-19 | Both fixes committed |
| Phase 1 | 2026-05-19 | — | Blocked by gguf writer limitation |
| Phase 2 | — | — | Depends on Phase 1 |
| Phase 3 | — | — | After Phase 1+2 |
