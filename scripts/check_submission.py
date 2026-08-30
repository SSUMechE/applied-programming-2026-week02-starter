"""Check student evidence, generated artifacts, and the built wheel."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "tests" / "test_student_evidence.py"
PUBLISHED_TEST_FILE = ROOT / "tests" / "test_published_contract.py"
NOTE_FILE = ROOT / "artifacts" / "engineering_note.md"
SUMMARY_FILE = ROOT / "artifacts" / "path_geometry_summary.json"
SVG_FILE = ROOT / "artifacts" / "path_geometry_preview.svg"
WHEEL_SMOKE_SCRIPT = ROOT / "scripts" / "smoke_test_wheel.py"

PUBLIC_FUNCTIONS = {
    "segment_length",
    "interpolate_segment",
    "path_length",
    "path_lengths",
}
CATEGORY_PREFIXES = {
    "normal": ("test_normal_",),
    "boundary": ("test_boundary_",),
    "invalid": ("test_invalid_",),
    "endpoint": ("test_endpoint_",),
    "translation": ("test_translation_",),
    "batch_or_ownership": (
        "test_batch_",
        "test_ownership_",
        "test_no_mutation_",
        "test_scalar_batch_",
    ),
}
TOLERANCE_CATEGORIES = ("normal", "translation", "batch_or_ownership")
NOTE_RESPONSE_MARKER = "<!-- STUDENT RESPONSE -->"
MIN_RESPONSE_CHARACTERS = 40


def _call_name(call: ast.Call) -> str | None:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return None


def _has_assertion(node: ast.FunctionDef) -> bool:
    if any(isinstance(item, ast.Assert) for item in ast.walk(node)):
        return True
    for item in ast.walk(node):
        if not isinstance(item, ast.With):
            continue
        for context in item.items:
            expression = context.context_expr
            if isinstance(expression, ast.Call) and _call_name(expression) == "raises":
                return True
    return False


def _has_public_call(node: ast.FunctionDef) -> bool:
    return any(
        isinstance(item, ast.Call) and _call_name(item) in PUBLIC_FUNCTIONS
        for item in ast.walk(node)
    )


def _has_explicit_tolerance(node: ast.FunctionDef) -> bool:
    for item in ast.walk(node):
        if not isinstance(item, ast.Call) or _call_name(item) not in {"isclose", "allclose"}:
            continue
        keywords = {keyword.arg for keyword in item.keywords}
        if {"rtol", "atol"}.issubset(keywords):
            return True
    return False


def _body_fingerprint(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    module = ast.Module(body=node.body, type_ignores=[])
    return ast.dump(module, include_attributes=False)


def _literal_sequences(node: ast.AST) -> set[str]:
    """Return literal tuple/list sequences used as candidate numerical inputs."""
    sequences: set[str] = set()
    for item in ast.walk(node):
        if not isinstance(item, (ast.List, ast.Tuple)) or len(item.elts) < 2:
            continue
        try:
            value = ast.literal_eval(item)
        except (ValueError, TypeError):
            continue
        sequences.add(repr(value))
    return sequences


def _read_test_trees() -> tuple[ast.Module | None, ast.Module | None, list[str]]:
    failures: list[str] = []
    trees: list[ast.Module | None] = []
    for label, path in (("student", TEST_FILE), ("published", PUBLISHED_TEST_FILE)):
        try:
            trees.append(ast.parse(path.read_text(encoding="utf-8")))
        except (OSError, SyntaxError) as exc:
            failures.append(f"cannot read {label} tests: {exc}")
            trees.append(None)
    return trees[0], trees[1], failures


def _check_test_structure() -> tuple[list[str], int]:
    student_tree, published_tree, failures = _read_test_trees()
    if student_tree is None:
        return failures, 0

    async_tests = [
        node.name
        for node in student_tree.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name.startswith("test_")
    ]
    if async_tests:
        failures.append("student evidence tests must be synchronous: " + ", ".join(async_tests))

    tests = [
        node
        for node in student_tree.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]
    names = [node.name for node in tests]
    if len(tests) < 6:
        failures.append(f"student evidence needs at least 6 test functions; found {len(tests)}")
    if len(names) != len(set(names)):
        failures.append("student evidence contains duplicate top-level test names")

    category_tests: dict[str, list[ast.FunctionDef]] = {}
    for category, prefixes in CATEGORY_PREFIXES.items():
        matches = [node for node in tests if node.name.startswith(prefixes)]
        category_tests[category] = matches
        if not matches:
            failures.append(
                f"missing {category} evidence test; use one of these prefixes: "
                + ", ".join(prefixes)
            )

    for node in tests:
        if not _has_assertion(node):
            failures.append(f"{node.name} contains no assertion or pytest.raises check")
        if not _has_public_call(node):
            failures.append(f"{node.name} does not call the public path-geometry API")

    for category in TOLERANCE_CATEGORIES:
        if category_tests[category] and not any(
            _has_explicit_tolerance(node) for node in category_tests[category]
        ):
            failures.append(
                f"{category} evidence must use np.isclose/np.allclose with explicit rtol and atol"
            )

    if published_tree is not None:
        published_fingerprints = {
            _body_fingerprint(node)
            for node in published_tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        }
        copied = [node.name for node in tests if _body_fingerprint(node) in published_fingerprints]
        if copied:
            failures.append(
                "student evidence contains exact copies of published test bodies: "
                + ", ".join(copied)
            )
        published_literals = _literal_sequences(published_tree)
        for category, matches in category_tests.items():
            if matches and not any(
                _literal_sequences(node).difference(published_literals)
                for node in matches
            ):
                failures.append(
                    f"{category} evidence needs a literal input sequence "
                    "not used in published tests"
                )

    if not failures:
        print(f"[OK] structured student evidence functions: {len(tests)}")
    return failures, len(tests)


def _run_student_tests(expected_minimum: int) -> list[str]:
    failures: list[str] = []
    collect_command = [
        sys.executable,
        "-m",
        "pytest",
        "--collect-only",
        "-q",
        str(TEST_FILE),
    ]
    collected = subprocess.run(
        collect_command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    collect_output = collected.stdout + collected.stderr
    node_ids = [
        line.strip()
        for line in collect_output.splitlines()
        if "test_student_evidence.py::" in line
    ]
    if collected.returncode != 0:
        failures.append("pytest could not collect student evidence tests")
        print(collect_output, end="" if collect_output.endswith("\n") else "\n")
        return failures
    if len(node_ids) < expected_minimum:
        failures.append(
            f"pytest collected {len(node_ids)} student tests; expected at least {expected_minimum}"
        )

    run_command = [sys.executable, "-m", "pytest", "-q", str(TEST_FILE)]
    completed = subprocess.run(
        run_command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    match = re.search(r"(\d+) passed in ", output)
    passed = int(match.group(1)) if match else -1
    if completed.returncode != 0 or passed != len(node_ids):
        failures.append(
            "every collected student evidence test must pass without skips or expected failures"
        )
    elif not failures:
        print(f"[OK] collected and passed student evidence tests: {passed}")
    return failures


def _note_sections(note: str) -> dict[int, str]:
    pattern = re.compile(
        r"^##\s+([0-5])\.\s+.*?\n(.*?)(?=^##\s+[0-5]\.\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    return {int(match.group(1)): match.group(2).strip() for match in pattern.finditer(note)}


def _student_response(section: str) -> str | None:
    """Return visible text after the preserved response marker.

    The question may remain above the marker. HTML comments below it are
    placeholders or authoring guidance and do not count as student evidence.
    """
    _, marker, response = section.partition(NOTE_RESPONSE_MARKER)
    if not marker:
        return None
    visible = re.sub(r"<!--.*?-->", " ", response, flags=re.DOTALL)
    return re.sub(r"\s+", " ", visible).strip()


def _check_engineering_note() -> list[str]:
    failures: list[str] = []
    try:
        note = NOTE_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"cannot read engineering note: {exc}"]

    sections = _note_sections(note)
    missing = [number for number in range(6) if number not in sections]
    if missing:
        failures.append("engineering note is missing sections: " + ", ".join(map(str, missing)))

    responses: dict[int, str] = {}
    for number, section in sections.items():
        response = _student_response(section)
        if response is None:
            failures.append(
                f"engineering-note section {number} is missing {NOTE_RESPONSE_MARKER}"
            )
        elif not response:
            failures.append(f"engineering-note section {number} is still template-only")
        else:
            responses[number] = response

    if 0 in responses:
        if "42 failed, 6 passed" not in responses[0]:
            failures.append("engineering-note section 0 must record 42 failed, 6 passed")
        if not re.search(
            r"tests/test_published_contract\.py::test_\S+", responses[0]
        ):
            failures.append(
                "engineering-note section 0 must record the first failing pytest test node ID"
            )
    for number in range(1, 6):
        visible_characters = len(re.findall(r"\w", responses.get(number, "")))
        if number in responses and visible_characters < MIN_RESPONSE_CHARACTERS:
            failures.append(f"engineering-note section {number} needs a substantive response")
    if not failures:
        print("[OK] engineering note has a recorded baseline and six completed sections")
    return failures


def _check_artifacts() -> list[str]:
    failures: list[str] = []
    try:
        from ap_week02_path import interpolate_segment, path_lengths
        from ap_week02_path.demo import DEMO_PATHS
        from ap_week02_path.visualize import (
            SAMPLES_PER_SEGMENT,
            _interpolate_path,
            _path_data,
        )

        displayed_paths = np.stack([_interpolate_path(path) for path in DEMO_PATHS])
        first_segment = interpolate_segment(
            DEMO_PATHS[0, 0], DEMO_PATHS[0, 1], SAMPLES_PER_SEGMENT
        )
        expected_lengths = path_lengths(displayed_paths)
    except Exception as exc:
        return [
            "cannot recompute artifact evidence from the public API: "
            f"{type(exc).__name__}: {exc}"
        ]

    try:
        summary = json.loads(SUMMARY_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"cannot read JSON artifact: {exc}")
    else:
        try:
            artifact_paths = np.asarray(summary["interpolated_paths"], dtype=np.float64)
            artifact_lengths = np.asarray(summary["path_lengths"], dtype=np.float64)
            artifact_endpoints = np.asarray(
                summary["first_segment_endpoints"], dtype=np.float64
            )
            if summary["source_path_shape"] != list(DEMO_PATHS.shape):
                failures.append("JSON source_path_shape is stale")
            if summary["path_shape"] != list(displayed_paths.shape):
                failures.append("JSON path_shape is stale")
            if summary["samples_per_segment"] != SAMPLES_PER_SEGMENT:
                failures.append("JSON samples_per_segment is stale")
            if artifact_paths.shape != displayed_paths.shape or not np.allclose(
                artifact_paths, displayed_paths, rtol=0.0, atol=1e-12
            ):
                failures.append("JSON interpolated_paths do not match current function outputs")
            if artifact_lengths.shape != expected_lengths.shape or not np.allclose(
                artifact_lengths, expected_lengths, rtol=1e-12, atol=1e-12
            ):
                failures.append("JSON path_lengths do not match current function outputs")
            if summary["first_segment_sample_shape"] != list(first_segment.shape):
                failures.append("JSON first_segment_sample_shape is stale")
            if artifact_endpoints.shape != (2, 2) or not np.allclose(
                artifact_endpoints,
                first_segment[[0, -1]],
                rtol=0.0,
                atol=1e-12,
            ):
                failures.append("JSON first-segment endpoints are stale")
            display = summary["display"]
            if display["format"] != "animated SVG":
                failures.append("JSON display format is stale")
            if display["sequence"] != "start -> ordered waypoints -> goal":
                failures.append("JSON display sequence is stale")
            if "interpolated student-function outputs" not in display["scope"]:
                failures.append("JSON display scope does not identify student outputs")
        except (KeyError, TypeError, ValueError) as exc:
            failures.append(f"JSON artifact has the wrong schema: {exc}")

    try:
        root = ET.parse(SVG_FILE).getroot()
    except (OSError, ET.ParseError) as exc:
        failures.append(f"cannot read SVG artifact: {exc}")
    else:
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        for label, expected in zip(("a", "b"), displayed_paths):
            element = root.find(
                f".//svg:path[@id='interpolated-path-{label}']", namespace
            )
            if element is None or element.attrib.get("d") != _path_data(expected):
                failures.append(f"SVG interpolated path {label.upper()} is stale")
        animations = root.findall(".//svg:animateMotion", namespace)
        if len(animations) != len(displayed_paths):
            failures.append("SVG must contain one animated marker per interpolated path")
        visible_text = " ".join(root.itertext()).lower()
        for phrase in (
            "interpolated path display",
            "returned samples",
            "no planner",
            "collision checker",
            "physics simulation",
        ):
            if phrase not in visible_text:
                failures.append(f"SVG boundary label is missing {phrase!r}")

    if not failures:
        print("[OK] JSON and SVG match current student-function outputs")
    return failures


def _check_wheel() -> list[str]:
    completed = subprocess.run(
        [sys.executable, str(WHEEL_SMOKE_SCRIPT)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    if completed.returncode != 0:
        return ["built-wheel clean install/import smoke test failed"]
    return []


def main() -> int:
    failures: list[str] = []
    structure_failures, test_count = _check_test_structure()
    failures.extend(structure_failures)
    failures.extend(_run_student_tests(max(6, test_count)))
    failures.extend(_check_engineering_note())
    failures.extend(_check_artifacts())
    failures.extend(_check_wheel())

    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1
    print("[PASS] Student tests, note, artifacts, and clean wheel are verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
