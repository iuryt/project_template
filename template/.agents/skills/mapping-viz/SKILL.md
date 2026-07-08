---
name: mapping-viz
description: Publication-quality oceanographic figures — maps, sections, and Hovmöller plots with matplotlib + cartopy. Use when plotting geospatial fields, choosing projections/colormaps, adding coastlines/land, or building multi-panel figures.
---

# Mapping & visualization (matplotlib · cartopy)

## Maps
- Build axes with a projection: `plt.axes(projection=ccrs.PlateCarree())` (or `Robinson`,
  `Mercator`, `NorthPolarStereo` for high latitudes). Always pass
  `transform=ccrs.PlateCarree()` to `pcolormesh`/`contourf` when data is on a lon/lat grid.
- Add context: `ax.coastlines()`, `ax.add_feature(cfeature.LAND, zorder=...)`,
  `ax.gridlines(draw_labels=True)`. Set extent with `ax.set_extent([w, e, s, n])`.
- Use `pcolormesh` (not `contourf`) for raw gridded fields — it shows real resolution and
  doesn't invent smooth contours.
- **Scale bar.** When the projection is *not* metric (e.g. `PlateCarree`, degrees), add a
  scale bar so readers can judge distance — don't make them mentally convert degrees to km
  (which varies with latitude anyway). Draw one from a great-circle distance at the map's
  center latitude, or use `cartopy` + a small helper / `matplotlib_scalebar`.
- **Basemap tiles.** For context, add imagery from a tile source —
  `cartopy.io.img_tiles.GoogleTiles(style="satellite")` or `style="street"` (or
  `Stamen`/`QuadtreeTiles`) via `ax.add_image(tiles, zoom)`. Pick a zoom matched to extent;
  cache tiles to avoid re-fetching (respect usage terms).
- **Locator inset.** Add a small **orthographic globe** inset that marks where the map sits
  in the world — a second `inset_axes` with `projection=ccrs.Orthographic(lon0, lat0)`,
  coastlines/land, and the main extent drawn as a red box/point. Orients the reader instantly.

## Fields: limits, masking, overlays
- **Robust color limits.** Set `vmin`/`vmax` from robust percentiles (2–98) rather than
  min/max, so a few outliers don't wash out the field (`da.plot(robust=True)`, or
  `np.nanpercentile(data, [2, 98])`). Reuse the same limits across panels/figures of one
  variable (see Multi-panel & comparison).
- **Mask land / NaNs explicitly.** Mask invalid data (`.where(mask)`) and set the bad color
  (`cmap = cmap.copy(); cmap.set_bad("0.8")`) so missing data reads as a deliberate neutral,
  not colormap zero. Draw land on top (`cfeature.LAND`, high `zorder`) where appropriate.
- **Contour overlays** add dynamical context cheaply: isobaths, SSH, or isotherms over a
  `pcolormesh`. Label them with `ax.clabel(cs, ...)`; keep line colors neutral (black/gray).
- **Dateline / longitude convention.** Decide 0–360 vs −180–180 up front and convert
  consistently. For global fields on `PlateCarree`, use
  `cartopy.util.add_cyclic_point` to close the seam at the wrap so there's no white stripe.

## Vector fields
- Currents/wind/stress: `quiver` (or `streamplot` for flow topology). **Subsample** to avoid
  a hairball — plot every *n*-th point (`u[::n, ::n]`) or regrid to a coarser display grid.
- **Always add a reference key** with `ax.quiverkey(q, X, Y, U, "U m s$^{-1}$")` so arrow
  length has a quantitative meaning. Pass `transform=ccrs.PlateCarree()` on map axes.
- For fields varying over orders of magnitude, color arrows by magnitude and keep a fixed
  arrow length, rather than letting length span the full range.

## Colormaps (get this right)
- **Sequential** (magnitude, e.g. speed, chlorophyll): `viridis`, `cmocean.cm.speed`.
- **Diverging** (anomalies, u/v, w — data with a meaningful zero): `RdBu_r`, `cmocean.cm.balance`;
  **center the norm** (`TwoSlopeNorm(vcenter=0)`) so zero maps to the neutral color.
- Domain colormaps: `cmocean` (`thermal`, `haline`, `deep`, `dense`) — perceptually uniform
  and made for ocean variables. Never use `jet`.

## Sections & Hovmöller
- Vertical sections: depth on y (inverted, `ax.invert_yaxis()`), distance/lat on x.
- Hovmöller: time on one axis, space on the other — great for propagation/variability.

## Multi-panel & comparison
- **Share color limits across panels/figures** of the same variable. Fix `vmin`/`vmax`
  (or a shared `norm`) once and reuse everywhere — panels and separate figures are only
  comparable if the colorscale is identical. Pick limits from robust percentiles (2–98)
  of the *combined* data, not per-panel.
- **Combine colorbars** when panels share a scale: draw one colorbar for the group
  (`fig.colorbar(mappable, ax=axes)`) instead of one per panel — less clutter, and it makes
  the shared scale explicit.
- **Drop redundant tick labels** on shared axes: with `sharex=True`/`sharey=True` (or
  `label_outer()`), keep tick labels only on the outer/left-bottom axes. Keep the *ticks*,
  drop the *labels*.
- Match figure size, font sizes, and DPI across a figure set so panels sit together cleanly.
- **Panel labels** for papers: don't hardcode a style — journals differ (`A B C`, `a) b) c)`,
  `(a) (b) (c)`). Put a `label_panels(axes, style=...)` helper in `src/<pkg>/plotting.py`
  that takes the format (case + delimiter) as a parameter, so switching journals is a
  one-line change, not a find-and-replace across scripts.

## Project fit
- Keep reusable styling/savers in `src/<pkg>/plotting.py`; analysis scripts call
  `savefig(fig, FIGURES / "name.png")`. Save vector (`.pdf`/`.svg`) for papers, `.png` for
  quick looks. Use `constrained_layout=True` for multi-panel.
- **`figures/` is committed** — figures are deliverables and reviewers should see them change.
- **Animations: always write frames to `figures/frames/<context>/`.** A project usually has
  several animations, so give each its own **context subfolder** under `frames/`
  (`figures/frames/coastal_eddies/`, `figures/frames/basin_overturning/`, ...) — never dump
  loose frames. The whole `frames/` tree is gitignored.
- **The rendered video sits in `figures/`**, named for its context
  (`figures/coastal_eddies.mp4`), right next to the still figures it belongs with. It's
  gitignored by extension (`.mp4`, `.mov`, ...), so it's co-located for humans but not
  tracked in git. Commit the stills and the animation script — not the frames or the video.
