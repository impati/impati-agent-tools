---
name: engineering-writeup
description: Use when the user asks to document, summarize, or write up an engineering problem-solving process, troubleshooting, implementation decisions, architecture choices, concurrency handling, or lessons learned as a Korean technical article that a reader outside the repository can follow and that preserves the author's experience for long-term memory.
---

# Engineering Writeup

Create an evidence-based Korean technical article that satisfies two purposes at once:

1. a public technical article that a reader who does not know the repository can read and follow
2. a record that helps the author remember the experience long after the work

Do not sacrifice one purpose for the other. The article is not a work diary: do not arrange it in the order the author discovered things, and do not make the reader trace what the author realized and in which order. It is also not an implementation completion report, test plan, PR description, or MR description.

## Establish the Writing Context

Before writing, identify from the request and available evidence:

- the subject the article should illuminate
- the most useful learning to preserve
- the relevant evidence, such as code changes, discussion, logs, experiments, or existing test results

If the user has already made the purpose clear, use that context without asking again. When essential context is absent, state a minimal assumption instead of inventing project details.

## Write for a Defined Reader

The default reader is a backend developer who does not know this repository. If the user names a different audience, that audience wins.

- Open the article with an entry point the reader can walk into: what situation the article is about and why it matters. Do not start from repository-internal circumstances the reader has never seen.
- Explain in detail only what the article is about. Domain concepts that are not the subject get one or two lines of context before moving on.
- Do not coin terms. Use commonly accepted English terminology or plainly written Korean. This applies to the title as well: no unexplained coinages or internal names in headings.
- Connect each project-specific name to the conceptual role it performs, and prefer a progression such as "concept → why it matters here → how this project applied it" over beginning with internal identifiers.

## Arrange by Logic, Not by Time

Use 배경 → 문제 → 해결 과정 → 마무리 as the default flow, and arrange content in logical order rather than the chronological order in which the author worked.

- State premises as fact statements, not as decision narration. "운영 환경은 인스턴스가 여러 개다" gives the reader the premise directly; "~하기로 했다" wraps it in one extra layer the reader must unwrap.
- Convert what the author went through into what the reader needs: not "내가 이렇게 헤맸다" but "이 방식은 이래서 안 맞는다."
- Keep comparisons of meaningful alternatives — they are the grounds of the decision and valuable to the reader. Present a rejected alternative as the reason it does not fit, not as the story of trying it.
- Do not manufacture alternatives merely to fill a section.
- Adjust section headings to the actual subject; the default flow fixes the order of reasoning, not the literal titles.

## Keep Side Topics Out of the Structure

A point that does not contribute to the subject of the article must not become its own section. If it is worth keeping, cover it briefly in the closing part of the article. Otherwise omit it.

## Handle Tests and Verification as Evidence

Mention tests, experiments, observations, or verification results only when they were actually performed and help explain why the conclusion is credible or what was learned.

- Do not create a new test or verification method for the sake of the writeup.
- Do not add a `테스트와 검증` section by default.
- Do not turn the article into a checklist of work that should be performed later.
- Omit routine compile, build, lint, and test success when it only proves that work completed normally.
- Include a verification result only when it changes the reader's understanding of the cause, decision, solution, limitation, or learning.
- If an unverified point materially limits the conclusion, state that boundary plainly.

## Separate Research Evidence from Reader-Facing Content

Treat repository inspection, diffs, logs, build output, and test results as source material. Do not copy each collected fact into the article merely because it was checked.

Before including a detail, ask whether removing it would weaken the explanation or erase an important lesson. Omit it when the answer is no. Keep delivery evidence, command transcripts, changed-file inventories, and routine validation summaries outside the article unless they are themselves part of the subject being explained.

Write the explanation for the reader; do not describe the writing strategy. Explain a concept directly instead of announcing that concepts will be explained first. Do not mention the prompt, skill, requested structure, evidence-gathering process, or assumptions about making the article accessible unless one of them is genuinely part of the engineering subject.

## Keep Publication Work Separate

Do not create branches, commits, PRs, MRs, reviews, or publication workflows as part of this skill. Use a separate skill when the user asks to publish or deliver the writeup through one of those workflows.

## Evidence Rules

When the user refers to repository work, inspect the relevant changed files, git diff, history, or other supplied artifacts as needed. Do not invent implementation details, decisions, outcomes, or verification results.

If the user wants the article saved as a file, create it in the requested location. If no location is requested, return the article in the response.

## Perform a Final Editorial Pass

Before delivering the article, reread it as the defined reader — someone who has never seen this repository — and check:

- the opening gives that reader an entry point instead of starting from repository-internal circumstances
- content follows the logical flow, not the author's working order; no section exists only because the author passed through it
- premises appear as fact statements rather than decision narration
- the title and headings contain no coined terms or unexplained internal names
- side topics have not been promoted to their own sections
- sentences that explain how the article was written, and completion-report details that do not advance the subject, are removed
- the result reads as a standalone technical article without requiring knowledge of the task or authoring process, while still preserving what the author wants to remember

## Style Rules

- Write in Korean.
- Keep the tone practical, explanatory, and engineering-focused.
- Make the reasoning and learning more prominent than a list of changed files.
- Prefer clear paragraphs and short lists where they improve comprehension.
- Avoid marketing language and unexplained technology lists.
- Use concrete project details after establishing the concepts they represent.
- Do not enforce a target length; let the subject determine it.
