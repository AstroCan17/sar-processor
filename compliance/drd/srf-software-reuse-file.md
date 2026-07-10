# Software Reuse File (SRF)

| Field | Value |
|---|---|
| **Document** | SRF — Software Reuse File |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex N (SRF DRD); ECSS-Q-ST-80C Rev.2 §6.2.7 |
| **Container** | Design Justification File (DJF) — `compliance/drd/` (source), published subset in `docs/srf.md` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | **SRR (initial)** / CDR (final) |
| **Status** | Draft for SRR — initial issue |

> **Purpose of this issue.** `sar-processor` reuses the **sensor-agnostic platform and process machinery**
> proven on the sibling `ipf/msi-processor` project, and reuses the **public Sentinel-1 algorithm basis**
> (the IPFDPM and the SentiWiki technical corpus) as the mathematical reference for its focusing,
> calibration and geocoding stages. The SAR **processing content is new development** — there is **no
> requirement that `sar-processor` be structurally identical to `msi-processor`**; the two are different
> sensors with different chains, data models and stage sets. This SRF (initial issue, SRR) records what
> is reused, on what licence, at what quality level, and — explicitly — the **reuse-vs-new boundary**. The
> detailed per-module evaluation and corrective-action results are finalised at CDR, before implementation
> (WP-5) starts. Sensor-private content (calibration coefficients, private ADF values) is **not**
> reproduced here (data policy).

---

## <1> Reused software items

Reused items are identified as **`SRF-RU-*`**. Three reuse bodies, each with its own category and
treatment:

| Id | Item | Origin | Category | Scope of reuse | Pedigree |
|---|---|---|---|---|---|
| SRF-RU-01 | CI pipeline (stages, quality/security gates, Pages / versioned-docs machinery) | `ipf/msi-processor` `.gitlab-ci.yml` | scaffold (as-is, names adapted) | adopted verbatim, project names adapted | CI green on donor through QR |
| SRF-RU-02 | Documentation toolchain (Sphinx conf, `compliance/` source + `docs/compliance/` symlink publishing, SUM/DRD skeletons) | `ipf/msi-processor` `docs/` + `compliance/` | scaffold (as-is) | adopted verbatim | published donor site |
| SRF-RU-03 | Package/process conventions — the **`core.py` (framework-free) + `unit.py` (`EOProcessingUnit`) + `models/*.json` (CPM computing model)** stage pattern; typed error hierarchy with `stage=` tags; Pydantic `SensorProfile` with ADF-reference bindings; single mode-only pipeline driver; `tests/ut`+`tests/it` layout | `ipf/msi-processor` | **pattern reuse** (not code copy) | the *conventions* are reused; SAR *content* is new | donor SDD, QR-verified |
| SRF-RU-04 | EOPF CPM runtime (`eopf == 2.8.1`) | ESA EOPF | COTS/platform (as-is) | mandated runtime | ESA-maintained, pinned |
| SRF-RU-05 | Shared data-store fetch/publish mechanism (`ipf/data-store`, GitLab generic package registry, sha256 manifest) | `ipf/msi-processor` driver | scaffold (as-is, `[TBC@PDR]` for SAR store layout) | fetch-store/publish-store convention | donor integration tests |
| SRF-RU-06 | **Public Sentinel-1 algorithm basis** — IPFDPM (focusing/DCE/calibration math), SentiWiki product/calibration/geocoding/TOPS-deramp/thermal-noise/ADF references | ESA/Aresys/DLR/UZH (public; vault `wiki/`) | **algorithm reuse — re-engineered** | equations reused; code written new into SAR Cores | public engineering, peer-referenced |
| SRF-RU-07 | Scientific-Python OSS stack (numpy, scipy, xarray, zarr, dask) + FFT backend (`numpy.fft` baseline; optional `scipy.fft`/`pyFFTW`) | OSS communities | OSS (as-is, by dependency) | numerical kernels inside the Cores | mature, semantically versioned |

## <2> Reuse categories and the reuse-vs-new boundary

- **Scaffold / process (SRF-RU-01/02/03/05):** reused from msi-processor because it is **sensor-agnostic
  infrastructure** — CI gates, docs publishing, the `core`/`unit`/`model` separation, the profile-driven
  design, the data-store protocol, the test layout. Reuse here is of *conventions and machinery*, adapted
  by name; it is **not** a constraint that the SAR chain mirror the MSI chain.
- **Platform (SRF-RU-04):** the EOPF CPM, reused as-is (mandated runtime), pinned at `eopf == 2.8.1`.
- **Algorithm basis (SRF-RU-06):** the public Sentinel-1 algorithm mathematics is reused as the
  *reference*; the SAR Cores that realise it (decode, focusing, DCE, TOPSAR, calibration, GRD, geocode)
  are **written new** against the ATBD/DPM — algorithm reuse, code new.
- **OSS kernels (SRF-RU-07):** reused as-is by dependency.

