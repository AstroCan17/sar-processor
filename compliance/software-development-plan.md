# Software Development Plan (SDP)

| | |
|---|---|
| **Document** | Software Development Plan (SDP) |
| **DRD** | ECSS-E-ST-40C Rev.1, Annex O |
| **Container** | Management File (MGT) |
| **Project** | `sar-processor` — generic spaceborne SAR data processor |
| **Configuration item** | `gitlab.eopf.copernicus.eu/ipf/sar-processor` |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | SRR |
| **Status** | Draft for SRR |

> This SDP is the top-level management artefact of the ECSS software life cycle for the
> `sar-processor` project. It follows the ECSS-E-ST-40C Rev.1 Annex O DRD section structure
> and records the management and development approach, the life-cycle model, the review
> milestones, and — through the tailoring in §5.5 / §5.6 — the documentation tree the project
> commits to. The footprint is tailored to a Category C, single-developer ground-segment
> processor. This issue **completes the SRR baseline**: the life-cycle model, tailored DRL, work
> breakdown and the WP-5 implementation increment plan are committed; the per-milestone technical
> documents (SRS/ICD/DPM/ATBD/SDD/…) follow at their respective gates (PDR/CDR/QR).

## <1> Introduction

The `sar-processor` is an **operational ground-segment forward data processor** that transforms
**downlinked raw (Level-0) synthetic aperture radar (SAR) instrument source packets** into focused
and calibrated products: **Level-1 SLC** (single-look complex), **Level-1 GRD** (detected,
multi-looked, ground-range projected), with Level-2 ocean products TBC at SRR. It is designed as a
**generic spaceborne SAR processor**: the processing chain (L0 decode → Doppler-centroid estimation
→ range compression → azimuth focusing → radiometric calibration → multilook/detection → geocoding)
is sensor-agnostic and driven by a per-sensor configuration/profile. The first instantiated profile
is a **C-band SAR**, with **Sentinel-1 C-SAR** as the public reference dataset.

The processor is built on the **ESA Earth Observation Processing Framework (EOPF)**: each
processing stage is an EOPF Core Python Modules (CPM) `EOProcessingUnit` (`eopf == 2.8.1`),
products are handled as EOPF `EOProduct` objects, and outputs are written as cloud-native **Zarr**.
The platform machinery (CI, documentation toolchain, package layout, single-driver convention) is
**reused from the sibling `ipf/msi-processor` project** (see SRF, RD-12).

The purpose of this SDP is to describe the established management and development approach for the
software items of `sar-processor`, in accordance with ECSS-E-ST-40C Rev.1. It is prepared at
project start to establish the SRR baseline and is maintained throughout the life cycle.

## <2> Applicable and reference documents

**Applicable documents**

| Ref | Document |
|---|---|
| AD-1 | ECSS-E-ST-40C Rev.1 (30 April 2025) — Space engineering — Software |
| AD-2 | ECSS-Q-ST-80C Rev.2 (30 April 2025) — Space product assurance — Software product assurance |
| AD-3 | ECSS-M-ST-10C Rev.1 — Space project management — Project planning and implementation |
| AD-4 | ECSS-M-ST-40C — Configuration and information management |

**Reference documents**

| Ref | Document |
|---|---|
| RD-1 | SSS — `compliance/drd/sss-software-system-specification.md` |
| RD-2 | IRD — `compliance/drd/ird-interface-requirements.md` |
| RD-3 | SRS — `compliance/drd/srs-software-requirements.md` |
| RD-4 | ICD — `compliance/drd/icd-interface-control.md` |
| RD-5 | SDD — `compliance/drd/sdd-software-design.md` |
| RD-6 | DPM — `compliance/drd/dpm-data-processing-model.md` |
| RD-7 | ATBD — `compliance/drd/atbd-algorithm-theoretical-basis.md` |
| RD-8 | V&V Plan — `compliance/drd/vv-plan.md` |
| RD-9 | Traceability matrix — `compliance/traceability/traceability-matrix.md` |
| RD-10 | SUITP — `compliance/drd/suitp-unit-integration-test-plan.md` |
| RD-11 | DJF — `compliance/drd/djf-design-justification.md` |
| RD-12 | SRF — `compliance/drd/srf-software-reuse-file.md` |
| RD-13 | SPAP — `compliance/drd/spa-plan.md` |
| RD-14 | SRevP — `compliance/drd/srevp-software-review-plan.md` |
| RD-15 | Risk Register — `compliance/drd/risk-register.md` |

## <3> Terms, definitions and abbreviated terms

Terms per AD-1 clause 3. The full project SAR glossary (ISP, FDBAQ, SLC, GRD, GTC, focusing, RDA,
DCE, TOPSAR, burst, deramp, PRF/SWST, chirp/replica, σ0/β0/γ0, EAP/AAP/AAEP, NESZ, PSLR/ISLR, IRW,
ALE, ENL, IPF, ADF, SAFE, annotation, …) is collected in the SSS (RD-1) <3> and applies here.

## <4> Software life cycle management

