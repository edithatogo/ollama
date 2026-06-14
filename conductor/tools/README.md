# Conductor Tools

Workspace-level helpers used by the ColBERT handoff and Conductor registry audit.

## audit-conductor-folders.py

Audits project-level `conductor/` registries under `/Volumes/PortableSSD/GitHub`
by default, records whether active registries have `tracks.md`, and compares the
current workspace against the saved June 14 audit baseline.

Common checks:

```bash
conductor/tools/audit-conductor-folders.py --compare-json /Volumes/PortableSSD/GitHub/conductor-folder-inventory-20260614.json
conductor/tools/audit-conductor-folders.py --verify-checksums /Volumes/PortableSSD/GitHub/conductor-folder-audit-20260614.sha256
```
