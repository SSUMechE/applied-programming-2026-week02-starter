"""Install the built wheel in a disposable venv and smoke-test that install."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import venv


ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
EXPECTED_VERSION = "0.8.0"
EXPECTED_PARAMETERS = {
    "segment_length": ["start_xy", "goal_xy"],
    "interpolate_segment": ["start_xy", "goal_xy", "num_samples"],
    "path_length": ["path_xy"],
    "path_lengths": ["paths_xy"],
}


def _venv_python(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def _run(command: list[str], *, cwd: Path, environment: dict[str, str]) -> bool:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if completed.returncode == 0:
        return True
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    return False


def main() -> int:
    wheels = sorted(DIST_DIR.glob("ap_week02_path-*.whl"))
    if len(wheels) != 1:
        candidates = ", ".join(path.name for path in wheels) or "none"
        print(
            "[FAIL] expected exactly one dist/ap_week02_path-*.whl; "
            f"found {len(wheels)} ({candidates})"
        )
        return 1
    wheel = wheels[0].resolve()

    child_environment = os.environ.copy()
    for name in tuple(child_environment):
        if name.upper() in {"PYTHONHOME", "PYTHONPATH"}:
            child_environment.pop(name)
    child_environment["PYTHONNOUSERSITE"] = "1"
    child_environment["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    child_environment["PIP_NO_INPUT"] = "1"

    smoke_code = textwrap.dedent(
        f"""
        import importlib.metadata
        import inspect
        from pathlib import Path
        import site
        import sys
        import sysconfig

        import numpy as np
        import ap_week02_path as package

        assert sys.prefix != sys.base_prefix
        assert site.ENABLE_USER_SITE is False
        package_path = Path(package.__file__).resolve()
        purelib = Path(sysconfig.get_path("purelib")).resolve()
        assert package_path.is_relative_to(purelib)
        assert importlib.metadata.version("ap-week02-path") == {EXPECTED_VERSION!r}
        assert importlib.metadata.version("numpy") == "2.5.1"
        expected = {EXPECTED_PARAMETERS!r}
        for name, parameters in expected.items():
            assert list(inspect.signature(getattr(package, name)).parameters) == parameters

        assert package.segment_length((0, 0), (3, 4)) == 5.0
        samples = package.interpolate_segment((0, 0), (2, 4), 3)
        assert samples.shape == (3, 2)
        assert samples.dtype == np.float64
        assert np.allclose(samples, [[0, 0], [1, 2], [2, 4]], rtol=0.0, atol=1e-12)
        paths = np.array([
            [[0.0, 0.0], [0.0, 0.0], [3.0, 4.0]],
            [[0.0, 0.0], [0.0, 3.0], [4.0, 3.0]],
        ])
        assert package.path_length(paths[1]) == 7.0
        batch = package.path_lengths(paths)
        assert batch.shape == (2,)
        assert batch.dtype == np.float64
        assert np.allclose(batch, [5.0, 7.0], rtol=0.0, atol=1e-12)
        print("[OK] installed package:", package_path)
        """
    )

    try:
        with tempfile.TemporaryDirectory(prefix="ap-week02-wheel-smoke-") as temp_name:
            temp_root = Path(temp_name)
            environment = temp_root / "venv"
            neutral_workdir = temp_root / "work"
            neutral_workdir.mkdir()
            venv.EnvBuilder(with_pip=True, system_site_packages=False).create(environment)
            python = _venv_python(environment)

            if not _run(
                [
                    str(python),
                    "-m",
                    "pip",
                    "install",
                    "--only-binary=:all:",
                    str(wheel),
                ],
                cwd=neutral_workdir,
                environment=child_environment,
            ):
                print("[FAIL] could not install the built wheel in the clean venv")
                return 1
            if not _run(
                [str(python), "-I", "-c", smoke_code],
                cwd=neutral_workdir,
                environment=child_environment,
            ):
                print("[FAIL] installed-wheel import or API smoke test failed")
                return 1
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"[FAIL] clean wheel smoke test could not run: {exc}")
        return 1

    print(f"[PASS] Clean wheel install and import passed: {wheel.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