**<4.1> Life cycle.** Incremental development within the ECSS review frame
**SRR → PDR → CDR → QR → AR**, mirroring the msi-processor precedent: requirements baseline at SRR,
architectural design + preliminary ICD/DPM/ATBD at PDR, detailed design + SUITP at CDR,
verification results at QR, acceptance at AR.

**Work breakdown (WP → milestone).**

| WP | Title | Milestone |
|---|---|---|
| WP-1 | Project setup (repo, CI, `ipf` group runner, milestones) | pre-SRR (done) |
| WP-2 | SRR documentation (SDP, SRevP, SPAP, Risk Register, SSS, IRD, initial SRF) | SRR |
| WP-3 | PDR documentation (SRS, V&V plan, ICD start, DPM, ATBD, preliminary SDD) | PDR |
| WP-4 | CDR documentation (detailed SDD+DJF, SUITP, final ICD, SRF, traceability matrix) | CDR |
| WP-5 | Implementation — SAR processing stages, decomposed into the increments below | post-CDR |
| WP-6 | Verification & validation (SVR, SUITR), release (SRelD/SRN), SUM | QR / AR |

**Implementation increment plan (WP-5, post-CDR).** WP-5 is decomposed into pedagogically-ordered
increments — **fundamentals before TOPSAR complexity**. The v1 target is IW/TOPSAR **SLC + GRD + GTC**,
validated against real Sentinel-1 data (tolerance-based, not bit-identical). Each increment carries a
teaching ATBD section + a reference notebook (authored during PDR/CDR as DPM breakpoint studies) that is
hardened — not rewritten — into `core.py`/`unit.py` after CDR.

| Inc | Scope | Principal artefacts |
|---|---|---|
| 0 | Ground zero: L0-package extract, one real IW datatake+ADFs into the data store, typed-but-empty package skeleton, point-target simulator, driver phases | `common/`, `exceptions/`, `sensors/profile.py`, empty `computing/<stage>/`, `product/*` stubs |
| 1 | L0 decode (FDBAQ) + product/annotation model + pre-processing | `computing/l0_decode/`, `computing/preproc/`, `product/{annotation,safe}.py` |
| 2 | Single-burst focusing (range + azimuth RDA); point-target then real burst | `computing/range_comp/`, `computing/azimuth_comp/` |
| 3 | Doppler-centroid estimation + TOPSAR deramp/UFR | `computing/doppler/`, `computing/topsar/` |
| 4 | Multi-burst deburst/merge → full IW SLC | `computing/topsar/` merge |
| 5 | Radiometric calibration (σ0/β0/γ0 + EAP) + thermal-noise | `computing/calibration/`, `computing/noise/` |
| 6 | GRD (detection / multilook / ground-range) | `computing/grd/` |
| 7 | GTC geocoding (Range-Doppler terrain correction + DEM) | `computing/geocode/` |
| 8 | Full-chain integration + calibration mode + QR hardening | `tests/it/`, `CALIBRATION_PHASES` |

Detailed activities are managed as GitLab issues assigned to the corresponding milestone.

**<4.2> Organisation.** Single developer (project owner) acting as designer, implementer and
verifier; reviews conducted asynchronously on the GitLab instance via MRs and milestone review
issues (SRevP, RD-14).

**<4.3> Development environment.** EOPF SDE: shared `cpm-build-environment` CI image, GitLab CI on
project runners, Python 3.11, EOPF CPM pinned (`eopf == 2.8.1`).

**<4.5> Risk management.** See Risk Register (RD-15).

## <5> Software development approach

**<5.1>–<5.4>** Development standards (PEP8 via black/flake8/isort at 120 columns, mypy strict on
the package, bandit security scanning), methods and tools follow the msi-processor conventions;
they are enforced by the CI pipeline (`.gitlab-ci.yml`). The **SAR-specific numerical addition** over
the msi toolchain is a fast-FFT backend for range/azimuth compression — `numpy.fft` as the deterministic
baseline, with `scipy.fft` / `pyFFTW` as an optional accelerated backend — declared in `pyproject.toml`
and justified in the SDD/SRF. The chosen FFT backend and the complex working dtype (`complex64`) are
fixed for reproducible CI budgets (SSS SYS-RAM-01); the design method (pure `core.py` + thin `unit.py`
`EOProcessingUnit` + CPM computing-model JSON, sensor-profile-driven) and the single mode-only pipeline
driver follow the msi-processor pattern.

### <5.5> Documentation plan

**<5.5.1>** The documentation tree lives in `compliance/` (authoritative markdown sources) and is
published through the Sphinx site (`docs/compliance/` symlinks). One document = one file.

#### <5.5.2> Tailored Document Requirements List (DRL)

*ECSS-E-ST-40C Rev.1 (engineering)*

