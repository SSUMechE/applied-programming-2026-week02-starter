"""Protected numerical demonstration that calls the student public API."""

from __future__ import annotations

import numpy as np

from .path_geometry import interpolate_segment, path_length, path_lengths, segment_length


DEMO_PATHS = np.array(
    [
        [[0.0, 0.0], [1.0, 1.4], [2.4, 1.1], [3.2, 2.0]],
        [[0.0, 0.0], [0.8, -0.5], [2.0, 0.2], [3.2, 2.0]],
    ],
    dtype=float,
)


def main() -> int:
    snapshot = DEMO_PATHS.copy()
    samples = interpolate_segment(DEMO_PATHS[0, 0], DEMO_PATHS[0, 1], 5)
    scalar = np.array([path_length(path) for path in DEMO_PATHS])
    batch = path_lengths(DEMO_PATHS)
    print("first_segment_length", segment_length(DEMO_PATHS[0, 0], DEMO_PATHS[0, 1]))
    print("path_batch_shape", DEMO_PATHS.shape)
    print("first_segment_samples_shape", samples.shape)
    print(
        "first_segment_endpoints_match",
        bool(np.allclose(samples[[0, -1]], DEMO_PATHS[0, :2], rtol=1e-12, atol=1e-12)),
    )
    print("scalar_lengths", np.array2string(scalar, precision=6))
    print("batch_lengths", np.array2string(batch, precision=6))
    print("scalar_batch_allclose", np.allclose(scalar, batch, rtol=1e-12, atol=1e-12))
    print("input_unchanged", bool(np.array_equal(DEMO_PATHS, snapshot)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
