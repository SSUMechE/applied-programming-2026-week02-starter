# Week 2 — Functions, Tests, and NumPy Review

## Windows installation correction — 17 September 2026

The corrected environment uses the Week 1 installation route: Conda supplies
Python and pip, then pip installs the pinned course packages. The previous YAML
selected conda-forge builds of NumPy and the test tools. Equal version numbers
do not imply identical binaries. Package versions and the assignment are unchanged.

If installation or import fails, follow [Conda environment repair](#conda-environment-repair).
Keep a working Week 1 environment. Do not delete environments, replace TODO
files, recreate your private repository or disable Windows security.

Use two-dimensional path geometry to review Python, implement reusable
functions, and verify NumPy calculations. You are not implementing a planner,
collision checker, robot controller, or physics simulator this week.

## Required reading order

1. Read `docs/week_02_functions_tests_numpy_reading_v30.pdf`, including its final
   **Assignment 2** section.
2. Follow this `README.md` for the repository commands.
3. Read `PROTECTED_FILES.md` before editing.

The integrated Reading contains the complete Assignment 2 procedure. This
README mirrors its seven steps. It does not replace the explanations or create
an alternative assignment. If the documents disagree, ask before changing a
protected file. Use the same Reading PDF as the copy under `docs/`.

## 1. Create this week's private repository and invite the instructor

Use your GitHub account from Week 1. If you have not created an account, visit
<https://github.com/signup>, complete registration and email verification, and
record your exact username. Never send passwords, tokens, or verification codes.

Open the designated public template:

<https://github.com/SSUMechE/applied-programming-2026-week02-starter>

1. Select **Use this template → Create a new repository**.
2. Select your personal account as owner. Use the name
   `applied-programming-w02-<student-id>`, replacing the bracketed part with your
   own student ID. For example, `applied-programming-w02-20260000` is fictional.
3. Select **Private** and create the repository. Keep Week 1 in its existing,
   separate repository. Do not rename or combine the weekly repositories.
4. In your new repository, open **Settings → Collaborators → Add people**.
   Search for and select the exact account `SSUMechE`, then send the collaborator
   invitation. GitHub may request account authentication before these controls.
5. Check the access state. **Pending invitation** means sent, not accepted.
   Active collaborator access means the instructor can access the private repo.

A URL alone does not grant access, and an invitation notification email is not
proof of acceptance. Continue working while acceptance is pending. A correct
invitation sent on time and awaiting only instructor acceptance is not a
student submission omission. Report the actual state in LMS. Do not claim
active access while it is pending. Follow the LMS contact guidance if access
remains unresolved at the instructor's announced checking time.

The deadline is one week after the corresponding lab class. Use the exact date
and time announced in LMS. The common Week 1 submission rules also apply:

- Follow the required repository name, file structure, and LMS format.
- Missing mandatory submission requirements by the deadline results in zero
  for the assignment. The timely pending-invitation exception above still applies.
- GitHub upload without LMS submission is not recognized as submission.

This submission-format rule does not mean that every failed numerical test
automatically makes the entire assignment zero.

## 2. Clone, prepare the environment, and record the starter baseline

On Windows, open **Anaconda Prompt**, as in Week 1. Replace `YOUR-GITHUB-ID`
and `YOUR-STUDENT-ID` below with your own values. Run the clone command from
the folder where you keep your course repositories, then enter the new folder.

```bat
git --version
git clone https://github.com/YOUR-GITHUB-ID/applied-programming-w02-YOUR-STUDENT-ID.git
cd applied-programming-w02-YOUR-STUDENT-ID
git remote -v
```

Both `origin` URLs must point to your private Week 2 repository, not the public
template. The ZIP is a review/recovery copy without Git history. Merely
extracting it is not the submitted repository. Run all following commands from
the repository root, where `pyproject.toml`, `scripts`, `src`, and `tests` reside.

Reuse the `applied-programming-2026` environment from Week 1:

If it does not exist on this computer, run `conda env create -f environment.yml`
once before activation. If it reports a defaults-channel terms-of-service
error, the following alternative uses only the published conda-forge
channel and the same frozen package versions:

```bat
conda create -n applied-programming-2026 --override-channels -c conda-forge ^
  python=3.12.13 pip=26.2.1
```

In Anaconda Prompt, `^` continues the command on the next line. Review and
confirm conda's package-installation prompt. This does not accept terms for
the unused defaults channels or change your persistent channel configuration.
Skip environment creation entirely if the Week 1 environment already works.
Then activate it and install the Week 2 package:

```bat
conda activate applied-programming-2026
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

If conda is unavailable, reopen Anaconda Prompt and check the Week 1 installation.
If unrelated packages conflict with the protected pins, retain the diagnostic
message and request help. Do not change the published pins.

Expected final verifier line:

```text
[PASS] Week 2 path-geometry environment is ready.
```

This checks the required execution setup, not the correctness of unfinished
calculations. Run the protected Python review and baseline next:

```bat
python -m ap_week02_path.review_data_flow
python scripts/run_baseline.py
```

The review shows tuple/list values, unpacking, indexing, slicing, `zip`, loops,
comprehension, and conversion to `(N, 2)`. It contains no completed TODO bodies.
If diagnosing an import problem, the following optional checks print a file
inside this repository's `src/ap_week02_path` and the module name
`ap_week02_path.path_geometry` respectively:

```bat
python -c "import ap_week02_path; print(ap_week02_path.__file__)"
python -c "from ap_week02_path.path_geometry import segment_length; print(segment_length.__module__)"
```

The unchanged starter baseline is **42 failed, 6 passed**. Its missing function
bodies raise `NotImplementedError`. This is different from an assertion failure
after a function returns a wrong number. `run_baseline.py` succeeds only when
the expected incomplete state is reproduced. Before editing, open the supplied
note and record the summary and first `FAILED` test node ID in section 0:

```bat
notepad artifacts\engineering_note.md
```

Save without changing the `.md` extension. Do not replace an already written
note with a fresh template. An `E` prefix in pytest's failure detail marks an
exception or failed assertion detail. It is not an extra command or test count.

## Conda environment repair

If `python scripts/verify_environment.py` passes in your existing environment,
keep using it. Otherwise, follow these steps in **Anaconda Prompt**, inside
your existing Week 2 repository. This does not replace any student code.

1. Create a separate environment without changing the old one.

   ```bat
   set PYTHONUTF8=1
   conda create -n applied-programming-w02 --override-channels -c conda-forge python=3.12.13 pip=26.2.1
   ```

   Confirm the installation prompt with `y`. If that name already exists,
   do not overwrite it. Activate it and try the following checks instead.
   `PYTHONUTF8` addresses a possible `cp949` decoding error. It does not
   remove an application-control block.

2. Activate it and install the pinned packages using pip, as in Week 1.

   ```bat
   conda activate applied-programming-w02
   python -c "import socket, ssl; print('IMPORTS_OK')"
   python -m pip install -r requirements.txt
   python -m pip install -e . --no-build-isolation
   python scripts/verify_environment.py
   ```

   Stop at the first error. The import check must print `IMPORTS_OK`. The
   verifier must finish with `[PASS] Week 2 path-geometry environment is ready.`
   Do not subsequently run `conda install numpy` in this pip-managed setup.

3. For an untouched starter, run `python scripts/run_baseline.py` and expect
   `42 failed, 6 passed`. If you have changed TODOs, run `python -m pytest -q`
   instead. Do not undo your work to reproduce the starter result.

4. In later command windows, return to this repository and run
   `conda activate applied-programming-w02` before the normal Week 2 commands.
   Artifact generation, wheel building and LMS submission remain unchanged.

These commands also work with the unchanged requirements in an older private
repository. You do not need to edit a protected file, pull the public template,
create another repository or send another invitation. If Windows still reports
that an application-control policy blocked a DLL, stop and send the command
and full error text to the instructor or your managed-PC administrator. Do not
disable antivirus or Smart App Control. Keep passwords and tokens out of logs.

## 3. Complete TODO 1–4 and check each dependency

Only three files are manually editable:

- `src/ap_week02_path/path_geometry.py`: TODO 1–4 and internal helpers.
- `tests/test_student_evidence.py`: your independent tests.
- `artifacts/engineering_note.md`: your written explanations.

A **public function** is imported and called by other code. All four public
functions are completed inside the same module. They are not four extra files
or four GitHub repositories. Preserve the exception and signatures:

| Public object | Input | Output |
|---|---|---|
| `PathInputError` | invalid public input | subclass of `ValueError` |
| `segment_length(start_xy, goal_xy)` | two points `(2,)` | nonnegative Python `float` |
| `interpolate_segment(start_xy, goal_xy, num_samples)` | two points `(2,)`, integer `M` | `float64` array `(M, 2)` |
| `path_length(path_xy)` | path `(N, 2)` | nonnegative Python `float` |
| `path_lengths(paths_xy)` | batch `(B, N, 2)` | `float64` array `(B,)` |

Coordinates and distances use course-defined Cartesian length units. Accept
integer/floating tuples, lists, and native numeric NumPy arrays. Reject Boolean,
complex, string, `dtype=object`, empty, wrong-shaped, and non-finite inputs with
`PathInputError`. Conversion failures must also become `PathInputError`, not a
leaked NumPy `ValueError`. A non-finite computed result is rejected. Do not
silently clip or reshape an invalid input, and do not modify caller-owned input.

Implement in this order, running the matching command after each TODO:

1. **TODO 1 — `segment_length`:** validate both `(2,)` points. Compute Euclidean
   distance. Run:
   `python -m pytest -q tests/test_published_contract.py -k segment_length -x`
2. **TODO 2 — `interpolate_segment`:** require a Python or NumPy integer
   `num_samples >= 2`, excluding Boolean. Use equally spaced fractions from
   `np.linspace(0.0, 1.0, num_samples)`. Preserve the normalized start and goal
   exactly by assigning them to the first and last rows of the new output.
   Run:
   `python -m pytest -q tests/test_published_contract.py -k interpolation -x`
3. **TODO 3 — `path_length`:** require `(N, 2)`, `N >= 2`. Sum consecutive
   segment lengths. Run:
   `python -m pytest -q tests/test_published_contract.py -k "path_length and not path_lengths" -x`
4. **TODO 4 — `path_lengths`:** require `(B, N, 2)`, `B >= 1`, `N >= 2`.
   Return one length per path. Use NumPy array operations, without a Python
   `for`, `while`, or comprehension inside this function. Run:
   `python -m pytest -q tests/test_published_contract.py -k path_lengths -x`

`-k` selects tests by name. `-x` stops at the first failing selected test.
`deselected` counts tests left out by the filter, not passed tests. Read the
first failure's test name, input, expected/actual values or exception, and
source line before changing code. Do not edit protected tests to remove failures.

After all four functions are complete, run the entire published suite:

```bat
python -m pytest -q tests/test_published_contract.py
```

The complete published result is **48 passed**. A focused pass alone does not
establish this checkpoint, and 48 passes are not the entire submission.

## 4. Write and run six independent tests

In `tests/test_student_evidence.py`, write at least six top-level synchronous
`test_...` functions, including one with each required prefix:

- `test_normal_`: one independently chosen normal case.
- `test_boundary_`: a boundary case.
- `test_invalid_`: invalid input and the required exception.
- `test_endpoint_`: interpolation endpoint preservation.
- `test_translation_`: translation does not change length.
- `test_batch_`, `test_ownership_`, `test_no_mutation_`, or `test_scalar_batch_`:
  scalar–batch agreement or unchanged caller input.

Every evidence test calls the public API and contains an assertion or
`pytest.raises`. Normal, translation, and batch/ownership tests use
`np.isclose` or `np.allclose` with explicit `rtol` and `atol`. Explain the chosen
tolerance in the note. Exact equality is appropriate for integer shapes,
Boolean conditions, or an exactly guaranteed invariant such as a copied endpoint
or zero length between identical points.

```bat
python -m pytest -q tests/test_student_evidence.py
python -m pytest -q
```

With exactly six single-case student tests, expect **6 passed** and **54 passed**
respectively. Extra passing tests or parametrized cases may increase the total.
The checker rejects duplicate names, copied published bodies, missing categories,
missing assertions/API calls, missing required explicit tolerances, and any
collected test that fails, skips, or is marked as an expected failure. Inputs
may be created through variables or NumPy operations. Literal tuple/list syntax
is not required. The instructor reviews whether your cases are genuinely
independent and whether they check meaningful behavior.

## 5. Generate outputs, complete the note, and build the wheel

Run the supplied callers from the repository root:

```bat
python -m ap_week02_path.demo
python scripts/generate_artifacts.py
start "" artifacts\path_geometry_preview.svg
```

The two generated files are `artifacts/path_geometry_summary.json` and
`artifacts/path_geometry_preview.svg`. The JSON records returned sample arrays,
shapes, endpoints, and lengths. The SVG is an animated browser preview: markers
follow your interpolated samples through the ordered waypoints. If `start`
does not open a browser, open the `.svg` file with a modern browser manually.
It is not a planner, collision checker, physics simulation, or robot-safety check.

Complete your existing note, not just the generated files:

```bat
notepad artifacts\engineering_note.md
```

Keep each supplied section and `<!-- STUDENT RESPONSE -->` marker. Replace the
placeholder comment below the marker with your own response:

0. the recorded starter summary and first failing test node ID.
1. accepted inputs, invalid inputs, and how your validation enforces the contract.
2. your normal and boundary cases, expected result, length units, and tolerance.
3. scalar–batch comparison, array shapes, result, and tolerance.
4. your translation and no-mutation checks and what defect each would detect.
5. what the SVG displays and what it cannot verify.

Save, close, and check that the saved file contains your writing:

```bat
type artifacts\engineering_note.md
python -m build --wheel --no-isolation
python scripts/check_submission.py
```

The automated checker confirms required responses are present. It has no
arbitrary minimum response length. Empty responses and unchanged placeholder
comments fail. Explanation accuracy remains an instructor review, not something
the checker proves by counting characters.

The checker runs your tests, recomputes JSON/SVG data, and runs the supplied
wheel smoke test. The smoke test installs the single wheel under `dist/` and
its dependencies into a temporary clean venv, imports it from a neutral folder,
and checks signatures and representative values. Package installation may use
pip's configured index or cache. A checker pass is not GitHub or LMS submission.

## 6. Review, stage, commit, push, and compare the revision

Rerun the checks, then inspect the changed source, tests, note, generated files,
and single wheel. Only stage the intended submission files:

```bat
python -m pytest -q
python scripts/check_submission.py
git status --short
git diff
git add src/ap_week02_path/path_geometry.py tests/test_student_evidence.py artifacts dist
git diff --staged --stat
git diff --staged
git commit -m "Complete Week 2 path-geometry package"
git push origin main
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

`git diff` reviews unstaged tracked changes. Open any new/untracked file as well.
`git diff --staged` reviews what the commit will include. A commit saves locally.
Push uploads it. The final short status should be empty. Compare the full
40-character hash from `git rev-parse HEAD` with the first field returned by
`git ls-remote`. They must match. Do not submit an unpushed local revision.

Open your private Week 2 repository on GitHub and check the note and generated
files at the pushed revision. Confirm active `SSUMechE` access or truthfully
record that the correct on-time invitation is still pending. Never commit
credentials, tokens, recovery codes, environment folders, caches, or unrelated
material.

If you change code or tests after verification:

1. Regenerate the affected outputs with the supplied commands.
2. Rebuild the wheel.
3. Run the tests and submission checker again.
4. Inspect, commit, and push the new state, then compare the full commit IDs again.

## 7. Submit the exact revision through LMS

For Week 2, use your private repository named
`applied-programming-w02-<student-id>`. Follow the same GitHub and LMS submission
procedure and common submission rules as in Week 1.

### Completion checklist

- Environment verification passes.
- The untouched starter baseline and first failure are recorded.
- All four TODOs are complete.
- All 48 published tests and at least six student tests pass.
- The JSON summary and SVG preview have been regenerated.
- Sections 0–5 of `engineering_note.md` are answered.
- One wheel passes the clean-installation check.
- The private repository name and `origin` are correct.
- The revision is pushed, and the local and remote full commit IDs match.
- `SSUMechE` has access, or a correct invitation sent by the deadline is awaiting
  acceptance.
- All three required LMS fields are submitted.

Keep every protected file unchanged. Tests, written explanations, packaging,
push, instructor access, and LMS submission remain separate checks.
