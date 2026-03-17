# TypeScript Monorepo Fix Verification

*2026-03-17T06:57:52Z by Showboat 0.6.1*
<!-- showboat-id: dae91fd1-f993-4e07-8134-af0b718727a3 -->

This demo proves the review-driven fixes in a fresh generated repo at /tmp/monorepo-test-2: default bootstrap follow-up works, a committed pnpm lockfile supports frozen installs, cross-package imports compile, root build/lint/test succeed, and the built client plus integration package execute correctly.

```bash
python3 -c "from pathlib import Path; import shutil; shutil.rmtree(Path('/tmp/monorepo-test-2'), ignore_errors=True); print('clean:ok')"
```

```output
clean:ok
```

```bash
./bin/ag-bootstrap bootstrap typescript /tmp/monorepo-test-2 --project-name 'Monorepo Test 2' --package-name monorepo-test-2 --description 'Generated monorepo test 2' >/tmp/monorepo-test-2.bootstrap.log 2>&1 && echo bootstrap:ok
```

```output
bootstrap:ok
```

```bash
test -d /tmp/monorepo-test-2/.git && test -f /tmp/monorepo-test-2/pnpm-lock.yaml && echo followup:ok
```

```output
followup:ok
```

```bash
grep '^import' /tmp/monorepo-test-2/packages/server/src/index.ts && printf '%s\n' '---' && grep '^import' /tmp/monorepo-test-2/packages/integration/src/index.ts
```

```output
import { formatGreeting } from "@monorepo-test-2/common"
import { createConnectionString } from "@monorepo-test-2/db"
---
import { renderHelloWorld } from "@monorepo-test-2/client"
import { createConnectionString } from "@monorepo-test-2/db"
import { buildServerBanner } from "@monorepo-test-2/server"
```

```bash
cd /tmp/monorepo-test-2 && pnpm install --frozen-lockfile >/tmp/monorepo-test-2.install.log 2>&1 && echo frozen-install:ok
```

```output
frozen-install:ok
```

```bash
cd /tmp/monorepo-test-2 && pnpm build >/tmp/monorepo-test-2.build.log 2>&1 && echo build:ok
```

```output
build:ok
```

```bash
cd /tmp/monorepo-test-2 && pnpm lint >/tmp/monorepo-test-2.lint.log 2>&1 && echo lint:ok
```

```output
lint:ok
```

```bash
cd /tmp/monorepo-test-2 && pnpm test >/tmp/monorepo-test-2.test.log 2>&1 && echo test:ok
```

```output
test:ok
```

```bash
cd /tmp/monorepo-test-2 && pnpm --dir packages/client start | tail -n 1
```

```output
Hello, world!
```

```bash
cd /tmp/monorepo-test-2 && node -e "const { runSmokeTest } = require('./packages/integration/dist'); console.log(JSON.stringify(runSmokeTest('world')))"
```

```output
{"client":"Hello, world!","database":"postgres://localhost:5432/service","server":"Hello, world! Connected to postgres://localhost:5432/service"}
```
