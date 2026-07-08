# preprocessing/

**Tier 1.** Ordered, expensive steps that turn `data/raw/` (+ `data/external/`) into
analysis-ready `data/processed/`. Numeric prefixes are a human signpost; the real run
order lives in `pyproject.toml` (`pixi run preprocess`, or `pixi run all`).

| Script              | Consumes                       | Produces                    |
| ------------------- | ------------------------------ | --------------------------- |
| `00_preprocess.py`  | `data/raw/model_output.nc`\*   | `data/processed/example.nc` |

\* Falls back to a synthesized field if no raw input exists yet, so the stage is
runnable on a fresh project.
