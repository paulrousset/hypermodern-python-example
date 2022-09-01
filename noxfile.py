""" Nox sessions"""

import nox
from nox.sessions import Session
import nox_poetry

package = "hypermodern_python_example"

nox.options.sessions = "lint", "safety", "tests"

locations = "src", "tests", "noxfile.py", "docs/conf.py"


@nox_poetry.session(python=["3.10", "3.9"])
def tests(session: Session) -> None:
    """Run the test suite"""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("coverage[toml]", "pytest", "pytest-cov", "pytest-mock", ".")
    session.run("pytest", *args)


@nox_poetry.session(python=["3.10", "3.9"])
def lint(session: Session) -> None:
    """Lint using flake8"""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox_poetry.session(python=["3.10"])
def black(session: Session) -> None:
    """Run Black code formatter"""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox_poetry.session(python=["3.10"])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages"""
    session.install("safety")
    session.run("safety", "check", "--full-report")


@nox_poetry.session(python=["3.10", "3.9"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox_poetry.session(python=["3.10"])
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")


@nox_poetry.session(python="3.10")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
