# Software Release Note (SRN / SRelD)

| Field | Value |
|---|---|
| **Document** | SRN — Software Release Note (Software Release Document, SRelD) |
| **DRD ref** | ECSS-E-ST-40C Rev.1 — Software Release Document (SRelD); ECSS-M-ST-40C (configuration management); ECSS-Q-ST-80C Rev.2 (software delivery, acceptance & release) |
| **Container** | Released-software documentation set — `compliance/drd/` (source) |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | QR / each release |
| **Status** | Draft for SRR — skeleton |

> Software Release Note for the `sar-processor` software configuration item. One entry per
> released version; maintained from the first tagged release onward.

---

## Releases

### v0.0.1 — repository skeleton (unreleased)

- Repository skeleton: package layout (`sar_processor/` C-COMMON / C-PU-\* / C-SENSORS),
  CI pipeline, documentation site, ECSS doc-first compliance tree (all documents
  `Draft for SRR — skeleton`).
- No processing functionality yet; pipeline driver validates arguments only.
- Known limitations: all technical content `TBD (SRR/PDR)` pending the SentiWiki Sentinel-1
  ingest.
