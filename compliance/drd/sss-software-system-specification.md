# Software System Specification (SSS)

| Field | Value |
|---|---|
| **Document** | SSS — Software System Specification |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex B |
| **Container** | EOPF SDE — `compliance/drd/` (source), published in online documentation (`docs/`) |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | SRR (System Requirements Review) |
| **Status** | Draft for SRR |

> This SSS is the highest-level specification of `sar-processor` and, together with the IRD, forms
> the requirements baseline and the primary input to the SRR. Per the SDP tailoring for a
> single-developer Category C project there is no external customer or separate system tier: the
> mission/ground-segment context that would otherwise sit in a parent system specification is folded
> into this document (clauses <1> and <4>). System-level requirements defined here (`SYS-*`) are
> decomposed into software requirements in the SRS (Annex D) at PDR.

---

## <1> Introduction

**Purpose.** This document specifies, at system level, the `sar-processor` software product: a
generic spaceborne **Synthetic Aperture Radar (SAR)** ground-segment **forward** data processor. It
transforms downlinked **RAW (Level-0)** SAR instrument source packets (ISPs) into focused,
calibrated and geolocated products — **Level-1 SLC** (Single Look Complex), **Level-1 GRD** (Ground
Range Detected) and geocoded terrain-corrected **GTC** imagery — through decoding, focusing,
radiometric calibration, detection/multi-looking and geocoding. The SSS captures *what* the
processor must do as a product within an Earth-observation ground segment — its capabilities,
performance and quality objectives, operational environment and system-level constraints —
independent of internal software design (the subject of the SDD, Annex F).

**Objective.** The SSS establishes the requirements baseline against which the software is validated
and accepted. It is the parent of the SRS: every software requirement traces back to a system
requirement (`SYS-*`) defined here, and every system requirement is associated with a validation
method (clause <5.1>, <6>).

**Content.** Clause <4> gives the general description (product perspective, capabilities,
constraints, operational environment, assumptions). Clause <5> states the specific system
requirements grouped by type. Clause <6> defines the verification, validation and integration
requirements. Clause <7> addresses system models.

**Reason for preparation.** The project is an **integration and ECSS productisation** effort. The
SAR processing chain's mathematical basis is established public engineering (ESA/Aresys Sentinel-1
Level-1 Detailed Algorithm Definition and the SentiWiki technical corpus, RD-05/RD-09); it is *not*
new-algorithm research. The SSS turns that algorithmic basis plus the EOPF platform into a
documented, verifiable, configuration-driven product. The chain is **sensor-agnostic**, driven by a
per-sensor *profile*; the first instantiated profile is **C-band SAR with Sentinel-1 C-SAR as the
public reference dataset and acquisition mode Interferometric Wide (IW, TOPSAR)**.

> **Contrast with the sibling `msi-processor` (informative).** Both products share the sensor-agnostic
> EOPF scaffold, but SAR is an **active, coherent, phase-preserving** instrument whereas MSI is
> passive optical. Consequently the SAR chain and its quality budgets differ fundamentally: L0 is an
> *unfocused complex echo stream* (not an image), the core work is **focusing** (range/azimuth
> compression), and quality is expressed as impulse-response (`PSLR`/`ISLR`/`IRW`), geolocation
> (`ALE`), noise-floor (`NESZ`) and **phase-preservation** budgets. No structural identity with
> `msi-processor` is levied; only the scaffold/process is reused (SRF, RD-12).

---

## <2> Applicable and reference documents

### Applicable documents (AD)

| Id | Document | Reference |
|---|---|---|
| AD-01 | ECSS Space engineering — Software | ECSS-E-ST-40C Rev.1 (30 April 2025) |
| AD-02 | ECSS Space product assurance — Software product assurance | ECSS-Q-ST-80C Rev.2 |
| AD-03 | ECSS System engineering — General requirements | ECSS-E-ST-10C Rev.1 |
| AD-04 | `sar-processor` Software Development Plan (SDP) | `compliance/software-development-plan.md` |
| AD-05 | EOPF Core Python Modules (CPM) — Product Structure and Format Definition (PSFD) / common data model | EOPF CPM documentation (`eopf == 2.8.1`) |

### Reference documents (RD)

