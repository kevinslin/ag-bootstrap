from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "bin" / "ag-bootstrap"


class AgBootstrapTest(unittest.TestCase):
    def run_cli(
        self, *args: str, cwd: Path | None = None, env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            [str(CLI), *args],
            cwd=cwd or REPO_ROOT,
            check=True,
            capture_output=True,
            env=merged_env,
            text=True,
        )

    def test_list_includes_typescript(self) -> None:
        result = self.run_cli("list")
        self.assertEqual(result.stdout.strip(), "typescript")

    def test_bootstrap_renders_template_with_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "hello-world"
            self.run_cli("bootstrap", "typescript", str(target), "--skip-followup")

            package_json = json.loads((target / "package.json").read_text(encoding="utf-8"))
            self.assertEqual(package_json["name"], "hello-world")
            self.assertEqual(package_json["description"], "Project bootstrapped from ag-bootstrap")
            self.assertTrue((target / "pnpm-lock.yaml").is_file())
            self.assertTrue((target / "pnpm-workspace.yaml").is_file())
            self.assertTrue((target / "tsconfig.json").is_file())
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / "design.md").is_file())
            self.assertTrue((target / "memory.md").is_file())
            self.assertTrue((target / "config.md").is_file())
            self.assertTrue((target / "progress.md").is_file())
            self.assertTrue((target / "docs" / "spec-01-monorepo-foundation.md").is_file())
            self.assertTrue((target / ".agents" / "runs" / "spec-01-progress.md").is_file())
            self.assertTrue((target / ".github" / "workflows" / "ci.yml").is_file())
            self.assertTrue((target / "packages" / "common" / "src" / "index.ts").is_file())
            self.assertTrue((target / "packages" / "common" / "test" / "index.test.ts").is_file())
            self.assertTrue((target / "packages" / "integration" / "test" / "app.integration.test.ts").is_file())
            self.assertTrue((target / ".husky" / "pre-commit").is_file())
            self.assertTrue((target / ".husky" / "pre-push").is_file())

            precommit = (target / ".husky" / "pre-commit").read_text(encoding="utf-8")
            self.assertIn("pnpm lint", precommit)
            self.assertIn("pnpm format", precommit)

            prepush = (target / ".husky" / "pre-push").read_text(encoding="utf-8")
            self.assertIn("pnpm format:check", prepush)

    def test_bootstrap_renders_template_with_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "unused-dir-name"
            self.run_cli(
                "bootstrap",
                "typescript",
                str(target),
                "--project-name",
                "Sample App",
                "--package-name",
                "sample-app",
                "--description",
                "Custom description",
                "--skip-followup",
            )

            package_json = json.loads((target / "package.json").read_text(encoding="utf-8"))
            self.assertEqual(package_json["name"], "sample-app")
            self.assertEqual(package_json["description"], "Custom description")
            readme = (target / "README.md").read_text(encoding="utf-8")
            self.assertIn("# Sample App", readme)

            common_package = json.loads(
                (target / "packages" / "common" / "package.json").read_text(encoding="utf-8")
            )
            self.assertEqual(common_package["name"], "@sample-app/common")

            server_source = (target / "packages" / "server" / "src" / "index.ts").read_text(
                encoding="utf-8"
            )
            self.assertIn('from "@sample-app/common"', server_source)

    def test_add_precommit_writes_husky_hook(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            (target / "pnpm-lock.yaml").write_text("", encoding="utf-8")
            (target / "package.json").write_text(
                json.dumps(
                    {
                        "scripts": {
                            "lint": "tsc -p tsconfig.json",
                            "format": "prettier --write .",
                        }
                    }
                ),
                encoding="utf-8",
            )

            self.run_cli("add-precommit", str(target))

            precommit = (target / ".husky" / "pre-commit").read_text(encoding="utf-8")
            self.assertIn("pnpm lint", precommit)
            self.assertIn("pnpm format", precommit)

            prepush = (target / ".husky" / "pre-push").read_text(encoding="utf-8")
            self.assertIn("pnpm format", prepush)

    def test_bootstrap_runs_followup_with_stubbed_tools(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target = root / "followup-app"
            bin_dir = root / "bin"
            bin_dir.mkdir()
            command_log = root / "commands.log"

            (bin_dir / "pnpm").write_text(
                "#!/bin/sh\n"
                'printf "pnpm %s\\n" "$*" >> "$AG_BOOTSTRAP_LOG"\n',
                encoding="utf-8",
            )
            (bin_dir / "git").write_text(
                "#!/bin/sh\n"
                'printf "git %s\\n" "$*" >> "$AG_BOOTSTRAP_LOG"\n'
                'if [ "$1" = "init" ]; then\n'
                "  mkdir -p .git\n"
                "fi\n",
                encoding="utf-8",
            )
            (bin_dir / "pnpm").chmod(0o755)
            (bin_dir / "git").chmod(0o755)

            env = {
                "AG_BOOTSTRAP_LOG": str(command_log),
                "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            }

            self.run_cli("bootstrap", "typescript", str(target), env=env)

            logged_commands = command_log.read_text(encoding="utf-8")
            self.assertIn("pnpm install", logged_commands)
            self.assertIn("pnpm test", logged_commands)
            self.assertIn("git init", logged_commands)
            self.assertIn("pnpm prepare", logged_commands)
            self.assertTrue((target / ".git").is_dir())


if __name__ == "__main__":
    unittest.main()
