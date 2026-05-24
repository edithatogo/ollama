# Validation Evidence

Last updated: 2026-05-24

This page records validation evidence for the GitHub work referenced by this Hugging Face documentation repository. It does not represent an uploaded model artifact.

## Ollama ColBERT PR

PR:

- https://github.com/ollama/ollama/pull/16195

Current validated head:

- `c0f56ec5e17c70da0d0dd213369b608d7ece66d5`

Rebase:

- Rebasing target: `ollama/ollama:main`
- Base commit: `275f122cd`
- Push method: `git push --force-with-lease fork feat/lfm2-embed-output-norm`

Focused validation passed:

```bash
go test -count=1 ./cmd ./convert ./parser ./model/models/lfm2 ./llama
```

Broad non-app package sweep passed:

```bash
find . -name '*.go' \
  -not -path './app/*' \
  -not -path './integration/*' \
  -not -path './.git/*' \
  -exec dirname {} \; | sort -u | sed 's#^\./#./#' | xargs go test -count=1
```

Notes:

- `app/*` was excluded because the local checkout does not include the built app distribution.
- `integration/*` was excluded because those packages are build-tagged and a blind sweep reports all Go files excluded by constraints.
- GitHub reported the PR as open and mergeable after the rebase.

Reviewer update comment:

- https://github.com/ollama/ollama/pull/16195#issuecomment-4528401509

## BitNet PR

PR:

- https://github.com/microsoft/BitNet/pull/563

Validated head:

- `dd1adf3e97f67335e79c27189a3262eace97dcf9`

Checks:

- Branch is based on current `microsoft/BitNet:main`.
- Branch is one commit ahead of `origin/main`.
- GitHub reported the PR as open and mergeable.
- `license/cla` check passed.

## Hugging Face Publication

Repository:

- https://huggingface.co/edithatogo/ollama-colbert-local-artifacts

Policy:

- Documentation only.
- No model weights uploaded.
- No GGUF files uploaded.
- No generated binaries uploaded.
- No third-party artifacts uploaded.