| Id | Document | Reference |
|---|---|---|
| RD-01 | ECSS Software engineering handbook | ECSS-E-HB-40A |
| RD-02 | ECSS Technical requirements specification | ECSS-E-ST-10-06C |
| RD-03 | ECSS Risk management | ECSS-M-ST-80C |
| RD-04 | `sar-processor` Software Reuse File (SRF) | `compliance/drd/srf-software-reuse-file.md` |
| RD-05 | Sentinel-1 Level-1 Detailed Algorithm Definition (IPFDPM) — focusing / DCE / calibration algorithm basis | ESA DI-MPC-IPFDPM (vault: `wiki/sources/s1-l1-detailed-algorithm-definition.md`) |
| RD-06 | `sar-processor` Interface Control Document (ICD) | `compliance/drd/icd-interface-control.md` |
| RD-07 | EOPF CPM API documentation | EOPF CPM API (`eopf == 2.8.1`) |
| RD-08 | Cloud-native data conventions | Zarr v2/v3, CF metadata, STAC |
| RD-09 | Sentinel-1 technical reference corpus (products, radiometric calibration, TOPS deramping, geocoding, thermal denoising, ADF specification) | Vault `wiki/` (SentiWiki / ESA MPC / DLR / UZH) |
| RD-10 | Sentinel-1 Product Definition & Product Specification | ESA S1-RS-MDA-52-7440/7441 (vault: `wiki/sources/s1-product-definition.md`, `s1-product-specification.md`) |
| RD-11 | Sentinel-1 IPF Auxiliary Product Specification (ADF set) | ESA S1-RS-MDA-52-7443 (vault: `wiki/sources/s1-ipf-auxiliary-product-specification.md`) |
| RD-12 | `msi-processor` reuse baseline (scaffold / process heritage) | `gitlab.eopf.copernicus.eu/ipf/msi-processor` |

---

## <3> Terms, definitions and abbreviated terms

Only terms not already defined in the AD/RD are listed. SAR-domain terms are collected here and are
the project glossary referenced by the IRD and SDP.

| Term / abbr. | Definition |
|---|---|
| SAR | Synthetic Aperture Radar (active, coherent microwave imaging instrument) |
| Profile | Per-sensor configuration set (radar constants, geometry, polarisations, calibration references, processing parameters) that specialises the generic chain for one instrument/mode |
| ISP | Instrument Source Packet — the Level-0 space-packet carrying compressed echo/calibration/noise samples + secondary header |
| FDBAQ | Flexible Dynamic Block Adaptive Quantization — the S1 echo compression scheme (Huffman-coded) decoded at L0 |
| L0 (RAW) | Level-0: compressed instrument source packets + annotation; the unfocused complex echo stream |
| SLC | Single Look Complex — focused, slant-range, **phase-preserving complex** L1 product (per-burst for TOPSAR) |
| GRD | Ground Range Detected — focused, **detected** (amplitude), multi-looked, ground-range-projected L1 product |
| GTC / GEC | Geocoded Terrain-Corrected (DEM) / Geocoded Ellipsoid-Corrected — map-projected geometry classes |
| Focusing | Conversion of the unfocused echo to an image via range compression (chirp matched filter) + azimuth compression (synthetic aperture) |
| RDA | Range-Doppler Algorithm — the focusing algorithm used by the S1 IPF |
| Range / azimuth compression | Matched-filtering in the range (fast-time) / azimuth (slow-time) direction |
| RCMC / SRC | Range Cell Migration Correction / Secondary Range Compression (RDA sub-steps) |
| DCE | Doppler Centroid Estimation (absolute from orbit/attitude; fine from data via ACCC) |
| TOPSAR | Terrain Observation by Progressive Scans — S1 IW/EW mode; azimuth beam-steering → bursts + azimuth-Doppler ramp |
| Burst / deburst | TOPSAR azimuth acquisition unit / the merge of focused bursts into a continuous image |
| De-ramp / re-ramp | Removal/reapplication of the TOPSAR azimuth-steering phase ramp (mandatory before any resampling) |
| PRF / SWST | Pulse Repetition Frequency / Sampling Window Start Time (instrument timing from ISP headers) |
| Chirp / replica | Linear-FM transmitted pulse / its reconstruction used as the range matched filter |
| σ0 / β0 / γ0 | Radiometric backscatter conventions (sigma/beta/gamma nought) |
| EAP / AAP / AAEP | Elevation / Azimuth Antenna Pattern / Azimuth Antenna Element Pattern (calibration corrections) |
| NESZ | Noise-Equivalent Sigma Zero — the σ0 of the instrument noise floor |
| PSLR / ISLR | Peak / Integrated Side-Lobe Ratio — impulse-response (focusing) quality metrics |
| IRW | Impulse Response Width — the −3 dB main-lobe width = spatial resolution |
| ALE | Absolute Location Error — geolocation accuracy (range/azimuth) |
| ENL | Equivalent Number of Looks — speckle-reduction measure of a multi-looked product |
| IPF | Instrument Processing Facility — the reference (ESA) Level-1/2 processor; its version gates corrections |
| ADF | Auxiliary Data File (AUX_CAL, AUX_INS, AUX_PP1, AUX_POE/RES/PRE, AUX_ATT, DEM) |
| DEM | Digital Elevation Model |
| SAFE | Standard Archive Format for Europe — the S1 product packaging (manifest + measurement + annotation) |
| QA | Quality assurance / quality indicators (per-pixel flags and masks) |
| CPM / EOProduct / EOProcessingUnit | EOPF Core Python Modules / CPM in-memory product object / CPM processing-stage unit |
| Zarr / EOPF / SDE | Cloud-native chunked array storage / Earth Observation Processing Framework (ESA) / EOPF cloud development & processing environment |
| DPM / ATBD | Data Processing Model / Algorithm Theoretical Basis Document (per-stage algorithm basis, PDR) |
| T / A / I / R | Validation/verification methods: Test / Analysis / Inspection / Review of design |

