# Configuration Item Data List (CIDL)

| Field | Value |
|---|---|
| **Document** | CIDL — Configuration Item Data List |
| **DRD ref** | ECSS-M-ST-40C Rev.1 (configuration item data list); ECSS-E-ST-40C Rev.1 (software configuration management); ECSS-Q-ST-80C Rev.2 §6.2.7 |
| **Container** | Management File (MGT) / QR data package — `compliance/drd/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | QR (Qualification Review) |
| **Status** | Draft for SRR — skeleton |

> This CIDL enumerates **every configuration item** that constitutes the Software Configuration
> Item (SCI) `sar-processor` at the **QR configuration baseline**. Produced at QR; this issue
> records only the item categories.

---

## <1> Configuration item categories

| Category | Items | Baseline |
|---|---|---|
| Source code | `sar_processor/`, `scripts/`, `tests/` | `TBD (QR)` |
| Documentation | `compliance/`, `docs/` | `TBD (QR)` |
| Build & CI | `pyproject.toml`, `.gitlab-ci.yml`, `Dockerfile`, linter configs | `TBD (QR)` |
| Auxiliary data | ADF set in `ipf/data-store` | `TBD (QR)` |

## <2> Item list

`TBD (QR)` — generated from the tagged `main` commit at the QR baseline.
