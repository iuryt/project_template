"""Low-level fetchers shared by the source modules (HTTP, S3, OpenDAP, THREDDS...).

Keep the transport/credentials plumbing here; keep the per-source query logic and
caching in the individual source modules (see ``example_source.py``).
"""

import numpy as np
import xarray as xr


def fetch_example(n):
    """Stand-in for a real network fetch -- returns a small synthetic dataset."""
    x = np.linspace(0, 1, n)
    return xr.Dataset({"value": ("x", np.sin(2 * np.pi * x))}, coords={"x": x})
