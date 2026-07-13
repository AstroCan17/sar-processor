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

> **Status: skeleton (pre-SRR).** The ECSS document tree is in place with the
> full tailored DRL; technical content (requirements, algorithms, product type
> codes) lands at SRR/PDR.

## Layout

| Path | Content |
|---|---|
| `sar_processor/` | Python package: `common/` (platform layer), `computing/` (processing stages), `sensors/` (profile layer), `exceptions/` |
| `compliance/` | ECSS-E-ST-40C document set (source of truth); `compliance/drd/` holds the DRDs |
| `docs/` | Sphinx site; `docs/compliance/` symlinks into `compliance/` (content is edited there) |
| `scripts/run_pipeline.py` | Single pipeline driver (mode-only CLI: `nominal` \| `calibration`) |
| `tests/ut`, `tests/it` | Unit / integration tests (`pytest -m unit` / `-m integration`) |

## Usage

```shell
pip install .
python scripts/run_pipeline.py <store> --mode nominal
```

Deployment settings come from environment variables defined in the ICD (PDR).

## Codespaces + private dataset setup

- `AstroCan17/sar-processor` (public): code
- `AstroCan17/ipf-data` (private): SAR release tag `datasets-sar-v1`

Set Codespaces secret `DATA_REPO_PAT` (read access to `ipf-data`). The devcontainer
fetches `input-data.tar.gz` into `data/`. Refresh with `make data-sync`.

## Development

```shell
pip install .[dev]
pre-commit install
pytest -m unit
```

The documentation set starts at the [Software Development Plan](compliance/software-development-plan.md),
which contains the tailored DRL of all delivered documents.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
