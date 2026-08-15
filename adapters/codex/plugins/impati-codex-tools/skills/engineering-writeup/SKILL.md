---
name: engineering-writeup
description: Use when the user asks to document, summarize, or write up an engineering problem-solving process, troubleshooting, implementation decisions, architecture choices, concurrency handling, or lessons learned as a Korean technical note that preserves the reasoning and learning from the work.
---

# Engineering Writeup

Create an evidence-based Korean technical note that helps a reader follow how an engineering problem was understood and solved, and what can be learned from that process.

Treat the writeup as a problem-solving narrative, not an implementation completion report, test plan, PR description, or MR description.

## Establish the Writing Context

Before writing, identify from the request and available evidence:

- the problem the note should illuminate
- the intended reader and what they are likely to know already
- the most useful learning to preserve
- the relevant evidence, such as code changes, discussion, logs, experiments, or existing test results

If the user has already made the purpose and audience clear, use that context without asking again. When essential context is absent, state a minimal assumption instead of inventing project details.

## Reconstruct the Problem-Solving Process

Explain the causal and decision-making flow of the work. Include only stages that materially help the reader understand the problem or the learning:

1. Describe the initial situation and why it became a problem.
2. Explain the cause, constraint, or failure mode that shaped the solution.
3. Introduce the concepts needed to understand the reasoning.
4. Compare meaningful alternatives when they actually influenced the decision.
5. Explain the selected approach, accepted tradeoffs, and important implementation boundaries.
6. Connect the outcome back to the original problem.
7. Draw out reusable lessons, changed understanding, and concerns worth remembering.

Do not manufacture alternatives merely to fill a section. Preserve uncertainty, discarded hypotheses, and failed attempts when they contributed to the learning.

## Explain Concepts Before Project Details

For readers who may not know the project:

- define a new technical term briefly when it first becomes necessary
- explain the general mechanism before naming the project's classes, modules, methods, or infrastructure
- connect each project-specific name to the conceptual role it performs
- use code snippets only when they make the reasoning easier to understand

Prefer a progression such as “concept → why it matters here → how this project applied it” over beginning with internal identifiers.

## Choose a Natural Structure

Use headings that reflect the actual story instead of applying a fixed template. A useful note will often cover the following ideas, but not necessarily with these titles or as separate sections:

- background and problem
- cause and constraints
- concepts needed for understanding
- explored approaches and decision
- application to the project
- outcome and learning

Omit irrelevant sections. Adjust the explanation density to the audience and complexity of the problem.

## Handle Tests and Verification as Evidence

Mention tests, experiments, observations, or verification results only when they were actually performed and help explain why the conclusion is credible or what was learned.

- Do not create a new test or verification method for the sake of the writeup.
- Do not add a `테스트와 검증` section by default.
- Do not turn the note into a checklist of work that should be performed later.
- Omit routine compile, build, lint, and test success when it only proves that work completed normally.
- Include a verification result only when it changes the reader's understanding of the cause, decision, solution, limitation, or learning.
- If an unverified point materially limits the conclusion, state that boundary plainly.

## Separate Research Evidence from Reader-Facing Content

Treat repository inspection, diffs, logs, build output, and test results as source material. Do not copy each collected fact into the note merely because it was checked.

Before including a detail, ask whether removing it would weaken the causal explanation or erase an important lesson. Omit it when the answer is no. Keep delivery evidence, command transcripts, changed-file inventories, and routine validation summaries outside the main narrative unless they are themselves part of the problem being explained.

Write the explanation for the reader; do not describe the writing strategy. Explain a concept directly instead of announcing that concepts will be explained first. Do not mention the prompt, skill, requested structure, evidence-gathering process, or assumptions about making the article accessible unless one of them is genuinely part of the engineering problem.

## Keep Publication Work Separate

Do not create branches, commits, PRs, MRs, reviews, or publication workflows as part of this skill. Use a separate skill when the user asks to publish or deliver the writeup through one of those workflows.

## Evidence Rules

When the user refers to repository work, inspect the relevant changed files, git diff, history, or other supplied artifacts as needed. Do not invent implementation details, decisions, outcomes, or verification results.

If the user wants the note saved as a file, create it in the requested location. If no location is requested, return the note in the response.

## Perform a Final Editorial Pass

Before delivering the note:

- remove sentences that explain how the article was written rather than the engineering subject
- remove completion-report details that do not advance the problem, cause, judgment, solution, or learning
- ensure each project-specific identifier is introduced through the concept it represents
- ensure headings follow the actual reasoning rather than a reusable template
- ensure the result reads as a standalone professional technical article without requiring knowledge of the task or authoring process

## Style Rules

- Write in Korean.
- Keep the tone practical, explanatory, and engineering-focused.
- Make the reasoning and learning more prominent than a list of changed files.
- Prefer clear paragraphs and short lists where they improve comprehension.
- Avoid marketing language and unexplained technology lists.
- Use concrete project details after establishing the concepts they represent.
