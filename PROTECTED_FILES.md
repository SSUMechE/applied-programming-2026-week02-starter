# Protected files and frozen public contract

Students may edit only:

- `src/ap_week02_path/path_geometry.py`
- `tests/test_student_evidence.py`
- `artifacts/engineering_note.md`

Do not edit:

- `src/ap_week02_path/__init__.py`
- `src/ap_week02_path/review_data_flow.py`
- `src/ap_week02_path/demo.py`
- `src/ap_week02_path/visualize.py`
- every file under `scripts/`
- `tests/test_published_contract.py`
- `pyproject.toml`
- `requirements.txt`
- `README.md`
- this protected-file list

Within `path_geometry.py`, the exception class, public function names,
parameter names and order, documented units, accepted shapes, and output
shapes are frozen. Students may add internal helpers whose names begin with
`_`. Invalid inputs must raise `PathInputError`; values must not be silently
clipped, reshaped, or repaired. `path_lengths` must be vectorized over the
path, waypoint, and coordinate axes. Do not use a Python `for`, `while`, or
comprehension inside that function.

`interpolate_segment` must generate `num_samples` uniformly spaced points with
`np.linspace(0.0, 1.0, num_samples)`. The count is a Python or NumPy integer
of at least two; Boolean values are invalid. A valid path contains at least
two configurations.

The artifact script and animated-SVG display are supplied callers of the
student package. They may not be modified to hide an incorrect result. The SVG
displays computed paths only; it does not plan, check collisions, or simulate
physics. AI-assisted editing does not change this contract; the grader restores
protected files before running the submission.
