"""Example external source with cache-on-first-use.

Copy this module per real source. The pattern: check the cache under
``data/external`` and reuse it; otherwise download, cache, and return.
"""

import xarray as xr

from ..config import EXTERNAL
from .download import fetch_example


def example_source(*, n=64, force=False):
    """Return the dataset, caching it under ``data/external`` on first call.

    Parameters
    ----------
    n : int
        Toy query parameter (grid size).
    force : bool
        Ignore the cache and re-download.
    """
    path = EXTERNAL / f"example_source_n{n}.nc"
    if path.exists() and not force:
        return xr.open_dataset(path)

    ds = fetch_example(n)
    path.parent.mkdir(parents=True, exist_ok=True)
    ds.to_netcdf(path)
    return ds
