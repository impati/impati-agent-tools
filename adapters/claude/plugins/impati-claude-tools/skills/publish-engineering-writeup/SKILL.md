---
name: publish-engineering-writeup
description: Publish verified engineering work as a Korean technical blog post by reusing the engineering-writeup skill, converting the result to the existing impati.github.io Jekyll/Chirpy format, checking for sensitive information, and opening a Draft PR without merging or deploying. Use when the user asks to leave a problem-solving process on the technical blog, turn an engineering writeup into a blog PR, publish implementation lessons to impati.github.io, or create a blog post from development learnings.
---

# Publish Engineering Writeup

Create an evidence-based Korean engineering post and publish only a Draft PR by default.

## Workflow

1. Verify prerequisites before changing anything.
   - Run `gh auth status` without displaying credential values.
   - Confirm `WRITE` or `ADMIN` access to both `impati/impati-agent-tools` and `impati/impati.github.io`.
   - Stop and state the exact missing authentication or repository permission when either check fails.

2. Investigate the source repository without modifying its working tree.
   - Record `git status -sb`, staged and unstaged diffs, relevant commits, changed code, repository rules, and available test evidence.
   - Base every implementation statement on code, diffs, commits, or observed verification output. Do not infer unverified behavior.
   - Prefer existing test output. If tests must run and may create files, reproduce the revision and applicable diff in an isolated temporary checkout, then run tests there.
   - Compare source-repository status before and after investigation. Never clean, reset, stage, or commit the source repository.
   - Ask only for facts that cannot be recovered and materially affect the article.

3. Reuse `$engineering-writeup`.
   - Load and follow the installed sibling `engineering-writeup` skill to create the Korean technical writeup from the collected evidence.
   - Do not recreate or override its section and style rules here.
   - Preserve uncertainty and test gaps explicitly.

4. Prepare the blog in isolation.
   - Read [references/jekyll-publishing.md](references/jekyll-publishing.md) completely before touching the blog checkout.
   - Clone `https://github.com/impati/impati.github.io.git` into a newly created temporary directory or use another clean, isolated checkout.
   - Inspect the latest existing posts, `_config.yml`, and build files directly. Derive front matter, permalink behavior, categories, and Korean tone from the current repository rather than stale assumptions.
   - Convert the writeup to exactly one `_posts/YYYY-MM-DD-slug.md` file. Preserve technical meaning while adapting headings and introduction to the observed blog style.

5. Apply the publication gate.
   - Manually review the article and diff for tokens, passwords, API keys, private keys, personal or customer data, private hosts and internal URLs, sensitive logs, and environment variables.
   - Run `python3 scripts/validate_post.py <post-path>` from this skill directory.
   - Treat every finding as blocking until removed or explicitly replaced with a safe placeholder. Never print a discovered secret value.
   - Confirm the blog diff contains only the intended post.
   - Run `bundle exec jekyll build` when the repository supports it. Report missing dependencies separately from a failing build; never merge a post whose build failed.

6. Publish a Draft PR only.
   - Create a dedicated branch, stage the single post path explicitly, commit it, and push that branch.
   - Immediately before the push, report and verify the repository, remote URL, branch, base branch, and changed file list.
   - Open a Draft PR against `impati/impati.github.io`'s default branch. Do not enable auto-merge, merge the PR, or trigger a deployment.
   - Report the article path, validation results, branch, commit, and Draft PR URL.

## Explicit Publish Approval

Treat “publish”, “merge”, or equivalent approval as a separate destructive boundary. Only after the user explicitly approves the specific Draft PR:

1. Re-run the sensitive-information gate and Jekyll build.
2. Confirm all required PR checks pass.
3. Merge the approved PR without enabling automatic merge.
4. Wait for the corresponding GitHub Actions Pages deployment to complete successfully.
5. Derive the public URL from the current site configuration and post permalink, then verify it returns a successful response.

Stop before merging when validation, checks, or deployment fail. Never use a live publication as a test; use fixtures, a temporary checkout, or dry-run validation.
