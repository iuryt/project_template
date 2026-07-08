# project_template

A [Copier](https://copier.readthedocs.io/) template for **oceanography** projects — an
opinionated, reproducible Python layout with a pixi environment, a code-lifecycle workflow
(prototype → library → pipeline), agent instructions (`AGENTS.md`), and lab skills.

## Generate a project

Copier is a scaffolding tool, not a project dependency. Run it with pixi (no install needed):

```bash
pixi exec copier copy gh:iuryt/project_template my_new_project
```

(Or `pixi global install copier` to keep it on your PATH.)

Then bootstrap it:

```bash
cd my_new_project
pixi install
pixi run setup          # CLAUDE.md, skill symlinks, data/ dirs
pixi run export-conda   # environment.yml for conda users
git init && git add -A && git commit -m "Initial commit from project_template"
pixi run check          # ruff + pytest + conda-export freshness
pixi run all            # toy pipeline runs green out of the box
```

Publish it to GitHub (the CLI creates the remote and pushes — don't pre-initialize it on
the website, since the generated files already include a README/LICENSE/`.gitignore`):

```bash
gh repo create my_new_project --public --source=. --remote=origin --push
# use --private instead of --public to start private
```

## Pull template improvements later

Generated projects record their answers in `.copier-answers.yml`, so you can re-apply
template updates:

```bash
pixi exec copier update
```

## What you get

- **`src/<pkg>/`** library (with `config.py`, `io/` cache-on-first-use, `plotting.py`).
- **Tiered pipeline** (`simulations/` optional → `preprocessing/` → `analysis/`) driven by a
  pixi task DAG; `exploratory/` for scratch `# %%` scripts.
- **`AGENTS.md`** canonical agent/human instructions; **`CLAUDE.md`** is generated
  (gitignored) and just imports it. Codex reads `AGENTS.md` natively.
- **`.agents/skills/`** (tool-neutral) symlinked into `.claude/skills` and `.codex/skills`:
  `data-io-analysis`, `mapping-viz`, `ocean-physics`, `model-obs-workflows`.
- **ruff** (lint+format), **pytest**, and a **CI** workflow running `pixi run check`.
- **pixi** as the source of truth; `environment.yml` generated for conda users.

## Questions asked at generation

`project_name` · `package_name` · `author_name` · `author_email` · `description` ·
`python_version` · `license` · `include_simulations` · `data_storage` (local/external) ·
`data_path`.

## Requirements

[pixi](https://pixi.sh) and [Copier](https://copier.readthedocs.io) (run via `pixi exec`).

## Citing

If you use this template in your work, please cite it. Metadata lives in
[`CITATION.cff`](CITATION.cff) (GitHub shows a "Cite this repository" button from it).

Once the repo is archived on [Zenodo](https://zenodo.org) (connect the GitHub repo, then cut
a release to mint a DOI), add the concept DOI to `CITATION.cff` and drop the badge here:

```
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

> Zenodo's GitHub integration archives **public** repositories on release; for a private repo
> you'd upload to Zenodo manually.
