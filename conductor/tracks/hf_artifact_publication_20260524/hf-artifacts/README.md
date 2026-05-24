---
license: other
library_name: ollama
tags:
- ollama
- colbert
- embeddings
- gguf
- bitnet
- local-ai
pipeline_tag: feature-extraction
---

# Ollama ColBERT Local Artifacts

This repository tracks local artifact notes for Ollama ColBERT and related BitNet setup work. It is documentation-only at this stage: no third-party model weights, GGUF files, or derived binaries are uploaded here.

## Status

Experimental public handoff repository for local validation and artifact planning.

GitHub remains the source of truth for code, review, branches, and pull requests. Hugging Face is used here for model-facing notes, artifact manifests, and future model-card context.

## Source Links

| Area | Link |
| --- | --- |
| Ollama ColBERT upstream PR | https://github.com/ollama/ollama/pull/16195 |
| Ollama handoff branch | https://github.com/edithatogo/ollama/tree/conductor/colbert-handoff |
| BitNet local wrapper branch | https://github.com/edithatogo/BitNet/tree/local-bitnet-runner-wrapper |
| BitNet generated-header ignore PR | https://github.com/microsoft/BitNet/pull/563 |

## What This Covers

- Local Ollama support work for LFM2/ColBERT-style embedding checkpoints.
- Handoff notes for validating ColBERT model loading and embedding behavior.
- Local BitNet setup notes for a Microsoft BitNet GGUF through the official BitNet runner.
- A conservative artifact manifest that separates safe documentation from blocked model-weight uploads.

## Local Ollama Validation

The Ollama work is tracked in GitHub. The key validation commands used for the code branch were:

```bash
go test -count=1 ./cmd ./convert ./parser ./model/models/lfm2 ./llama
find . -name '*.go' \
  -not -path './app/*' \
  -not -path './integration/*' \
  -not -path './.git/*' \
  -exec dirname {} \; | sort -u | sed 's#^\./#./#' | xargs go test -count=1
```

## Local BitNet Notes

The BitNet wrapper branch is a personal-fork convenience layer for local use. It is not proposed upstream as-is because it assumes local paths, a repo-local virtual environment, and Unix shell conventions.

Example local invocation from the fork branch:

```bash
bin/bitnet "Say ok" -n 1 -c 128 -temp 0
```

The upstream-suitable generated-header ignore change was split into a separate Microsoft BitNet pull request.

## Artifact Policy

This repository does not redistribute:

- Microsoft BitNet model weights.
- LiquidAI model weights.
- Generated GGUF files derived from third-party model weights.

Those artifacts should only be uploaded after source license, redistribution permissions, and provenance are reviewed and documented in `artifact-manifest.md`.

## Source Model Metadata Checked

The source model metadata was checked on 2026-05-24 before publication:

| Source model | Hugging Face metadata | Publication decision here |
| --- | --- | --- |
| `LiquidAI/LFM2-ColBERT-350M` | `license:other`, public, ungated, sha `0c31032e995fe698f3ddd74f0ddb566cfd3d4d5a` | Reference only; no weights or derived GGUF uploaded. |
| `microsoft/bitnet-b1.58-2B-4T` | `license:mit`, public, ungated, sha `04c3b9ad9361b824064a1f25ea60a8be9599b127` | Reference only; no weights or derived GGUF uploaded. |

## Recommended Use

Use this repository as a model-facing index for the GitHub work:

1. Follow the GitHub PRs for source changes.
2. Use this Hugging Face repo for artifact status and usage notes.
3. Add GGUF/model files only after license and provenance checks are complete.
