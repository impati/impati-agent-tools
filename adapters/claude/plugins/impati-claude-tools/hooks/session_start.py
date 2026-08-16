#!/usr/bin/env python3
"""플러그인에 포함된 공통 작업 원칙을 세션 컨텍스트로 출력한다."""

from pathlib import Path


def main() -> None:
    plugin_root = Path(__file__).resolve().parent.parent
    instructions = (plugin_root / "AGENTS.md").read_text(encoding="utf-8")
    print(
        "다음은 Impati Agent Tools의 Claude 어댑터가 제공하는 공통 기본 규칙이다. "
        "현재 작업 대상 프로젝트의 더 구체적인 로컬 규칙과 충돌하면 로컬 규칙을 우선한다.\n\n"
        f"{instructions}"
    )


if __name__ == "__main__":
    main()
