"""Public Week 2 path-geometry programming interface."""

from .path_geometry import (
    PathInputError,
    interpolate_segment,
    path_length,
    path_lengths,
    segment_length,
)

__all__ = [
    "PathInputError",
    "segment_length",
    "interpolate_segment",
    "path_length",
    "path_lengths",
]
