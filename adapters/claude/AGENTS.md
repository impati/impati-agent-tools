# Claude 어댑터 규칙

`core/AGENTS.md`의 공통 원칙과 함께 다음 규칙을 적용한다.

## 원본과 배포물

- 공통 원칙과 공통 스킬의 원본은 `core/`에 둔다.
- Claude 전용 스킬의 원본은 `adapters/claude/skills/`에 둔다.
- 설치 가능한 플러그인은 `adapters/claude/plugins/impati-claude-tools/`에 둔다.
- 플러그인 안의 `AGENTS.md`와 `skills/`는 생성된 배포물이므로 직접 수정하지 않는다.
- 코어나 Claude 전용 스킬이 바뀌면 `python3 adapters/claude/scripts/sync-plugin.py`로 배포물을 갱신한다.
- 스킬의 `agents/` 디렉터리는 Codex 인터페이스 전용 메타데이터이므로 Claude 배포물에서 제외한다.

## Claude Code 규격

- 플러그인 매니페스트는 `adapters/claude/plugins/impati-claude-tools/.claude-plugin/plugin.json`을 사용한다.
- 마켓플레이스 파일은 Claude Code가 저장소 루트의 `.claude-plugin/marketplace.json`에서만 읽으므로 위치를 옮기지 않는다.
- 훅에서 플러그인 경로는 `${CLAUDE_PLUGIN_ROOT}`로 참조한다.
- 설치 시 플러그인 디렉터리만 캐시로 복사되므로 번들에서 `../` 상위 경로를 참조하지 않는다.
- 플러그인 버전은 `plugin.json`에만 기록하고 마켓플레이스 항목에는 중복해서 넣지 않는다.

## 릴리스와 설치

- 사용자가 Claude 플러그인 버전 릴리스 또는 최신 플러그인의 로컬 설치를 요청하면 `release-plugin` 스킬을 사용한다.
- 저장소는 모든 어댑터에 같은 버전을 사용한다. Claude 배포물이 바뀌면 Codex 플러그인의 `version`도 같은 값으로 맞춘다.
- 호환되지 않는 스킬·규칙 계약 변경은 MAJOR, 하위 호환 기능 추가는 MINOR, 호환 가능한 수정은 PATCH로 올린다.
- 플러그인 밖의 문서나 개발 보조 파일만 변경되었다면 버전을 올리지 않는다.
- 버전 변경은 `CHANGELOG.md` 최상단에 해당 버전의 의도와 핵심 변경을 함께 기록한다.
- tag, push와 GitHub release는 사용자의 명시적 요청 없이 자동 수행하지 않는다.
