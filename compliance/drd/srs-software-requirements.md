# Software Requirements Specification (SRS)

| Field | Value |
|---|---|
| **Document** | SRS — Software Requirements Specification |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex D |
| **Container** | Technical Specification (TS) — `compliance/drd/` (source), published subset in `docs/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | PDR (Preliminary Design Review) |
| **Status** | Draft for SRR — skeleton |

> This SRS is a major constituent of the Technical Specification of `sar-processor`. It decomposes
> the system requirements (`SYS-*`, SSS) and the interface requirements (`REQ-IF-*`, IRD) into
> uniquely identified **software requirements (`REQ-*`)**, each bound to a verification method
> (**T** Test / **A** Analysis / **I** Inspection / **R** Review of design). The
> processing-algorithm mathematical basis is *not* (re)specified here: it is the subject of the
> DPM and ATBD. The footprint is tailored to a Category C, single-developer ground-segment
> processor. Requirements content is `TBD (PDR)`.

---

## <1> Introduction

**Purpose.** Specify the software requirements for `sar-processor`, a generic spaceborne **SAR**
ground-segment forward processor that transforms downlinked **raw Level-0** SAR instrument source
packets into focused **L1 SLC** and detected/projected **L1 GRD** products (L2 ocean TBC).
`TBD (PDR)`.

**Objective.** Parent specification for the design (SDD) and the V&V activities (V&V Plan). Every
`REQ-*` traces upward to `SYS-*` and/or `REQ-IF-*`, and downward to a verification method
(clause <6>) and, at CDR, to a design element and a test case (traceability matrix).

## <2> Applicable and reference documents

Per SDP <2>. `TBD (PDR)`.

## <3> Terms, definitions and abbreviated terms

See SSS <3>. `TBD (PDR)`.

## <4> Software overview

**<4.1> Function.** Sensor-agnostic SAR forward chain driven by a per-sensor profile (first
profile: C-band, Sentinel-1 C-SAR reference data). **<4.2> Environment.** EOPF CPM
(`eopf == 2.8.1`), Python 3.11, Zarr outputs. **<4.3> Relations.** Sibling of `ipf/msi-processor`
(platform reuse, SRF); shared `ipf/data-store`. `TBD (PDR)`.

## <5> Requirements

ID scheme (mirrors msi-processor):

- `REQ-F-<STAGE>-NN` — functional, per processing stage (stage set fixed at PDR from the ATBD
  chain: L0 decode, Doppler-centroid estimation, range compression, azimuth focusing, radiometric
  calibration, multilook/detection, geocoding);
- `REQ-P-*` performance, `REQ-D-*` design & implementation constraints, `REQ-AD-*` adaptation
  data (per-sensor profile / ADFs), `REQ-S-*` security, `REQ-DAT-*` data/product requirements.

All `TBD (PDR — pending SentiWiki S1 ingest)`.

| ID | Requirement | Trace | Ver. |
|---|---|---|---|
| REQ-F-TBD-01 | `TBD (PDR)` | SYS-TBD | — |

## <6> Validation approach

Per requirement group; delegated to the V&V Plan. `TBD (PDR)`.

## <7> Traceability

`SYS-*`/`REQ-IF-*` → `REQ-*` in `compliance/traceability/traceability-matrix.md`. `TBD (PDR)`.

## <8> Logical model

Top-level logical model of the forward chain (mermaid diagram). `TBD (PDR)`.
