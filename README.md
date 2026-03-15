# ag-bootstrap

Bootstrap project skeletons from local templates.

`ag-bootstrap` is intentionally small:

- Templates live in `./templates/<project-type>`.
- The CLI renders template files in place.
- Skills can call the same CLI instead of duplicating bootstrap logic.

For now, only one project type is supported:

- `typescript`

## Layout

```text
.
├── SKILL.md
├── bin/ag-bootstrap
├── templates/
│   └── typescript/
└── tests/
```

## Usage

List available project types:

```bash
./bin/ag-bootstrap list
```

Bootstrap a TypeScript project:

```bash
./bin/ag-bootstrap bootstrap typescript ~/code/example-ts
```

Skip install and test follow-up:

```bash
./bin/ag-bootstrap bootstrap typescript ~/code/example-ts --skip-followup
```

Override template variables:

```bash
./bin/ag-bootstrap bootstrap typescript ~/code/example-ts \
  --project-name "Example TS" \
  --package-name example-ts \
  --description "Example project" \
  --var author="Kevin Lin"
```

Add a Husky pre-commit hook to an existing project:

```bash
./bin/ag-bootstrap add-precommit ~/code/example-ts
```

## Template Variables

Every template currently receives these variables:

- `project_name`
- `package_name`
- `description`

Extra values can be passed with repeated `--var key=value`.

## Follow-up

`bootstrap` runs these steps by default:

1. `pnpm install`
2. `pnpm test`
3. `git init` when the target is not already a git repo
4. write the standard `.husky/pre-commit` hook
5. `pnpm prepare` after `git init` so Husky hooks activate

Pass `--skip-followup` to only render files.