| DRD | Annex | Decision | Delivered | File |
|---|---|---|---|---|
| SSS — Software System Specification | B | PRODUCE | SRR | `compliance/drd/sss-software-system-specification.md` |
| IRD — Interface Requirements Document | C | PRODUCE | SRR | `compliance/drd/ird-interface-requirements.md` |
| SRS — Software Requirements Specification | D | PRODUCE | PDR | `compliance/drd/srs-software-requirements.md` |
| ICD — Interface Control Document | E | PRODUCE | PDR (prelim) / CDR (final) | `compliance/drd/icd-interface-control.md` |
| SDD — Software Design Document | F | PRODUCE | CDR | `compliance/drd/sdd-software-design.md` |
| DJF — Design Justification | §4.2.4/5 | PRODUCE (light) | CDR | `compliance/drd/djf-design-justification.md` |
| DPM — Data Processing Model | — (EOPF DPR) | PRODUCE | PDR | `compliance/drd/dpm-data-processing-model.md` |
| ATBD — Algorithm Theoretical Basis | — (EO domain) | PRODUCE | PDR | `compliance/drd/atbd-algorithm-theoretical-basis.md` |
| SVerP / SValP — Verification & Validation Plans | I / J | PRODUCE (merged) | PDR | `compliance/drd/vv-plan.md` |
| SUITP — Unit & Integration Test Plan | K | PRODUCE | CDR | `compliance/drd/suitp-unit-integration-test-plan.md` |
| SVR — Verification Report | M | PRODUCE | QR | `compliance/drd/vv-report.md` |
| SUITR — Unit & Integration Test Report | K→M | PRODUCE | QR | `compliance/drd/suitr-unit-integration-test-report.md` |
| SRF — Software Reuse File | N | PRODUCE | SRR (initial) / CDR | `compliance/drd/srf-software-reuse-file.md` |
| SRevP — Software Review Plan | P | PRODUCE (light) | SRR | `compliance/drd/srevp-software-review-plan.md` |
| SRN / SRelD — Software Release Note | SRelD | PRODUCE | QR / each release | `compliance/drd/srn-software-release-note.md` |
| SUM — Software User Manual | H | PRODUCE | QR | `docs/sum/` |
| SMP — Software Maintenance Plan | T | TAILORED-OUT (light) | AR | maintenance = GitLab issues + SemVer |

*ECSS-Q-ST-80C Rev.2 + cross-discipline*

| Artefact | Decision | Delivered | File |
|---|---|---|---|
| SPAP — Software Product Assurance Plan | PRODUCE (light) | SRR | `compliance/drd/spa-plan.md` |
| Risk Register | PRODUCE | SRR (living) | `compliance/drd/risk-register.md` |
| Traceability matrix | PRODUCE | PDR (living) | `compliance/traceability/traceability-matrix.md` |
| CIDL — Configuration Item Data List | PRODUCE | QR | `compliance/drd/cidl-configuration-item-data-list.md` |
| SCF — Software Configuration File | PRODUCE | QR | `compliance/drd/scf-software-configuration-file.md` |
| QR report | PRODUCE | QR | `compliance/qr-qualification-review-report.md` |

### <5.6> Tailoring rationale

Category C, single-developer, ground-segment-only: documents merged or lightened exactly as in the
msi-processor precedent (V&V plans merged per Annex I/J; SMP tailored out in favour of the GitLab
issue tracker + SemVer releases; DJF kept light).

**Clause-5 tailoring summary (ECSS-E-ST-40C, Category C / Annex R).** Requirements, interface, design,
verification and validation clauses are applied in full (SSS/IRD → SRS/ICD → SDD → vv-plan → SVR).
Formal system-specification-language models (E-40 §5.2.7 / SSS <7>) are tailored out — concrete project
artefacts (the `EOProcessingUnit` pipeline graph, the profile schema, the EOProduct/Zarr data model, the
DPM/ATBD) serve the model role. Independent IV&V and separate PA/verification roles are replaced by
**automated CI gates + review checklists** (Category C, single developer). TAILORED-OUT with rationale:
SMP (light — GitLab issues + SemVer); SPAMR (subsumed by the SVR + milestone reviews); SVS (realised by
the test suite + vv-plan). Reuse is only of the **sensor-agnostic scaffold/process** from msi-processor:
the `product/` subpackage and the SAR-specific data types (`complex64`, per-burst grouping) and stage
set are **new development** recorded in the SRF (RD-12) — no structural identity with msi-processor is
levied.

## <6> Schedule and milestones

| Milestone | Scope | Target |
|---|---|---|
| SRR | Requirements baseline (SSS, IRD, SDP, SPAP, SRevP, Risk Register, initial SRF) | GitLab milestone |
| PDR | SRS, preliminary ICD, DPM, ATBD, V&V Plan | GitLab milestone |
| CDR | SDD, final ICD, DJF, SUITP, SRF, traceability matrix | GitLab milestone |
| QR | SVR, SUITR, SRN, CIDL, SCF, QR report, SUM | GitLab milestone |
| AR | Acceptance, delivery baseline | GitLab milestone |

Calendar dates are managed in the GitLab group `ipf` milestones, not duplicated here. The milestone
order is fixed **SRR → PDR → CDR → QR → AR**; implementation (WP-5, §4.1) starts only after CDR closure.

*End of SDP. Authored per ECSS-E-ST-40C Rev.1 Annex O.*
