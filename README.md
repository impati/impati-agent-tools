# impati-codex-tools

개인 작업 원칙과 반복 가능한 Codex 스킬을 한곳에서 관리하고 플러그인으로 배포하는 저장소입니다.

## 동작 방식

플러그인을 설치하고 활성화하면 다음 항목이 모든 Codex 세션에서 발견됩니다.

- `SessionStart` 훅: `AGENTS.md`의 공통 작업 원칙을 세션 컨텍스트에 주입
- `skills/`: 필요할 때 호출하거나 자동 선택할 수 있는 반복 작업 스킬

현재 포함된 스킬은 다음과 같습니다.

- `start-work`: 필수 `BL-NNNN` 백로그를 기반으로 인터뷰, feature 브랜치, 검증·리뷰 단위 커밋까지 관리
- `capture-backlog`: 순차 증가하는 고유 `BL-NNNN` ID로 문제의 배경과 목표를 독립 항목에 기록
- `rca-code-review`: 명시적 요청 시 백로그 브랜치를 RCA 다관점으로 리뷰하고 채팅에 보고
- `engineering-writeup`: 엔지니어링 작업을 한국어 기술 문서로 정리
- `release-plugin`: 플러그인 SemVer 릴리스와 원격 변경의 안전한 로컬 재설치를 관리

이 저장소 자체에서 작업할 때도 같은 원본을 사용하도록 루트 `AGENTS.md`와 `.agents/skills/`를 플러그인 내부 파일에 연결해 두었습니다.

## 로컬 설치

1. 이 저장소를 로컬에 clone 합니다.
2. 저장소 루트에서 로컬 마켓플레이스를 Codex에 등록합니다.

   ```bash
   codex plugin marketplace add .
   ```

3. 플러그인을 설치합니다.

   ```bash
   codex plugin add impati-codex-tools@personal
   ```

4. Codex에서 `/hooks`를 열어 플러그인의 `SessionStart` 훅을 검토하고 신뢰합니다.
5. 새 세션을 열어 플러그인 규칙과 스킬을 사용합니다.

기능 코드 작업 전 인터뷰는 `$start-work`, 미래 작업 기록은 `$capture-backlog`, 코드 리뷰는 `$rca-code-review`, 기술 문서 작성은 `$engineering-writeup`을 호출합니다.

## 로컬 업데이트

원격 저장소에 새 버전이 반영된 뒤 로컬 clone에서 다음 명령으로 갱신하고 재설치합니다.

```bash
git pull --ff-only
python3 scripts/update-local-plugin.py
```

업데이트 스크립트는 다음 작업만 수행합니다.

- 플러그인 버전, 매니페스트, 마켓플레이스, 훅과 스킬 구조 검증
- 필요한 경우 현재 clone을 로컬 마켓플레이스로 등록
- `impati-codex-tools@personal` 재설치
- 설치 버전과 `installed, enabled` 상태 확인

스크립트는 `git pull`을 대신 실행하지 않으며 플러그인 배포물에 커밋되지 않은 변경이 있으면 설치를 중단합니다. Codex에 “최신 플러그인 업데이트 설치해줘”라고 요청하면 `$release-plugin` 절차가 원격과 로컬 상태를 확인한 뒤 이 흐름을 수행합니다.

설치 후에는 새 Codex 세션을 시작합니다. 훅 정의가 변경된 버전은 `/hooks`에서 신뢰를 다시 요청할 수 있습니다.

## 버전 정책

플러그인 버전의 단일 기준은 `plugins/impati-codex-tools/.codex-plugin/plugin.json`이며 SemVer를 사용합니다.

- **MAJOR:** 기존 스킬 제거·이름 변경 또는 호환되지 않는 규칙 계약 변경
- **MINOR:** 새로운 스킬·훅·워크플로 추가
- **PATCH:** 기존 동작의 호환 가능한 수정

플러그인 배포물이 변경될 때만 버전을 올리고 같은 버전의 변경 의도를 `CHANGELOG.md`에 기록합니다. 릴리스 준비는 `$release-plugin`으로 요청할 수 있으며 tag와 push는 별도 요청이 있을 때만 수행합니다.

## 원격 마켓플레이스로 배포

저장소를 GitHub 등에 올린 뒤 다른 환경에서는 로컬 경로 대신 원격 저장소를 마켓플레이스로 등록할 수 있습니다.

```bash
codex plugin marketplace add <owner>/<repository>
codex plugin add impati-codex-tools@personal
```

원격 변경을 받은 뒤에는 다음 명령으로 마켓플레이스 스냅샷을 갱신합니다.

```bash
codex plugin marketplace upgrade personal
```

플러그인을 설치하거나 갱신한 뒤에는 새 세션에서 동작을 확인합니다.

## 적용 범위와 우선순위

- 플러그인이 활성화되고 훅이 신뢰된 세션에서 공통 원칙이 주입됩니다.
- 사용자가 플러그인이나 훅을 비활성화하거나 관리 정책이 플러그인 훅을 막으면 주입되지 않습니다.
- 공통 하네스와 대상 프로젝트의 로컬 규칙이 충돌하면 더 구체적인 로컬 프로젝트 규칙을 우선합니다.
- 스킬은 설치 후 사용할 수 있지만, 각 스킬의 설명과 명시적 호출 조건에 따라 선택적으로 실행됩니다.

플러그인 훅은 작업 원칙을 안정적으로 주입하는 가드레일이며, Codex 자체의 시스템·개발자·안전 정책보다 높은 강제 경계는 아닙니다.

## 구조

```text
.
├── AGENTS.md -> plugins/impati-codex-tools/AGENTS.md
├── CHANGELOG.md
├── README.md
├── scripts/
│   └── update-local-plugin.py
├── .agents/
│   ├── plugins/marketplace.json
│   └── skills/ -> 플러그인 스킬 호환 링크
└── plugins/
    └── impati-codex-tools/
        ├── .codex-plugin/plugin.json
        ├── AGENTS.md
        ├── hooks/
        │   ├── hooks.json
        │   └── session_start.py
        └── skills/
            ├── capture-backlog/
            ├── engineering-writeup/
            ├── release-plugin/
            ├── rca-code-review/
            └── start-work/
```