---

## <4> General description

### <4.1> Product perspective

`sar-processor` is a **software product within an Earth-observation ground segment**. In the wider
mission, a spaceborne SAR satellite acquires coherent microwave echoes and downlinks RAW (Level-0)
data; the ground segment ingests, archives and processes that data into user-facing products.
`sar-processor` occupies the **payload data processing** function: it consumes Level-0 SAR ISPs plus
auxiliary/calibration data (ADFs) and produces focused, calibrated and geolocated products up to
L1 SLC, L1 GRD and geocoded GTC. (Level-2 ocean products — OWI/OSW/RVL — are **out of scope for the
current baseline**, TBC at a later increment.)

The product is **sensor-agnostic by design**: the processing chain is fixed, while the
instrument-specific behaviour is supplied as a per-sensor *profile*. The first instantiated profile
is C-band SAR (Sentinel-1 C-SAR, IW/TOPSAR). Because SAR products are **coherent and
phase-preserving**, the chain maintains complex (I/Q) data through focusing and preserves phase into
the SLC product (a prerequisite for interferometric use downstream).

The product does **not** replace a specific legacy system; it is a new, EOPF-native implementation.
The ESA Sentinel-1 IPF is used as the **numerical cross-validation reference** (clause <6.2>), not
replaced in place. Upstream (reception, demodulation, downlink to L0) and downstream (archiving,
cataloguing, dissemination, Level-2 geophysical retrieval) ground-segment functions are external and
not specified here.

### <4.2> General capabilities

The software provides the end-to-end L0→L1→GTC capability, decomposed by processing stage:

- **Ingestion & decoding (L0):** ingest Level-0 SAR ISPs and the profile-selected ADFs; decode the
  compressed echo (FDBAQ), reconstruct instrument timing (PRF, SWST) from the ISP headers, and
  de-multiplex per sub-swath / polarisation into complex channels.
- **Pre-processing:** I/Q bias removal, internal-calibration and transmitted-**replica**
  reconstruction (for range matched-filtering and spectrum whitening), missing-line detection.
- **Doppler-centroid estimation (DCE):** absolute Doppler centroid from orbit & attitude and fine
  estimation from the data; for TOPSAR, azimuth-steering de-ramp prior to estimation.
- **Focusing to SLC:** **range compression** (chirp matched filter) and **azimuth compression**
  (Range-Doppler Algorithm — SRC, RCMC, azimuth matched filter), preserving phase; for TOPSAR,
  azimuth de-ramp/re-ramp, spectral unfolding and **deburst/merge** of the focused bursts and
  sub-swaths into a continuous SLC.
- **Radiometric calibration:** application of the σ0/β0/γ0 calibration (range look-up tables folding
  the absolute constant, elevation antenna pattern and range-spreading loss), elevation-antenna-
  pattern (gain **and** phase) correction, and optional thermal-noise removal.
- **GRD generation:** range weighting, azimuth multi-looking, TOPSAR de-scalloping, **detection**
  (power), and slant-range-to-ground-range projection.
- **GTC geocoding:** Range-Doppler terrain correction using orbit and a DEM, mapping the product to
  a cartographic grid (GTC with DEM; GEC on the ellipsoid where no DEM is available).
- **Product generation:** output of cloud-native **Zarr** `EOProduct`s conformant to the EOPF data
  model, carrying acquisition/processing metadata, provenance and per-pixel QA flags.
- **Configuration / profile management** and **pipeline orchestration**: each stage is a CPM
  `EOProcessingUnit`; stages are chainable, individually runnable and chunked (per burst / sub-swath)
  for bounded-memory / parallel execution.

**States and modes (informative).** At system level the processor exhibits: *configured/idle*
(profile and inputs resolved, ready), *processing* (one or more stages executing), and
*error/aborted* (a stage failed; outputs flagged, no partial product silently published). Two
production **modes** are foreseen: **nominal** (L0→SLC→GRD→GTC) and **calibration** (internal-cal /
replica characterisation and cross-check). The processor is a non-resident batch component — no
continuous resident or real-time mode.

### <4.3> General constraints

- The product **shall be built on the EOPF CPM** (`EOProcessingUnit`, `EOProduct`) pinned to
  `eopf == 2.8.1`, matching the SDE build image.
- Products **shall be cloud-native Zarr** conforming to the EOPF data model (AD-05).
- The implementation language is **Python 3.11**.
- The processing algorithms **reuse the established public mathematical basis** (RD-05/RD-09); the
  project is an integration/productisation effort, not new-algorithm research. Bit-identical
  reproduction of the reference IPF output is **not** an objective (it would require the reference
  IPF binary); correctness is demonstrated against **tolerance budgets** (clause <5.9>, <6.2>).
- **Data policy:** source code is public (Apache-2.0); raw input data and instrument calibration
  (ADFs) are **private** — never committed, never used in public CI. The private calibration set may
  be held in the project's Studio VM data store and referenced at run time.
