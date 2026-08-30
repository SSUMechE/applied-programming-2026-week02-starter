from __future__ import annotations

# Published contract. Students must not edit this file.

import ast
import inspect
import textwrap

import numpy as np
import pytest

import ap_week02_path
from ap_week02_path import (
    PathInputError,
    interpolate_segment,
    path_length,
    path_lengths,
    segment_length,
)


PUBLIC_PATHS = np.array(
    [
        [[0.0, 0.0], [3.0, 4.0], [6.0, 4.0]],
        [[-1.0, 2.0], [-1.0, 2.0], [1.0, 2.0]],
        [[0.0, 0.0], [0.0, 1.0], [0.0, 3.0]],
    ],
    dtype=np.float64,
)


def test_domain_exception_is_a_value_error() -> None:
    assert issubclass(PathInputError, ValueError)


def test_public_exports_are_frozen() -> None:
    assert ap_week02_path.__all__ == [
        "PathInputError",
        "segment_length",
        "interpolate_segment",
        "path_length",
        "path_lengths",
    ]


@pytest.mark.parametrize(
    "function,parameters",
    [
        (segment_length, ["start_xy", "goal_xy"]),
        (interpolate_segment, ["start_xy", "goal_xy", "num_samples"]),
        (path_length, ["path_xy"]),
        (path_lengths, ["paths_xy"]),
    ],
)
def test_public_signatures_are_frozen(function: object, parameters: list[str]) -> None:
    assert list(inspect.signature(function).parameters) == parameters


@pytest.mark.parametrize(
    "start,goal,expected",
    [
        ((0.0, 0.0), (3.0, 4.0), 5.0),
        ([-2, 1], [1, 1], 3.0),
        (np.array([1.25, -0.5]), np.array([1.25, -0.5]), 0.0),
    ],
)
def test_segment_length_normal_and_boundary_values(
    start: object, goal: object, expected: float
) -> None:
    start_before = np.asarray(start).copy()
    goal_before = np.asarray(goal).copy()
    result = segment_length(start, goal)  # type: ignore[arg-type]
    assert isinstance(result, float)
    assert result == pytest.approx(expected, rel=1e-12, abs=1e-12)
    assert np.array_equal(np.asarray(start), start_before)
    assert np.array_equal(np.asarray(goal), goal_before)


@pytest.mark.parametrize(
    "point",
    [
        [0.0],
        [0.0, 1.0, 2.0],
        np.array([0.0, 1.0], dtype=object),
        [0.0, np.nan],
        [0.0, np.inf],
        [True, 1.0],
        [1.0 + 0.0j, 2.0 + 0.0j],
        ["0", "1"],
    ],
)
def test_segment_length_rejects_invalid_point(point: object) -> None:
    with pytest.raises(PathInputError):
        segment_length(point, (1.0, 2.0))  # type: ignore[arg-type]


def test_interpolation_shape_dtype_and_endpoints() -> None:
    # NumPy integer scalars are valid sample counts; Boolean values are not.
    result = interpolate_segment((1.0, -1.0), (5.0, 3.0), np.int64(5))
    assert result.shape == (5, 2)
    assert result.dtype == np.float64
    assert np.allclose(
        result,
        [[1.0, -1.0], [2.0, 0.0], [3.0, 1.0], [4.0, 2.0], [5.0, 3.0]],
        rtol=0.0,
        atol=1e-12,
    )


def test_interpolation_uses_uniform_spacing() -> None:
    result = interpolate_segment((0.0, 0.0), (2.0, 4.0), 3)
    assert np.allclose(result, [[0.0, 0.0], [1.0, 2.0], [2.0, 4.0]])
    tree = ast.parse(textwrap.dedent(inspect.getsource(interpolate_segment)))
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "linspace"
        for node in ast.walk(tree)
    )


def test_interpolation_degenerate_segment_repeats_point() -> None:
    result = interpolate_segment((2.0, -3.0), (2.0, -3.0), 4)
    assert np.allclose(result, [[2.0, -3.0]] * 4, rtol=0.0, atol=0.0)


