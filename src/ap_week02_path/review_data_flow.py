"""Protected tuple/list/unpacking/loop review for Week 2.

The example prepares path data but deliberately does not implement or call any
of the five assessed public objects.
"""

from __future__ import annotations

import numpy as np


def _format_point(label: str, point: tuple[float, float]) -> str:
    x_value, y_value = point
    return f"{label}=({x_value:.2f}, {y_value:.2f})"


def main() -> None:
    start = (0.0, 0.0)
    waypoint = (1.0, 1.5)
    goal = (3.0, 1.0)
    path = [start, waypoint, goal]

    start_x, start_y = start
    print("container_types", type(start).__name__, type(path).__name__)
    print("unpacked_start", start_x, start_y)
    print("first_point", path[0])
    print("first_two_points", path[:2])

    labels = ["start", "waypoint", "goal"]
    summaries_by_loop: list[str] = []
    for label, point in zip(labels, path):
        summaries_by_loop.append(_format_point(label, point))

    summaries_by_comprehension = [
        _format_point(label, point) for label, point in zip(labels, path)
    ]
    print("loop_equals_comprehension", summaries_by_loop == summaries_by_comprehension)
    for index, summary in enumerate(summaries_by_loop):
        print(f"point_{index}", summary)

    consecutive_pairs = list(zip(path[:-1], path[1:]))
    print("number_of_segments", len(consecutive_pairs))
    print("first_segment", consecutive_pairs[0])

    path_array = np.asarray(path, dtype=float)
    print("array_shape", path_array.shape)
    print("array_dtype", path_array.dtype)
    print("x_column", path_array[:, 0])


if __name__ == "__main__":
    main()
