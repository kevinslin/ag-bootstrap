# TypeScript Monorepo Bootstrap Demo

*2026-03-17T03:14:40Z by Showboat 0.6.1*
<!-- showboat-id: 7da55c8e-e326-4827-90cb-7cc60ebe1956 -->

This demo bootstraps a fresh pnpm/Nx/Lerna/Jest monorepo from the local ag-bootstrap template, verifies lint/build/test, and runs the generated client entrypoint.

```bash
python3 -c "from pathlib import Path; import shutil; shutil.rmtree(Path('/tmp/monorepo-test-showboat'), ignore_errors=True); print('clean:ok')"
```

```output
clean:ok
```

```bash
./bin/ag-bootstrap bootstrap typescript /tmp/monorepo-test-showboat --project-name 'Monorepo Showboat' --package-name monorepo-showboat --description 'Showboat demo monorepo' --skip-followup
```

```output
Note: husky is not installed. Run "pnpm install" or "npx husky install" to enable hooks.
```

```bash
find /tmp/monorepo-test-showboat/packages -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
```

```output
client
common
db
integration
scripts
server
```

```bash
cd /tmp/monorepo-test-showboat && pnpm install >/tmp/monorepo-test-showboat.install.log && echo install:ok
```

```output
install:ok
```

```bash
cd /tmp/monorepo-test-showboat && pnpm build >/tmp/monorepo-test-showboat.build.log 2>&1 && echo build:ok
```

```output
build:ok
```

```bash
cd /tmp/monorepo-test-showboat && pnpm lint >/tmp/monorepo-test-showboat.lint.log 2>&1 && echo lint:ok
```

```output
lint:ok
```

```bash
cd /tmp/monorepo-test-showboat && pnpm test >/tmp/monorepo-test-showboat.test.log 2>&1 && echo test:ok
```

```output
test:ok
```

```bash
cd /tmp/monorepo-test-showboat && pnpm --dir packages/client start
```

```output

> @monorepo-showboat/client@0.1.0 start /private/tmp/monorepo-test-showboat/packages/client
> node dist/index.js

Hello, world!
```
