# Hugging Face Artifact Publication Track

## Overview

Create a Hugging Face publication path for the Ollama ColBERT and BitNet work that complements the GitHub repositories. GitHub remains the source of truth for code, issues, branches, and upstream pull requests. Hugging Face should hold model-facing artifacts, model cards, usage examples, and optional demos once artifact provenance and licensing are verified.

## Recommendation

Use Hugging Face as well as GitHub, not instead of GitHub.

- GitHub: source code, upstream PRs, review history, issue tracking, patches, and reproducible development state.
- Hugging Face: model card, GGUF artifact references or uploads, Ollama usage instructions, benchmark notes, and optional Space/demo material.

Do not upload Microsoft BitNet weights, LiquidAI weights, or derived GGUF artifacts until the source license, redistribution terms, and generated artifact provenance are explicitly checked.

## Candidate Hugging Face Repositories

### Preferred initial repo

`edithatogo/ollama-colbert-local-artifacts`

Purpose:
- Store a model-card-style README describing the local Ollama ColBERT integration.
- Link to GitHub PRs and branches.
- Document tested commands, hardware, and expected model behavior.
- Reference upstream model repositories instead of re-uploading weights by default.

Repo type:
- Model repo if it will eventually host GGUF/model artifacts.
- Space only if a runnable web demo is built.
- Dataset repo only if publishing benchmark data, logs, or evaluation outputs.

### Optional later repos

- `edithatogo/lfm2-colbert-ollama-gguf`: only if a redistributable GGUF conversion is produced and licensed for upload.
- `edithatogo/bitnet-local-runner-notes`: only if BitNet setup notes need their own standalone card.

## Functional Requirements

- Create a Hugging Face repo plan that does not duplicate GitHub as the code home.
- Prepare a README/model card with:
  - Summary of the Ollama ColBERT support work.
  - Links to GitHub PRs and branches.
  - Hardware and software validation context.
  - Exact local usage commands.
  - License and provenance notes.
  - Clear statement when model weights are referenced but not redistributed.
- Include an artifact manifest before upload:
  - File name.
  - Source repository.
  - Generation command.
  - Checksum.
  - License status.
  - Upload decision.
- Use `hf` CLI for authentication and upload.
- Keep public/private visibility explicit before repo creation.

## Non-Functional Requirements

- Avoid uploading third-party model weights without a verified redistribution basis.
- Avoid presenting experimental local integration as an official Ollama, LiquidAI, or Microsoft release.
- Keep artifact descriptions reproducible and date-stamped.
- Keep GitHub links as canonical for source changes.

## Acceptance Criteria

- A Hugging Face repo target is selected and documented.
- A README/model card draft exists locally before any upload.
- Artifact manifest records each candidate upload and its license/provenance decision.
- If a repo is created, it is initialized with documentation only unless model redistribution has been cleared.
- GitHub PR and branch references are included in the Hugging Face documentation.

## Out of Scope

- Replacing GitHub branches or pull requests with Hugging Face repos.
- Uploading Microsoft BitNet or LiquidAI model files before license review.
- Publishing benchmark claims without reproducible commands and outputs.
- Creating a Hugging Face Space before there is a stable runnable demo.

