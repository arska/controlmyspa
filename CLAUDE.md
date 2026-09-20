# controlmyspa

Python client for the Balboa ControlMySpa cloud API. Single module,
`controlmyspa.py`, published to PyPI on a git tag via trusted publishing.

## Commands

```bash
uvx nox                          # everything: tests on 3.11-3.14, ruff, pylint, coverage
uvx nox -s tests-3.14            # one Python version
uvx nox -s ruff -s pylint        # linters only
```

Linters and coverage run on the latest Python only. `ruff format` must be clean
or CI fails.

## The checkout directory must be named `controlmyspa`

`uvx nox` fails in any checkout whose directory has a different name. This bites
git worktrees, which get generated names like `modular-launching-gosling`.

Symptoms, neither of which points at the real cause:

- about 40 pytest collection errors, all
  `ModuleNotFoundError: No module named 'controlmyspa.controlmyspa';
  'controlmyspa' is not a package`
- ruff `N999 Invalid module name`

Cause: `pyproject.toml` sets `[tool.setuptools.package-dir] controlmyspa = "."`,
so the package is the repository root. With both a root `__init__.py` and
`tests/__init__.py` present, pytest walks up past both and derives the test
module's import path from the directory name on disk.

To verify a change from a worktree, copy the tree to a correctly named directory
and run there:

```bash
mkdir -p /tmp/verify/controlmyspa
tar --exclude=.nox --exclude=__pycache__ -cf - . | (cd /tmp/verify/controlmyspa && tar -xf -)
cd /tmp/verify/controlmyspa && uvx nox
```

Copy the `.git` entry along with everything else. In a worktree it is a file
holding an absolute path, so setuptools_scm still resolves the version from it.

## Releases

Tags are bare semver, no `v` prefix: `4.2.0`. setuptools_scm derives the version
from the tag with `python-simplified-semver`, so there is no version field in
`pyproject.toml` to edit. Pushing a tag builds, publishes to TestPyPI and PyPI,
and signs the artifacts with Sigstore.

Check PyPI before picking a number. Version numbers here have been consumed by
an earlier merge more than once, and a tag that collides with a published
release cannot be reused.

After publishing, verify the artifact rather than trusting a green workflow:

```bash
uv pip install --refresh --no-cache controlmyspa==<version>
```

`--refresh` is needed on top of `--no-cache`, and PyPI's JSON endpoint serves a
stale `info.version` for a while after upload. The simple index
(`https://pypi.org/simple/controlmyspa/`) updates first.

## Conventions

- Private helpers carry the HTTP plumbing: `_send` makes one authenticated
  request, `_request` retries it once after a fresh login on a 401, and
  `_get_json` and `_post_json` wrap `_request`. New API calls go through these
  rather than calling `requests` directly.
- `_do_login` is the deliberate exception. It is the one call with no token to
  attach, so it stays a raw `requests.post`.
- Properties read `self._info`, which `refresh()` populates. They do not fetch.
  A caller holding a long-lived client calls `refresh()` when it wants new data.
- `pyproject.toml` lists `requests.codes.ok` under pylint `generated-members`.
  Prefer `http.HTTPStatus` constants for other status codes; pylint rejects
  `requests.codes.<name>` with E1101.
