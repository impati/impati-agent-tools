---
name: capture-backlog
description: Capture a problem, idea, or future work item that should be remembered but not implemented now. Use when the user says 백로그로 남겨줘, 나중에 할 일로 기록해줘, 다음에 해야 할 일로 남겨줘, capture this backlog, or invokes $capture-backlog. Allocate a sequential unique BL-NNNN tracking ID and create one Jira-ticket-like file per item under docs/backlog with only its background and goal, without status tracking or starting implementation.
---

# Capture Backlog

지금 구현하지 않을 문제나 작업 후보를 미래에 다시 이해할 수 있도록 `docs/backlog`에 독립 항목으로 기록하라. 기록 과정에서 구현, 해결책 설계 또는 ADR 작성을 시작하지 말라.

## 1. 필요한 맥락 추출

현재 대화와 사용자가 제공한 자료에서 다음 내용을 추출하라.

- **배경:** 어떤 상황에서 무엇을 문제나 필요로 인지했는가
- **목표:** 나중에 작업했을 때 어떤 결과를 이루고 싶은가

두 내용이 충분하면 다시 묻지 말라. 미래의 작업자가 이해하기 어려운 핵심 정보가 빠졌을 때만 누락된 내용을 짧게 질문하라.

사용자가 요청하지 않은 해결 방법, 구현 범위, 우선순위, 담당자, 기한, 상태 또는 수용 기준을 추가하지 말라.

## 2. 기존 항목 확인

`docs/backlog`의 기존 항목을 읽고 같은 문제나 목표가 이미 기록되어 있는지 확인하라.

- 명백히 같은 항목이면 새 파일을 만들지 말고 기존 항목을 알려라.
- 일부만 겹쳐 병합 여부가 불명확하면 기존 항목을 갱신할지 별도 항목으로 만들지 사용자에게 물어라.
- 관련은 있지만 목표가 독립적이면 새 항목으로 기록하라.

## 3. 파일 생성

각 백로그 항목에 `BL-NNNN` 형식의 추적 ID를 부여하라. 이 ID는 백로그 파일, 작업 브랜치, 커밋과 코드 리뷰를 연결하는 기준이다.

- 현재 `docs/backlog`와 Git에서 확인 가능한 전체 이력의 `BL-NNNN` 번호를 조사하라.
- 지금까지 사용한 가장 큰 번호의 다음 번호를 네 자리로 부여하라. 첫 항목은 `BL-0001`이다.
- 삭제된 항목의 번호도 다시 사용하지 말라.
- 파일을 쓰기 직전에 같은 ID가 생성되지 않았는지 다시 확인하고, 충돌하면 다음 번호를 다시 할당하라.
- 중앙 번호 발급 시스템이 없으므로 서로 다른 clone에서 동시에 만든 ID는 병합 시 충돌할 수 있다. 충돌을 발견하면 임의로 덮어쓰지 말고 사용자와 새 번호를 확정하라.

파일명은 `docs/backlog/bl-NNNN-kebab-case-title.md` 형식을 사용하라. 제목은 문제나 목표를 짧고 구체적으로 나타내라.

다음 형식만 기본으로 사용하라.

```markdown
# 제목

- **ID:** BL-NNNN
- **기록일:** YYYY-MM-DD

## 배경

문제나 필요를 인지한 맥락을 적는다.

## 목표

나중에 작업하여 이루고 싶은 결과를 적는다.
```

내용은 사용자의 표현과 의도를 보존하면서도 미래에 단독으로 읽을 수 있게 작성하라. 해결책을 확정하거나 작업을 시작한 것처럼 쓰지 말라.

## 4. 커밋하고 보고

개별 백로그 항목은 `CHANGELOG.md`나 ADR에 중복 기록하지 말라.

- `git status`와 diff를 확인하고 새 백로그 항목만 스테이징하라.
- 기존 사용자 변경을 포함하지 말라.
- 로컬 커밋 규칙을 우선하고, 규칙이 없으면 `docs(bl-NNNN): <한국어 요약>` 형식을 사용하라.
- 저장소가 Git을 사용하지 않거나 사용자가 커밋하지 말라고 하면 파일만 생성하고 상태를 보고하라.
- 완료 시 백로그 ID, 파일 경로, 한 줄 목표, 커밋 해시와 메시지를 보고하라.
- push, 브랜치 생성, PR 생성은 별도 요청 없이는 수행하지 말라.

나중에 이 항목을 실제 기능 코드 작업으로 시작할 수 있음을 안내하고, 시작하려면 `BL-NNNN 작업 시작` 또는 `$start-work`를 요청하도록 알려라. 사용자의 명시적 요청 없이 `start-work`를 자동 실행하거나 브랜치를 만들지 말라.
