# impati-codex-tools

개인 작업 원칙과 반복 가능한 Codex 스킬을 한곳에서 관리하는 저장소입니다.

## 동작 방식

이 저장소를 작업 루트로 새 Codex 세션을 시작하면 다음 항목이 자동으로 발견됩니다.

- `AGENTS.md`: 모든 작업에 적용할 사용자 의도·범위 확인 원칙
- `.agents/skills/`: 필요할 때 호출하거나 자동 선택할 수 있는 저장소 스킬

현재 포함된 스킬은 다음과 같습니다.

- `start-work`: 기능 코드 작업 전 의도와 주요 결정을 인터뷰하고 검증·리뷰 단위 커밋까지 관리
- `capture-backlog`: 지금 구현하지 않을 문제의 배경과 목표를 `docs/backlog`에 독립 항목으로 기록
- `engineering-writeup`: 엔지니어링 작업을 한국어 기술 문서로 정리

## 사용 방법

1. 이 저장소를 로컬에 clone 합니다.
2. Codex에서 clone한 저장소를 프로젝트 또는 작업 디렉터리로 엽니다.
3. 새 작업을 이 저장소를 기준으로 시작합니다.
4. 기능 코드 작업 전 인터뷰는 `$start-work`, 미래 작업 기록은 `$capture-backlog`, 기술 문서 작성은 `$engineering-writeup`을 명시적으로 호출하거나 자연어로 요청합니다.

`AGENTS.md`와 저장소 스킬의 자동 발견 범위는 이 저장소 안에서 시작한 세션입니다. 다른 저장소를 직접 작업 루트로 연 세션까지 이 규칙을 자동 적용하려면 추후 전역 설치 또는 플러그인 배포 단계가 별도로 필요합니다.

## 구조

```text
.
├── AGENTS.md
├── CHANGELOG.md
├── README.md
├── docs/
│   └── backlog/
│       ├── README.md
│       └── NNNN-*.md
└── .agents/
    └── skills/
        ├── capture-backlog/
        │   ├── SKILL.md
        │   └── agents/
        │       └── openai.yaml
        ├── start-work/
        │   ├── SKILL.md
        │   ├── agents/
        │   │   └── openai.yaml
        │   └── references/
        │       └── adr-convention.md
        └── engineering-writeup/
            ├── SKILL.md
            └── agents/
                └── openai.yaml
```
