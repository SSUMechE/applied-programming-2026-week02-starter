# Week 2 — Functions, Tests, and NumPy Review

This starter uses two-dimensional path geometry as one continuous programming
example. You are **not** implementing a motion planner or collision checker in
Week 2. You are implementing and testing reusable numerical functions that
later planners will call.

## Required reading order

Before changing code, read the student materials in this order:

1. `docs/week_02_functions_tests_numpy_reading_v26.pdf`, including its final
   **Assignment 2** section;
2. this `README.md`;
3. `PROTECTED_FILES.md`.

The integrated Reading explains the programming concepts and then gives the
complete Assignment 2 procedure, evidence, and submission conditions in its
final section. This README supplies the exact repository commands. The LMS
copy must be identical to the versioned Reading under `docs/`. If the Reading,
README, and protected-file list appear inconsistent, stop and ask before
changing a protected file.

The editable module `src/ap_week02_path/path_geometry.py` has the Python import
path `ap_week02_path.path_geometry`. Complete TODO 1 through TODO 4 in that
module. The protected demo and scripts are callers of your public functions;
they are not substitute implementations. The animated SVG is display evidence.
Correctness is established by the published numerical contract and tests, not
by visual appearance. Do not claim that this assignment implements planning,
control, collision checking, or physical execution.

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
The downloadable starter ZIP is a review and recovery copy and intentionally
does not contain Git history. A directory produced by merely extracting that
ZIP is not the submitted repository. The evaluated repository begins when you
create a private repository from the public template and clone it as above.

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
lists, and native numeric NumPy arrays are accepted. NumPy arrays with
`dtype=object` are invalid even if every stored object is numeric. Boolean,
complex, string, empty, wrong-shaped, and non-finite inputs are also invalid and
must raise `PathInputError`. `num_samples` may be a Python or NumPy integer of
at least two; Boolean values are not accepted as integers. Interpolation uses
equally spaced fractions from zero to one and includes both endpoints. None of
the functions may modify an input owned by the caller.

## 3. Install and verify the environment

Run commands from the repository root. The normal path is to reuse the
`applied-programming-2026` environment created in Week 1.

