# Validation Evidence

Last updated: 2026-06-14

This page records validation evidence for the GitHub work referenced by this Hugging Face documentation repository. It does not represent an uploaded model artifact.

## Ollama ColBERT PR

PR:

- https://github.com/ollama/ollama/pull/16195

Current validated head:

- `1f4302ef4a65b6927242771249682ad4f014816d`

Rebase:

- Rebasing target: `ollama/ollama:main`
- Base commit: `12e04379c`
- Push method: `git push --force-with-lease fork feat/lfm2-embed-output-norm`
- Current shape: one focused commit containing conversion/documentation support. Older vendored `llama/llama.cpp` path changes were dropped because current `main` no longer tracks those files.

Focused validation passed:

```bash
go test -count=1 ./cmd ./convert ./parser
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

- https://github.com/ollama/ollama/pull/16195#issuecomment-4698915854

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
