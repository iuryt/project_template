# Changelog

All notable changes to this template are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Generated projects can pull changes from newer template versions with `copier update`.

## [Unreleased]

## [0.1.0] - 2026-07-07

### Added

- Initial Copier template for oceanography projects.
- Opinionated layout: `src/<pkg>/` library (`config.py`, `io/` cache-on-first-use,
  `plotting.py`), tiered pipeline (`simulations/` optional → `preprocessing/` → `analysis/`),
  `exploratory/`, `tests/`, `docs/`, `archive/`.
- pixi environment with a task DAG: `setup`, `all`, `check` (ruff + pytest + conda-export
  freshness), and `export-conda`.
- `AGENTS.md` agent/human instructions; generated `CLAUDE.md` importing it; `.agents/skills/`
  (`data-io-analysis`, `mapping-viz`, `ocean-physics`, `model-obs-workflows`) symlinked into
  `.claude/` and `.codex/`.
- GitHub Actions CI in generated projects; ruff config; MIT license.
- Questionnaire: `project_name`, `package_name`, author, `description`, `python_version`,
  `license`, `include_simulations`, `data_storage` (local/external), `data_path`.
