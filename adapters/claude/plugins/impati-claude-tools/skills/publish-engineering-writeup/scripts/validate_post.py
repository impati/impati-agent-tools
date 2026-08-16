#!/usr/bin/env python3
"""Validate a Jekyll post path, front matter, and obvious publication secrets."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


POST_PATH = re.compile(r"(?:^|/)_posts/(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
FRONT_MATTER_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$")
REQUIRED_FIELDS = ("layout", "title", "date", "categories")
SAFE_PLACEHOLDERS = re.compile(
    r"(?:redacted|masked|example|placeholder|dummy|changeme|<[^>]+>|\$\{[^}]+\})",
    re.IGNORECASE,
)

SENSITIVE_PATTERNS = (
    ("private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub credential", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    (
        "assigned credential or environment secret",
        re.compile(
            r"(?i)\b(?:password|passwd|pwd|api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|secret[_-]?key)\b\s*[:=]\s*[\"']?([^\s\"']+)"
        ),
    ),
    ("private or local URL", re.compile(r"(?i)https?://(?:localhost|127(?:\.\d{1,3}){3}|10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}|[^/\s]+\.(?:internal|local))(?:[:/\s]|$)")),
    ("possible Korean phone number", re.compile(r"(?<!\d)01[016789][ -]?\d{3,4}[ -]?\d{4}(?!\d)")),
)


def parse_front_matter(text: str) -> tuple[dict[str, str], int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("front matter must start on the first line")

    fields: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return fields, index
        match = FRONT_MATTER_LINE.match(line)
        if match:
            fields[match.group(1)] = (match.group(2) or "").strip()
    raise ValueError("front matter closing delimiter is missing")


def validate_post(path: Path) -> list[tuple[int | None, str]]:
    findings: list[tuple[int | None, str]] = []
    match = POST_PATH.search(path.as_posix())
    if not match:
        findings.append((None, "path must match _posts/YYYY-MM-DD-lowercase-slug.md"))
    else:
        try:
            date.fromisoformat(match.group(1))
        except ValueError:
            findings.append((None, "filename contains an invalid calendar date"))

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return findings + [(None, f"cannot read UTF-8 post: {error}")]

    try:
        fields, closing_line = parse_front_matter(text)
    except ValueError as error:
        findings.append((None, str(error)))
        fields = {}
        closing_line = 0

    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            findings.append((None, f"required front matter field is missing or empty: {field}"))

    layout = fields.get("layout", "").strip("\"'")
    if layout and layout != "post":
        findings.append((None, "front matter layout must be post"))

    raw_date = fields.get("date", "").strip("\"'")
    if raw_date:
        try:
            date.fromisoformat(raw_date[:10])
        except ValueError:
            findings.append((None, "front matter date must start with YYYY-MM-DD"))

    if closing_line and not any(line.strip() for line in text.splitlines()[closing_line:]):
        findings.append((None, "post body is empty"))

    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in SENSITIVE_PATTERNS:
            match = pattern.search(line)
            if not match:
                continue
            captured = match.group(1) if match.lastindex else match.group(0)
            if SAFE_PLACEHOLDERS.search(captured):
                continue
            findings.append((line_number, label))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post", type=Path, help="Jekyll Markdown post to validate")
    args = parser.parse_args()

    findings = validate_post(args.post)
    if findings:
        print(f"Validation failed with {len(findings)} finding(s).", file=sys.stderr)
        for line_number, label in findings:
            location = f"line {line_number}" if line_number else "file"
            print(f"- {location}: {label}", file=sys.stderr)
        return 1

    print("Post path, front matter, body, and sensitive-pattern checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
