# Software Design Document (SDD)

| Field | Value |
|---|---|
| **Document** | SDD — Software Design Document |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex F |
| **Container** | Design Definition File (DDF) — `compliance/drd/` (source), published subset in `docs/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | CDR (Critical Design Review) |
| **Status** | Draft for SRR — skeleton |

> This SDD records the architectural (PDR) and detailed (CDR) design of `sar-processor`. Design
> components trace to `REQ-*` (SRS), `DPM-M-*` (DPM) and `ALG-*` (ATBD); post-CDR code internals
> are marked `[impl]`. This issue fixes only the component layout, which mirrors the repository
> package skeleton; all design content is `TBD (PDR/CDR)`.

---

## <1> Introduction

`TBD (PDR)`.

## <2> Applicable and reference documents

Per SDP <2>. `TBD (PDR)`.

## <3> Terms, definitions and abbreviated terms

See SSS <3>. `TBD (PDR)`.

## <4> Software design overview

**<4.1> Architecture.** Three layers, mirroring the msi-processor precedent and the
`sar_processor/` package:

- **C-COMMON** (`sar_processor/common/`) — platform/services layer: CPM-free shared types and QA
  metrics.
- **C-PU-\*** (`sar_processor/computing/<stage>/`) — one component per processing stage
  (stage set fixed at PDR from the ATBD chain); each stage = `core.py` (pure numpy algorithm,
  CPM-free) + `unit.py` (EOPF `EOProcessingUnit` wrapper).
- **C-SENSORS** (`sar_processor/sensors/`) — sensor adaptation layer: per-sensor profile loading;
  no instrument constants in code (ADFs by URI).

**<4.2>–<4.7>** Runtime (EOPF CPM `eopf == 2.8.1`, dask), single pipeline driver
(`scripts/run_pipeline.py`, mode-only CLI `nominal` | `calibration`), error-handling strategy
(typed `SarProcessorError` hierarchy). `TBD (PDR)`.

## <5> Software design

**<5.1>–<5.3>** Component decomposition and interfaces. `TBD (PDR)`.
**<5.4>** Per-component detailed design (one subsection per `C-PU-*`). `TBD (CDR)`.
**<5.5>** Internal-interface data structures. `TBD (CDR)`.

## <6> Traceability

`REQ-*` → components → test designs in the traceability matrix. `TBD (CDR)`.
