# Artifact Manifest

Created: 2026-05-24

This manifest records candidate Hugging Face artifacts for the Ollama ColBERT and BitNet work. The initial upload is documentation-only.

| Candidate | Source | Intended HF location | Status | Upload decision | Reason |
| --- | --- | --- | --- | --- | --- |
| `README.md` model card | Local handoff documentation | Repository root | Prepared | Upload | Safe documentation created for this work. |
| `artifact-manifest.md` | Local handoff documentation | Repository root | Prepared | Upload | Safe documentation created for this work. |
| LFM2-ColBERT GGUF artifact | LiquidAI LFM2/ColBERT source model or generated local conversion | Future model file | Not prepared | Blocked | Redistribution and generated-artifact provenance must be reviewed before upload. |
| Microsoft BitNet GGUF artifact | Microsoft BitNet source model or local Ollama blob | Future model file | Local reference only | Blocked | Do not re-upload Microsoft weights or derived files without explicit redistribution review. |
| BitNet local runner wrapper | `edithatogo/BitNet:local-bitnet-runner-wrapper` | GitHub source link only | Available on GitHub fork | Do not upload as model artifact | This is source code and belongs on GitHub, not as a Hugging Face model file. |
| Ollama ColBERT code branch | `edithatogo/ollama:feat/lfm2-embed-output-norm` | GitHub source link only | Open upstream PR | Do not upload as model artifact | Source code and review history belong on GitHub. |

## Upload Rules

- Documentation is uploadable.
- Source-code branches stay on GitHub.
- Third-party or derived model files require license review before upload.
- Any future binary artifact must include:
  - Source repository.
  - Source revision or release.
  - Generation command.
  - SHA256 checksum.
  - License and redistribution decision.
  - Date generated.

