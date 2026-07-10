# Algorithm Theoretical Basis Document (ATBD)

| Field | Value |
|---|---|
| **Document** | ATBD — Algorithm Theoretical Basis Document |
| **DRD ref** | EO-domain ATBD convention (no ECSS-E-ST-40C Rev.1 annex); algorithm constituent of the DPM, supporting the SRS |
| **Container** | Technical documentation — `docs/atbd/` (published); source in `compliance/drd/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | PDR (Preliminary Design Review) |
| **Status** | Draft for SRR — skeleton |

> This ATBD records the **theoretical and mathematical basis** of every processing stage of
> `sar-processor`, the generic spaceborne **SAR** ground-segment forward processor. Algorithms are
> identified as **`ALG-<STAGE>-NN`** and traced from `REQ-F-*` (SRS) and into the SDD components.
> All algorithm content is `TBD (PDR — pending SentiWiki S1 ingest)`; this issue fixes only the
> stage decomposition of the forward chain.

---

## <1> Introduction

Scope: L0 → L1 SLC → L1 GRD forward chain, sensor-agnostic formulation with per-sensor profile
parameters; Sentinel-1 C-SAR is the reference for symbols, conventions and validation data.
`TBD (PDR)`.

## <2> Applicable and reference documents

Per SDP <2>; canonical technical reference: SentiWiki Sentinel-1 documentation set (vault-ingested).
`TBD (PDR)`.

## <3> Conventions and symbols

Radar geometry, slant/ground range, zero-Doppler convention, units. `TBD (PDR)`.

## <4> Processing stages

Each stage section: purpose, inputs/outputs, mathematical description (`ALG-*`), accuracy and
error budget, references.

### <4.1> L0 decode (`ALG-L0D-*`)
ISP extraction, decompression (FDBAQ/BAQ TBC), echo/annotation separation.
`TBD (PDR — pending SentiWiki S1 ingest)`.

### <4.2> Doppler-centroid estimation (`ALG-DCE-*`)
`TBD (PDR — pending SentiWiki S1 ingest)`.

### <4.3> Range compression (`ALG-RGC-*`)
`TBD (PDR — pending SentiWiki S1 ingest)`.

### <4.4> Azimuth focusing (`ALG-AZF-*`)
Focusing algorithm selection (range-Doppler / chirp scaling / ω-k) is a PDR trade-off recorded in
the DJF. `TBD (PDR — pending SentiWiki S1 ingest)`.

### <4.5> Radiometric calibration (`ALG-CAL-*`)
`TBD (PDR — pending SentiWiki S1 ingest)`.

### <4.6> Multilook / detection (`ALG-MLD-*`)
`TBD (PDR — pending SentiWiki S1 ingest)`.

### <4.7> Geocoding (`ALG-GEO-*`)
`TBD (PDR — pending SentiWiki S1 ingest)`.

## <5> Validation approach

Reference-data comparison against public Sentinel-1 products (mirroring the msi-processor
real-data validation precedent). `TBD (PDR)`.

## <6> Traceability

`REQ-F-*` → `ALG-*` → SDD components, recorded in the traceability matrix. `TBD (CDR)`.
