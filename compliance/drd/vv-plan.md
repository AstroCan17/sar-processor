# Software Verification & Validation Plan (V&V Plan — SVerP + SValP)

| Field | Value |
|---|---|
| **Document** | V&V Plan — Software Verification Plan (SVerP) merged with Software Validation Plan (SValP) |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex I (SVerP) + Annex J (SValP); ECSS-Q-ST-80C Rev.2 §6.2.6.1 |
| **Container** | Design Justification File (DJF) — `compliance/drd/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | PDR (Preliminary Design Review) |
| **Status** | Draft for SRR — skeleton |

> This document merges the **Software Verification Plan** (Annex I) and the **Software Validation
> Plan** (Annex J) into one V&V plan, per the tailored DRL of the SDP <5.5.2>. Content
> `TBD (PDR)`; the three-tier scheme below is committed at skeleton, mirroring msi-processor.

---

## <1> Introduction

`TBD (PDR)`.

## <2> V&V strategy

Three tiers, as on the donor project:

1. **Unit tests** (`tests/ut/`, marker `unit`) — pure-algorithm `core.py` tests + wrapper
   `unit.py` tests per stage; CI-blocking.
2. **Integration tests** (`tests/it/`, marker `integration`) — end-to-end chain over the shared
   data-store.
3. **Real-data validation** — comparison against public **Sentinel-1** reference products;
   criteria `TBD (PDR)`.

## <3> Verification methods

Every `REQ-*` bound to **T/A/I/R**; matrix in clause <5>. `TBD (PDR)`.

## <4> Validation scenarios

`TBD (PDR — pending SentiWiki S1 ingest and reference-data selection)`.

## <5> Requirements-to-method matrix

`TBD (PDR)` — maintained with the traceability matrix.
