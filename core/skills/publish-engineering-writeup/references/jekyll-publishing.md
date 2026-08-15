# Jekyll/Chirpy publishing procedure

Use this procedure only inside a newly created temporary directory or another clean checkout dedicated to `impati/impati.github.io`.

## Inspect the current contract

1. Confirm identity and access without exposing a token:

   ```bash
   gh auth status
   gh repo view impati/impati.github.io --json nameWithOwner,viewerPermission,defaultBranchRef
   ```

2. Create an isolated checkout and verify its remote and status:

   ```bash
   blog_dir="$(mktemp -d)"
   git clone https://github.com/impati/impati.github.io.git "$blog_dir"
   git -C "$blog_dir" remote -v
   git -C "$blog_dir" status -sb
   ```

3. Read any repository `AGENTS.md`. Inspect `_config.yml`, `Gemfile`, relevant workflow files, and at least the three newest files in `_posts`. Use both filenames and Git history to avoid mistaking a future-dated or renamed file for the latest style.

4. Derive, rather than assume:
   - required front matter keys and value shapes
   - site timezone and date representation
   - category spelling and casing
   - heading progression, Korean voice, code-fence conventions, and image-path usage
   - permalink behavior from explicit configuration or the active Chirpy/Jekyll defaults

If recent posts disagree, follow the newest consistent convention and mention the ambiguity in the Draft PR.

## Create and validate the post

- Use `_posts/YYYY-MM-DD-slug.md` with a lowercase ASCII slug containing only letters, digits, and single hyphens.
- Create `title`, `date`, `categories`, and every other field required by the inspected posts and configuration. Do not copy placeholder categories or image paths blindly.
- Keep the evidence-backed content produced with `$engineering-writeup`; adapt presentation without inventing implementation details.
- Replace repository names, URLs, identifiers, log fragments, and environment values that are not necessary for the public explanation with neutral examples.
- Review personal and customer data manually because pattern matching cannot establish consent or business sensitivity.
- Run the bundled validator from the active skill directory:

  ```bash
  python3 scripts/validate_post.py "$blog_dir/_posts/YYYY-MM-DD-slug.md"
  ```

- Build without publishing:

  ```bash
  bundle exec jekyll build
  ```

Run the build from the blog checkout. A missing local Ruby dependency may be reported as a limitation for a Draft PR, but a build that actually runs and fails blocks merging.

## Limit the Git change

Use a dedicated branch such as `writeup/YYYY-MM-DD-slug`. Before staging, pushing, and opening the Draft PR, require all of the following:

```bash
git status --short
git diff --check
git diff --name-only
git remote get-url origin
git branch --show-current
```

The change list must contain exactly the intended `_posts/YYYY-MM-DD-slug.md`. Stage that explicit path; never use `git add -A` in a mixed tree. Recheck the committed diff against the remote default branch before pushing.

Open a Draft PR and include the evidence source, redactions performed, validation command, Jekyll build result, and remaining gaps. Draft PR creation is not publication approval.

## Merge and deployment gate

Do not proceed merely because a user originally asked for a blog post. Require a later, explicit approval to merge the identified Draft PR. Then:

1. Fetch the current PR state and required checks.
2. Re-run content validation and the Jekyll build on the exact head commit.
3. Merge only when both local validation and required checks pass.
4. Identify the Pages workflow run associated with the merge commit and wait for successful completion.
5. Derive the final URL from the repository's current permalink behavior and confirm a successful HTTP response.

Never enable auto-merge. Never force-push the default branch. Never test by merging a fixture or temporary post.