@pytest.mark.parametrize(
    "num_samples",
    [1, 2.5, True, np.int64(1), "5", np.nan],
)
def test_interpolation_rejects_invalid_num_samples(num_samples: object) -> None:
    with pytest.raises(PathInputError):
        interpolate_segment((0.0, 0.0), (1.0, 1.0), num_samples)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "start,goal",
    [
        ([True, 0.0], (1.0, 1.0)),
        ((0.0, 0.0), [1.0, np.inf]),
    ],
)
def test_interpolation_rejects_invalid_endpoint(start: object, goal: object) -> None:
    with pytest.raises(PathInputError):
        interpolate_segment(start, goal, 3)  # type: ignore[arg-type]


def test_interpolation_translation_invariance() -> None:
    shift = np.array([3.5, -2.25])
    base = interpolate_segment(np.array([0.0, 1.0]), np.array([2.0, 5.0]), 6)
    shifted = interpolate_segment(
        np.array([0.0, 1.0]) + shift,
        np.array([2.0, 5.0]) + shift,
        6,
    )
    assert np.allclose(shifted, base + shift, rtol=0.0, atol=1e-12)


def test_interpolation_does_not_mutate_inputs() -> None:
    start = np.array([0.0, 1.0])
    goal = np.array([2.0, 5.0])
    before = (start.copy(), goal.copy())
    interpolate_segment(start, goal, 5)
    assert np.array_equal(start, before[0])
    assert np.array_equal(goal, before[1])


def test_path_length_polyline() -> None:
    assert path_length([[0.0, 0.0], [3.0, 4.0], [6.0, 4.0]]) == pytest.approx(8.0)


def test_path_length_agrees_with_scalar_segment_sum() -> None:
    path = np.array([[0.0, 0.0], [1.0, 2.0], [4.0, 6.0], [4.0, 7.0]])
    expected = sum(segment_length(a, b) for a, b in zip(path[:-1], path[1:]))
    assert path_length(path) == pytest.approx(expected, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize(
    "path",
    [
        [],
        [[4.0, -2.0]],
        [[True, 0.0], [1.0, 2.0]],
        [[0.0, 1.0, 2.0]],
        np.array([[0.0, 1.0], [2.0, 3.0]], dtype=object),
        [[0.0, 0.0], [1.0, np.nan]],
    ],
)
def test_path_length_rejects_invalid_path(path: object) -> None:
    with pytest.raises(PathInputError):
        path_length(path)  # type: ignore[arg-type]


def test_path_length_translation_invariance_and_no_mutation() -> None:
    path = PUBLIC_PATHS[0].copy()
    before = path.copy()
    shift = np.array([7.0, -4.0])
    assert path_length(path + shift) == pytest.approx(path_length(path), abs=1e-12)
    assert np.array_equal(path, before)


def test_path_lengths_shape_dtype_and_values() -> None:
    result = path_lengths(PUBLIC_PATHS.tolist())
    assert result.shape == (3,)
    assert result.dtype == np.float64
    assert np.allclose(result, [8.0, 2.0, 3.0], rtol=0.0, atol=1e-12)
    tree = ast.parse(textwrap.dedent(inspect.getsource(path_lengths)))
    forbidden = (
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
    )
    assert not any(isinstance(node, forbidden) for node in ast.walk(tree))


def test_path_lengths_agree_with_scalar_reference() -> None:
    batch = path_lengths(PUBLIC_PATHS)
    scalar = np.array([path_length(path) for path in PUBLIC_PATHS])
    assert np.allclose(batch, scalar, rtol=1e-12, atol=1e-12)


def test_path_lengths_translation_invariance_and_no_mutation() -> None:
    paths = PUBLIC_PATHS.copy()
    before = paths.copy()
    shift = np.array([2.0, -9.0])
    assert np.allclose(path_lengths(paths + shift), path_lengths(paths), atol=1e-12)
    assert np.array_equal(paths, before)


@pytest.mark.parametrize(
    "paths",
    [
        np.empty((0, 3, 2)),
        np.empty((2, 0, 2)),
        np.zeros((2, 1, 2)),
        np.ones((2, 3, 3)),
        np.full((2, 3, 2), np.nan),
        [[[True, 0.0], [1.0, 2.0]]],
    ],
)
def test_path_lengths_reject_invalid_batch(paths: object) -> None:
    with pytest.raises(PathInputError):
        path_lengths(paths)  # type: ignore[arg-type]
    with pytest.raises(PathInputError):
        path_lengths(np.ones((1, 2, 2), dtype=object))
