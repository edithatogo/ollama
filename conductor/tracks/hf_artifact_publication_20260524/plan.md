# Implementation Plan

## Phase 1: Repository Decision

- [ ] Task: Select the Hugging Face repo target
    - [ ] Confirm repo owner: `edithatogo`
    - [ ] Confirm repo name: `ollama-colbert-local-artifacts` unless superseded
    - [ ] Confirm repo type: model repo for model-card and possible future artifacts
    - [ ] Confirm visibility: private for staging, public only after content review
- [ ] Task: Record GitHub source-of-truth links
    - [ ] Link Ollama PR `https://github.com/ollama/ollama/pull/16195`
    - [ ] Link Ollama handoff branch `edithatogo/ollama:conductor/colbert-handoff`
    - [ ] Link BitNet fork utility branch `edithatogo/BitNet:local-bitnet-runner-wrapper`
    - [ ] Link BitNet upstream PR `https://github.com/microsoft/BitNet/pull/563`

## Phase 2: Artifact and License Review

- [ ] Task: Build artifact manifest
    - [ ] List candidate ColBERT GGUF artifacts
    - [ ] List candidate BitNet setup notes or wrapper docs
    - [ ] Record source model repo and license for each candidate
    - [ ] Record generation command and checksum for any generated file
- [ ] Task: Decide upload eligibility
    - [ ] Mark third-party weights as referenced-only until license review is complete
    - [ ] Mark local documentation as safe to upload
    - [ ] Mark generated model files as blocked unless redistribution is verified

## Phase 3: Model Card Draft

- [ ] Task: Draft `README.md`
    - [ ] Summarize scope and experimental status
    - [ ] Include GitHub source links
    - [ ] Include local Ollama commands
    - [ ] Include BitNet runner notes as a related setup section
    - [ ] Include hardware/software validation context
    - [ ] Include license and provenance section
- [ ] Task: Draft `artifact-manifest.md`
    - [ ] Use one row per candidate artifact
    - [ ] Include upload decision and reason

## Phase 4: Hugging Face Repo Setup

- [ ] Task: Verify auth
    - [ ] Run `hf auth whoami`
- [ ] Task: Create staging repo only after repo name and visibility are confirmed
    - [ ] Run `hf repo create edithatogo/ollama-colbert-local-artifacts --type model --private`
- [ ] Task: Upload documentation-only initial state
    - [ ] Run `hf upload edithatogo/ollama-colbert-local-artifacts ./hf-artifacts . --repo-type model`
- [ ] Task: Verify remote content
    - [ ] Open or inspect the Hugging Face repo page
    - [ ] Confirm no model weights were uploaded accidentally

## Phase 5: Publication Decision

- [ ] Task: Decide whether to make the repo public
    - [ ] Confirm wording avoids official-project ambiguity
    - [ ] Confirm all third-party licenses are respected
    - [ ] Confirm links to upstream PRs are current
- [ ] Task: Publish or keep private
    - [ ] If public, document the publication date
    - [ ] If private, document remaining blockers

