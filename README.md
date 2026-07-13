# sar-processor

A **generic spaceborne SAR ground-segment forward processor**: downlinked raw
Level-0 SAR instrument source packets → focused **L1 SLC** → detected/projected
**L1 GRD** (L2 ocean products TBC). The processing chain is sensor-agnostic and
driven by a per-sensor profile; the first instantiated profile is a C-band SAR
with **Sentinel-1 C-SAR** as the public reference dataset.

Built on the ESA **EOPF Core Python Modules** (CPM, `eopf == 2.8.1`): each
processing stage is an `EOProcessingUnit`, products are EOPF `EOProduct`
objects, outputs are cloud-native **Zarr**. Sibling project of
[`ipf/msi-processor`](https://github.com/AstroCan17/msi-processor),
whose platform machinery (CI, documentation toolchain, package layout, single
pipeline driver) it reuses (see the SRF).

> **Status: SRR documentation baseline complete; implementation skeleton (pre-CDR).**
> The tailored ECSS document tree is in place. System and interface requirements
> are baselined at SRR (SSS, IRD, SDP, SPAP, SRevP, Risk Register, initial SRF).
> Software requirements, algorithms, and detailed design land at PDR/CDR;
> processing-stage implementation (WP-5) starts after CDR per the SDP.

## Documentation milestones

| Milestone | State | Key artefacts |
|---|---|---|
| SRR | **Done** | SSS, IRD, SDP, SPAP, SRevP, Risk Register, SRF (initial) |
| PDR | Planned | SRS, ICD (prelim), DPM, ATBD, V&V Plan |
| CDR | Planned | SDD, SUITP, final ICD, traceability matrix |
| QR | Planned | SVR, SUITR, SRN, SUM |

## Layout

| Path | Content |
|---|---|
| `sar_processor/` | Python package: `common/` (platform layer), `computing/` (processing stages), `sensors/` (profile layer), `exceptions/` — target layout; current code is scaffold placeholders until WP-5 |
| `compliance/` | ECSS-E-ST-40C document set (source of truth); `compliance/drd/` holds the DRDs |
| `docs/` | Sphinx site; `docs/compliance/` symlinks into `compliance/` (content is edited there) |
| `scripts/run_pipeline.py` | Single pipeline driver (mode-only CLI: `nominal` \| `calibration`) |
| `tests/ut`, `tests/it` | Unit / integration tests (`pytest -m unit` / `-m integration`) |
| `.devcontainer/` | Devcontainer/Codespaces config; `postCreateCommand` runs install + dataset fetch |
| `Makefile` | `make install`, `make data-sync`, `make devcontainer-setup`, `make publish-dataset` |
| `.github/workflows/` | Primary CI for the GitHub mirror (lint, test, docs, e2e, data-fetch smoke) |

## Usage

```shell
pip install .
python scripts/run_pipeline.py <store> --mode nominal
```

Deployment settings come from environment variables defined in the ICD (PDR).

## Development

```shell
# Local setup
pip install .[dev]          # or: make install
pre-commit install
pytest -m unit

# Optional: integration tests (when data available)
pytest -m integration
```

- **CI:** GitHub Actions on push/PR ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)); GitLab CI ([`.gitlab-ci.yml`](.gitlab-ci.yml)) remains for the official EOPF instance
- **Data:** `make data-sync` refreshes `data/` from `ipf-data` (see Codespaces section)
- **Docs build:** `pip install ".[doc]" && sphinx-build docs _site` (local); `main` deploys via [`.github/workflows/docs.yml`](.github/workflows/docs.yml)

For a full devcontainer bootstrap, open in Codespaces or run `make devcontainer-setup`.

## Codespaces + private dataset setup

- `AstroCan17/sar-processor` (public): code
- `AstroCan17/ipf-data` (private): SAR release tag `datasets-sar-v1`

[`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) sets `DATASET_TAG=datasets-sar-v1`
and runs [`.devcontainer/scripts/setup.sh`](.devcontainer/scripts/setup.sh) on create (install + dataset fetch).

Set Codespaces secret `DATA_REPO_PAT` (read access to `ipf-data`). The devcontainer
fetches `input-data.tar.gz` into `data/`. Refresh with `make data-sync`.

## Documentation

Entry point: the [Software Development Plan](compliance/software-development-plan.md) contains
the tailored DRL and life-cycle model.

**SRR-baselined documents** (source of truth in `compliance/drd/`):

- [SSS](compliance/drd/sss-software-system-specification.md) — system requirements
- [IRD](compliance/drd/ird-interface-requirements.md) — interface requirements
- [SRevP](compliance/drd/srevp-software-review-plan.md) · [SPAP](compliance/drd/spa-plan.md) · [Risk Register](compliance/drd/risk-register.md) · [SRF](compliance/drd/srf-software-reuse-file.md)

**Published site:**

- GitHub Pages (mirror, `main`): <https://astrocan17.github.io/sar-processor/>
- GitLab Pages (official EOPF): <https://ipf.pages.eopf.copernicus.eu/sar-processor/>

## License

Apache License 2.0 — see [LICENSE](LICENSE).
