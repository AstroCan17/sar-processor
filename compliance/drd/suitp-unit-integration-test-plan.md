# Software Unit & Integration Test Plan (SUITP)

| Field | Value |
|---|---|
| **Document** | SUITP — Software [Unit / Integration] Test Plan |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex K; ECSS-Q-ST-80C Rev.2 §6.2.8.2/§6.2.8.7, §6.3.5.22–25 |
| **Container** | Design Justification File (DJF) — `compliance/drd/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | CDR (Critical Design Review) |
| **Status** | Draft for SRR — skeleton |

> This SUITP is the **CDR extension** of the V&V Plan: it refines the V&V strategy into concrete
> unit/integration **test designs** (`TD-UT-*` / `TD-IT-*`) with procedures and pass criteria.
> Produced at CDR; this issue records only the scheme.

---

## <1> Test design scheme

- `TD-UT-<STAGE>-NN` — unit test designs, one file pair per stage
  (`tests/ut/computing/test_<stage>_core.py` + `test_<stage>_unit.py`).
- `TD-IT-NN` — integration test designs (`tests/it/`), end-to-end chain.

`TBD (CDR)`.

## <2> Test environment and data

CI runners (EOPF SDE image); fixture data as `.npy` under `tests/ut/computing/data/`; reference
Sentinel-1 subsets via the shared data-store. `TBD (CDR)`.

## <3> Pass criteria and coverage targets

`TBD (CDR)`.
