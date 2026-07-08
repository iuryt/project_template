"""Central configuration -- every path in the project lives here.

No script should ever call ``os.chdir`` or hardcode ``'../data/...'``. Import the
constants below instead. Relocate the data root without touching code by setting
the ``PROJECT_DATA`` environment variable (handy on HPC / shared storage).
"""

import os
from pathlib import Path

# src/<pkg>/config.py -> parents[2] is the repo root.
PROJ_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = Path(os.environ.get("PROJECT_DATA", PROJ_ROOT / "data"))
RAW = DATA_DIR / "raw"  # original immutable inputs (obs AND simulation output)
EXTERNAL = DATA_DIR / "external"  # third-party reference data (bathymetry, static fields...)
PROCESSED = DATA_DIR / "processed"  # analysis-ready datasets (+ result tables)

FIGURES = PROJ_ROOT / "figures"  # rendered figures (committed deliverables)