- The project is **single-developer, Category C**; process rigour is achieved through automated
  tooling and checklists rather than independent organisational roles.

### <4.4> Operational environment

**Narrative.** `sar-processor` runs as a batch payload-data processor in a cloud-native Linux
environment. The reference operational and development environment is the **EOPF SDE**: a container
image based on `registry.eopf.copernicus.eu/sde/...`, with optional Dask-based parallelism and
object storage (S3-compatible) or POSIX filesystem for Zarr input/output. The same software also
runs locally / on the Studio VM for numerical verification against private real data.

**Context (external exchanges).** Detailed in the ICD (RD-06):

| Direction | Counterpart | Exchange |
|---|---|---|
| Input | Upstream L0 production (reception/downlink) | Level-0 SAR product (SAFE: ISPs + annotation) |
| Input | Auxiliary/calibration store (**private**, Studio VM) | AUX_CAL (EAP/AAP/AAEP/K_abs), AUX_INS (roll-steering/decode tables/timeline), AUX_PP1 (processing params), AUX_POE/RES/PRE (orbit), AUX_ATT (attitude), DEM |
| Input | Configuration store | Per-sensor profile + production parameters |
| Output | Downstream archive / dissemination | `SLC` / `GRD` / `GTC` `EOProduct` (Zarr) + QA + metadata |
| Output | Operations / monitoring | Processing logs, reports, QA summaries |

**Computer infrastructure.** Target: x86-64 Linux, multi-core CPU, no GPU required; RAM and storage
scale with sub-swath/burst size and chunking; optional Dask cluster for horizontal scaling.
Constraint: the public CI runner is a **shell executor** with no container runtime, Dask gateway or
S3 — jobs requiring those are non-blocking in CI, and numerical verification on real data is
performed locally / on the Studio VM (clause <6>).

### <4.5> Assumptions and dependencies

- **A-1** — Level-0 SAR products (ISPs + annotation) are available and well-formed; reception/downlink
  are done upstream and out of scope.
- **A-2** — A complete, version-controlled ADF set matching the input's **IPF version** exists per
  profile (AUX_CAL, AUX_INS, AUX_PP1, orbit, attitude, DEM). This data is private and supplied at run
  time, not embedded in the software.
- **A-3** — The public algorithm basis (RD-05/RD-09) is correct and sufficient for the targeted
  accuracy; the project integrates rather than re-derives it.
- **A-4** — `eopf == 2.8.1` (CPM) and the EOPF Zarr data model are stable for the development baseline,
  and support **complex** (I/Q) variables and per-burst grouping (or a documented convention exists —
  tracked as a project risk, RD-03).
- **A-5** — DEM and orbit/attitude auxiliaries cover the processed scene's footprint and epoch.
- **A-6** — A reference Sentinel-1 product set (matching L0 + L1 SLC/GRD + ADFs, plus point-target /
  corner-reflector or stable-σ0 ground truth) is available locally / on the Studio VM for numerical
  validation (clause <6.2>).

---

## <5> Specific requirements

### <5.1> General

- **a.** Each system requirement is uniquely identified by a `SYS-<group>-<nn>` tag.
- **b.** Where requirements are expressed through schemas/models (the profile JSON schema, the CPM
  computing-model JSON, the EOProduct data model), identifiers are assigned within the schema for
  traceability.
- **c.** Each requirement is associated with a **validation method** — **T** (Test), **A** (Analysis),
  **I** (Inspection), **R** (Review of design) — baselined at version 1.0 (this issue). The
  requirement-to-method mapping is consolidated in the project traceability matrix
  (`compliance/traceability/`).

> Performance figures that depend on instrument calibration (radiometric, geolocation and focusing
> budgets) are expressed as **per-profile budget parameters** (clause <5.9>). Their baseline
> numerical values are held in the private auxiliary/calibration store and verified locally; the
> public Sentinel-1 specification values (RD-10) are cited as *informative* references only.

### <5.2> Capabilities requirements

System behaviour and associated performance, organised by capability (processing stage).

**Ingestion & L0 decoding**

- **SYS-CAP-01** — The system shall ingest Level-0 SAR products (ISPs + annotation) and the
  auxiliary/calibration data resolved by the active profile, and shall reject or flag inputs that
  fail structural and metadata legality checks before processing. *(Validation: T)*
- **SYS-CAP-02** — The system shall decode the compressed Level-0 echo (FDBAQ), reconstruct
  instrument timing (PRF, SWST, acquisition time) from the ISP secondary headers, detect lost/missing
  lines, and de-multiplex the stream per sub-swath and polarisation into complex (I/Q) channels, per
  the DPM (RD-05). *(Validation: T)*

**Focusing to SLC**

- **SYS-CAP-03** — The system shall pre-process the decoded echo (I/Q bias removal, transmitted-
  replica / internal-calibration reconstruction, missing-line handling) and estimate the Doppler
  centroid (absolute from orbit/attitude and fine from the data), per the DPM. *(Validation: T, A)*
