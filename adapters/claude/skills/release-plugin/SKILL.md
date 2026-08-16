---
name: release-plugin
description: Manage versioned releases and local updates of the impati-claude-tools plugin for Claude Code. Use when the user asks 플러그인 버전 올려줘, 플러그인 릴리스 준비해줘, 최신 플러그인 업데이트 설치해줘, 로컬 플러그인에 반영해줘, release the plugin, or invokes the skill by name. Apply Semantic Versioning, update CHANGELOG.md, validate the package, safely fast-forward from the configured remote when requested, and reinstall the plugin locally without automatically tagging, pushing, or overwriting local work.
---

# Release Plugin

`impati-claude-tools`의 릴리스 버전과 로컬 설치를 안전하게 관리하라. 요청을 **릴리스 준비** 또는 **로컬 업데이트 설치**로 구분하고 필요한 절차만 실행하라.

## 공통 확인

- 저장소 루트, 현재 브랜치, upstream, `git status`를 확인하라.
- `adapters/claude/AGENTS.md`를 읽고 적용하라.
- 플러그인 매니페스트는 `adapters/claude/plugins/impati-claude-tools/.claude-plugin/plugin.json`을 사용하라.
- 현재 버전과 `CHANGELOG.md` 최신 기록을 읽어라.
- 다른 작업의 변경을 포함하거나 되돌리지 말라.
- tag, push, GitHub release는 사용자가 명시적으로 요청한 경우에만 수행하라.

## 릴리스 준비

플러그인 배포물의 변경을 확인하고 다음 기준으로 SemVer 증가안을 제시하라.

- **MAJOR:** 기존 스킬 제거·이름 변경, 호환되지 않는 호출 방식이나 규칙 계약 변경
- **MINOR:** 새 스킬·훅·워크플로 추가처럼 하위 호환되는 기능 확장
- **PATCH:** 기존 동작의 호환 가능한 수정이나 정확성 개선
- 플러그인 밖의 문서나 개발 보조 파일만 바뀌었다면 버전을 올리지 않는다.

사용자가 버전을 지정하지 않았다면 추천 버전과 이유를 제시하고 승인받아라. 승인 후 다음을 수행하라.

1. 공통 코어나 Claude 전용 스킬이 변경되었다면 `python3 adapters/claude/scripts/sync-plugin.py`를 실행한다.
2. `plugin.json`의 `version`을 확정된 버전으로 변경한다.
3. 저장소는 어댑터 간 버전을 일치시키므로 Codex 플러그인의 `version`도 같은 값으로 맞추고, 필요하면 `python3 adapters/codex/scripts/sync-plugin.py`도 실행한다.
4. `CHANGELOG.md` 최상단에 버전, 날짜, 변경 의도와 핵심 변경을 기록한다.
5. `python3 adapters/claude/scripts/update-local-plugin.py --check`를 실행한다.
6. 다른 어댑터의 배포물도 함께 바뀌었다면 해당 어댑터의 검증 명령도 실행한다.
7. 변경을 하나의 논리적 커밋으로 정리하고 버전과 검증 결과를 보고한다.

릴리스 커밋 메시지는 별도 로컬 규칙이 없으면 `chore: 플러그인 <version> 릴리스` 형식을 사용한다. 사용자의 명시적 요청 없이 tag나 push로 확대하지 말라.

## 로컬 업데이트 설치

사용자가 원격에 반영된 최신 플러그인을 로컬에 설치해 달라고 요청하면 다음 순서로 진행하라.

1. 작업 트리가 깨끗한지 확인한다. 로컬 변경이 있으면 pull이나 설치 전에 중단하고 사용자에게 알린다.
2. 현재 브랜치와 upstream을 확인한다. upstream이 없거나 대상 브랜치가 불명확하면 묻는다.
3. 원격 갱신까지 요청한 맥락이면 `git fetch` 후 ahead/behind 상태를 확인한다.
4. 로컬이 원격보다 뒤에 있고 분기되지 않았다면 `git pull --ff-only`로 갱신한다.
5. 로컬 커밋이 앞서 있거나 브랜치가 분기되었으면 임의로 merge, rebase 또는 reset하지 말고 사용자에게 알린다.
6. 저장소 루트에서 `python3 adapters/claude/scripts/update-local-plugin.py`를 실행한다.
7. 설치된 버전과 활성화 상태를 보고하고 새 Claude Code 세션을 시작하도록 안내한다.

설치 범위를 바꿔야 하면 `--scope user|project|local`을 사용한다. 사용자가 특정 프로젝트에서만 이 플러그인을 쓰고 싶다고 하면 `user` 대신 `project` 또는 `local`을 제안하라.

`project` 또는 `local` 범위는 명령을 실행한 디렉터리가 아니라 `--project-dir`로 지정한 프로젝트에 설치된다. 이 저장소가 아닌 다른 프로젝트가 대상이면 반드시 `--project-dir`를 함께 넘겨라. 생략하면 이 저장소에 설치된다.

```bash
python3 adapters/claude/scripts/update-local-plugin.py --scope local --project-dir <프로젝트 경로>
```

이미 설치된 상태에서는 스크립트가 기존 설치를 먼저 제거한 뒤 다시 설치한다. `claude plugin install`만으로는 버전이 갱신되지 않으므로 이 순서를 건너뛰지 말라. 스크립트는 원격 변경을 자동으로 가져오지 않으므로 Git 갱신과 설치 단계를 혼동하지 말라.

## 다른 플러그인과의 공존

- 이 플러그인의 `SessionStart` 훅은 공통 원칙을 세션에 주입한다. 다른 플러그인도 같은 훅으로 규칙을 주입하면 두 규칙이 함께 적용된다.
- 규칙이 충돌하면 `core/AGENTS.md`의 규칙 우선순위에 따라 더 구체적인 로컬 프로젝트 규칙을 우선하고, 불명확하면 사용자에게 확인한다.
- 사용자가 특정 세션에서 이 플러그인만 끄고 싶다고 하면 `claude plugin disable impati-claude-tools`, 다시 켤 때는 `claude plugin enable impati-claude-tools`를 안내한다. 설치 범위별로 끄려면 `--scope`를 함께 사용한다.

## 완료 보고

- 원격에서 가져온 커밋 범위 또는 변경 없음
- 설치한 플러그인 버전과 설치 범위
- 검증과 `enabled` 확인 결과
- 새 세션 안내
- 남은 로컬 변경이나 충돌 여부
