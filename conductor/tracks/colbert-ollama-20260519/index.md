# Track: LFM2-ColBERT-350M Ollama Integration

## ID
`colbert-ollama-20260519`

## Status
🟡 In Upstream Review

## Summary
Implement Ollama conversion support for LFM2-ColBERT-350M style embedding models. The current upstream PR is a focused conversion/docs branch; older runtime tensor-loading and GGUF metadata experiments are retained here as historical context only.

## Sub-tracks

| ID | Name | Status | Priority |
|----|------|--------|----------|
| T-01 | Tensor Name Fix (token_embd_norm -> output_norm) | Historical | P0-MUST |
| T-02 | DENSE_2_OUT Expected Tensor Addition | Historical | P0-MUST |
| T-03 | Pooling Type Metadata Patching | Deferred / separate track | P0-MUST |
| T-04 | ColBERT Per-Token Embedding Forward Pass | Deferred / separate track | P1-SHOULD |
| T-05 | Upstream PR Submission & Merge | 🟡 In Review | P0-MUST |
| T-06 | Build System & Testing Framework | ✅ Complete | P1-SHOULD |
| T-07 | Documentation & Handoff | ✅ Complete | P2-COULD |

## Documents
- [requirements.md](./requirements.md) — MoSCoW requirements
- [design.md](./design.md) — Mermaid architecture diagrams
- [contract.md](./contract.md) — Interface contracts
- [plan.md](./plan.md) — Implementation plan
- [spec.md](./spec.md) — Technical specification
- [metadata.json](./metadata.json) — Machine-readable metadata

## Key Artifacts
- Branch: `feat/lfm2-embed-output-norm` on `edithatogo/ollama`
- PR #16195: https://github.com/ollama/ollama/pull/16195
- Current PR head: `1f4302ef4a65b6927242771249682ad4f014816d`
- Handoff: `HANDOFF.md` (repo root)
