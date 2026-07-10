# Software System Specification (SSS)

| Field | Value |
|---|---|
| **Document** | SSS — Software System Specification |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex B |
| **Container** | EOPF SDE — `compliance/drd/` (source), published in online documentation (`docs/`) |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | SRR (System Requirements Review) |
| **Status** | Draft for SRR — skeleton |

> This SSS is the highest-level specification of `sar-processor` and, together with the IRD,
> forms the requirements baseline and the primary input to the SRR. It states **system-level
> requirements (`SYS-*`)** for a generic spaceborne SAR ground-segment forward processor:
> downlinked raw Level-0 SAR instrument source packets → focused **L1 SLC** → detected/projected
> **L1 GRD** (L2 ocean products TBC). System requirements content is `TBD (SRR)` — pending the
> SentiWiki Sentinel-1 technical-reference ingest.

---

## <1> Introduction

**Purpose.** Specify the system-level requirements of `sar-processor`, a sensor-agnostic SAR
forward processor driven by a per-sensor profile; first instantiated profile: C-band SAR with
Sentinel-1 C-SAR as the public reference dataset. `TBD (SRR)`.

## <2> Applicable and reference documents

AD/RD tables per the SDP (RD numbering inherited from `compliance/software-development-plan.md`
<2>). `TBD (SRR)`.

## <3> Terms, definitions and abbreviated terms

Glossary of SAR terms (ISP, SLC, GRD, Doppler centroid, chirp, PRF, NESZ, DN, ADF, …).
`TBD (SRR — populated from the SentiWiki S1 ingest)`.

## <4> System description

**<4.1> Mission and context.** Ground-segment payload data processing; EOPF CPM runtime; Zarr
products. `TBD (SRR)`.

**<4.2> Processing levels.** L0 (raw ISPs) → L1 SLC → L1 GRD; L2 ocean `TBC (SRR)`. Product type
codes: `TBD — S01 SAR product type codes fixed in ICD at PDR`.

## <5> System requirements (`SYS-*`)

ID scheme: `SYS-NN`, one requirement per identifier, each with rationale and verification method
(**T** Test / **A** Analysis / **I** Inspection / **R** Review of design). Grouped: capability,
performance, interface (delegating to IRD `REQ-IF-*`), operational, data. `TBD (SRR)`.

| ID | Requirement | Ver. |
|---|---|---|
| SYS-01 | `TBD (SRR)` | — |

## <6> Verification and validation

Delegated to the V&V Plan (RD-8). `TBD (SRR)`.

## <7> Traceability

`SYS-*` → `REQ-*` (SRS) recorded in the traceability matrix
(`compliance/traceability/traceability-matrix.md`). `TBD (PDR)`.