```powershell
conda activate applied-programming-2026
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

If `conda activate applied-programming-2026` reports that the environment does
not exist, create it once from the protected environment file, then repeat the
installation and verification commands above.

```powershell
conda env create -f environment.yml
conda activate applied-programming-2026
```

If the `conda` command itself is unavailable, use the supported repository-local
virtual-environment fallback below. Continue to run later commands with this
environment activated.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

The official Week 1–2 core environment does not install `numba`. If pip reports
a conflict caused by unrelated packages that were added to your existing
course environment, do not change the published NumPy or setuptools pins. Use
the clean repository-local `.venv` fallback above and include the diagnostic
message when requesting help.

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

The command above launches the module named `ap_week02_path.review_data_flow`.
Before continuing, also verify the package and function import paths from the
repository root:

```powershell
python -c "import ap_week02_path; print(ap_week02_path.__file__)"
python -c "from ap_week02_path.path_geometry import segment_length; print(segment_length.__module__)"
```

The first command must print a path inside this repository's
`src/ap_week02_path` directory. The second must print
`ap_week02_path.path_geometry`. These checks distinguish the installed package,
its source module, and the terminal command that launches a caller.

## 5. Record the intentional baseline

```powershell
python scripts/run_baseline.py
```

The starter intentionally contains `NotImplementedError`. The script checks
the exact published-suite baseline: **42 failed, 6 passed**. Do not edit
`tests/test_published_contract.py` to remove failures. Before editing the TODO
file, copy both the summary and the first `FAILED` pytest test node ID into section 0
of `artifacts/engineering_note.md`.

## 6. Complete the functions in dependency order

Edit only the files listed as student-editable in `PROTECTED_FILES.md`.

### In-class checkpoint A — segment functions

1. `segment_length`: validate two `(2,)` points and compute their Euclidean
   distance.
2. `interpolate_segment`: validate start, goal, and `num_samples`, then return
   uniformly spaced affine samples including both endpoints.

### In-class checkpoint B — path functions

3. `path_length`: add the lengths of consecutive segments in one `(N, 2)`
   path, where `N >= 2`.
4. `path_lengths`: compute a `(B,)` batch result with NumPy operations over
   the path, waypoint, and coordinate axes. Do not use a Python `for`,
   `while`, or comprehension inside this function.

These four function bodies are the intended in-class core. If they are not
complete at the end of class, finish them before the independent evidence work.

### Homework completion — independent evidence and packaging

5. Add independent tests in `tests/test_student_evidence.py` using inputs that
   are different from the published examples.
6. Regenerate the JSON/SVG artifacts and complete
   `artifacts/engineering_note.md`.
7. Build the wheel, commit and push one clean revision, then submit the private
   repository URL and full commit ID through LMS.

Use the focused checkpoint after each dependency, then run the complete
published suite after all four functions are implemented:

```powershell
python -m pytest -q tests/test_published_contract.py -k segment_length -x
python -m pytest -q tests/test_published_contract.py -k interpolation -x
python -m pytest -q tests/test_published_contract.py -k "path_length and not path_lengths" -x
python -m pytest -q tests/test_published_contract.py -k path_lengths -x
python -m pytest -q tests/test_published_contract.py
```

After the four TODO functions are correct, the final command must report
**48 passed**.

## 7. Required independent tests

Add at least six top-level `test_...` functions that are not copies of the
published cases. Include:

- one new normal case;
- one boundary case;
- one invalid input;
- endpoint preservation for interpolation;
- translation invariance;
- scalar-batch equivalence or no mutation.

Name one test with each matching prefix: `test_normal_`, `test_boundary_`,
`test_invalid_`, `test_endpoint_`, `test_translation_`, and one of
`test_batch_`, `test_ownership_`, `test_no_mutation_`, or
`test_scalar_batch_`. Every evidence test must call the public API and contain
an assertion or `pytest.raises`. The normal, translation, and batch-or-ownership
tests must use `np.isclose` or `np.allclose` with explicit `rtol` and `atol`.
Exact equality may be used for integer shapes, exact Boolean conditions, and a
boundary invariant that the public contract guarantees exactly, such as zero
length for identical endpoints.
The protected checker rejects duplicate names and exact copies of published
test bodies. It also requires each category to contain at least one literal
input sequence absent from the published test file, collects the file with
pytest, and requires every collected test to pass.

In `artifacts/engineering_note.md`, keep the supplied questions and each
`<!-- STUDENT RESPONSE -->` marker. Replace only the placeholder comment below
each marker with your evidence. The checker evaluates the response region of
each numbered section, so retaining the question text does not cause a false
failure; an empty or template-only response does.

## 8. Generate numerical evidence and open the provided animated path display

After all tests pass, run:

```powershell
python -m ap_week02_path.demo
python scripts/generate_artifacts.py
```

`generate_artifacts.py` is the canonical artifact command; it invokes the
protected visualization module once. The script interpolates every supplied
segment with your public function, computes lengths from those returned arrays,
and writes:

```text
artifacts/path_geometry_summary.json
artifacts/path_geometry_preview.svg
```

Open `artifacts/path_geometry_preview.svg` in a modern browser. Two markers
automatically follow the interpolated arrays returned by your function, from
the supplied start through the ordered waypoints to the goal. The JSON records
those arrays, their shapes, endpoints, and computed lengths. The animation then
repeats. Neither artifact plans a route, inspects obstacles, checks collisions,
or simulates robot dynamics.

## 9. Build and submit a reproducible package

```powershell
python -m pytest -q
python -m ap_week02_path.demo
python scripts/generate_artifacts.py
python -m build --wheel --no-isolation
python scripts/check_submission.py
git status --short
git add src/ap_week02_path/path_geometry.py tests/test_student_evidence.py artifacts dist
git commit -m "Complete Week 2 path-geometry package"
git push
git status --short
git rev-parse HEAD
```

The final checker reruns the student-evidence tests, validates all six evidence
categories and the completed engineering note, recomputes and compares the
JSON/SVG evidence, and invokes `scripts/smoke_test_wheel.py`. The wheel smoke
test installs the single wheel under `dist/` with its dependencies in a
temporary venv with no system site-packages, imports it from a neutral working
directory, checks the frozen signatures and representative values, and removes
the temporary environment. Dependency installation may use pip's configured
package index or local cache. Run the smoke script directly only when
diagnosing a wheel-specific failure.

Submit through the LMS:

1. the private GitHub repository URL;
2. the full 40-character commit identifier; and
3. confirmation that `SSUMechE` has active access.

Example (fictional - replace every value):

```text
Repository URL: https://github.com/ssu-example-student/applied-programming-w02-20261234
Full commit ID: 7f3c9a1d5e8b4c2f6a0d9e3b1c7f4a8d2e6b0c5f
SSUMechE access: Active collaborator access confirmed (not Pending)
```

Copy the URL from the main page of your private Week 2 repository. Run
`git rev-parse HEAD` only after the final push, and confirm in the repository
settings that `SSUMechE` has active access rather than a pending invitation.
Do not submit the public template URL, a local folder path, a branch name,
`latest`, a short hash, or an unpushed commit.

The final revision must include the preserved exception and four completed
functions, at least six top-level `test_...` functions in
`tests/test_student_evidence.py`, the engineering note, JSON and SVG artifacts,
the recorded baseline in engineering-note section 0, and the single wheel under
`dist/`.
