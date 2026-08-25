"""Protected animated-SVG display of supplied paths using the student API.

This module does not plan a route, check collisions, or simulate dynamics.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .demo import DEMO_PATHS
from .path_geometry import interpolate_segment, path_length, path_lengths


ARTIFACT_DIR = Path("artifacts")
SCALE = 130.0
OFFSET_X = 86.0
OFFSET_Y = 370.0


def _display_xy(point: np.ndarray) -> tuple[float, float]:
    return (
        OFFSET_X + SCALE * float(point[0]),
        OFFSET_Y - SCALE * float(point[1]),
    )


def _path_data(path: np.ndarray) -> str:
    coordinates = [_display_xy(point) for point in path]
    return " ".join(
        ("M" if index == 0 else "L") + f" {x_value:.1f} {y_value:.1f}"
        for index, (x_value, y_value) in enumerate(coordinates)
    )


def _svg_path_layer(
    path: np.ndarray,
    *,
    path_id: str,
    label: str,
    color: str,
    duration_s: float,
    begin_s: float,
) -> str:
    path_data = _path_data(path)
    waypoint_marks: list[str] = []
    for index, point in enumerate(path):
        x_value, y_value = _display_xy(point)
        waypoint_marks.append(
            f'<circle cx="{x_value:.1f}" cy="{y_value:.1f}" r="5" '
            f'fill="white" stroke="{color}" stroke-width="3" />'
        )
        if 0 < index < len(path) - 1:
            waypoint_marks.append(
                f'<text x="{x_value + 9:.1f}" y="{y_value - 9:.1f}" '
                f'class="waypoint-label" fill="{color}">{label}{index}</text>'
            )

    return (
        f'<path id="{path_id}" d="{path_data}" fill="none" stroke="{color}" '
        'stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />'
        + "".join(waypoint_marks)
        + f'<circle r="9" fill="{color}" stroke="white" stroke-width="3">'
        + f'<animateMotion dur="{duration_s:.1f}s" begin="{begin_s:.1f}s" '
        + 'repeatCount="indefinite" calcMode="paced" rotate="auto">'
        + f'<mpath href="#{path_id}" xlink:href="#{path_id}" />'
        + '</animateMotion></circle>'
    )


def main() -> int:
    ARTIFACT_DIR.mkdir(exist_ok=True)
    first_segment_samples = interpolate_segment(
        DEMO_PATHS[0, 0], DEMO_PATHS[0, 1], 5
    )
    scalar_lengths = [path_length(path) for path in DEMO_PATHS]
    batch_lengths = path_lengths(DEMO_PATHS)
    if not np.allclose(scalar_lengths, batch_lengths, rtol=1e-12, atol=1e-12):
        raise RuntimeError("scalar and batch path lengths disagree")

    summary = {
        "coordinate_unit": "course Cartesian length unit",
        "path_shape": list(DEMO_PATHS.shape),
        "path_lengths": batch_lengths.tolist(),
        "first_segment_sample_shape": list(first_segment_samples.shape),
        "first_segment_endpoints": [
            first_segment_samples[0].tolist(),
            first_segment_samples[-1].tolist(),
        ],
        "display": {
            "format": "animated SVG",
            "animation": "SMIL animateMotion",
            "sequence": "start -> ordered waypoints -> goal",
            "scope": "computed path display only; no planning, collision checking, or physics simulation",
        },
    }
    (ARTIFACT_DIR / "path_geometry_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    start_x, start_y = _display_xy(DEMO_PATHS[0, 0])
    goal_x, goal_y = _display_xy(DEMO_PATHS[0, -1])
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" width="640" height="520" '
        'viewBox="0 0 640 520">'
        '<title>Animated display of two computed paths</title>'
        '<desc>Markers repeatedly follow supplied configurations from start '
        'through ordered waypoints to goal. This display performs no planning, '
        'collision checking, or physics simulation.</desc>'
        '<style>'
        'text{font-family:"Times New Roman",serif;fill:black}'
        '.title{font-size:24px;font-weight:bold}'
        '.subtitle{font-size:17px}'
        '.legend{font-size:16px}'
        '.waypoint-label{font-size:15px;font-weight:bold}'
        '</style>'
        '<rect width="640" height="520" fill="white" />'
        '<text x="28" y="36" class="title">Computed path display</text>'
        '<text x="28" y="64" class="subtitle">Markers follow start → ordered '
        'waypoints → goal and repeat automatically.</text>'
        '<text x="28" y="88" class="subtitle">No planner, collision checker, '
        'or physics simulation is executed here.</text>'
        '<line x1="510" y1="210" x2="548" y2="210" stroke="#1f4e79" '
        'stroke-width="4" /><text x="558" y="216" class="legend">Path A</text>'
        '<line x1="510" y1="240" x2="548" y2="240" stroke="#555555" '
        'stroke-width="4" /><text x="558" y="246" class="legend">Path B</text>'
        + _svg_path_layer(
            DEMO_PATHS[0],
            path_id="computed-path-a",
            label="A",
            color="#1f4e79",
            duration_s=6.0,
            begin_s=0.0,
        )
        + _svg_path_layer(
            DEMO_PATHS[1],
            path_id="computed-path-b",
            label="B",
            color="#555555",
            duration_s=6.8,
            begin_s=0.0,
        )
        + f'<text x="{start_x - 20:.1f}" y="{start_y + 28:.1f}" '
        + 'class="legend">Start</text>'
        + f'<text x="{goal_x + 12:.1f}" y="{goal_y + 6:.1f}" '
        + 'class="legend">Goal</text>'
        + '<text x="28" y="500" class="subtitle">Open this SVG in a modern '
        'browser; the animation starts automatically.</text>'
        + '</svg>\n'
    )
    (ARTIFACT_DIR / "path_geometry_preview.svg").write_text(svg, encoding="utf-8")
    print("[PASS] Wrote artifacts/path_geometry_summary.json")
    print("[PASS] Wrote animated artifacts/path_geometry_preview.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
