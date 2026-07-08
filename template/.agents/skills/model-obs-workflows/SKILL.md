---
name: model-obs-workflows
description: Working with ocean model output (ROMS, MITgcm, MOM6, NEMO) and observations (Argo, satellite altimetry/SST), plus regridding for model–obs comparison. Use when reading model grids, colocating obs with model, or interpolating between grids.
---

# Model & observation workflows

## Model output
- **Respect the native grid.** Ocean models use staggered (Arakawa C) grids — u, v, and
  tracer points differ. Don't naively `np.gradient`; use **`xgcm`** `Grid` objects with the
  model's metrics for derivatives, interpolation, and integrals.
- Loaders/conventions:
  - **MITgcm** → `xmitgcm.open_mdsdataset` (or use its xgcm grid).
  - **MOM6 / NEMO** → CF/SGRID-ish; open with xarray, build the xgcm grid from the
    coordinate/metric variables.
  - **ROMS** → `xroms` for grid handling and common diagnostics.
- Vertical coords are often terrain-following (σ) or hybrid — convert to depth explicitly;
  never assume a fixed z-level.
- Open lazily with `open_mfdataset` + sensible chunks (see `data-io-analysis`).

## Observations
- **Argo:** use `argopy` to fetch/cache profiles; convert to TEOS-10 (see `ocean-physics`);
  mind QC flags and pressure levels; grid to standard depths before compositing.
- **Satellite altimetry (SSH/geostrophy), SST, ocean color:** gridded L3/L4 products open
  directly with xarray; watch fill values, `scale_factor`/`add_offset`, and time encoding.

### Data-access packages (put these behind `src/<pkg>/io/`)
- **`earthaccess`** — NASA Earthdata: authenticated search + stream/download (SWOT, PACE,
  MODIS, SMAP, GHRSST, ECCO...). `earthaccess.login()`, `search_data(...)`, then
  `open()`/`download()`; prefer streaming (`xr.open_mfdataset(earthaccess.open(results))`)
  over full downloads when on the cloud.
- **`copernicusmarine`** — Copernicus Marine (CMEMS) products: SSH/altimetry, SST, physics
  & biogeochemistry reanalyses/forecasts. Use `copernicusmarine.open_dataset(dataset_id,
  variables=..., minimum/maximum_longitude=..., start/end_datetime=...)` to lazily subset
  server-side instead of downloading whole datasets. Needs CMEMS credentials.
- Keep every fetch behind `src/<pkg>/io/` with cache-on-first-use so obs are pulled once and
  credentials/subsetting logic live in one place.

## Regridding & model–obs comparison
- **Structured → structured:** `xesmf` (`Regridder`, methods `bilinear`, `conservative`,
  `nearest_s2d`). Use **conservative** for fluxes/budgets, **bilinear** for smooth fields.
  Build the regridder once, reuse it; save weights for expensive grids.
- **Colocation (model at obs points):** `xarray` advanced/vectorized `.interp` or
  `.sel(..., method="nearest")` along track; for unstructured obs, interpolate in
  (time, lat, lon, depth) with matching coordinate conventions.
- **Compare like with like:** same units, same reference level, same land mask, same
  temporal averaging before differencing. Regrid the *finer* onto the *coarser* grid for
  fair statistics; report the direction you chose.
- `xesmf` is heavy (ESMF/esmpy) and not a default dependency — add it deliberately with
  `pixi add xesmf` when a project needs regridding.

## Geospatial: pick the right tool (they are NOT interchangeable)
- **`xesmf`** — regrid between *model grids* (structured/curvilinear lon–lat). Flux-aware,
  works in lon/lat, no CRS. Use for model↔model / model↔obs grid transfer.
- **`rioxarray`** — xarray + rasterio/GDAL for *GIS rasters* (GeoTIFF/COG). CRS-aware:
  `.rio.reproject(epsg)`, `.rio.clip(geometries)`, `.rio.write_crs(...)`. Use for
  bathymetry/coastline rasters, satellite scenes, anything with an EPSG/affine transform.
- **`geopandas`** — *vector* data: points/lines/polygons with a CRS. Use for station
  locations, transects, basin/MPA/region polygons, coastlines-as-geometry; spatial joins
  (`gpd.sjoin`), and **building region masks** to subset gridded fields (e.g. rasterize
  polygons with `regionmask`, or `.rio.clip` a raster by a GeoDataFrame). Read/write
  shapefiles and GeoPackage. Keep CRS explicit and consistent (`.to_crs(...)`).
