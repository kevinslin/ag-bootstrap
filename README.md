# ag-bootstrap

Bootstrap project skeletons from local templates.

`ag-bootstrap` keeps the bootstrap logic small and reusable:

- Templates live in `./templates/<project-type>`.
- The CLI renders template files into a destination directory.
- Skills can call the same CLI instead of re-implementing scaffold logic.

For now, one project type is supported:

- `typescript`: a pnpm monorepo with Lerna, Nx, Jest, ESLint, Prettier, Husky, GitHub Actions, and AGD starter docs.

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

Bootstrap the TypeScript monorepo template:

```bash
./bin/ag-bootstrap bootstrap typescript ~/code/example-monorepo
```

Skip install and test follow-up:

```bash
./bin/ag-bootstrap bootstrap typescript ~/code/example-monorepo --skip-followup
```

Override template variables:

```bash
./bin/ag-bootstrap bootstrap typescript ~/code/example-monorepo \
  --project-name "Example Monorepo" \
  --package-name example-monorepo \
  --description "Example pnpm monorepo" \
  --var author="Kevin Lin"
```

Install the standard Husky hooks in an existing project:

```bash
./bin/ag-bootstrap add-precommit ~/code/example-monorepo
```

## Template Variables

Every template currently receives these variables:

- `project_name`
- `package_name`
- `package_scope`
- `description`

Extra values can be passed with repeated `--var key=value`.

## Follow-up

`bootstrap` runs these steps by default:

1. `pnpm install`
2. `pnpm test`
3. `git init` when the target is not already a git repo
4. write the standard `.husky/pre-commit` and `.husky/pre-push` hooks
5. `pnpm prepare` after `git init` so Husky hooks activate

Pass `--skip-followup` to only render files.
