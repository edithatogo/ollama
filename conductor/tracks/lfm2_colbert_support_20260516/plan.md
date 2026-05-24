# Implementation Plan

## Phase 1: Reproduce and confirm
- [x] Task: Reproduce failure
  - [x] Run model load with recent logs reproducing missing tensor
  - [x] Confirm expected tensor mapping path
- [x] Task: Conductor - User Manual Verification 'Phase 1'

## Phase 2: Implement fix in llm loader
- [x] Task: Patch LFM2 output norm mapping
  - [x] Update tensor key resolution to use `token_embd_norm` alias where needed
  - [x] Keep non-LFM2 behavior unchanged
- [x] Task: Conductor - User Manual Verification 'Phase 2'

## Phase 3: Validate + upstream path
- [x] Task: Validate compilation and model load checks
  - [x] Confirm no missing tensor errors for the target model family
- [x] Task: Conductor - User Manual Verification 'Phase 3'

## Completion Notes
- Existing llama.cpp loader code uses `token_embd_norm` for LFM2 output norm lookup.
- Validation passed: `go test -count=1 ./llama`, `go build -o ./ollama .`, and `cmake --build --preset CPU`.
