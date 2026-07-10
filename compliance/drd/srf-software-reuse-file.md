# Software Reuse File (SRF)

| Field | Value |
|---|---|
| **Document** | SRF — Software Reuse File |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex N (SRF DRD); ECSS-Q-ST-80C Rev.2 §6.2.7 |
| **Container** | Design Justification File (DJF) — `compliance/drd/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | SRR (initial) / CDR (final) |
| **Status** | Draft for SRR — skeleton |

> `sar-processor` deliberately reuses the **platform and process machinery** proven on the sibling
> `ipf/msi-processor` project; the SAR-specific processing algorithms are new development. Reused
> items are identified as **`SRF-RU-*`** with their verification pedigree.

---

## <1> Reused software items

| ID | Item | Origin | Scope of reuse | Pedigree |
|---|---|---|---|---|
| SRF-RU-01 | CI pipeline (stages, quality gates, pages/versioned-docs machinery) | `ipf/msi-processor` `.gitlab-ci.yml` | adopted verbatim, names adapted | CI green on donor project through QR |
| SRF-RU-02 | Documentation toolchain (Sphinx book theme conf, compliance symlink publishing, SUM skeleton) | `ipf/msi-processor` `docs/` | adopted verbatim | published donor site |
| SRF-RU-03 | Package/architecture conventions (C-COMMON / C-PU-\* / C-SENSORS layers; `core.py`+`unit.py` stage pattern; typed error hierarchy; single mode-only pipeline driver) | `ipf/msi-processor` | pattern reuse | donor SDD <5>, QR-verified |
| SRF-RU-04 | EOPF CPM runtime (`eopf == 2.8.1`) | ESA EOPF | as platform | ESA-maintained |
| SRF-RU-05 | Shared data-store fetch/publish mechanism (`ipf/data-store`) | `ipf/msi-processor` driver | `TBC (PDR)` | donor integration tests |

## <2> Reuse assessment

Per Annex N: fitness, modification needs and re-verification scope assessed per item.
`TBD (SRR)`.
