#!/usr/bin/env python3
"""Automated repository checks for the Midterm Project: Whiteboard Writing.

Run with: pytest test_midterm.py -v

These checks inspect the README, ROS 2 package, Python syntax, and tracked build output.
Course staff grade the writeup and the code from the Gradescope PDF, and the
whiteboard run at the lab station.
"""

from __future__ import annotations

import ast
import subprocess
import warnings
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent

WORKSPACE_SRC = Path("ros2_ws/src")
README_STARTER_FINGERPRINTS = ("Update this README", "[Your Name]")
IGNORED_PARTS = {"build", "install", "log", ".git", "__pycache__"}
NOT_STUDENT_CODE = {"setup.py"}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _files_under(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return [
        path for path in root.rglob("*")
        if path.is_file() and not (set(path.relative_to(root).parts) & IGNORED_PARTS)
    ]


def find_packages(repo: Path) -> list[Path]:
    """Packages under ros2_ws/src, found by their package.xml."""
    src = repo / WORKSPACE_SRC
    packages = []
    for manifest in sorted(src.rglob("package.xml")) if src.is_dir() else []:
        package = manifest.parent
        if set(package.relative_to(repo).parts) & IGNORED_PARTS:
            continue
        packages.append(package)
    return packages


def _student_python(package: Path) -> list[Path]:
    """Non-empty Python files in a package, without setup.py and the test/ folder
    that ros2 pkg create generates."""
    return [
        path for path in _files_under(package)
        if path.suffix == ".py"
        and path.name not in NOT_STUDENT_CODE
        and "test" not in path.relative_to(package).parts[:-1]
        and _read_text(path).strip()
    ]


def check_package(repo: Path) -> list[str]:
    packages = find_packages(repo)
    if not packages:
        return [
            "Add your ROS 2 package under ros2_ws/src/, as in Lab 6: a folder with "
            "package.xml and your Python code (for example "
            "ros2_ws/src/midterm_writer/midterm_writer/write_initials.py)."
        ]

    errors: list[str] = []
    defines_function = False
    found_python = False
    for package in packages:
        for source in _student_python(package):
            found_python = True
            name = source.relative_to(repo).as_posix()
            try:
                tree = ast.parse(_read_text(source), filename=name)
            except SyntaxError as exc:
                errors.append(
                    f"{name} has a Python syntax error on line {exc.lineno}: {exc.msg}. "
                    "Fix it, then run the file again."
                )
                continue
            if any(
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                for node in ast.walk(tree)
            ):
                defines_function = True

    if not found_python:
        names = ", ".join(package.relative_to(repo).as_posix() for package in packages)
        errors.append(
            f"No Python code found in {names}. Add the script that writes your initials "
            "to the package."
        )
    elif not defines_function and not errors:
        errors.append(
            "Your Python code defines no functions. The handout asks for at least one "
            "function; move a repeated piece of your program, such as drawing one "
            "stroke, into a function."
        )
    return errors


def check_required_files(repo: Path) -> list[str]:
    errors: list[str] = []

    readme = repo / "README.md"
    if not readme.is_file():
        errors.append("Add the missing required file: README.md")
    else:
        leftovers = [m for m in README_STARTER_FINGERPRINTS if m in _read_text(readme)]
        if leftovers:
            errors.append(
                "README.md still contains starter text: "
                + ", ".join(f"'{marker}'" for marker in leftovers)
                + ". Replace it with your name, NetID, and a 1-3 line summary."
            )

    errors.extend(check_package(repo))
    return errors


def check_repository_hygiene(repo: Path) -> list[str]:
    if not (repo / ".git").exists():
        return [
            "Run pytest from the root of your cloned repository. "
            "The grader could not find its .git directory."
        ]

    result = _run_git(repo, "ls-files")
    if result.returncode != 0:
        return [
            "The grader could not inspect tracked files with 'git ls-files'. "
            "Run 'git status' and resolve the reported Git problem first."
        ]

    forbidden_directories = {"build", "install", "log"}
    tracked = [Path(line) for line in result.stdout.splitlines() if line]
    prohibited = [
        path.as_posix()
        for path in tracked
        if ({part.casefold() for part in path.parts[:-1]} & forbidden_directories)
    ]
    if prohibited:
        shown = prohibited[:8]
        remainder = len(prohibited) - len(shown)
        summary = ", ".join(shown)
        if remainder:
            summary += f", and {remainder} more"
        return [
            "Remove generated build/, install/, and log/ files from Git tracking, "
            "then commit and push again. The files may remain on your VM if .gitignore "
            f"excludes them. Tracked generated files: {summary}"
        ]
    return []


def _assert_no_errors(errors: list[str]) -> None:
    assert not errors, "\n- " + "\n- ".join(errors)


def test_repository_evidence() -> None:
    _assert_no_errors(check_required_files(REPO_ROOT))
    for notice in check_repository_hygiene(REPO_ROOT):
        warnings.warn("No points lost: " + notice)
