# Implementation Plan

## Phase 1: Repository Decision

- [x] Task: Select the Hugging Face repo target
    - [x] Confirm repo owner: `edithatogo`
    - [x] Confirm repo name: `ollama-colbert-local-artifacts` unless superseded
    - [x] Confirm repo type: model repo for model-card and possible future artifacts
    - [x] Confirm visibility: private for staging, public only after content review
- [x] Task: Record GitHub source-of-truth links
    - [x] Link Ollama PR `https://github.com/ollama/ollama/pull/16195`
    - [x] Link Ollama handoff branch `edithatogo/ollama:conductor/colbert-handoff`
    - [x] Link BitNet fork utility branch `edithatogo/BitNet:local-bitnet-runner-wrapper`
    - [x] Link BitNet upstream PR `https://github.com/microsoft/BitNet/pull/563`

## Phase 2: Artifact and License Review

- [x] Task: Build artifact manifest
    - [x] List candidate ColBERT GGUF artifacts
    - [x] List candidate BitNet setup notes or wrapper docs
    - [x] Record source model repo and license for each candidate
    - [x] Record generation command and checksum for any generated file
- [x] Task: Decide upload eligibility
    - [x] Mark third-party weights as referenced-only until license review is complete
    - [x] Mark local documentation as safe to upload
    - [x] Mark generated model files as blocked unless redistribution is verified

## Phase 3: Model Card Draft

- [x] Task: Draft `README.md`
    - [x] Summarize scope and experimental status
    - [x] Include GitHub source links
    - [x] Include local Ollama commands
    - [x] Include BitNet runner notes as a related setup section
    - [x] Include hardware/software validation context
    - [x] Include license and provenance section
- [x] Task: Draft `artifact-manifest.md`
    - [x] Use one row per candidate artifact
    - [x] Include upload decision and reason

## Phase 4: Hugging Face Repo Setup

- [x] Task: Verify auth
    - [x] Run `hf auth whoami`
- [x] Task: Create staging repo only after repo name and visibility are confirmed
    - [x] Run `hf repo create edithatogo/ollama-colbert-local-artifacts --type model --private --exist-ok`
- [x] Task: Upload documentation-only initial state
    - [x] Run `hf upload edithatogo/ollama-colbert-local-artifacts ./hf-artifacts . --repo-type model`
- [x] Task: Verify remote content
    - [x] Download and inspect uploaded Markdown files
    - [x] Confirm no model weights were uploaded accidentally

## Phase 5: Publication Decision

- [x] Task: Decide whether to make the repo public
    - [x] Confirm wording avoids official-project ambiguity
    - [x] Confirm all third-party licenses are respected
    - [x] Confirm links to upstream PRs are current
- [x] Task: Publish or keep private
    - [x] If public, document the publication date
    - [x] If private, document remaining blockers

## Completion Notes

- Created private Hugging Face model repo: `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts`
- Uploaded documentation-only initial state: `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/bd929947cadbfdc1ff553afd2a0191b354680ec3`
- Uploaded files:
    - `README.md`
    - `artifact-manifest.md`
    - `github-links.md`
- Verified by downloading the three uploaded Markdown files to `/tmp/ollama-colbert-local-artifacts-verify`.
- No model weights, GGUF files, or generated binaries were uploaded.
- Repo was later made public after documentation-only contents and source metadata were verified.

## Phase 6: Public Documentation Release

- [x] Task: Check source model metadata before making docs public
    - [x] `LiquidAI/LFM2-ColBERT-350M`: public, ungated, `license:other`, sha `0c31032e995fe698f3ddd74f0ddb566cfd3d4d5a`
    - [x] `microsoft/bitnet-b1.58-2B-4T`: public, ungated, `license:mit`, sha `04c3b9ad9361b824064a1f25ea60a8be9599b127`
- [x] Task: Publish documentation-only Hugging Face repo
    - [x] Upload updated provenance wording
    - [x] Set repo visibility to public
    - [x] Verify remote metadata reports `private: false`

## Public Release Notes

- Updated provenance commit: `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/421e4a3002e372ecd029cff2628c4618c6925da7`
- Public repo URL: `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts`
- Verified remote metadata:
    - `private: false`
    - `gated: false`
    - `sha: 421e4a3002e372ecd029cff2628c4618c6925da7`
    - files: `.gitattributes`, `README.md`, `artifact-manifest.md`, `github-links.md`
- No model weights, GGUF files, or generated binaries were uploaded.

## Phase 7: Status Index

- [x] Task: Add public status page
    - [x] Record Ollama PR state
    - [x] Record BitNet PR state
    - [x] Record HF visibility and docs-only policy
    - [x] Upload `status.md` to Hugging Face

Status page upload commit:

- `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/3ff2608dd33b3af8f80776b33e46f9f7ac292ff7`
- Follow-up commit removed the self-referential current-commit row from `status.md` because uploading the file necessarily changes the latest HF commit:
  `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/1c152a60ff4418172d0f2f49aa73fcc293a57a18`

## Phase 8: Status Maintenance

- [x] Task: Add refresh commands to public status page
    - [x] Include Ollama PR status command
    - [x] Include BitNet PR status command
    - [x] Include Hugging Face repo metadata command
    - [x] Upload refreshed status page

Refresh commands upload commit:

- `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/96a4e104a9c99be9c4ae14a5c193622660c505fe`

## Phase 9: Status Refresh Automation

- [x] Task: Add refresh script
    - [x] Query Ollama PR status with `gh`
    - [x] Query BitNet PR status with `gh`
    - [x] Query Hugging Face repo metadata with `hf`
    - [x] Regenerate `hf-artifacts/status.md`
    - [x] Upload regenerated status page

Automation upload commit:

- `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/11abba164a530cc3f7ab6ca034cf71faf5aa8006`
- Stable metadata wording upload commit:
  `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/6408328ee6407dc42091a269281574cb9dd11c64`
- June 14 maintenance fix: `refresh-status.sh` now uses local date instead of UTC date so the public status page matches the Australia/Sydney working context.

## Phase 10: Validation Evidence Page

- [x] Task: Add `validation.md`
    - [x] Record Ollama PR head and rebase base
    - [x] Record focused validation command
    - [x] Record broad non-app validation command
    - [x] Record BitNet PR freshness and CLA check
    - [x] Record docs-only HF publication policy
    - [x] Upload validation page to Hugging Face

Validation page upload commit:

- `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/b2281f1b1c362e42a3d34546bd0ee55fe496e81f`
- June 14 validation refresh:
  `https://huggingface.co/edithatogo/ollama-colbert-local-artifacts/commit/97ed641cb2c65f6a622c5280f0a87ae954666aaf`
