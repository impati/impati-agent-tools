#!/usr/bin/env python3
"""Regression tests for validate_post.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_post import validate_post


VALID_POST = """---
layout: post
date: 2026-08-15
categories: [CODEX, WORKFLOW]
title: "안전한 게시물"
---

## 들어가며

검증된 내용이다.

```bash
API_KEY=<redacted>
```
"""

UNSAFE_POST = """---
layout: page
date: invalid
title: "위험한 게시물"
---

token = ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890
endpoint = http://service.internal/private
"""


class ValidatePostTest(unittest.TestCase):
    def write_post(self, root: Path, name: str, content: str) -> Path:
        posts = root / "_posts"
        posts.mkdir()
        post = posts / name
        post.write_text(content, encoding="utf-8")
        return post

    def test_valid_post_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            post = self.write_post(
                Path(directory), "2026-08-15-safe-writeup.md", VALID_POST
            )

            self.assertEqual([], validate_post(post))

    def test_unsafe_post_is_blocked_without_echoing_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            post = self.write_post(
                Path(directory), "2026-99-42-Bad_Slug.md", UNSAFE_POST
            )
            labels = {label for _, label in validate_post(post)}

            self.assertIn("path must match _posts/YYYY-MM-DD-lowercase-slug.md", labels)
            self.assertIn("required front matter field is missing or empty: categories", labels)
            self.assertIn("front matter layout must be post", labels)
            self.assertIn("front matter date must start with YYYY-MM-DD", labels)
            self.assertIn("GitHub credential", labels)
            self.assertIn("private or local URL", labels)

            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("validate_post.py")), str(post)],
                capture_output=True,
                check=False,
                text=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertNotIn("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", result.stderr)
            self.assertNotIn("service.internal", result.stderr)


if __name__ == "__main__":
    unittest.main()
