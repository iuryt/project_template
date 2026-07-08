# Contributing

Thanks for your interest in improving **project_template** — a Copier template for
oceanography projects.

## Repo layout

- `template/` — the files that get generated into a new project (Jinja-templated).
- `copier.yml` — the questionnaire and Copier config.
- Root `README.md`, `LICENSE`, `CITATION.cff` — the template repo's own metadata (never
  copied into generated projects).

## Proposing a change

1. Open an issue describing the change (or comment on an existing one) before large work.
2. Branch off `main`, make your change under `template/` (or `copier.yml`).
3. **Test generation locally** (see below) — a broken template helps no one.
4. **Update `CHANGELOG.md`** under `[Unreleased]` — every change that ships (i.e. every push
   to `main` / merged PR) should leave a changelog entry so `copier update` users can see
   what changed.
5. Open a PR. CI (`template-ci`) generates a project and runs its checks; it must pass.

## Testing the template locally

Generate a throwaway project and run its checks:

```bash
pixi exec copier copy --defaults -d project_name="Scratch" --vcs-ref=HEAD . /tmp/scratch
cd /tmp/scratch
pixi install
pixi run setup
pixi run export-conda
git init && git add -A && git commit -m init
pixi run check   # ruff + pytest + conda-export freshness
pixi run all     # toy pipeline must go green
```

Test both branches of the conditionals when relevant:

```bash
# simulations + external data storage
pixi exec copier copy --defaults -d project_name="Scratch2" \
  -d include_simulations=true -d data_storage=external -d data_path=/tmp/store \
  --vcs-ref=HEAD . /tmp/scratch2
```

## Style

The generated projects use `ruff`. Keep template Python (in `template/`) formatted so a
freshly generated project passes `pixi run format-check` out of the box.

## Code of conduct

By participating you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
