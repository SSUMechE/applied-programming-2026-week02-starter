"""Verify the Week 2 environment without executing student TODO functions."""

from __future__ import annotations

import importlib
import importlib.metadata
import inspect
import sys
from pathlib import Path


EXPECTED_PYTHON = (3, 12)
REQUIRED_DISTRIBUTIONS = {
    "numpy": "2.5.1",
    "pytest": "9.1.1",
    "setuptools": "81.0.0",
    "build": "1.3.0",
}
PUBLIC_NAMES = (
    "PathInputError",
    "segment_length",
    "interpolate_segment",
    "path_length",
    "path_lengths",
)


def check_environment() -> list[str]:
    failures: list[str] = []
    if sys.version_info[:2] != EXPECTED_PYTHON:
        failures.append(
            "Python must be 3.12.x; current interpreter is "
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )

    for distribution, expected_version in REQUIRED_DISTRIBUTIONS.items():
        try:
            version = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            failures.append(f"missing distribution: {distribution}")
        else:
            if version != expected_version:
                failures.append(
                    f"{distribution} must be {expected_version}; current version is {version}"
                )
            else:
                print(f"[OK] {distribution} {version}")

    try:
        package = importlib.import_module("ap_week02_path")
    except Exception as exc:  # pragma: no cover - diagnostic path
        failures.append(f"cannot import ap_week02_path: {type(exc).__name__}: {exc}")
    else:
        print(f"[OK] ap_week02_path import: {Path(package.__file__).resolve()}")
        for name in PUBLIC_NAMES:
            if not hasattr(package, name):
                failures.append(f"missing public object: {name}")
        expected_parameters = {
            "segment_length": ["start_xy", "goal_xy"],
            "interpolate_segment": ["start_xy", "goal_xy", "num_samples"],
            "path_length": ["path_xy"],
            "path_lengths": ["paths_xy"],
        }
        for name, expected in expected_parameters.items():
            if hasattr(package, name):
                actual = list(inspect.signature(getattr(package, name)).parameters)
                if actual != expected:
                    failures.append(f"wrong signature for {name}: {actual}")

    return failures


def main() -> int:
    print(
        "[INFO] Python",
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )
    failures = check_environment()
    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1
    print("[PASS] Week 2 path-geometry environment is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
