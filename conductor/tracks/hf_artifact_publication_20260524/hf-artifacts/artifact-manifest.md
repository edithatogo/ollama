# Artifact Manifest

Created: 2026-05-24

This manifest records candidate Hugging Face artifacts for the Ollama ColBERT and BitNet work. The initial upload is documentation-only.

| Candidate | Source | Intended HF location | Status | Upload decision | Reason |
| --- | --- | --- | --- | --- | --- |
| `README.md` model card | Local handoff documentation | Repository root | Prepared | Upload | Safe documentation created for this work. |
| `artifact-manifest.md` | Local handoff documentation | Repository root | Prepared | Upload | Safe documentation created for this work. |
| LFM2-ColBERT GGUF artifact | `LiquidAI/LFM2-ColBERT-350M`, sha `0c31032e995fe698f3ddd74f0ddb566cfd3d4d5a`, tagged `license:other` | Future model file | Not prepared | Blocked | Source license is not a standard permissive SPDX license in HF metadata; redistribution and generated-artifact provenance must be reviewed before upload. |
| Microsoft BitNet GGUF artifact | `microsoft/bitnet-b1.58-2B-4T`, sha `04c3b9ad9361b824064a1f25ea60a8be9599b127`, tagged `license:mit` | Future model file | Local reference only | Blocked | MIT tag is permissive, but this repo is not intended to mirror Microsoft weights; only upload a derived artifact if there is a separate, documented publication reason and checksum/provenance record. |
| BitNet local runner wrapper | `edithatogo/BitNet:local-bitnet-runner-wrapper` | GitHub source link only | Available on GitHub fork | Do not upload as model artifact | This is source code and belongs on GitHub, not as a Hugging Face model file. |
| Ollama ColBERT code branch | `edithatogo/ollama:feat/lfm2-embed-output-norm` | GitHub source link only | Open upstream PR | Do not upload as model artifact | Source code and review history belong on GitHub. |

## Source Metadata Snapshot

Checked on 2026-05-24 with `hf models info`:

| Source | License tag | Visibility | Gated | Last modified |
| --- | --- | --- | --- | --- |
| `LiquidAI/LFM2-ColBERT-350M` | `other` | Public | False | 2026-05-05 |
| `microsoft/bitnet-b1.58-2B-4T` | `mit` | Public | False | 2025-12-17 |

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
