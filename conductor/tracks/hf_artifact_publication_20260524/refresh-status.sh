#!/usr/bin/env bash
set -euo pipefail

TRACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_DIR="$TRACK_DIR/hf-artifacts"
STATUS_FILE="$ARTIFACT_DIR/status.md"
HF_REPO="edithatogo/ollama-colbert-local-artifacts"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_cmd gh
require_cmd jq

if command -v hf >/dev/null 2>&1; then
  HF_BIN="hf"
elif [ -x /Users/doughnut/.local/bin/hf ]; then
  HF_BIN="/Users/doughnut/.local/bin/hf"
else
  echo "Missing required command: hf" >&2
  exit 1
fi

ollama_json="$(gh pr view 16195 --repo ollama/ollama --json title,url,state,mergeable,statusCheckRollup,headRefName)"
bitnet_json="$(gh pr view 563 --repo microsoft/BitNet --json title,url,state,mergeable,statusCheckRollup,headRefName)"
hf_json="$("$HF_BIN" models info "$HF_REPO")"

format_mergeable() {
  case "$1" in
    MERGEABLE) echo "Yes" ;;
    CONFLICTING) echo "No" ;;
    UNKNOWN|"") echo "Unknown" ;;
    *) echo "$1" ;;
  esac
}

format_checks() {
  local json="$1"
  local count
  count="$(jq '.statusCheckRollup | length' <<<"$json")"
  if [ "$count" -eq 0 ]; then
    echo "No status checks reported by GitHub."
    return
  fi

  jq -r '
    .statusCheckRollup
    | map(
        if .__typename == "CheckRun" then
          "\(.name): \(.conclusion // .status)"
        else
          "\(.context // "status"): \(.state // "unknown")"
        end
      )
    | join("; ")
  ' <<<"$json"
}

ollama_state="$(jq -r '.state' <<<"$ollama_json")"
ollama_branch="$(jq -r '.headRefName' <<<"$ollama_json")"
ollama_mergeable="$(format_mergeable "$(jq -r '.mergeable // ""' <<<"$ollama_json")")"
ollama_checks="$(format_checks "$ollama_json")"

bitnet_state="$(jq -r '.state' <<<"$bitnet_json")"
bitnet_branch="$(jq -r '.headRefName' <<<"$bitnet_json")"
bitnet_mergeable="$(format_mergeable "$(jq -r '.mergeable // ""' <<<"$bitnet_json")")"
bitnet_checks="$(format_checks "$bitnet_json")"

hf_private="$(jq -r '.private' <<<"$hf_json")"
hf_gated="$(jq -r '.gated' <<<"$hf_json")"
hf_files="$(jq -r '.siblings[].rfilename' <<<"$hf_json" | sort)"

if [ "$hf_private" = "false" ]; then
  hf_visibility="Public"
else
  hf_visibility="Private"
fi

today="$(date -u +%Y-%m-%d)"

{
  cat <<EOF
# Current Status

Last checked: $today

## GitHub Pull Requests

| Repository | PR | Branch | State | Mergeable | Checks |
| --- | --- | --- | --- | --- | --- |
| \`ollama/ollama\` | [\`#16195\`](https://github.com/ollama/ollama/pull/16195) | \`$ollama_branch\` | $ollama_state | $ollama_mergeable | $ollama_checks |
| \`microsoft/BitNet\` | [\`#563\`](https://github.com/microsoft/BitNet/pull/563) | \`$bitnet_branch\` | $bitnet_state | $bitnet_mergeable | $bitnet_checks |

## Hugging Face Repository

| Field | Value |
| --- | --- |
| Repo | \`$HF_REPO\` |
| Visibility | $hf_visibility |
| Gated | $hf_gated |
| Latest commit | See the Hugging Face repository commit history for the latest revision. |
| Content policy | Documentation only |

## Uploaded Files

EOF

  while IFS= read -r file; do
    printf -- "- \`%s\`\n" "$file"
  done <<<"$hf_files"

  cat <<'EOF'

No model weights, GGUF files, generated binaries, or third-party artifacts are uploaded here.

## Refresh Commands

Use this script from the Conductor handoff branch:

```bash
conductor/tracks/hf_artifact_publication_20260524/refresh-status.sh
```

To regenerate and upload the documentation-only status page:

```bash
conductor/tracks/hf_artifact_publication_20260524/refresh-status.sh --upload
```
EOF
} > "$STATUS_FILE"

echo "Updated $STATUS_FILE"

if [ "${1:-}" = "--upload" ]; then
  "$HF_BIN" upload "$HF_REPO" "$ARTIFACT_DIR" . \
    --repo-type model \
    --commit-message "Refresh publication status"
fi
