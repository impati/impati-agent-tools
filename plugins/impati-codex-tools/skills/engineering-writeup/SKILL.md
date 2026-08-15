---
name: engineering-writeup
description: Use when the user asks to document, summarize, or write up code work, troubleshooting, implementation decisions, architecture choices, concurrency handling, tests, or lessons learned as a Korean technical note with consistent structure.
---

# Engineering Writeup

Use this skill when the user asks for a document, technical note, retrospective, blog-style explanation, or summary of recent engineering work.

The output should explain not only what was implemented, but also why the chosen approach was selected among possible alternatives.

## Default Output Structure

Use this structure unless the user explicitly asks for another format.

### 개요

Briefly explain the topic, context, and final outcome.

Include:
- what area of the system was changed
- what business or technical goal the work served
- the final direction in one or two sentences

### 문제 상황

Explain what problem was encountered and why it mattered.

Include:
- the symptom or requirement
- the root cause or risk
- what could go wrong if it was not handled
- relevant code flow, domain rule, or system constraint

For concurrency, data consistency, transactions, external systems, or test reliability, name the specific failure mode such as race condition, stale read, lost update, timeout, connection scope, or nondeterministic test.

### 해결 방법 후보

Describe the viable ways to solve the problem.

Use one subsection per candidate when there are multiple meaningful options.

For each candidate, explain:
- what the approach is
- how it would solve the problem
- strengths
- weaknesses or operational caveats
- whether it fits the current codebase and why

If there is only one realistic solution, say that briefly and explain why alternatives were not meaningful in this context.

### 선택한 해결 방안

Explain the final decision.

Include:
- the selected approach
- why it was chosen over the alternatives
- which constraints made it a good fit
- what tradeoffs were accepted

Prefer concrete project details over generic theory. Mention class names, method names, interfaces, database functions, libraries, or test tools when known.

### 구현 내용

Explain how the selected approach was implemented.

Include:
- important classes, methods, and boundaries
- where abstraction was introduced and why
- how production and test implementations differ, if applicable
- any important lifecycle, transaction, connection, or resource cleanup details

Use short code snippets only when they clarify the explanation.

### 테스트와 검증

Explain how correctness was verified.

Include:
- what behavior the test proves
- how test data was arranged
- important testing tools or techniques
- expected result
- any remaining test gap or limitation

For concurrency tests, explain how simultaneous execution was coordinated and what invariant was asserted.

### 마무리

Summarize the learning and final value.

Include:
- what became safer, clearer, or more maintainable
- the main technical takeaway
- any follow-up concern worth remembering

## Style Rules

- Write in Korean.
- Keep the tone practical and engineering-focused.
- Prefer clear paragraphs and short bullet lists.
- Do not force every section to be long; adapt depth to the complexity of the work.
- Avoid marketing language.
- Avoid listing technologies without explaining their role in this problem.
- Make the decision process visible: problem, candidate options, selected option, reason.
- If context is missing, state the assumption and write from the available code or conversation.

## Before Writing

When working in a repository and the user refers to recent code work, inspect the relevant changed files or git diff if needed before writing. Do not invent implementation details.

If the user wants the note saved as a file, create it in the requested location. If no location is requested, ask only when saving the file is required; otherwise return the document in the response.
