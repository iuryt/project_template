---
name: data-io-analysis
description: Loading, chunking, and analyzing large gridded ocean datasets with xarray, dask, and netCDF/zarr. Use when reading/writing model or observational data, working with lazy/out-of-core arrays, resampling, or combining datasets.
---

# Data I/O & analysis (xarray · dask · netCDF/zarr)

## Core habits
- **Prefer `xarray` whenever possible — for the *math*, not just loading.** Do calculations
  with xarray's label-aware methods instead of pulling `.values` into numpy: `.differentiate`,
  `.integrate`, `.cumulative_integrate`, `.cumsum`, `.rolling` (+ `.construct`), `.coarsen`,
  `.interp`/`.interp_like`, `.resample`, `.groupby`, `.weighted(...).mean()`, `.polyfit`.
  They operate along *named* dims, carry coords/units through, and stay lazy over dask.
  Drop to bare `numpy` only for small, local, hot-loop numerics.
- **Spectral analysis: use `xrft`.** For FFTs, power spectra, cross-spectra, and coherence,
  use `xrft` (`xrft.power_spectrum`, `xrft.cross_spectrum`) — it keeps xarray dims/coords,
  returns proper frequency/wavenumber coordinates, and handles detrending/windowing. Don't
  hand-roll `np.fft` with manual frequency bookkeeping.
  - **Always verify Parseval's theorem holds.** The variance in physical space must equal
    the integral of the spectrum over frequency/wavenumber:
    `var(f) ≈ ∫ PSD df`. Check it numerically (e.g. `float(da.var())` vs
    `xrft.power_spectrum(da, ...).integrate(<freq dims>)`) — a mismatch means a windowing,
    detrending, or normalization mistake. Use `window_correction=True` when windowing so
    the spectrum stays variance-preserving.
- **Label everything.** Use `xarray` with named dims/coords (`time`, `lat`, `lon`, `depth`);
  never index by bare position. Attach `units` and `long_name` attrs — figures and
  downstream checks depend on them.
- **Open lazily.** `xr.open_dataset(path, chunks={...})` or `xr.open_mfdataset(glob,
  chunks=..., parallel=True)` for multi-file. Compute only at the end (`.compute()` /
  `.load()`), not in the middle.
- **Chunk along the axis you *don't* reduce over.** Chunk time for a spatial-mean-over-time;
  chunk space for per-gridpoint time series. Aim for ~100 MB chunks.

## Formats & stores
- **netCDF** for interchange and archival single files.
- **zarr** for large, cloud/parallel-write workloads and appendable stores
  (`ds.to_zarr(store, mode="w")`, region writes for parallel pipelines).
- Prefer `engine="h5netcdf"` for speed when available.
- **`arraylake` (Earthmover)** — optional managed catalog, **mostly for reading** shared,
  versioned datasets across the lab: open a repo and read xarray as usual. The `io/` cache
  pattern still applies.
- **`icechunk`** — the underlying versioned Zarr store (git-like commits/branches). Use it to
  **store data locally or on AWS S3** without the arraylake catalog: a `local_filesystem`
  storage for on-disk repos, or `s3_storage` for the cloud. Prefer this for produced datasets
  that benefit from versioning/appends over loose `.zarr` dirs. Add deliberately
  (`pixi add arraylake icechunk`); S3/Earthmover use needs credentials.

## dask
- Start with the threaded scheduler; reach for `distributed.Client()` only when you need
  a dashboard or multi-node. On HPC use `dask-jobqueue` (SLURM).
- Watch for accidental `.values` / `.item()` that trigger eager compute inside loops.

## Project fit
- Put all reads behind `src/<pkg>/io/` (cache-on-first-use). Preprocessing writes to
  `data/processed/`; analysis reads from it. Never re-download in an analysis script.
- Reach for `flox` for fast groupby/resample over dask arrays.
