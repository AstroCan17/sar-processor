# Software Interface Requirements Document (IRD)

| | |
|---|---|
| **Document** | Software Interface Requirements Document (IRD) |
| **DRD** | ECSS-E-ST-40C Rev.1, Annex C |
| **Container** | Requirements Baseline (RB) |
| **Project** | `sar-processor` — generic spaceborne SAR data processor |
| **Configuration item** | `gitlab.eopf.copernicus.eu/ipf/sar-processor` |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | SRR |
| **Status** | Draft for SRR — skeleton |

> This IRD is part of the **requirements baseline** of the `sar-processor` project and, together
> with the SSS, is the primary input to the SRR. It states **interface requirements (`REQ-IF-*`)**
> at requirement level; concrete field-level definitions are controlled in the ICD (PDR/CDR).
> Content is `TBD (SRR)`.

---

## <1> Introduction

Interface requirements for the external interfaces of `sar-processor`: input L0 products (SAR
instrument source packets), auxiliary/calibration data files (ADFs), output L1 SLC / L1 GRD
products, the shared `ipf/data-store` registry, and the EOPF CPM runtime contract. `TBD (SRR)`.

## <2> Applicable and reference documents

Per SDP <2>. `TBD (SRR)`.

## <3> Terms, definitions and abbreviated terms

See SSS <3>. `TBD (SRR)`.

## <4> Interface requirements (`REQ-IF-*`)

ID scheme: `REQ-IF-NN`; each requirement bound to a verification method (T/A/I/R) and traced to
`SYS-*`. Groups:

- **<4.1> Input products** — L0 ISP structure, annotation, orbit/attitude ancillary. `TBD (SRR)`.
- **<4.2> Auxiliary data** — ADF set (calibration constants, antenna patterns, orbit files);
  private calibration lives in ADFs referenced by URI, never in code. `TBD (SRR)`.
- **<4.3> Output products** — L1 SLC / L1 GRD as EOPF `EOProduct` / Zarr;
  `TBD — S01 SAR product type codes fixed in ICD at PDR`.
- **<4.4> Platform** — EOPF CPM (`eopf == 2.8.1`), data-store fetch/publish protocol. `TBD (SRR)`.

| ID | Requirement | Ver. |
|---|---|---|
| REQ-IF-01 | `TBD (SRR)` | — |

## <5> Traceability

`SYS-*` ↔ `REQ-IF-*` ↔ `ICD-IF-*` in the traceability matrix. `TBD (PDR)`.