- **SYS-CAP-04** — The system shall **focus** the echo to a Single Look Complex (SLC) product by
  range compression and azimuth compression (Range-Doppler Algorithm), **preserving phase**. Focusing
  quality shall meet the per-profile impulse-response budgets — resolution `IRW_RG`/`IRW_AZ`, peak
  side-lobe ratio `PSLR`, integrated side-lobe ratio `ISLR` — verified on a point-target /
  corner-reflector response. *(Validation: T, A)*
- **SYS-CAP-05** — For TOPSAR acquisition modes (e.g. IW/EW), the system shall perform azimuth
  de-ramp/re-ramp and spectral unfolding, and shall merge focused bursts and sub-swaths (**deburst /
  merge**) into a continuous SLC without introducing seams or phase discontinuities across burst
  overlaps. *(Validation: T, A)*
- **SYS-CAP-06** — The SLC product shall be **phase-preserving** to interferometric grade
  (`PHASE_PRES`): all focusing and calibration operations shall maintain the relative phase required
  for downstream interferometric use, verified by phase continuity across burst overlaps and (where
  reference data exist) against the reference product. *(Validation: A, T)*

**Radiometric calibration**

- **SYS-CAP-07** — The system shall radiometrically calibrate the product to the selectable backscatter
  conventions σ0/β0/γ0 using the calibration look-up tables and applying the elevation-antenna-pattern
  (gain **and** phase) and range-spreading-loss corrections, per the DPM and the active profile.
  Radiometric accuracy shall meet the per-profile budget `RAD_ACC` on stable/reference targets.
  *(Validation: T, A)*
- **SYS-CAP-08** — The system shall support optional **thermal-noise removal** (subtract-in-power
  using the noise vectors), disabled by default; where enabled it shall flag rather than silently
  clip non-physical (negative) results. The noise-floor `NESZ` shall be characterisable. *(Validation:
  T, A)*

**GRD generation and geocoding**

- **SYS-CAP-09** — The system shall generate a Ground Range Detected (GRD) product by range
  weighting, azimuth multi-looking, TOPSAR de-scalloping, **detection** (power) and slant-range-to-
  ground-range projection; the multi-looked product shall meet the per-profile speckle budget `ENL`.
  *(Validation: T, A)*
- **SYS-CAP-10** — The system shall geocode the product by Range-Doppler terrain correction using
  orbit and a DEM (**GTC**; ellipsoid **GEC** where no DEM is available), meeting the per-profile
  geolocation budget `ALE_RG`/`ALE_AZ` on ground reference (corner reflectors / GCPs). *(Validation:
  A, T)*

**Version gating, product generation, configuration and orchestration**

- **SYS-CAP-11** — Corrections whose definition depends on the reference processor version shall be
  **IPF-version-gated**: the system shall read the input's IPF version (product manifest) and apply
  the correction variant valid for that version (e.g. antenna-pattern phase, noise-vector form),
  within the profile's `supported_ipf_versions` envelope. *(Validation: T, R)*
- **SYS-CAP-12** — The system shall write outputs as cloud-native **Zarr** `EOProduct`s conformant to
  the EOPF data model (AD-05), each carrying acquisition/processing metadata, provenance, and
  per-pixel QA flags (including no-data, missing-line, black-fill/SWST, saturation, thermal-noise-
  subtracted, deramp-invalid, layover/shadow, cal-invalid). *(Validation: I, T)*
- **SYS-CAP-13** — The system shall be **sensor-agnostic**: all instrument-specific behaviour shall be
  supplied through the per-sensor profile and the product annotation, with no instrument constants
  hard-coded in the processing core. *(Validation: R, T)*
- **SYS-CAP-14** — Each processing stage shall be implemented as a CPM `EOProcessingUnit`; stages
  shall be runnable individually, as a sub-chain, or as the full L0→GTC chain. *(Validation: T)*
- **SYS-CAP-15** — The system shall support chunked / per-burst / per-sub-swath processing so that
  large SAR scenes are processed within bounded memory, optionally distributed via Dask. *(Validation:
  T, A)*

**Real-time behaviour and constraints.** The processor has **no hard real-time constraints**; it is a
throughput-oriented batch component. Timing is expressed as a throughput objective in clause <5.5.2>,
not as a real-time deadline. *HMI capability and on-board control procedures are not applicable
(CLI / Python API only, no on-board element).*

### <5.3> System interface requirements

Interface requirements are listed here and detailed in the ICD (RD-06); the IRD (Annex C) states them
at requirement level (`REQ-IF-*`).

- **SYS-IF-01 (software interfaces)** — The system shall expose its capabilities through a Python API
  built on the CPM (`EOProcessingUnit`, `EOProduct`, `EOZarrStore`) and a command-line interface for
  batch invocation. *(Validation: T, I)*
- **SYS-IF-02 (data — input)** — The system shall consume Level-0 SAR products and ADFs in the formats
  defined in the ICD; the profile and the product annotation/IPF-version select the concrete sources
  and versions. *(Validation: T)*
