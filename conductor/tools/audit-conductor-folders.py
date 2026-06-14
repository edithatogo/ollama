#!/usr/bin/env python3
"""Audit Conductor registries under a workspace root.

The script intentionally ignores dependency/build folders and the local archive
folder created during the 2026-06-14 cleanup. It reports project-level
Conductor registries, flags active registries missing tracks.md, and lists
archived orphan/placeholder entries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SKIP_PARTS = {
    ".git",
    ".mypy_cache",
    ".nox",
    ".playwright-cli",
    ".playwright-mcp",
    ".pytest_cache",
    ".ruff_cache",
    ".snakemake",
    "node_modules",
    ".venv",
    ".venvs",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "target",
    "venv",
}

TOOL_INTERNAL_MARKERS = (
    "/conductor/.claude/",
    "/conductor/commands/",
    "/conductor/skills/",
)


def default_artifact_paths(root: Path) -> list[Path]:
    return [
        root / "audit-conductor-folders.py",
        root / "conductor-folder-inventory-20260614.md",
        root / "conductor-folder-inventory-20260614.json",
        root / "conductor-folder-audit-20260614.generated.md",
    ]


def default_json_path(root: Path) -> Path:
    return root / "conductor-folder-inventory-20260614.json"


def default_markdown_path(root: Path) -> Path:
    return root / "conductor-folder-audit-20260614.generated.md"


def default_checksum_path(root: Path) -> Path:
    return root / "conductor-folder-audit-20260614.sha256"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checksum_manifest(paths: list[Path]) -> str:
    lines = [f"{sha256_file(path)}  {path}" for path in paths]
    return "\n".join(lines) + "\n"


def verify_checksum_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            expected, filename = line.split(None, 1)
        except ValueError:
            errors.append(f"line {line_number}: malformed checksum line")
            continue
        candidate = Path(filename.strip())
        if not candidate.exists():
            errors.append(f"{candidate}: missing")
            continue
        actual = sha256_file(candidate)
        if actual != expected:
            errors.append(f"{candidate}: expected {expected}, got {actual}")
    return errors


def git_value(path: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def should_skip(path: Path, include_archive: bool) -> bool:
    parts = set(path.parts)
    if parts & SKIP_PARTS:
        return True
    if not include_archive and "_archive" in parts:
        return True
    normalized = str(path)
    return any(marker in normalized for marker in TOOL_INTERNAL_MARKERS)


def track_dir_count(conductor_dir: Path) -> int:
    tracks_dir = conductor_dir / "tracks"
    if not tracks_dir.exists():
        return 0
    return sum(1 for child in tracks_dir.iterdir() if child.is_dir())


def iter_conductor_dirs(root: Path, include_archive: bool) -> list[Path]:
    conductor_dirs: list[Path] = []

    for current, dirnames, _filenames in os.walk(root):
        current_path = Path(current)

        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in SKIP_PARTS
            and (include_archive or dirname != "_archive")
        ]

        for dirname in dirnames:
            if dirname == "conductor":
                conductor_dirs.append(current_path / dirname)

    return sorted(conductor_dirs)


def discover(root: Path, include_archive: bool = False) -> dict[str, Any]:
    active: list[dict[str, Any]] = []
    missing_tracks_md: list[str] = []

    for conductor_dir in iter_conductor_dirs(root, include_archive):
        if not conductor_dir.is_dir() or should_skip(conductor_dir, include_archive):
            continue

        has_tracks_md = (conductor_dir / "tracks.md").exists()
        has_tracks_dir = (conductor_dir / "tracks").exists()
        if not has_tracks_md and not has_tracks_dir:
            continue

        entry = {
            "path": str(conductor_dir),
            "git_root": git_value(conductor_dir, "rev-parse", "--show-toplevel") or None,
            "branch": git_value(conductor_dir, "branch", "--show-current") or None,
            "has_tracks_md": has_tracks_md,
            "has_tracks_dir": has_tracks_dir,
            "track_dirs": track_dir_count(conductor_dir),
        }
        active.append(entry)
        if not has_tracks_md:
            missing_tracks_md.append(str(conductor_dir))

    archive_root = root / "_archive" / "orphaned-conductor-registries"
    archived: list[str] = []
    if archive_root.exists():
        archived = [
            str(child)
            for child in sorted(archive_root.iterdir())
            if child.is_dir()
        ]

    return {
        "root": str(root),
        "active_registry_count": len(active),
        "missing_tracks_md_count": len(missing_tracks_md),
        "archived_entry_count": len(archived),
        "active_registries": active,
        "missing_tracks_md": missing_tracks_md,
        "archived_entries": archived,
    }


def print_markdown(report: dict[str, Any]) -> None:
    print(markdown_report(report), end="")


def markdown_report(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Conductor Registry Audit")
    lines.append("")
    lines.append(f"Root: `{report['root']}`")
    lines.append("")
    lines.append(f"- Active project-level Conductor registries: {report['active_registry_count']}")
    lines.append(f"- Active registries missing `tracks.md`: {report['missing_tracks_md_count']}")
    lines.append(f"- Archived orphan/placeholder entries: {report['archived_entry_count']}")
    lines.append("")
    lines.append("## Active Registries")
    lines.append("")
    lines.append("| Conductor folder | Git root | Branch | Track dirs |")
    lines.append("| --- | --- | --- | ---: |")
    for entry in report["active_registries"]:
        git_root = entry["git_root"] or ""
        branch = entry["branch"] or ""
        lines.append(f"| `{entry['path']}` | `{git_root}` | `{branch}` | {entry['track_dirs']} |")

    if report["missing_tracks_md"]:
        lines.append("")
        lines.append("## Missing tracks.md")
        lines.append("")
        for path in report["missing_tracks_md"]:
            lines.append(f"- `{path}`")

    if report["archived_entries"]:
        lines.append("")
        lines.append("## Archived Entries")
        lines.append("")
        for path in report["archived_entries"]:
            lines.append(f"- `{path}`")

    lines.append("")
    return "\n".join(lines)


def comparable_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "active_registry_count": report["active_registry_count"],
        "missing_tracks_md_count": report["missing_tracks_md_count"],
        "archived_entry_count": report["archived_entry_count"],
        "active_paths": [entry["path"] for entry in report["active_registries"]],
        "registry_details": {
            entry["path"]: {
                "git_root": entry["git_root"],
                "has_tracks_md": entry["has_tracks_md"],
                "has_tracks_dir": entry["has_tracks_dir"],
                "track_dirs": entry["track_dirs"],
            }
            for entry in report["active_registries"]
        },
        "missing_tracks_md": report["missing_tracks_md"],
        "archived_entries": report["archived_entries"],
    }


def compare_reports(current: dict[str, Any], baseline: dict[str, Any]) -> list[str]:
    current_summary = comparable_summary(current)
    baseline_summary = comparable_summary(baseline)
    diffs: list[str] = []

    for key in ("active_registry_count", "missing_tracks_md_count", "archived_entry_count"):
        if current_summary[key] != baseline_summary.get(key):
            diffs.append(f"{key}: current={current_summary[key]} baseline={baseline_summary.get(key)}")

    for key in ("active_paths", "missing_tracks_md", "archived_entries"):
        current_values = set(current_summary[key])
        baseline_values = set(baseline_summary.get(key, []))
        added = sorted(current_values - baseline_values)
        removed = sorted(baseline_values - current_values)
        for value in added:
            diffs.append(f"{key}: added {value}")
        for value in removed:
            diffs.append(f"{key}: removed {value}")

    current_details = current_summary["registry_details"]
    baseline_details = baseline_summary.get("registry_details", {})
    for path in sorted(set(current_details) & set(baseline_details)):
        for key in ("git_root", "has_tracks_md", "has_tracks_dir", "track_dirs"):
            if current_details[path].get(key) != baseline_details[path].get(key):
                diffs.append(
                    f"registry_details[{path}].{key}: "
                    f"current={current_details[path].get(key)} "
                    f"baseline={baseline_details[path].get(key)}"
                )

    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit project-level Conductor registries under a workspace root.",
        epilog=(
            "Exit codes: 0 = success, 1 = active registry missing tracks.md, "
            "2 = baseline drift, 3 = checksum verification failure."
        ),
    )
    parser.add_argument(
        "root",
        nargs="?",
        default="/Volumes/PortableSSD/GitHub",
        help="workspace root to audit",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--write-json",
        metavar="PATH",
        help="write the full JSON report to PATH",
    )
    parser.add_argument(
        "--write-markdown",
        metavar="PATH",
        help="write the Markdown report to PATH",
    )
    parser.add_argument(
        "--compare-json",
        metavar="PATH",
        help="compare the current audit against a saved JSON report",
    )
    parser.add_argument(
        "--write-checksums",
        metavar="PATH",
        help="write SHA-256 checksums for the audit script and generated reports",
    )
    parser.add_argument(
        "--verify-checksums",
        metavar="PATH",
        help="verify a SHA-256 checksum manifest",
    )
    parser.add_argument(
        "--refresh-baseline",
        action="store_true",
        help="write the default JSON, Markdown, and checksum artifacts",
    )
    parser.add_argument(
        "--include-archive",
        action="store_true",
        help="include conductor folders under _archive in active scan",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = discover(root, include_archive=args.include_archive)
    if args.refresh_baseline:
        default_json_path(root).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        default_markdown_path(root).write_text(markdown_report(report))
        default_checksum_path(root).write_text(checksum_manifest(default_artifact_paths(root)))

    if args.write_json:
        output_path = Path(args.write_json)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.write_markdown:
        output_path = Path(args.write_markdown)
        output_path.write_text(markdown_report(report))
    if args.write_checksums:
        output_path = Path(args.write_checksums)
        output_path.write_text(checksum_manifest(default_artifact_paths(root)))

    if args.verify_checksums:
        manifest_path = Path(args.verify_checksums)
        errors = verify_checksum_manifest(manifest_path)
        if errors:
            print("Checksum verification failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 3
        print(f"Checksum verification passed: {manifest_path}")
        return 0

    if args.compare_json:
        baseline_path = Path(args.compare_json)
        baseline = json.loads(baseline_path.read_text())
        diffs = compare_reports(report, baseline)
        if diffs:
            print("Conductor registry audit drift detected:", file=sys.stderr)
            for diff in diffs:
                print(f"- {diff}", file=sys.stderr)
            return 2
        print(f"Conductor registry audit matches baseline: {baseline_path}")
        return 0

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_markdown(report)

    return 1 if report["missing_tracks_md_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