**New development (NOT reuse) — the SAR-specific boundary.** The following are new to `sar-processor` and
are *expected* differences from msi-processor, not deviations to be justified against a msi baseline:

| New element | Reason it is SAR-specific |
|---|---|
| `sar_processor/product/` subpackage (SAFE/annotation/LUT/orbit I/O) | SAR's per-product metadata (annotation XML, CADS/NADS LUTs, orbit/attitude) is far heavier than MSI's; kept out of the framework-free cores |
| Complex data model — `SlcImage` (`complex64`), `BurstStack`, per-burst grouping | SAR is coherent/phase-preserving; MSI is real-valued |
| SAR stage set — `l0_decode`(+FDBAQ), `preproc`, `doppler`, `range_comp`, `azimuth_comp`, `topsar`, `calibration`, `noise`, `grd`, `geocode` | the SAR chain (focusing + TOPSAR + geocoding) has no MSI counterpart |
| SAR QA flags — `BLACK_FILL`, `DERAMP_INVALID`, `THERMAL_NOISE_SUBTRACTED`, `GEO_LAYOVER_SHADOW`, … | SAR-specific quality conditions |
| Image-quality metrics — PSLR, ISLR, IRW, ENL, NESZ, ALE | SAR focusing/geolocation/noise metrics |
| SAR `SensorProfile` extension (carrier frequency, polarisations, sub-swath specs, IPF-version envelope) + the annotation-vs-ADF split | SAR radar geometry and IPF-version gating |
| FFT backend dependency | range/azimuth compression |

## <3> Licence compatibility (project code is public)

Project licence: **Apache-2.0**. All reused runtime software is permissive and Apache-2.0-compatible:
EOPF CPM (Apache-2.0), numpy/scipy/dask (BSD-3-Clause), xarray (Apache-2.0), zarr (MIT); the FFT backend
options are BSD (`numpy`/`scipy`) or, if `pyFFTW` is adopted, **BSD-3-Clause** (its FFTW binding wrapper)
— note FFTW itself is **GPL**, so `pyFFTW` is admitted only if the deployment can accept that or is kept
optional/non-distributed; `numpy.fft` (BSD) is the default to avoid any copyleft obligation. The public
Sentinel-1 algorithm basis (SRF-RU-06) is documentation/engineering, not code, and imposes no code
licence. `[confirm-before-release]`: the final FFT-backend decision and any optional accelerated backend
are pinned and licence-audited at CDR/release.

## <4> Reuse assessment (initial — Annex N <5>)

| Item | Quality level vs Category C | Decision | Re-verification |
|---|---|---|---|
| SRF-RU-01/02 (CI, docs) | HIGH — donor CI green through QR | reuse as-is (names adapted) | pipeline runs green on SAR repo |
| SRF-RU-03 (patterns) | HIGH — donor SDD, QR-verified | pattern reuse | SAR Cores/units verified under project V&V |
| SRF-RU-04 (EOPF CPM) | HIGH — mandated, pinned | reuse as-is | verify *use* (Wrapper/Zarr round-trip), not internals; complex/burst support probed (RSK-05) |
| SRF-RU-05 (data-store) | HIGH — donor integration-tested | reuse as-is; SAR store layout `[TBC@PDR]` | fetch/publish round-trip |
| SRF-RU-06 (S1 algorithm basis) | HIGH as *reference* (public, peer-referenced); LOW as *code* (there is no code to reuse) | **reuse algorithm, write code new** | each Core re-derived vs ATBD, validated on point-target + real data (tolerance-based) |
| SRF-RU-07 (OSS + FFT) | HIGH — mature, versioned | reuse as-is | verify kernel use vs ATBD; pin versions; licence audit |

## <5> Corrective actions / conditions (initial)

| Id | Action | Applies to | Closes at |
|---|---|---|---|
| CA-01 | Confirm EOPF Zarr support for `complex64` + per-burst grouping, or define a documented convention | SRF-RU-04 | PDR (RSK-05) |
| CA-02 | Fix the FFT-backend decision + licence audit (avoid FFTW/GPL by default) | SRF-RU-07 | CDR/release |
| CA-03 | Baseline the SAR data-store layout for `fetch-store`/`publish-store` | SRF-RU-05 | PDR |
| CA-04 | Finalise the per-stage algorithm-basis → Core mapping (ALG-*), with keep/adapt notes | SRF-RU-06 | CDR |
| CA-05 | Record the `product/` subpackage + complex/burst types + SAR stage set as new development in the SDD | new-dev boundary | CDR |

> **Status at SRR: initial.** No corrective action is closed at this issue; implementation (code) starts
> only after CDR. The final SRF (CDR) will carry the per-module evaluation, the closed corrective actions,
> and the configuration status of every reused baseline.

---

*End of SRF (initial issue). Authored per ECSS-E-ST-40C Rev.1 Annex N, tailored for Category C; finalised
at CDR.*
