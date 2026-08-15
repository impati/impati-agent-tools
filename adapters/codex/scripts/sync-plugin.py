#!/usr/bin/env python3
"""Synchronize shared core files into the installable Codex plugin bundle."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path


PLUGIN_NAME = "impati-codex-tools"


def collect_files(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def build_expected(destination: Path) -> None:
    shutil.copy2(CORE_AGENTS, destination / "AGENTS.md")
    skills_destination = destination / "skills"
    skills_destination.mkdir()

    skill_names: set[str] = set()
    for source_root in (CORE_SKILLS, ADAPTER_SKILLS):
        for skill_dir in sorted(path for path in source_root.iterdir() if path.is_dir()):
            if skill_dir.name in skill_names:
                raise RuntimeError(f"중복된 스킬 이름입니다: {skill_dir.name}")
            skill_names.add(skill_dir.name)
            shutil.copytree(skill_dir, skills_destination / skill_dir.name)


def synchronize(check_only: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="impati-codex-plugin-") as temp_dir:
        expected_root = Path(temp_dir)
        build_expected(expected_root)
        expected = collect_files(expected_root)
        actual = {
            Path("AGENTS.md"): PLUGIN_AGENTS.read_bytes()
        } if PLUGIN_AGENTS.is_file() else {}
        if PLUGIN_SKILLS.is_dir():
            actual.update(
                {
                    Path("skills") / relative: content
                    for relative, content in collect_files(PLUGIN_SKILLS).items()
                }
            )

        if actual == expected:
            print("Codex 플러그인 배포물이 core 및 adapter 원본과 일치합니다.")
            return
        if check_only:
            missing = sorted(str(path) for path in expected.keys() - actual.keys())
            extra = sorted(str(path) for path in actual.keys() - expected.keys())
            changed = sorted(
                str(path)
                for path in expected.keys() & actual.keys()
                if expected[path] != actual[path]
            )
            details = ", ".join(
                part
                for part in (
                    f"누락: {missing}" if missing else "",
                    f"불필요: {extra}" if extra else "",
                    f"변경: {changed}" if changed else "",
                )
                if part
            )
            raise RuntimeError(f"Codex 플러그인 배포물이 원본과 다릅니다. {details}")

        if PLUGIN_AGENTS.exists():
            PLUGIN_AGENTS.unlink()
        if PLUGIN_SKILLS.exists():
            shutil.rmtree(PLUGIN_SKILLS)
        shutil.copy2(expected_root / "AGENTS.md", PLUGIN_AGENTS)
        shutil.copytree(expected_root / "skills", PLUGIN_SKILLS)
        print("Codex 플러그인 배포물을 core 및 adapter 원본과 동기화했습니다.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="파일을 변경하지 않고 배포물 동기화 상태만 확인합니다.",
    )
    return parser.parse_args()


REPO_ROOT = Path(__file__).resolve().parents[3]
CORE_AGENTS = REPO_ROOT / "core" / "AGENTS.md"
CORE_SKILLS = REPO_ROOT / "core" / "skills"
ADAPTER_SKILLS = REPO_ROOT / "adapters" / "codex" / "skills"
PLUGIN_ROOT = REPO_ROOT / "adapters" / "codex" / "plugins" / PLUGIN_NAME
PLUGIN_AGENTS = PLUGIN_ROOT / "AGENTS.md"
PLUGIN_SKILLS = PLUGIN_ROOT / "skills"


def main() -> int:
    try:
        synchronize(parse_args().check)
        return 0
    except (OSError, RuntimeError) as error:
        print(f"오류: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
