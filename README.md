# impati-agent-tools

개인 작업 원칙과 반복 가능한 에이전트 워크플로를 공통 코어로 관리하고, 에이전트별 어댑터로 배포하는 저장소입니다.

현재 제공하는 어댑터는 Codex뿐입니다. Claude 등 다른 에이전트는 실제 필요가 생기고 사용자가 요청한 시점에 별도 어댑터로 추가합니다.

## 구성

### 공통 코어

`core/`는 특정 에이전트에 종속되지 않는 단일 원본입니다.

- `AGENTS.md`: 사용자 의도, 요청 범위와 로컬 프로젝트 규칙을 우선하는 공통 원칙
- `start-work`: `BL-NNNN` 백로그를 기반으로 인터뷰, feature 브랜치와 리뷰 단위 커밋 관리
- `capture-backlog`: 순차 ID로 문제의 배경과 목표 기록
- `rca-code-review`: 명시적 요청 시 백로그 브랜치를 RCA 다관점으로 리뷰
- `engineering-writeup`: 엔지니어링 작업을 한국어 기술 문서로 정리
- `publish-engineering-writeup`: 검증된 기술 문서를 블로그 게시물로 변환해 안전한 Draft PR 생성

`.agents/skills/`는 에이전트가 이 저장소의 스킬을 발견하기 위한 심볼릭 링크 모음입니다. 공통 스킬의 실제 원본은 `core/skills/`, Codex 전용 스킬의 원본은 `adapters/codex/skills/`에 있으므로 `.agents/skills/`의 링크를 직접 수정하지 않습니다.

### Codex 어댑터

`adapters/codex/`는 공통 코어를 Codex에서 사용할 수 있게 만드는 전용 구현입니다.

- `impati-codex-tools` 플러그인
- `SessionStart` 훅을 통한 공통 원칙 주입
- Codex 전용 `release-plugin` 스킬
- 플러그인 동기화, 검증과 로컬 재설치 스크립트

플러그인의 `AGENTS.md`와 공통 스킬 사본은 생성된 배포물입니다. 원본을 변경한 뒤 다음 명령으로 다시 생성합니다.

```bash
python3 adapters/codex/scripts/sync-plugin.py
```

## Codex 로컬 설치

```bash
git clone https://github.com/impati/impati-agent-tools.git
cd impati-agent-tools
codex plugin marketplace add .
codex plugin add impati-codex-tools@personal
```

Codex에서 `/hooks`를 열어 플러그인의 `SessionStart` 훅을 검토하고 신뢰한 뒤 새 세션을 시작합니다.

## Codex 로컬 업데이트

원격 저장소에 새 버전이 반영된 뒤 다음 명령으로 갱신하고 재설치합니다.

```bash
git pull --ff-only
python3 adapters/codex/scripts/update-local-plugin.py
```

업데이트 스크립트는 다음을 수행합니다.

- 공통 코어와 Codex 플러그인 배포물의 동기화 상태 확인
- 플러그인 버전, 매니페스트, 마켓플레이스, 훅과 스킬 구조 검증
- 필요한 경우 현재 clone을 로컬 마켓플레이스로 등록
- `impati-codex-tools@personal` 재설치
- 설치 버전과 `installed, enabled` 상태 확인

스크립트는 `git pull`을 대신 실행하지 않으며 공통 코어나 Codex 어댑터에 커밋되지 않은 변경이 있으면 설치를 중단합니다. Codex에 “최신 플러그인 업데이트 설치해줘”라고 요청하면 `$release-plugin`이 원격과 로컬 상태를 확인한 뒤 이 흐름을 수행합니다.

설치 후에는 새 Codex 세션을 시작합니다. 훅 정의가 변경된 버전은 `/hooks`에서 신뢰를 다시 요청할 수 있습니다.

## Codex 플러그인 버전

버전의 단일 기준은 `adapters/codex/plugins/impati-codex-tools/.codex-plugin/plugin.json`이며 SemVer를 사용합니다.

- **MAJOR:** 기존 스킬 제거·이름 변경 또는 호환되지 않는 규칙 계약 변경
- **MINOR:** 새로운 스킬·훅·워크플로 추가
- **PATCH:** 기존 동작의 호환 가능한 수정

플러그인 배포물이 변경될 때만 버전을 올리고 같은 버전의 변경 의도를 `CHANGELOG.md`에 기록합니다. tag와 push는 별도 요청이 있을 때만 수행합니다.

## 원격 마켓플레이스 사용

로컬 clone 없이 GitHub 저장소를 마켓플레이스로 등록할 수도 있습니다.

```bash
codex plugin marketplace add impati/impati-agent-tools
codex plugin add impati-codex-tools@personal
```

원격 변경을 반영할 때는 다음 명령을 사용합니다.

```bash
codex plugin marketplace upgrade personal
codex plugin add impati-codex-tools@personal
```

## 적용 범위와 우선순위

- 공통 하네스와 대상 프로젝트의 로컬 규칙이 충돌하면 더 구체적인 로컬 프로젝트 규칙을 우선합니다.
- 스킬은 각 어댑터가 제공하는 탐색·호출 방식에 따라 실행됩니다.
- Codex에서는 플러그인이 활성화되고 훅이 신뢰된 세션에 공통 원칙이 주입됩니다.
- 플러그인 훅은 가드레일이며 시스템·개발자·안전 정책보다 높은 강제 경계는 아닙니다.

## 구조

```text
.
├── AGENTS.md -> core/AGENTS.md
├── CHANGELOG.md
├── README.md
├── core/
│   ├── AGENTS.md
│   └── skills/
│       ├── capture-backlog/
│       ├── engineering-writeup/
│       ├── publish-engineering-writeup/
│       ├── rca-code-review/
│       └── start-work/
├── adapters/
│   └── codex/
│       ├── AGENTS.md
│       ├── skills/
│       │   └── release-plugin/
│       ├── scripts/
│       │   ├── sync-plugin.py
│       │   └── update-local-plugin.py
│       └── plugins/
│           └── impati-codex-tools/
│               ├── .codex-plugin/plugin.json
│               ├── hooks/
│               └── skills/  # 생성된 배포물
└── .agents/
    ├── plugins/marketplace.json
    └── skills/  # 원본 스킬을 가리키는 탐색용 심볼릭 링크
```
