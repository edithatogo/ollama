# Track: LFM2-ColBERT-350M Ollama Integration

## ID
`colbert-ollama-20260519`

## Status
🟡 In Progress

## Summary
Implement native support for the LFM2-ColBERT-350M model as an embedding model in ollama. This involves fixing two bugs in the C++ model loader (tensor name mismatch and missing expected tensor), adding pooling type metadata to the GGUF file, and optionally implementing per-token ColBERT late interaction embeddings.

## Sub-tracks

| ID | Name | Status | Priority |
|----|------|--------|----------|
| T-01 | Tensor Name Fix (token_embd_norm → output_norm) | ✅ Complete | P0-MUST |
| T-02 | DENSE_2_OUT Expected Tensor Addition | ✅ Complete | P0-MUST |
| T-03 | Pooling Type Metadata Patching | 🟡 In Progress | P0-MUST |
| T-04 | ColBERT Per-Token Embedding Forward Pass | ⬜ Not Started | P1-SHOULD |
| T-05 | Upstream PR Submission & Merge | 🟡 In Progress | P0-MUST |
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
- Built binary: `/tmp/ollama-final`
- Handoff: `HANDOFF.md` (repo root)
