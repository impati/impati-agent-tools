# Claude Code 어댑터 추가

- **ID:** BL-0002
- **기록일:** 2026-08-16

## 배경

이 저장소는 공통 코어와 에이전트별 어댑터로 구성되어 있지만 실제로 제공하는 어댑터는 Codex뿐이었다. 같은 작업 원칙과 워크플로를 Claude Code 세션에서도 사용하려면 매번 저장소를 열어 `core/AGENTS.md`를 직접 읽히거나 스킬 내용을 복사해야 했고, 다른 프로젝트에서 시작한 Claude 세션에는 공통 원칙이 전혀 적용되지 않았다.

Codex와 Claude Code는 플러그인 설치 규격이 다르다. 매니페스트 경로가 `.codex-plugin/plugin.json`과 `.claude-plugin/plugin.json`으로 다르고, 마켓플레이스 파일 위치도 `.agents/plugins/marketplace.json`과 저장소 루트의 `.claude-plugin/marketplace.json`으로 고정되어 있다. 훅 정의에서 플러그인 경로를 가리키는 변수도 `${PLUGIN_ROOT}`와 `${CLAUDE_PLUGIN_ROOT}`로 다르며, 설치 시 플러그인 디렉터리가 캐시로 복사되므로 번들이 `core/`를 상대 경로로 참조할 수 없다.

또한 스킬 안의 `agents/openai.yaml`은 Codex 인터페이스 전용 메타데이터이고, Codex 전용 `release-plugin` 스킬은 `codex plugin` 명령에 묶여 있어 Claude Code에서 그대로 사용할 수 없다.

## 목표

Codex 어댑터와 대칭되는 Claude Code 어댑터를 추가해, 공통 코어를 단일 원본으로 유지한 채 Claude Code 세션에도 같은 작업 원칙과 스킬을 제공한다. 다른 프로젝트에서 시작한 세션에도 `SessionStart` 훅으로 공통 원칙이 주입되어야 한다.

배포물은 Codex와 동일하게 생성물로 관리하여 사람이 직접 수정하지 않고, 동기화 상태와 패키지 구조를 스크립트로 검증할 수 있어야 한다. Claude Code에서 "최신 플러그인 설치해줘"라고 요청했을 때 Codex와 같은 수준으로 릴리스와 로컬 재설치를 수행할 수 있어야 한다.

공통 코어의 변경이 두 어댑터에 같은 내용으로 반영되도록 저장소 버전을 하나로 유지하고, 어댑터가 늘어나도 코어의 단일 원본 원칙이 유지되어야 한다.
