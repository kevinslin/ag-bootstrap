---
name: ag-bootstrap
description: Bootstrap local projects from in-repo templates through one shared CLI. Use when asked to scaffold a new project or add the standard Husky hooks to an existing project.
---

# ag-bootstrap

## Overview

Use this repo's CLI instead of embedding one-off bootstrap logic in the skill.

## Workflow

### 1. Inspect supported project types

- Run `bin/ag-bootstrap list`.

### 2. Bootstrap a new project

- Run `bin/ag-bootstrap bootstrap <project-type> <target-dir>`.
- For now, `<project-type>` must be `typescript`.
- Pass `--skip-followup` to render files without installing dependencies or running tests.
- Use `--project-name`, `--package-name`, `--description`, and repeated `--var key=value` to override template values.

### 3. Post-bootstrap follow-up

- By default, `bin/ag-bootstrap bootstrap ...` writes the standard Husky hooks, runs `pnpm install`, `pnpm test`, and initializes git when needed.
- If follow-up is skipped, from the generated project run `pnpm install` and `pnpm test`.
- If no `.git` directory exists yet, run `git init` then `pnpm prepare`.

### 4. Add Husky hooks to an existing project

- Ensure `package.json` exists and defines `lint` and `format` scripts.
- Run `bin/ag-bootstrap add-precommit [project_root]`.
- If `.husky/_/husky.sh` is missing, run your package manager install or `npx husky install`.
