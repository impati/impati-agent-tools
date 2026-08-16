#!/usr/bin/env python3
"""Validate and reinstall the repository's local Claude Code plugin."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


PLUGIN_NAME = "impati-claude-tools"
MARKETPLACE_NAME = "personal"
PLUGIN_ID = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
PLUGIN_SOURCE = f"./adapters/claude/plugins/{PLUGIN_NAME}"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def run(
    *args: str, check: bool = True, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd or REPO_ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def run_json(*args: str, cwd: Path | None = None) -> object:
    result = run(*args, cwd=cwd)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"명령 출력을 JSON으로 읽지 못했습니다: {' '.join(args)}: {error}"
        ) from error


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


def validate_manifest() -> str:
    manifest = load_json(MANIFEST_PATH)
    version = manifest.get("version")
    if manifest.get("name") != PLUGIN_NAME:
        raise RuntimeError("plugin.json의 name이 플러그인 폴더명과 일치하지 않습니다.")
    if not isinstance(version, str) or SEMVER.fullmatch(version) is None:
        raise RuntimeError(f"유효한 SemVer가 아닙니다: {version!r}")
    return version


def validate_marketplace(version: str) -> None:
    marketplace = load_json(MARKETPLACE_PATH)
    if marketplace.get("name") != MARKETPLACE_NAME:
        raise RuntimeError("marketplace.json의 마켓플레이스 이름이 예상값과 다릅니다.")
    if not isinstance(marketplace.get("owner"), dict) or not marketplace["owner"].get("name"):
        raise RuntimeError("marketplace.json에 owner.name이 없습니다.")
    entry = next(
        (
            item
            for item in marketplace.get("plugins") or []
            if isinstance(item, dict) and item.get("name") == PLUGIN_NAME
        ),
        None,
    )
    if entry is None:
        raise RuntimeError("marketplace.json에 플러그인 항목이 없습니다.")
    if entry.get("source") != PLUGIN_SOURCE:
        raise RuntimeError("marketplace.json의 플러그인 소스가 현재 저장소를 가리키지 않습니다.")
    if "version" in entry and entry["version"] != version:
        raise RuntimeError(
            "marketplace.json의 version이 plugin.json과 다릅니다. "
            "버전은 plugin.json 한 곳에서만 관리합니다."
        )


def validate_adapter_versions(version: str) -> None:
    codex_manifest = load_json(CODEX_MANIFEST_PATH)
    if codex_manifest.get("version") != version:
        raise RuntimeError(
            "어댑터 간 버전이 다릅니다: "
            f"claude {version}, codex {codex_manifest.get('version')!r}. "
            "저장소는 모든 어댑터에 같은 버전을 사용합니다."
        )


def validate_package() -> str:
    synchronized = run("python3", str(SYNC_SCRIPT), "--check")
    print(synchronized.stdout.strip())

    version = validate_manifest()
    validate_marketplace(version)
    validate_adapter_versions(version)

    load_json(HOOKS_PATH)
    if not SESSION_HOOK_PATH.is_file():
        raise RuntimeError(f"세션 훅 스크립트가 없습니다: {SESSION_HOOK_PATH}")

    skill_dirs = sorted(path for path in SKILLS_PATH.iterdir() if path.is_dir())
    if not skill_dirs:
        raise RuntimeError("플러그인에 스킬이 없습니다.")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir)

    validated = run("claude", "plugin", "validate", str(PLUGIN_ROOT))
    print(validated.stdout.strip())
    return version


def ensure_release_tree_is_clean() -> None:
    result = run(
        "git",
        "status",
        "--porcelain",
        "--",
        str(CORE_ROOT.relative_to(REPO_ROOT)),
        str(ADAPTER_ROOT.relative_to(REPO_ROOT)),
        str(MARKETPLACE_PATH.relative_to(REPO_ROOT)),
    )
    if result.stdout.strip():
        raise RuntimeError(
            "플러그인 배포물에 커밋되지 않은 변경이 있습니다. "
            "원격 릴리스 버전과 섞이지 않도록 먼저 변경을 정리하세요."
        )


def ensure_marketplace_registered() -> None:
    marketplaces = run_json("claude", "plugin", "marketplace", "list", "--json")
    if not isinstance(marketplaces, list):
        raise RuntimeError("마켓플레이스 목록을 배열로 읽지 못했습니다.")
    entry = next(
        (
            item
            for item in marketplaces
            if isinstance(item, dict) and item.get("name") == MARKETPLACE_NAME
        ),
        None,
    )
    if entry is not None and str(REPO_ROOT) not in json.dumps(entry):
        raise RuntimeError(
            f"'{MARKETPLACE_NAME}' 마켓플레이스가 다른 소스로 등록되어 있습니다: {entry}. "
            "이름이 겹치면 기존 등록이 대체되므로 먼저 사용자와 확인하세요."
        )
    if entry is None:
        added = run("claude", "plugin", "marketplace", "add", str(REPO_ROOT))
        print(added.stdout.strip())
    else:
        updated = run("claude", "plugin", "marketplace", "update", MARKETPLACE_NAME)
        print(updated.stdout.strip())


def find_installed(project_dir: Path) -> dict | None:
    """설치 상태는 대상 프로젝트 기준으로 달라지므로 그 디렉터리에서 조회한다."""
    plugins = run_json("claude", "plugin", "list", "--json", cwd=project_dir)
    if not isinstance(plugins, list):
        raise RuntimeError("플러그인 목록을 배열로 읽지 못했습니다.")
    return next(
        (
            item
            for item in plugins
            if isinstance(item, dict) and item.get("id") == PLUGIN_ID
        ),
        None,
    )


def install(version: str, scope: str, project_dir: Path) -> None:
    ensure_release_tree_is_clean()
    ensure_marketplace_registered()

    existing = find_installed(project_dir)
    if existing is not None:
        # `claude plugin install`은 이미 설치된 플러그인을 no-op으로 넘기므로
        # 새 버전을 반영하려면 먼저 제거해야 한다.
        removed = run(
            "claude",
            "plugin",
            "uninstall",
            PLUGIN_NAME,
            "--scope",
            existing.get("scope") or scope,
            "--keep-data",
            cwd=project_dir,
        )
        print(removed.stdout.strip())

    added = run(
        "claude",
        "plugin",
        "install",
        PLUGIN_ID,
        "--scope",
        scope,
        cwd=project_dir,
    )
    print(added.stdout.strip())

    installed = find_installed(project_dir)
    if installed is None:
        raise RuntimeError(f"설치 후 플러그인을 목록에서 찾지 못했습니다: {PLUGIN_ID}")
    if not installed.get("enabled"):
        raise RuntimeError(f"플러그인이 활성화되지 않았습니다: {installed}")
    if installed.get("version") != version:
        raise RuntimeError(
            f"설치된 버전이 {version}이 아닙니다: {installed.get('version')!r}"
        )
    if installed.get("scope") != scope:
        raise RuntimeError(
            f"설치 범위가 {scope}가 아닙니다: {installed.get('scope')!r}"
        )
    if scope in ("project", "local"):
        project_path = installed.get("projectPath")
        if project_path is None or Path(project_path).resolve() != project_dir:
            raise RuntimeError(
                f"설치 대상 프로젝트가 {project_dir}가 아닙니다: {project_path!r}"
            )
    print(
        f"확인 완료: {PLUGIN_ID} {installed['version']} "
        f"(scope: {installed.get('scope')}, enabled, 대상: {project_dir})"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="패키지만 검증하고 Claude Code 설치 상태는 변경하지 않습니다.",
    )
    parser.add_argument(
        "--scope",
        choices=("user", "project", "local"),
        default="user",
        help="설치 범위를 지정합니다. 기본값은 user입니다.",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=REPO_ROOT,
        help=(
            "project 또는 local 범위로 설치할 대상 프로젝트 경로입니다. "
            "기본값은 이 저장소 루트입니다."
        ),
    )
    return parser.parse_args()


REPO_ROOT = Path(__file__).resolve().parents[3]
CORE_ROOT = REPO_ROOT / "core"
ADAPTER_ROOT = REPO_ROOT / "adapters" / "claude"
PLUGIN_ROOT = ADAPTER_ROOT / "plugins" / PLUGIN_NAME
MANIFEST_PATH = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
SKILLS_PATH = PLUGIN_ROOT / "skills"
HOOKS_PATH = PLUGIN_ROOT / "hooks" / "hooks.json"
SESSION_HOOK_PATH = PLUGIN_ROOT / "hooks" / "session_start.py"
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
SYNC_SCRIPT = ADAPTER_ROOT / "scripts" / "sync-plugin.py"
CODEX_MANIFEST_PATH = (
    REPO_ROOT / "adapters" / "codex" / "plugins" / "impati-codex-tools"
    / ".codex-plugin" / "plugin.json"
)


def main() -> int:
    try:
        args = parse_args()
        version = validate_package()
        print(f"패키지 검증 완료: {PLUGIN_NAME} {version}")
        if args.check:
            return 0
        project_dir = args.project_dir.expanduser().resolve()
        if not project_dir.is_dir():
            raise RuntimeError(f"대상 프로젝트 경로가 없습니다: {project_dir}")
        install(version, args.scope, project_dir)
        print("새 Claude Code 세션에서 업데이트된 플러그인을 확인하세요.")
        print("설치 요약에 /reload-plugins 안내가 있으면 해당 명령을 실행하세요.")
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