- **SYS-IF-03 (data — output)** — The system shall produce `SLC`/`GRD`/`GTC` `EOProduct`s as Zarr
  stores on object storage (S3-compatible) or POSIX filesystem, per the ICD. *(Validation: T, I)*
- **SYS-IF-04 (communication / storage)** — Storage and (optional) Dask cluster interfaces shall be
  configurable (endpoint, credentials via environment/CI variables) and shall not require a resident
  network service for single-host operation. *(Validation: T)*
- **SYS-IF-05 (HMI)** — Human interaction shall be limited to the CLI, configuration files and
  logs/reports; no graphical user interface is provided. *(Validation: I)*

### <5.4> Adaptation and missionization requirements

- **SYS-ADP-01** — All data that varies by sensor or acquisition mode shall be externalised into the
  **profile**, including at least: carrier frequency / wavelength; acquisition mode; polarisation
  channels; sub-swath static definitions (nominal incidence, PRF band); the ADF bindings (AUX_CAL,
  AUX_INS, AUX_PP1, orbit, attitude, DEM by URI); the supported-IPF-version envelope; and per-stage
  processing parameters/toggles. *(Validation: R, T)*
- **SYS-ADP-02** — **Per-acquisition** varying parameters — azimuth steering rate, Doppler-centroid and
  azimuth-FM-rate polynomials, burst times, SWST, calibration/noise LUTs — shall be read from the
  **product annotation** at run time and shall **not** be stored in the profile or hard-coded.
  *(Validation: T, R)*
- **SYS-ADP-03** — Site- and epoch-dependent data (DEM, orbit, attitude) shall be selected by reference
  from the profile / run configuration, not embedded in the software. *(Validation: T)*
- **SYS-ADP-04** — The profile schema shall be versioned and validated at load time; an invalid or
  incomplete profile shall cause a controlled, reported failure before processing. *(Validation: T)*

> The auxiliary/calibration store acts as the "system database" of ECSS-E-ST-40 5.2.4.4; it is private
> and out of the source repository (clause <4.3>). The annotation-vs-ADF split (per-acquisition vs
> sensor/version constants) is a defining SAR characteristic and is enforced at this level.

### <5.5> Computer resource requirements

#### <5.5.1> Computer hardware resource requirements

- **SYS-RES-01** — The system shall run on x86-64 Linux with a multi-core CPU and shall not require a
  GPU. *(Validation: T)*
- **SYS-RES-02** — The system shall operate against object storage (S3-compatible) or a POSIX
  filesystem for input/output; no other specialised hardware is required. *(Validation: T)*

#### <5.5.2> Computer hardware resource utilization requirements

- **SYS-RES-03** — Peak memory shall be bounded by the configured chunk granularity (per burst /
  per sub-swath) so that a datatake is processed within a per-worker memory budget `MEM_BUDGET`.
  *(Validation: A, T)*
- **SYS-RES-04** — End-to-end L0→GTC throughput shall meet the per-profile objective `THRU_SCENE`
  (datatakes or km²/hour on a stated reference configuration), measured locally. *(Validation: A, T)*

#### <5.5.3> Computer software resource requirements

- **SYS-RES-05** — The system shall run on Python 3.11 with EOPF CPM `eopf == 2.8.1` and its declared
  dependency stack (numpy, xarray, zarr, Dask, and the SAR numerical additions — FFT backend —
  recorded in the SRF (RD-04) and `pyproject.toml`). No proprietary runtime is required. *(Validation:
  I, T)*

### <5.6> Security requirements

- **SYS-SEC-01** — Source code shall be public under Apache-2.0; raw input data and instrument
  calibration ADFs shall remain **private** and shall never be committed to the repository nor used in
  public CI. *(Validation: I, R)*
- **SYS-SEC-02** — Credentials and access tokens (storage, registry, Dask, Studio VM) shall be provided
  exclusively via environment / CI variables and shall never appear in source or product artefacts.
  *(Validation: I, T)*
- **SYS-SEC-03** — Access to the private auxiliary/calibration store (Studio VM data store) shall be
  controlled and independent of the public code repository. *(Validation: R)*

### <5.7> Safety requirements

- **SYS-SAF-01** — The product is a ground-segment data processor with no command authority over the
  space segment and no direct human-safety hazard; therefore no safety-critical functions are defined.
  The principal residual hazard class is **product-data integrity** (e.g. a mislabelled, mis-calibrated
  or phase-corrupted product); this shall be mitigated by QA flags, provenance metadata and fail-stop
  behaviour (SYS-CAP-12, SYS-OPS-02). *(Validation: R)*

### <5.8> Reliability and availability requirements

- **SYS-RAM-01** — Processing shall be **deterministic and reproducible**: identical inputs, auxiliary
  data, profile version and processor version shall yield identical products (bit-identical where the
  operation is deterministic — e.g. FDBAQ decode; otherwise within a documented numerical tolerance —
  e.g. FFT-based focusing). *(Validation: T, A)*
- **SYS-RAM-02** — Processing shall be **resumable / re-runnable** at stage granularity; a failed run
  shall not leave a partial product presented as complete. *(Validation: T)*
