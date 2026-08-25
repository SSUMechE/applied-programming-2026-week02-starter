"""Student implementation target for Week 2.

Implement pure numerical functions only. Do not print, plot, write files,
modify caller-owned data, implement a planner, or perform collision checking
in this module.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray


PointLike = Sequence[float] | NDArray[np.integer | np.floating]
RealArrayLike = Sequence[Sequence[float]] | NDArray[np.integer | np.floating]


class PathInputError(ValueError):
    """Raised when an input violates the published path-geometry contract."""


def segment_length(start_xy: PointLike, goal_xy: PointLike) -> float:
    """Return the Euclidean distance between two points of shape ``(2,)``.

    Coordinates and the returned distance use course-defined Cartesian length
    units. Inputs must contain finite real numbers and remain unchanged.
    """
    # TODO 1: validate both points and return a nonnegative Python float.
    raise NotImplementedError("Implement segment_length")


def interpolate_segment(
    start_xy: PointLike,
    goal_xy: PointLike,
    num_samples: int,
) -> NDArray[np.float64]:
    """Return affine samples along a segment with shape ``(M, 2)``.

    ``num_samples`` is a Python or NumPy integer ``M >= 2``; Boolean values are
    invalid. Samples are uniformly spaced and include ``start_xy`` and
    ``goal_xy`` exactly as the first and last rows.
    """
    # TODO 2: validate both points and num_samples, generate uniform fractions,
    # broadcast them against coordinates, and return float64 without mutation.
    raise NotImplementedError("Implement interpolate_segment")


def path_length(path_xy: RealArrayLike) -> float:
    """Return the total length of one polyline with shape ``(N, 2)``.

    ``N`` must be at least two so the path contains at least one segment.
    """
    # TODO 3: validate the path and sum consecutive segment lengths.
    raise NotImplementedError("Implement path_length")


def path_lengths(
    paths_xy: Sequence[Sequence[Sequence[float]]]
    | NDArray[np.integer | np.floating],
) -> NDArray[np.float64]:
    """Return lengths for a batch of paths of shape ``(B, N, 2)``.

    ``B`` must be at least one and ``N`` at least two. The result has shape ``(B,)`` and
    dtype ``float64``. Do not use a Python ``for``, ``while``, or comprehension
    inside this function; compute over the batch with NumPy operations.
    """
    # TODO 4: validate, use differences along the vertex axis, and return one
    # length per path without modifying the input.
    raise NotImplementedError("Implement path_lengths")
