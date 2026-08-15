#!/usr/bin/env python3
"""Validate and reinstall the repository's local Codex plugin."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


PLUGIN_NAME = "impati-codex-tools"
MARKETPLACE_NAME = "personal"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"유효한 JSON 파일이 아닙니다: {path}: {error}") from error
    if not isinstance(payload, dict):
        raise RuntimeError(f"JSON 최상위 값이 객체가 아닙니다: {path}")
    return payload


def validate_skill(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise RuntimeError(f"SKILL.md가 없습니다: {skill_dir}")
    content = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if match is None:
        raise RuntimeError(f"YAML frontmatter가 올바르지 않습니다: {skill_file}")
    frontmatter = match.group(1)
    expected_name = skill_dir.name
    if re.search(rf"^name:\s*{re.escape(expected_name)}\s*$", frontmatter, re.MULTILINE) is None:
        raise RuntimeError(f"스킬 이름이 폴더명과 일치하지 않습니다: {skill_file}")
    if re.search(r"^description:\s*\S.+$", frontmatter, re.MULTILINE) is None:
        raise RuntimeError(f"스킬 description이 없습니다: {skill_file}")


def validate_package() -> str:
    manifest = load_json(MANIFEST_PATH)
    version = manifest.get("version")
    if manifest.get("name") != PLUGIN_NAME:
        raise RuntimeError("plugin.json의 name이 플러그인 폴더명과 일치하지 않습니다.")
    if not isinstance(version, str) or SEMVER.fullmatch(version) is None:
        raise RuntimeError(f"유효한 SemVer가 아닙니다: {version!r}")

    marketplace = load_json(MARKETPLACE_PATH)
    if marketplace.get("name") != MARKETPLACE_NAME:
        raise RuntimeError("marketplace.json의 마켓플레이스 이름이 예상값과 다릅니다.")
    entries = marketplace.get("plugins")
    entry = next(
        (
            item
            for item in entries or []
            if isinstance(item, dict) and item.get("name") == PLUGIN_NAME
        ),
        None,
    )
    if entry is None:
        raise RuntimeError("marketplace.json에 플러그인 항목이 없습니다.")
    if entry.get("source") != {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"}:
        raise RuntimeError("marketplace.json의 플러그인 소스가 현재 저장소를 가리키지 않습니다.")

    load_json(HOOKS_PATH)
    if not SESSION_HOOK_PATH.is_file():
        raise RuntimeError(f"세션 훅 스크립트가 없습니다: {SESSION_HOOK_PATH}")

    skill_dirs = sorted(path for path in SKILLS_PATH.iterdir() if path.is_dir())
    if not skill_dirs:
        raise RuntimeError("플러그인에 스킬이 없습니다.")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir)
    return version


def ensure_release_tree_is_clean() -> None:
    result = run(
        "git",
        "status",
        "--porcelain",
        "--",
        str(PLUGIN_ROOT.relative_to(REPO_ROOT)),
        str(MARKETPLACE_PATH.relative_to(REPO_ROOT)),
    )
    if result.stdout.strip():
        raise RuntimeError(
            "플러그인 배포물에 커밋되지 않은 변경이 있습니다. "
            "원격 릴리스 버전과 섞이지 않도록 먼저 변경을 정리하세요."
        )


def ensure_marketplace_registered() -> None:
    result = run("codex", "plugin", "marketplace", "list")
    if str(REPO_ROOT) not in result.stdout:
        added = run("codex", "plugin", "marketplace", "add", str(REPO_ROOT))
        print(added.stdout.strip())


def install(version: str) -> None:
    ensure_release_tree_is_clean()
    ensure_marketplace_registered()
    added = run("codex", "plugin", "add", f"{PLUGIN_NAME}@{MARKETPLACE_NAME}")
    print(added.stdout.strip())

    plugins = run("codex", "plugin", "list")
    expected = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
    matching_lines = [line.strip() for line in plugins.stdout.splitlines() if expected in line]
    if not matching_lines or not any("installed, enabled" in line for line in matching_lines):
        raise RuntimeError("설치 후 플러그인의 enabled 상태를 확인하지 못했습니다.")
    if not any(version in line for line in matching_lines):
        raise RuntimeError(f"설치된 플러그인 버전이 {version}인지 확인하지 못했습니다.")
    print(f"확인 완료: {matching_lines[0]}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="패키지만 검증하고 Codex 설치 상태는 변경하지 않습니다.",
    )
    return parser.parse_args()


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = REPO_ROOT / "plugins" / PLUGIN_NAME
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
SKILLS_PATH = PLUGIN_ROOT / "skills"
HOOKS_PATH = PLUGIN_ROOT / "hooks" / "hooks.json"
SESSION_HOOK_PATH = PLUGIN_ROOT / "hooks" / "session_start.py"
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"


def main() -> int:
    try:
        args = parse_args()
        version = validate_package()
        print(f"패키지 검증 완료: {PLUGIN_NAME} {version}")
        if args.check:
            return 0
        install(version)
        print("새 Codex 세션에서 업데이트된 플러그인을 확인하세요.")
        print("훅 정의가 변경되었다면 /hooks에서 다시 신뢰해야 할 수 있습니다.")
        return 0
    except subprocess.CalledProcessError as error:
        print(f"오류: 명령 실행에 실패했습니다: {' '.join(error.cmd)}", file=sys.stderr)
        if error.stdout:
            print(error.stdout.strip(), file=sys.stderr)
        return 1
    except (RuntimeError, FileNotFoundError) as error:
        print(f"오류: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
