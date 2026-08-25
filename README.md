# Week 2 — Functions, Tests, and NumPy Review

This starter uses two-dimensional path geometry as one continuous programming
example. You are **not** implementing a motion planner or collision checker in
Week 2. You are implementing and testing reusable numerical functions that
later planners will call.

## Required reading order

Before changing code, read the student materials in this order:

1. `week_02_functions_tests_numpy_reading_v22_motion_path.pdf` from the LMS;
2. `ASSIGNMENT_2_PATH_GEOMETRY_AND_VERIFICATION_V21.pdf` from the LMS;
3. this `README.md`;
4. `PROTECTED_FILES.md`.

The Reading explains the programming concepts. The Assignment fixes the TODO
order, evidence, and submission conditions. This README supplies the exact
repository commands. If the three sources appear inconsistent, stop and ask
before changing a protected file.

## 1. Create the private submission repository

Open the public course template:

<https://github.com/SSUMechE/applied-programming-2026-week02-starter>

1. Select **Use this template**, then **Create a new repository**.
2. Name it `applied-programming-w02-<student-id>` using your own student ID.
3. Set its visibility to **Private**.
4. Invite the GitHub account `SSUMechE` as a collaborator.
5. Confirm that `SSUMechE` shows active access, not a pending invitation.
6. Clone your private repository. Do not submit a clone whose `origin` still
   points to the public course template.

```powershell
git clone https://github.com/YOUR-GITHUB-ID/applied-programming-w02-YOUR-STUDENT-ID.git
cd applied-programming-w02-YOUR-STUDENT-ID
git remote -v
```

Both `origin` URLs must point to the private repository that you created.

## 2. Public programming contract

Keep the provided `PathInputError` exception and complete the four public
functions in `src/ap_week02_path/path_geometry.py` without changing their names,
signatures, units, or output shapes.

| Public object | Input contract | Output contract |
|---|---|---|
| `PathInputError` | invalid public input | subclass of `ValueError` |
| `segment_length(start_xy, goal_xy)` | two points, each shape `(2,)` | nonnegative distance, `float` |
| `interpolate_segment(start_xy, goal_xy, num_samples)` | start and goal `(2,)`; Python or NumPy integer `num_samples=M` | uniformly sampled points `(M, 2)`, `float64` |
| `path_length` | one path `(N, 2)` | total polyline length, `float` |
| `path_lengths` | path batch `(B, N, 2)` | one length per path, `(B,)`, `float64` |

Coordinates and distances use course-defined Cartesian length units. `M` and
`N` must be at least two; `B` must be at least one. Integer and floating-point tuples,
lists, and NumPy arrays are accepted. Boolean, complex, string, object, empty,
wrong-shaped, and non-finite inputs are invalid and must raise
`PathInputError`. `num_samples` may be a Python or NumPy integer of at least
two; Boolean values are not accepted as integers. Interpolation uses equally spaced fractions from
zero to one and includes both endpoints. None of the functions may modify an
input owned by the caller.

## 3. Install and verify the environment

Run commands from the repository root.

```powershell
conda activate applied-programming-2026
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

The final line must be:

```text
[PASS] Week 2 path-geometry environment is ready.
```

## 4. Review familiar Python containers

Run the protected review example before editing the TODO file.

```powershell
python -m ap_week02_path.review_data_flow
```

It shows one point as a tuple, a path as a list of tuples, unpacking, indexing,
slicing, `zip`, a `for` loop, a list comprehension, and conversion to an
`(N, 2)` NumPy array. It does not contain the four function bodies that you
must complete.

## 5. Record the intentional baseline

```powershell
python scripts/run_baseline.py
```

The starter intentionally contains `NotImplementedError`. The script checks
the exact published-suite baseline: **42 failed, 6 passed**. Do not edit
`tests/test_published_contract.py` to remove failures.

## 6. Complete the functions in dependency order

Edit only the files listed as student-editable in `PROTECTED_FILES.md`.

1. `segment_length`: validate two `(2,)` points and compute their Euclidean
   distance.
2. `interpolate_segment`: validate start, goal, and `num_samples`, then return
   uniformly spaced affine samples including both endpoints.
3. `path_length`: add the lengths of consecutive segments in one `(N, 2)`
   path, where `N >= 2`.
4. `path_lengths`: compute a `(B,)` batch result with NumPy operations over
   the path, waypoint, and coordinate axes. Do not use a Python `for`,
   `while`, or comprehension inside this function.
5. Add independent tests in `tests/test_student_evidence.py` and explain the
   evidence in `artifacts/engineering_note.md`.

Run the published suite after each dependency is completed:

```powershell
python -m pytest -q tests/test_published_contract.py
```

## 7. Required independent tests

Add at least six top-level `test_...` functions that are not copies of the
published cases. Include:

- one new normal case;
- one boundary case;
- one invalid input;
- endpoint preservation for interpolation;
- translation invariance;
- scalar-batch equivalence or no mutation.

Use `np.isclose` or `np.allclose` with an explicit tolerance for floating-point
results.

## 8. Generate numerical evidence and open the provided animated path display

After all tests pass, run:

```powershell
python -m ap_week02_path.demo
python -m ap_week02_path.visualize
python scripts/generate_artifacts.py
```

The protected script calls your public functions on supplied paths and writes:

```text
artifacts/path_geometry_summary.json
artifacts/path_geometry_preview.svg
```

Open `artifacts/path_geometry_preview.svg` in a modern browser. Two markers
automatically follow the supplied configurations in order from start, through
the intermediate waypoints, to the goal. The animation then repeats. The SVG
only displays paths computed by your functions. It does not plan a route,
inspect obstacles, check collisions, or simulate robot dynamics.

## 9. Build and submit a reproducible package

```powershell
python -m pytest -q
python -m ap_week02_path.demo
python -m ap_week02_path.visualize
python scripts/generate_artifacts.py
python scripts/check_submission.py
python -m build --wheel --no-isolation
git status --short
git add src/ap_week02_path/path_geometry.py tests/test_student_evidence.py artifacts dist
git commit -m "Complete Week 2 path-geometry package"
git push
git status --short
git rev-parse HEAD
```

Submit through the LMS:

1. the private GitHub repository URL;
2. the full 40-character commit identifier; and
3. confirmation that `SSUMechE` has active access.

The final revision must include the preserved exception and four completed
functions, at least six top-level `test_...` functions in
`tests/test_student_evidence.py`, the engineering note, JSON and SVG artifacts,
and the wheel under `dist/`.
