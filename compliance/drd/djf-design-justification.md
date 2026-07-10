# Design Justification File (DJF) — Design Justification

| Field | Value |
|---|---|
| **Document** | DJF — Design Justification (design rationale, trade-offs, make-or-buy and feasibility record) |
| **DRD ref** | ECSS-E-ST-40C Rev.1 §4.2.4 / §4.2.5 (DJF concept); ECSS-M-ST-10-01C (review/justification concept); design-level summary of Annex F <6> |
| **Container** | Design Justification File (DJF) — `compliance/drd/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | **CDR** |
| **Status** | Draft for SRR — skeleton |

> Per ECSS-E-ST-40C Rev.1 §4.2.4/§4.2.5 the **Design Justification File** records the result of
> all significant trade-offs, feasibility analyses and make-or-buy decisions. For `sar-processor`
> the anticipated headline trade-offs are listed below; each is recorded here when decided.

---

## <1> Introduction

`TBD (PDR/CDR)`.

## <2> Trade-off register

| ID | Trade-off | Decided at | Record |
|---|---|---|---|
| DJF-01 | Azimuth focusing algorithm: range-Doppler vs chirp scaling vs ω-k | PDR | `TBD (PDR)` |
| DJF-02 | L0 decompression handling (FDBAQ/BAQ decode scope) | PDR | `TBD (PDR)` |
| DJF-03 | FFT backend / numerical toolchain addition beyond eopf-provided numpy | PDR | `TBD (PDR)` |
| DJF-04 | L2 ocean products in or out of scope | SRR | `TBC (SRR)` |
| DJF-05 | Reuse boundary with msi-processor platform machinery (see SRF) | SRR | committed at skeleton: CI, doc toolchain, package layout, driver convention reused |

## <3> Feasibility and make-or-buy

`TBD (PDR)`.

## <4> Traceability

Decisions trace into SDD components and SRS constraints (`REQ-D-*`). `TBD (CDR)`.
