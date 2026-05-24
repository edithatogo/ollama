# Track Spec

## Goal
Implement native ColBERT support in Ollama model loading for LFM2-style models while preserving compatibility.

## Functional Requirements
- Ensure `llama.cpp` uses correct output norm tensor name for LFM2 outputs.
- Add/verify ColBERT-specific handling in the model loading path.
- Validate loading of the target model without `missing tensor 'output_norm'` failures.

## Acceptance Criteria
- Loading logs no longer report missing `output_norm` for affected LFM2/ColBERT model.
- No regressions to unrelated model families.
- Reproducible changesets and PR/issue references prepared upstream.
