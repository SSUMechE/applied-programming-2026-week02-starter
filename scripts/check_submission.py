"""Check student-authored evidence before the final package is built."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "tests" / "test_student_evidence.py"
NOTE_FILE = ROOT / "artifacts" / "engineering_note.md"


def main() -> int:
    failures: list[str] = []

    try:
        tree = ast.parse(TEST_FILE.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        failures.append(f"cannot read student tests: {exc}")
    else:
        tests = [
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        ]
        if len(tests) < 6:
            failures.append(
                f"student evidence needs at least 6 test functions; found {len(tests)}"
            )
        else:
            print(f"[OK] student-authored test functions: {len(tests)}")

    try:
        note = NOTE_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        failures.append(f"cannot read engineering note: {exc}")
    else:
        remaining_prompts = ("Explain how", "Report one", "Describe your")
        if any(prompt in note for prompt in remaining_prompts):
            failures.append("replace every prompt in the engineering note with evidence")
        else:
            print("[OK] engineering-note prompts have been replaced")

    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1
    print("[PASS] Student-authored submission evidence is present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