- **SYS-RAM-03** — Service availability is a property of the hosting ground segment, not of this batch
  component; no continuous-availability target is levied on the software itself. *(Validation: R)*

### <5.9> Quality requirements

- **SYS-QUA-01** — The software shall conform to ECSS-Q-ST-80C Rev.2 for Category C and to the project
  coding standards enforced by the toolchain (black, isort, flake8, mypy, bandit, xenon). *(Validation:
  I)*
- **SYS-QUA-02** — Automated test coverage shall meet the project gate (inherited EOPF threshold),
  measured by the unit-test CI job. *(Validation: T)*
- **SYS-QUA-03** — The software shall be **portable / relocatable** between the EOPF SDE, the Studio VM
  and a local workstation without code changes (configuration only). *(Validation: T, I)*
- **SYS-QUA-04** — Numerical product-quality objectives shall be met per the following **per-profile
  budget parameters**, validated locally on mission-representative real data (informative public
  Sentinel-1 reference values in brackets, RD-10):
  - focusing: `IRW_RG`/`IRW_AZ` (resolution), `PSLR` (≈ −13.3 dB unweighted point target; deeper with
    the product's weighting window), `ISLR`;
  - geolocation: `ALE_RG`/`ALE_AZ` (target ≤ ~1 pixel with precise orbit);
  - radiometry: `RAD_ACC` (≈ 1 dB, 3σ), `NESZ` (≤ ~ −22 dB);
  - speckle: `ENL` (≈ nominal number of looks);
  - phase: `PHASE_PRES` (interferometric-grade phase continuity). *(Validation: A, T)*
- **SYS-QUA-05** — Maintainability shall be supported by reusability of the generic chain across
  profiles and by bounded cyclomatic complexity (xenon thresholds). *(Validation: I, A)*

### <5.10> Design requirements and constraints

- **SYS-DES-01 (architecture)** — Each processing stage shall be a CPM `EOProcessingUnit` and products
  shall be `EOProduct` instances; the architecture shall be a config-driven, sensor-agnostic pipeline
  with a framework-free algorithmic core per stage. *(Validation: R)*
- **SYS-DES-02 (standards)** — The software shall conform to the ECSS-E-ST-40C / Q-ST-80C tailoring in
  the SDP (AD-04) and to PEP 8 (enforced by the toolchain). *(Validation: I)*
- **SYS-DES-03 (existing components / COTS)** — The software shall reuse EOPF CPM, numpy, xarray, zarr,
  Dask and a declared FFT backend per the SRF (RD-04); no customer-furnished components are levied.
  *(Validation: I)*
- **SYS-DES-04 (data standard)** — Outputs shall use Zarr with EOPF/CF-style metadata and STAC-
  compatible cataloguing fields (RD-08, AD-05); complex (I/Q) SLC variables and per-burst grouping
  shall follow a documented convention. *(Validation: I, T)*
- **SYS-DES-05 (language / version pin)** — Implementation shall be Python 3.11 with `eopf == 2.8.1`
  pinned. *(Validation: I)*
- **SYS-DES-06 (naming)** — Product, variable and metadata naming shall follow the EOPF data-model and
  the S1 SAFE-naming conventions. *(Validation: I)*
- **SYS-DES-07 (flexibility and expansion)** — Adding a new sensor/mode shall be achievable by adding a
  profile (and its private auxiliaries) without modifying the processing core. *(Validation: T, R)*
- **SYS-DES-08 (data confidentiality)** — No raw or calibration data shall be required at build time or
  embedded in any delivered artefact. *(Validation: I)*

*Utilization of HMI standards is not applicable (no GUI).*

### <5.11> Software operations requirements

- **SYS-OPS-01** — The system shall be operable as a batch job (CLI or Python API), invoked with a
  profile, an input reference and an auxiliary-data reference, optionally restricted to a single stage,
  a sub-chain, or a production mode (nominal / calibration). *(Validation: T)*
- **SYS-OPS-02** — Each run shall emit structured logs and a processing report sufficient to determine
  success/failure, parameters used and product provenance (including the IPF version applied); on
  failure it shall exit non-zero and shall not publish a misleading product. *(Validation: T)*

### <5.12> Software maintenance requirements

- **SYS-MNT-01** — Maintenance shall be performed under a GitLab issue → branch → merge-request workflow
  with SemVer releases, by the single developer acting in the supplier roles. *(Validation: R)*
- **SYS-MNT-02** — Calibration/auxiliary and IPF-version-gating updates shall be deliverable by
  replacing the referenced private data / extending the version envelope, without changing the
  processing core (clause <5.4>). *(Validation: T, R)*
- **SYS-MNT-03** — A documented procedure shall govern bumping the pinned `eopf` version and re-running
  the full V&V before re-baselining. *(Validation: R)*

### <5.13> System and software observability requirements

- **SYS-OBS-01** — The system shall record, in the product and/or report, the processing chain version,
  profile version, ADF versions, the input IPF version applied, and key parameters (processing
  provenance) so that any product can be reproduced. *(Validation: I, T)*
- **SYS-OBS-02** — Per-pixel QA flags and per-stage quality indicators (focusing metrics, saturation,
  missing lines, black-fill, thermal-noise-subtracted, layover/shadow, no-data) shall be carried
  through to the output product. *(Validation: T)*
- **SYS-OBS-03** — Unit and integration test reports shall be generated and published with the
  documentation (SUITR). *(Validation: I)*

### <5.14> Security constraints for the software development and integration environment

- **SYS-DEVSEC-01** — Development and integration shall use the self-hosted EOPF SDE GitLab; CI shall run
  on the SDE shell executor with secrets injected as masked CI variables. *(Validation: I)*
- **SYS-DEVSEC-02** — The CI pipeline shall run dependency and code security scanning (bandit, Trivy) and
  quality gating (SonarQube); private real data shall never be introduced into the CI environment.
  *(Validation: I, T)*
- **SYS-DEVSEC-03** — Pre-commit hooks shall enforce hygiene (formatting, large-file and secret-leak
  prevention) before code enters the repository. *(Validation: I)*

### <5.15> Secure software delivery requirements

- **SYS-DEL-01** — Releases shall be delivered as versioned Python wheels published to the GitLab package
  registry and as versioned documentation via GitLab Pages, built reproducibly by CI from a tagged
  commit. *(Validation: T, I)*
- **SYS-DEL-02** — Delivered artefacts shall contain no private data; integrity is anchored to the Git
  tag and registry record of the delivered version (cf. SCF / SRN). *(Validation: I)*

---

## <6> Verification, validation and system integration

### <6.1> Verification and validation process requirements

- **SYS-VV-01** — The V&V process shall combine **T/A/I/R** methods (clause <5.1>): automated
  unit/integration tests, static analysis, design/inspection review against this SSS, and numerical
  analysis against the DPM/ATBD (RD-05). *(Validation: R)*
- **SYS-VV-02** — Public CI shall execute all tests that do **not** require private data, a container
  runtime, a Dask gateway or S3 — including a **synthetic point-target focusing test** (Tier A) that
  needs no private data; tests needing those shall be marked non-blocking in CI and executed locally.
  *(Validation: I)*
- **SYS-VV-03** — Security V&V (dependency/code scanning, secret-leak prevention, confidentiality of
  private data) shall be part of the V&V process. *(Validation: I, T)*

### <6.2> Validation approach

- **SYS-VV-04** — The software shall be validated against this requirements baseline and the DPM/ATBD
  using **mission-representative real Sentinel-1 data**, processed locally / on the Studio VM. For the
  first sensor profile, focusing quality shall be validated on a synthetic point-target impulse
  response (`PSLR`/`ISLR`/`IRW`) and on real corner-reflector / bright-target responses; SLC/GRD/GTC
  outputs shall be compared against the reference Sentinel-1 products within the clause <5.9> tolerance
  budgets (amplitude correlation, burst-overlap phase continuity, σ0 over stable targets, ALE on
  corner reflectors). Bit-identical reproduction is explicitly **not** required. Operational procedures
  (CLI runs, configuration, modes) shall be exercised as part of validation. *(Validation: A, T)*

### <6.3> Validation requirements

- **SYS-VV-05** — Each requirement in clause <5> shall carry a validation method (assigned inline and
  consolidated in the traceability matrix). A requirement excluded from validation against the baseline
  shall be explicitly identified there with rationale. *(Validation: R)*

### <6.4> Verification requirements

- **SYS-VV-06 (installation & acceptance)** — Clean installation (`pip install`) into the SDE / Studio
  VM and a local environment, and successful execution of the acceptance test set, shall be verified.
  *(Validation: T, I)*
- **SYS-VV-07 (versions, content, medium)** — The delivered versions, their content and medium (Zarr
  `EOProduct`s, Python wheel, versioned documentation) shall be verified against the SCF / SRN.
  *(Validation: I)*
- **SYS-VV-08 (integration support)** — The single developer shall provide the support needed for
  integration of the product into the ground segment / SDE. *(Validation: R)*
- **SYS-VV-09 (exchanged-data format & medium)** — The format and delivery medium of all exchanged data
  — input L0 (SAFE), private ADFs, and output products — shall be verified against the ICD (RD-06).
  *(Validation: I, T)*

---

## <7> System models

Formal system-specification-language models (computational, data, event, failure) are **tailored out**
for this Category C, single-developer project. The role of the system model is served by concrete
project artefacts, maintained as the design matures:

- the **EOProcessingUnit pipeline graph** (functional/processing model) — detailed in the SDD;
- the **per-sensor profile schema** (configuration/data model) — clause <5.4>;
- the **EOProduct / Zarr data model** (product data model, AD-05), including the complex-SLC / per-burst
  convention — referenced by the ICD;
- the **DPM / ATBD** (RD-05) as the algorithm/behavioural model per processing stage.

No schedulability analysis or model checking is required (no real-time or on-board element, clause
<5.2>).

*End of SSS. Authored per ECSS-E-ST-40C Rev.1 Annex B.*
