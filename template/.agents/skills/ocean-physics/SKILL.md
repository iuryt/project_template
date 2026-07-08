---
name: ocean-physics
description: Seawater thermodynamics (TEOS-10 / gsw) and dynamical diagnostics — geostrophy, vorticity, stratification, fluxes. Use when computing density/buoyancy, converting temperature/salinity variables, or deriving dynamical quantities from ocean fields.
---

# Ocean physics (TEOS-10 · dynamics)

## Seawater thermodynamics — use TEOS-10 (`gsw`), not EOS-80
- **Convert to TEOS-10 variables first.** From in-situ `T`, practical salinity `SP`,
  pressure `p`, lon/lat:
  - `SA = gsw.SA_from_SP(SP, p, lon, lat)` — Absolute Salinity
  - `CT = gsw.CT_from_t(SA, T, p)` — Conservative Temperature
- Then derive: `sigma0 = gsw.sigma0(SA, CT)` (potential density anomaly, 0 dbar ref),
  `rho = gsw.rho(SA, CT, p)`, `N2, p_mid = gsw.Nsquared(SA, CT, p, lat)` (stratification).
- **Mind the variable zoo.** Potential vs Conservative Temperature; practical vs Absolute
  Salinity; pressure (dbar) vs depth (m, `gsw.p_from_z` / `gsw.z_from_p`, z negative down).
  State which convention a function expects/returns.

## Dynamical diagnostics
- **Coriolis:** `f = gsw.f(lat)` (or `2*Ω*sin(φ)`); `β = df/dy`.
- **Geostrophy:** `u_g = -(g/f) ∂η/∂y`, `v_g = (g/f) ∂η/∂x` from SSH `η`; or thermal-wind
  from the density field. Watch sign conventions and the equatorial `1/f` blow-up.
- **Vorticity:** relative `ζ = ∂v/∂x − ∂u/∂y`; potential vorticity for layered/QG work.
- **Buoyancy:** `b = −g ρ'/ρ₀`; buoyancy frequency from `N2` above.
- Use **`xgcm`** for finite-difference operators (grad/div/curl/interp) on model C-grids —
  it respects grid staggering and metrics instead of naive `np.gradient`.

## Practice
- Keep these as pure, unit-aware functions in `src/<pkg>/` (e.g. `dynamics.py`,
  `thermodynamics.py`), named for the science. Document units in every docstring.
- Preserve `xarray` coords/attrs through calculations; set `units`/`long_name` on outputs.
- Sanity-check magnitudes (mid-latitude `f ~ 1e-4 s⁻¹`, `N ~ 1e-2 s⁻¹`, geostrophic
  currents O(0.1–1 m/s)).
