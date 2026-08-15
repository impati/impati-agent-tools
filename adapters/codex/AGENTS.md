# Codex 어댑터 규칙

`core/AGENTS.md`의 공통 원칙과 함께 다음 규칙을 적용한다.

## 원본과 배포물

- 공통 원칙과 공통 스킬의 원본은 `core/`에 둔다.
- Codex 전용 스킬의 원본은 `adapters/codex/skills/`에 둔다.
- 설치 가능한 플러그인은 `adapters/codex/plugins/impati-codex-tools/`에 둔다.
- 플러그인 안의 `AGENTS.md`와 `skills/`는 생성된 배포물이므로 직접 수정하지 않는다.
- 코어나 Codex 전용 스킬이 바뀌면 `python3 adapters/codex/scripts/sync-plugin.py`로 배포물을 갱신한다.

## 릴리스와 설치

- 사용자가 Codex 플러그인 버전 릴리스 또는 최신 플러그인의 로컬 설치를 요청하면 `release-plugin` 스킬을 사용한다.
- `adapters/codex/plugins/impati-codex-tools/.codex-plugin/plugin.json`의 `version`을 Codex 플러그인 버전의 단일 기준으로 사용한다.
- 플러그인 배포물에 변경이 생기면 SemVer 영향도를 판단하여 같은 변경에서 버전을 갱신한다.
- 호환되지 않는 스킬·규칙 계약 변경은 MAJOR, 하위 호환 기능 추가는 MINOR, 호환 가능한 수정은 PATCH로 올린다.
- 플러그인 밖의 문서나 개발 보조 파일만 변경되었다면 버전을 올리지 않는다.
- 버전 변경은 `CHANGELOG.md` 최상단에 해당 버전의 의도와 핵심 변경을 함께 기록한다.
- tag, push와 GitHub release는 사용자의 명시적 요청 없이 자동 수행하지 않는다.
