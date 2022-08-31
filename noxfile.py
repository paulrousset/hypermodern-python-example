""" Nox sessions"""
import tempfile
from typing import Any

import nox
from nox.sessions import Session


nox.options.sessions = "lint", "safety", "tests"


@nox.session(python=["3.10", "3.9"])
def tests(session: Session) -> None:
    """Run the test suite"""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session,
                             "coverage[toml]",
                             "pytest",
                             "pytest-cov",
                             "pytest-mock")
    session.run("pytest", *args)


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.10", "3.9"])
def lint(session: Session) -> None:
    """Lint using flake8"""
    args = session.posargs or locations
    # session.install(
    #     "flake8",
    #     "flake8-bandit",
    #     "flake8-black",
    #     "flake8-bugbear",
    #     "flake8-import-order",
    # )
    install_with_constraints(
        session,
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


@nox.session(python="3.10")
def black(session: Session) -> None:
    """Run Black code formatter"""
    args = session.posargs or locations
    # session.install("black")
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.10")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages"""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        # session.install("safety")
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lockfile"""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)