"""Run and verify the intentional starter baseline."""

from __future__ import annotations

import re
import subprocess
import sys


# Updated by the release audit after the published suite is frozen.
EXPECTED_FAILED = 42
EXPECTED_PASSED = 6


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--tb=no",
        "tests/test_published_contract.py",
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    match = re.search(r"(\d+) failed, (\d+) passed", output)
    if match is None:
        print("[FAIL] Could not read the pytest baseline summary.")
        return 1
    failed, passed = map(int, match.groups())
    if (failed, passed) != (EXPECTED_FAILED, EXPECTED_PASSED):
        print(
            "[FAIL] Unexpected baseline: "
            f"{failed} failed, {passed} passed; expected "
            f"{EXPECTED_FAILED} failed, {EXPECTED_PASSED} passed."
        )
        return 1
    print(f"[PASS] Intentional baseline confirmed: {failed} failed, {passed} passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
