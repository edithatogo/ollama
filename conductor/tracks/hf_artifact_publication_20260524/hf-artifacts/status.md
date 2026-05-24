# Current Status

Last checked: 2026-05-24

## GitHub Pull Requests

| Repository | PR | Branch | State | Mergeable | Checks |
| --- | --- | --- | --- | --- | --- |
| `ollama/ollama` | [`#16195`](https://github.com/ollama/ollama/pull/16195) | `feat/lfm2-embed-output-norm` | Open | Yes | No status checks reported by GitHub. |
| `microsoft/BitNet` | [`#563`](https://github.com/microsoft/BitNet/pull/563) | `ignore-generated-kernel-headers` | Open | Yes | `license/cla` passed. |

## Hugging Face Repository

| Field | Value |
| --- | --- |
| Repo | `edithatogo/ollama-colbert-local-artifacts` |
| Visibility | Public |
| Gated | False |
| Current commit | See the Hugging Face repository commit history for the latest revision. |
| Content policy | Documentation only |

## Uploaded Files

- `.gitattributes`
- `README.md`
- `artifact-manifest.md`
- `github-links.md`
- `status.md`

No model weights, GGUF files, generated binaries, or third-party artifacts are uploaded here.

## Refresh Commands

Use these commands from a machine with `gh` and `hf` authenticated as the repository owner:

```bash
gh pr view 16195 --repo ollama/ollama \
  --json title,url,state,mergeable,statusCheckRollup,headRefName

gh pr view 563 --repo microsoft/BitNet \
  --json title,url,state,mergeable,statusCheckRollup,headRefName

hf models info edithatogo/ollama-colbert-local-artifacts
```

After editing this page locally, upload the documentation-only folder:

```bash
hf upload edithatogo/ollama-colbert-local-artifacts \
  conductor/tracks/hf_artifact_publication_20260524/hf-artifacts \
  . \
  --repo-type model \
  --commit-message "Refresh publication status"
```
