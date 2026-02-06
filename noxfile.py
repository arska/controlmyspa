import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.install("-e", ".", "pytest", "pytest-cov", "responses")
    session.run("pytest", "--cov", "--ignore", ".nox")


@nox.session(python="3.14")
def ruff(session):
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(python="3.14")
def pylint(session):
    session.install(".", "pylint")
    session.run("pylint", "controlmyspa")


@nox.session
def report(session):
    session.install("coverage")
    session.run("coverage", "report", "--omit", ".nox/*")
    session.run("coverage", "html", "--omit", ".nox/*")
