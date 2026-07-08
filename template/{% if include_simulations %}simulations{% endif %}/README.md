# simulations/

**Tier 1 source.** Scripts here run models and write raw output to `data/raw/`.
Numeric prefixes (`00_`, `01_`, ...) are a human signpost for order; the executable
order lives in `pyproject.toml` (`pixi run simulate`).

| Script         | Consumes | Produces                     |
| -------------- | -------- | ---------------------------- |
| `00_run.py`    | (none)   | `data/raw/model_output.nc`   |
