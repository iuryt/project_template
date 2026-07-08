"""Tests for the Copier template itself: generate projects and assert on the output.

Generation uses the committed template (``vcs_ref="HEAD"``), so commit your changes before
running ``pixi run test`` locally.
"""

from pathlib import Path

import copier
import pytest

TEMPLATE = Path(__file__).resolve().parents[1]


def generate(dst, **data):
    copier.run_copy(
        str(TEMPLATE),
        str(dst),
        data={"project_name": "Test Proj", **data},
        defaults=True,
        unsafe=True,
        vcs_ref="HEAD",
        quiet=True,
    )


def test_default_layout(tmp_path):
    dst = tmp_path / "proj"
    generate(dst)
    for rel in [
        "pyproject.toml",
        "AGENTS.md",
        "README.md",
        "LICENSE",
        ".copier-answers.yml",
        "src/test_proj/config.py",
        "src/test_proj/io/__init__.py",
        "src/test_proj/data/README.md",
        "preprocessing/00_preprocess.py",
        "analysis/make_results.py",
        "tests/test_dynamics.py",
        ".github/workflows/ci.yml",
    ]:
        assert (dst / rel).is_file(), f"missing {rel}"


def test_template_only_files_do_not_leak(tmp_path):
    dst = tmp_path / "proj"
    generate(dst)
    for name in ["CITATION.cff", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "CHANGELOG.md",
                 "TEMPLATE.md", "copier.yml"]:
        assert not (dst / name).exists(), f"{name} leaked into generated project"


def test_no_unrendered_jinja(tmp_path):
    dst = tmp_path / "proj"
    generate(dst)
    for p in dst.rglob("*"):
        if p.is_file():
            text = p.read_text(errors="ignore")
            assert "{{" not in text and "{%" not in text, f"unrendered jinja in {p}"


def test_simulations_included_when_flagged(tmp_path):
    dst = tmp_path / "proj"
    generate(dst, include_simulations=True)
    assert (dst / "simulations/00_run.py").is_file()
    assert "simulate" in (dst / "pyproject.toml").read_text()


def test_simulations_absent_by_default(tmp_path):
    dst = tmp_path / "proj"
    generate(dst)
    assert not (dst / "simulations").exists()
    assert "simulate" not in (dst / "pyproject.toml").read_text()


def test_external_data_uses_symlink_task(tmp_path):
    dst = tmp_path / "proj"
    generate(dst, data_storage="external", data_path="/tmp/store")
    pyproject = (dst / "pyproject.toml").read_text()
    assert "ln -sfn" in pyproject
    assert "/tmp/store" in pyproject


def test_local_data_uses_mkdir_task(tmp_path):
    dst = tmp_path / "proj"
    generate(dst)
    pyproject = (dst / "pyproject.toml").read_text()
    assert "mkdir -p data/raw data/external data/processed" in pyproject


def test_gitignore_keeps_figures_ignores_data(tmp_path):
    dst = tmp_path / "proj"
    generate(dst)
    gi = (dst / ".gitignore").read_text()
    assert "CLAUDE.md" in gi
    assert "/data" in gi
    assert "**/frames/" in gi
    # figures/ is committed, so it must NOT be ignored
    assert "\n/figures" not in gi


def test_package_data_dir_not_gitignored(tmp_path):
    """The root `/data` ignore must not swallow src/<pkg>/data/ package data."""
    dst = tmp_path / "proj"
    generate(dst)
    gi_lines = (dst / ".gitignore").read_text().splitlines()
    assert "/data" in gi_lines  # anchored
    assert "data" not in gi_lines  # never the unanchored form


@pytest.mark.parametrize("bad", ["123bad", "bad-name", "Bad", "bad name", "bad!", ""])
def test_invalid_package_name_rejected(tmp_path, bad):
    dst = tmp_path / "proj"
    with pytest.raises(Exception):
        generate(dst, package_name=bad)
