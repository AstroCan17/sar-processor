# Data Processing Model (DPM)

| Field | Value |
|---|---|
| **Document** | DPM — Data Processing Model |
| **DRD ref** | EOPF Data Processor (DPR) concept — Detailed Processing Model (no ECSS-E-ST-40C annex; complements the ATBD per AD-1 §5.4) |
| **Container** | Technical Specification (TS) — authoritative source in `compliance/drd/`, rendered subset published in `docs/dpm/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | PDR (Preliminary Design Review) |
| **Status** | Draft for SRR — skeleton |

> This DPM is the **engineering processing model** of `sar-processor`: the end-to-end
> transformation of downlinked raw Level-0 SAR instrument source packets into L1 SLC / L1 GRD
> products, decomposed into processing modules with their data flows, parameters and breakpoints.
> ID schemes: **`DPM-M-*`** modules, **`DPM-PR-*`** products, **`DPM-ADF-*`** auxiliary data
> files, **`DPM-PRM-*`** parameters, **`DPM-BKP-*`** breakpoints. Content `TBD (PDR)`.

---

## <1> Introduction

Engineering counterpart of the ATBD: same stage chain, expressed as modules with concrete data
interfaces. `TBD (PDR)`.

## <2> Applicable and reference documents

Per SDP <2>. `TBD (PDR)`.

## <3> Processing model overview

End-to-end flow diagram (mermaid) L0 → SLC → GRD; module list `DPM-M-*` mirrors the ATBD stage
set (<4.1>–<4.7>). `TBD (PDR)`.

## <4> Modules (`DPM-M-*`)

Per module: function, inputs (`DPM-PR-*` / `DPM-ADF-*`), outputs, parameters (`DPM-PRM-*`),
breakpoints (`DPM-BKP-*`). `TBD (PDR — pending SentiWiki S1 ingest)`.

## <5> Products and auxiliary data

Product tree (`DPM-PR-*`): `TBD — S01 SAR product type codes fixed in ICD at PDR`. ADF set
(`DPM-ADF-*`): calibration constants, antenna patterns, orbit files. `TBD (PDR)`.

## <6> Traceability

`REQ-*` → `DPM-M-*` → SDD components in the traceability matrix. `TBD (CDR)`.
