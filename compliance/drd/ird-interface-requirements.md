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
| **Status** | Draft for SRR |

> This IRD is part of the **requirements baseline** of the `sar-processor` project and, together with
> the SSS, is a primary input for the System Requirements Review (SRR). It follows the ECSS-E-ST-40C
> Rev.1 Annex C section structure and the heading style of the SDP. It states the **interface
> requirements** imposed on the processor at its external boundary — the downlinked RAW (L0) SAR
> input and its product **annotation**, the instrument calibration auxiliary data (ADF set), the
> L1 SLC / L1 GRD / geocoded GTC Zarr products, the EOPF CPM framework, the triggering payload, and
> the sensor-profile/configuration interface. The **concrete interface definitions** (field-level
> schemas, ISP/annotation structure, ADF schemas, product structure, chunking, payload syntax) are
> *not* fixed here: they are produced in the **ICD** (Annex E) at PDR/CDR. The footprint is tailored
> to a Category C, single-developer ground-segment processor.

## <1> Introduction

The `sar-processor` is an operational ground-segment **forward** data processor that transforms
**downlinked RAW (Level-0) Synthetic Aperture Radar (SAR) instrument source packets** into focused,
calibrated and geolocated products **up to L1 and geocoded GTC** (decode → focusing → radiometric
calibration → detection/multi-look → geocoding). It is a **generic spaceborne SAR processor**: the
chain is sensor-agnostic and driven by a per-sensor configuration/profile plus the per-acquisition
product annotation; the first instantiated profile is C-band SAR with Sentinel-1 C-SAR (IW/TOPSAR)
as the public reference. The processor is built on the ESA Earth Observation Processing Framework
(EOPF): each stage is an EOPF CPM `EOProcessingUnit`, products are `EOProduct` objects, and outputs
are written as cloud-native **Zarr** via the EOPF `EOZarrStore`.

The **purpose** of this document is to specify the interfaces between `sar-processor` and the
external systems and data it exchanges with, as a set of uniquely identified, verifiable
**interface requirements**. It is the highest-level interface description of the software and, with
the SSS, provides criteria used to validate and accept the software (per AD-1 §5.2.4.3 and the IRD
DRD, Annex C).

The **reason prompting its preparation** is the SRR baseline of the requirements: before the SRS
(Annex D) and the detailed interface control (ICD, Annex E) are written, the external interface
boundary of the processor must be fixed at requirements level so that the requirements, data
processing model and design downstream are anchored to a stable interface envelope. This IRD is
produced as a **standalone document** (Annex C.1.2).

> **SAR-specific interface note (informative).** Two boundary characteristics distinguish this IRD
> from the `msi-processor` precedent: (a) the SAR input carries a rich **product annotation** whose
> *per-acquisition* parameters (azimuth steering rate, Doppler-centroid / azimuth-FM-rate polynomials,
> burst times, calibration/noise LUTs) drive focusing and are read at run time — distinct from the
> ADFs that carry *sensor/version* constants; (b) every calibration-related interface is
> **IPF-version-gated**, so the input's IPF version is part of the selection metadata. Output SLC is
> **complex (I/Q), phase-preserving**, with a per-burst structure for TOPSAR.

## <2> Applicable and reference documents

**Applicable documents**

| Ref | Document |
|---|---|
| AD-1 | ECSS-E-ST-40C Rev.1 (30 April 2025) — Space engineering — Software |
| AD-2 | ECSS-Q-ST-80C Rev.2 (30 April 2025) — Space product assurance — Software product assurance |
| AD-3 | ECSS-E-ST-10-06C — Technical requirements specification (IRD context) |
| AD-4 | ECSS-M-ST-40C — Configuration and information management |

**Reference documents**

| Ref | Document |
|---|---|
| RD-1 | `sar-processor` Software Development Plan (SDP) — `compliance/software-development-plan.md` |
| RD-2 | `sar-processor` Software System Specification (SSS) — `compliance/drd/sss-software-system-specification.md` |
| RD-3 | `sar-processor` Interface Control Document (ICD) — `compliance/drd/icd-interface-control.md` (produced at PDR/CDR; defines the concrete interfaces) |
| RD-4 | EOPF Core Python Modules (CPM) documentation (`eopf == 2.8.1`) — `EOProduct`, `EOProcessingUnit`, `EOZarrStore`, triggering |
| RD-5 | EOPF Product Structure and Format Definition (PSFD) — Zarr product structure reference |
| RD-6 | EOPF Software Development Environment (SDE) — User Manual & Guidelines |
| RD-7 | Sentinel-1 Level-1 Detailed Algorithm Definition (IPFDPM) + product/ADF specifications (algorithm & interface heritage; see SRF) — vault `wiki/sources/` |

## <3> Terms, definitions and abbreviated terms

Terms and definitions follow AD-1, AD-2, the EOPF SDE glossary and the SAR glossary in the SSS
(RD-2 <3>). Abbreviations used in this document and not already defined in the applicable/reference
documentation:

| Abbreviation | Definition |
|---|---|
| ADF | Auxiliary Data File (AUX_CAL, AUX_INS, AUX_PP1, AUX_POE/RES/PRE, AUX_ATT, DEM) |
| Annotation | The per-acquisition product metadata (timing, orbit, burst list, DC/FM/steering polynomials, calibration/noise LUTs) accompanying the L0/L1 product |
| ISP | Instrument Source Packet (Level-0 space packet: compressed echo/cal/noise + secondary header) |
| SLC / GRD / GTC | Single Look Complex / Ground Range Detected / Geocoded Terrain-Corrected products |
| IPF | Instrument Processing Facility — reference processor; its version (in the product manifest) gates corrections |
| CPM / PU | (EOPF) Core Python Modules / (CPM) Processing Unit (`EOProcessingUnit`) |
| CRS | Coordinate Reference System |
| DEM | Digital Elevation Model |
| ICD / IRD | Interface Control Document / Interface Requirements Document |
| L0 / L1 | Processing levels: raw ISPs / focused-calibrated |
| PSFD | (EOPF) Product Structure and Format Definition |
| RB | Requirements Baseline |
| SAFE | Standard Archive Format for Europe (product packaging: manifest + measurement + annotation) |
| SDE | (EOPF) Software Development Environment (incl. the project Studio VM data store) |
| URI | Uniform Resource Identifier (product/ADF/DEM locator) |

(ECSS review acronyms SRR/PDR/CDR/QR/AR and DRD acronyms per AD-1 and RD-1.)

## <4> General description

### <4.1> Product perspective

`sar-processor` is a batch, non-interactive component embedded in a larger EO ground segment. Its
**external interfaces to other systems** are:

| # | External system / actor | Direction | Exchange |
|---|---|---|---|
| E1 | **L0 ingestion / downlink chain** | → in | Downlinked RAW (Level-0) SAR product (SAFE): instrument source packets (compressed echo) + acquisition **annotation** (timing, orbit/attitude, burst list, DC/FM/steering polynomials) |
| E2 | **Instrument calibration facility / ADF provider** (private, Studio VM store) | → in | ADF set: AUX_CAL (EAP/AAP/AAEP, absolute constant), AUX_INS (roll-steering, decode tables, timeline), AUX_PP1 (processing params), AUX_POE/RES/PRE (orbit), AUX_ATT (attitude), DEM |
| E3 | **Sensor profile / configuration provider** | → in | Per-sensor profile + run configuration (identified and versioned) |
| E4 | **Processing orchestration / trigger** | → in | Triggering payload (job order) invoking a run / sub-chain / mode |
| E5 | **Product store / archive / dissemination** | ← out | L1 SLC / L1 GRD / GTC as cloud-native Zarr `EOProduct` |
| E6 | **EOPF CPM framework + storage backend** | host | Runtime within which the processor executes; `EOProduct`/`EOProcessingUnit`/`EOZarrStore` API and the POSIX/object-store backend |

```mermaid
flowchart LR
  E1[E1 L0 downlink<br/>SAFE: ISPs + annotation] -->|RAW L0 product| SAR[sar-processor<br/>chain of EOPF CPM PUs]
  E2[E2 Calibration facility / ADF<br/>AUX_CAL/INS/PP1/orbit/attitude/DEM] -->|ADF set by URI| SAR
  E3[E3 Sensor profile / config] -->|profile id + version| SAR
  E4[E4 Orchestration / trigger] -->|triggering payload JSON| SAR
  SAR -->|SLC / GRD / GTC Zarr EOProduct| E5[E5 Product store / archive]
  SAR -. runs within .- E6[E6 EOPF CPM + EOZarrStore]
```

### <4.2> General constraints

- **EOPF CPM API is fixed.** Stage interfaces must be `EOProcessingUnit`s; products must be
  `EOProduct`s; persistence/access must use `EOZarrStore`. The processor may not define its own
  product/IO format outside the CPM abstractions.
- **Framework version is pinned to `eopf == 2.8.1`** (matching the SDE build image). Interface
  compatibility is bound to that CPM API surface; the version is not upgraded.
- **Output format is mandated as cloud-native Zarr** (per EOPF / PSFD); other output product formats
  are out of scope. The SLC output must represent **complex (I/Q)** data and a **per-burst** structure
  (TOPSAR) via a documented convention.
- **Generic / sensor-agnostic design.** All sensor-specific interface content must be supplied through
  the sensor profile (§<5.4>); all *per-acquisition* parameters must be read from the product
  annotation. Hardcoding any sensor's radar constants, sub-swath geometry or calibration model into
  the interfaces is not permitted.
- **IPF-version gating.** Calibration-related interfaces are conditioned on the input's IPF version
  (read from the product manifest); the interface envelope is bounded by the profile's supported
  versions.
- **Data policy.** Source **code is public**; **RAW (L0) inputs and instrument calibration ADFs are
  private** — never committed, never used in public CI. Interfaces reference these inputs at run time
  by identifier/URI (resolved against the Studio VM data store), not embedded.
- **CI environment.** The CI runner is a **shell executor** (no container runtime, no Dask gateway, no
  S3). Interface paths requiring those services are non-blocking in CI and must have a local-filesystem
  equivalent for verification (including a **synthetic point-target** path needing no private data).

### <4.3> Operational environment

a. The operational context is summarised by the context diagram in §<4.1>. `sar-processor` runs as
   one or more `EOProcessingUnit`s triggered by the orchestration layer (E4), reading the L0 product
   and its annotation (E1) and the ADF set (E2) selected via the sensor profile (E3) and the input's
   IPF version, and writing Zarr products to the store (E5), all within the EOPF CPM runtime (E6).

b. **Nature of the exchanges with external systems:**
   - **File/object based** for data products, annotation and ADFs/DEM — SAFE packages and ADF files
     referenced by **URI**, on a POSIX filesystem or object storage, accessed through `EOZarrStore` /
     the EOPF store mapper.
   - **Structured payload (JSON)** for triggering — the job order declaring inputs, ADFs, output target,
     profile, mode and parameters.
   - **Process status / logs** — completion status, structured diagnostics and quality flags surfaced
     to the orchestration layer.

c. **Activities supported by external systems** (parent ground segment): E1 produces and delivers the
   L0 product; E2 produces and maintains the calibration ADFs and DEM; E4 schedules and triggers
   processing; E5 stores and disseminates the L1/GTC products. `sar-processor` consumes E1–E4 and feeds
   E5.

d. **References to the interface control documents.** The concrete definition of every interface in
   §<5> (ISP/annotation structure, ADF schemas, product structure, group/variable tree, complex-SLC and
   per-burst encoding, chunking, CRS encoding, triggering-payload syntax, profile schema) is provided in
   the **ICD** (RD-3, ECSS-E-ST-40C Annex E), baselined at PDR (start) and CDR (final), with the EOPF
   **PSFD** (RD-5) as the normative product-structure reference. This IRD states the requirements; the
   ICD states the control.

### <4.4> Assumptions and dependencies

- **Assumptions:** the algorithm/calibration/interface basis is available from the public Sentinel-1
  engineering corpus (RD-7, see SRF); a reference Sentinel-1 data set (matching L0 + L1 SLC/GRD + ADFs,
  plus ground truth) is available for **local** numerical verification on the Studio VM; the
  orchestration layer can supply a triggering payload in the CPM form.
- **Dependencies:** EOPF CPM (`eopf == 2.8.1`) and the SDE build image; the EOPF Zarr store backend
  (POSIX and, where available, object storage) with a convention for complex/per-burst variables;
  availability, IPF-version match and validity metadata of the calibration ADFs and the sensor profile.
- Further project-level assumptions/dependencies/constraints are in the SDP (RD-1 §<4.3>) and are not
  repeated here.

## <5> Specific requirements

### <5.1> General

Each interface requirement is **uniquely identified** by an identifier of the form `REQ-IF-*`.
Requirements are stated here (Statement + Rationale); the **validation method** for each is given in
§<6>. Concrete, field-level interface definitions are deferred to the ICD (RD-3) per §<4.3>d; where
this document writes "(ICD)" the detail is controlled there.

### <5.2> Capabilities requirements

External interface requirements specifying interface behaviour and associated performances.

#### REQ-IF-CAP-01 — Staged, decoupled product interfaces with breakpoints
- **Statement:** The processor shall expose the processing chain as a sequence of stages (decode → L0
  pre-processing → focusing (SLC) → TOPSAR deburst → radiometric calibration → GRD → GTC) in which
  **each stage boundary is a defined product interface**: a stage consumes a defined set of input
  product(s), ADF(s), annotation and parameters and produces a defined output product. The processor
  shall support starting and stopping at these boundaries (breakpoints), i.e. running a sub-chain
  from/to a given level (with **SLC** and **GRD** as the principal product boundaries).
- **Rationale:** Stage decoupling is the EOPF CPM design model and is required for incremental
  development, independent verification of each stage against its requirement, and reprocessing from
  intermediate levels (e.g. re-deriving GRD/GTC from a stored SLC).

#### REQ-IF-CAP-02 — Chunked / lazy access at burst / sub-swath granularity
- **Statement:** The product interfaces shall support **larger-than-memory** products through chunked,
  lazy read and write (Zarr chunking) at the SAR acquisition granularity (per burst / per sub-swath /
  per polarisation as set by the annotation and profile); the processor shall not require a whole
  datatake to be resident in memory.
- **Rationale:** SAR datatakes (multi-burst, multi-sub-swath, complex) exceed memory; per-burst chunking
  is the natural and efficient processing granularity and lets downstream consumers read partial
  products.

#### REQ-IF-CAP-03 — Metadata and provenance propagation across interfaces
- **Statement:** Every output product interface shall carry the processing metadata needed for
  traceability: the input product identifier(s), the **input IPF version applied**, the ADF
  identifier(s) and version(s), the sensor profile identifier and version, the processor/baseline
  version, the processing parameters and the processing timestamp.
- **Rationale:** Traceability of a product to exactly the inputs, calibration, IPF-version gating and
  configuration used is required by the ECSS life cycle and by the data policy (provenance without
  exposing private calibration values, see REQ-IF-SEC-02).

#### REQ-IF-CAP-04 — Reproducible interface behaviour
- **Statement:** Given identical inputs, ADF set, annotation, sensor profile and processor version, the
  output product interface shall be reproducible: **bit-identical** where the operation is deterministic
  (e.g. L0/FDBAQ decode), and within a **documented numerical tolerance** where it is FFT/interpolation-
  based (focusing, geocoding).
- **Rationale:** Reproducibility is a stated project priority (RD-1) and the basis for regression
  verification; the decode/focusing distinction reflects the genuine determinism boundary of a SAR
  processor (bit-identical reproduction of a reference IPF's focused output is not an objective).

#### REQ-IF-CAP-05 — Completion status and structured diagnostics
- **Statement:** The processor shall expose, at its external boundary, a completion status
  (success/failure) and structured diagnostics (errors, warnings, focusing-quality indicators and
  per-product quality flags) consumable by the orchestration layer.
- **Rationale:** The orchestration layer (E4) needs an unambiguous, machine-readable run outcome to
  drive scheduling, retries and quality control.

### <5.3> System interface requirements

Interface requirements imposed on the system, organised by the Annex C categories.

#### <5.3.1> System-level data interfaces

**Input — downlinked RAW (Level-0) SAR data and annotation**

#### REQ-IF-IN-L0-01 — L0 input product interface
- **Statement:** The processor shall ingest downlinked RAW (Level-0) SAR data as its primary input
  through a defined input product interface. The L0 interface shall provide at least: the instrument
  source packets (compressed echo per sub-swath / polarisation, with per-packet secondary headers
  carrying timing — PRF, SWST, acquisition time, swath/mode) and the associated acquisition
  **annotation** required to drive the chain. The concrete ISP/annotation encoding is defined in the
  ICD.
- **Rationale:** L0 is the entry point of the chain; decoding, focusing, calibration and geocoding all
  derive from the ISPs and the annotation they are packaged with.

#### REQ-IF-IN-L0-02 — Product annotation interface (per-acquisition parameters)
- **Statement:** The processor shall read, through a defined annotation interface, the **per-acquisition**
  parameters needed for focusing and calibration — at least: orbit state vectors and attitude, burst
  list and azimuth times, azimuth **steering rate**, Doppler-centroid and azimuth-FM-rate polynomials,
  sampling geometry, and the calibration/noise look-up-table references. These parameters shall be
  taken from the annotation at run time and shall not be sourced from the sensor profile or hard-coded.
- **Rationale:** The annotation-vs-ADF split is a defining SAR characteristic: per-acquisition geometry
  varies scene-to-scene and must come from the product, while the profile/ADFs carry only
  sensor/version constants (REQ-IF-AD-01, SSS SYS-ADP-02).

#### REQ-IF-IN-L0-03 — L0 identification and selection metadata (incl. IPF version)
- **Statement:** Each L0 input shall be uniquely identified and shall carry (or be accompanied by) the
  metadata required to select the applicable sensor profile and ADF set — at least the instrument/sensor
  identifier, the acquisition time, the acquisition mode, and the **IPF/product version** used for
  version-gated corrections.
- **Rationale:** The generic chain must resolve the correct profile (§<5.4>), the validity- and
  IPF-version-matching ADFs (REQ-IF-IN-ADF-02) and the correct correction variants (SSS SYS-CAP-11) from
  the input itself, without operator guesswork.

#### REQ-IF-IN-L0-04 — L0 immutability
- **Statement:** The L0 input interface shall be **read-only** to the processor; the processor shall not
  modify its L0 input or annotation.
- **Rationale:** The L0 archive is authoritative and shared; reprocessing must always start from an
  unaltered input.

**Input — instrument calibration auxiliary data (ADF set)**

#### REQ-IF-IN-ADF-01 — Calibration/auxiliary ADF input interface
- **Statement:** The processor shall ingest the instrument auxiliary data as ADFs through a defined
  auxiliary input interface. The ADF interface shall provide at least: **AUX_CAL** (elevation/azimuth
  antenna patterns and elements, absolute calibration constant), **AUX_INS** (roll-steering law, ISP
  decoding tables, instrument timeline), **AUX_PP1** (Level-1 processing parameters), **orbit**
  (AUX_POE/RES/PRE) and **attitude** (AUX_ATT); and, for geocoding, a **DEM**. Concrete ADF schemas are
  defined in the ICD.
- **Rationale:** AUX_CAL and AUX_INS are the radiometric and geometric backbones of the chain; AUX_PP1
  parametrises the stages; orbit/attitude and the DEM feed the geometric/geocoding stages.

#### REQ-IF-IN-ADF-02 — ADF identification, versioning, validity and IPF-version match
- **Statement:** Each ADF shall be uniquely identified and **versioned**, and the ADF interface shall
  expose its validity (applicable sensor/mode, applicability time range, version, and the IPF-version
  compatibility) so the processor can select the ADF valid for a given L0 input and its IPF version.
- **Rationale:** Calibration evolves over the instrument's life and is IPF-version-gated; selecting the
  ADF valid for the acquisition **and** the IPF version is required for radiometric/phase correctness
  and for provenance (REQ-IF-CAP-03).

#### REQ-IF-IN-ADF-03 — Runtime-resolved, private ADF references
- **Statement:** The ADF interface shall reference auxiliary data by identifier/URI resolved at **run
  time** (against the private Studio VM data store); ADF content shall **not** be embedded in the source
  code or committed to the repository, and shall not be required by public CI.
- **Rationale:** Calibration data are private per the data policy (§<4.2>); the interface must keep them
  external to the public code base.

#### REQ-IF-IN-ADF-04 — ADF immutability
- **Statement:** ADFs and the DEM shall be **read-only** to the processor.
- **Rationale:** Auxiliary references are authoritative inputs maintained by E2, not processor outputs.

**Output — L1 SLC / L1 GRD / GTC products**

#### REQ-IF-OUT-01 — Output product interface as cloud-native Zarr
- **Statement:** The processor shall produce its output products — **L1 SLC** (focused, complex,
  phase-preserving, slant-range), **L1 GRD** (detected, multi-looked, ground-range) and **GTC**
  (geocoded terrain-corrected) — through a defined output product interface written as cloud-native
  **Zarr** via the EOPF `EOZarrStore`.
- **Rationale:** Zarr output via the EOPF store is mandated by the framework (§<4.2>) and is the delivery
  format consumed by E5.

#### REQ-IF-OUT-02 — Self-describing output `EOProduct` (complex SLC / per-burst)
- **Statement:** Each output product shall be a self-describing `EOProduct` exposing, through the output
  interface: the measurement variables (**complex I/Q** for SLC; detected amplitude/backscatter for
  GRD/GTC), the **per-burst / per-sub-swath / per-polarisation** structure where applicable, per-pixel
  quality/mask layers, geolocation / geo-referencing (slant-range grid for SLC; ground-range for GRD;
  map CRS for GTC), and the product + processing metadata (provenance per REQ-IF-CAP-03). The concrete
  product structure (group/variable tree, complex encoding, burst grouping, dtypes, chunking, CRS
  encoding) is defined in the ICD with the EOPF PSFD as the normative reference.
- **Rationale:** Downstream systems (including interferometric users of the SLC) must interpret the
  product — including its phase and burst structure — without out-of-band knowledge; self-description is
  the EOPF product principle.

#### REQ-IF-OUT-03 — Output storage backends and chunked access
- **Statement:** The output Zarr interface shall be writable to the supported storage backends — POSIX
  filesystem and, where available, object storage (S3-compatible) — through the EOPF store abstraction,
  and shall be chunked (per burst / sub-swath) to support partial/lazy reads by downstream consumers.
- **Rationale:** Operational deployment uses object storage while local verification uses the filesystem
  / Studio VM; both must be served by the same interface (with the CI constraint of §<4.2>).

#### REQ-IF-OUT-04 — Output identification and versioning
- **Statement:** Each output product shall carry a unique product identifier (following the S1 SAFE-style
  naming convention) and the processing baseline/version, and shall be linkable back to the inputs, ADFs,
  IPF version and profile that produced it.
- **Rationale:** Product identity and baseline are required for catalogue management, reprocessing and
  traceability.

#### <5.3.2> Software interfaces

#### REQ-IF-SW-01 — Stages as EOPF CPM `EOProcessingUnit`s
- **Statement:** Each processing stage shall be exposed as an EOPF CPM `EOProcessingUnit` conforming to
  the CPM processing-unit interface, declaring its mandatory input products, ADFs, output products and
  parameters in the CPM computing-model description (JSON).
- **Rationale:** The `EOProcessingUnit` contract is the framework's software interface and the basis for
  orchestration, triggering and breakpoints (REQ-IF-CAP-01, REQ-IF-COM-01).

#### REQ-IF-SW-02 — `EOProduct` exchange and `EOZarrStore` persistence
- **Statement:** Products shall be exchanged across the software interface as EOPF `EOProduct` objects,
  and product persistence/access shall use the EOPF `EOZarrStore`. The processor shall not implement
  product I/O outside these CPM abstractions.
- **Rationale:** Uniform product handling and storage access via the CPM is mandated (§<4.2>) and
  guarantees interoperability with the rest of the EOPF ecosystem.

#### REQ-IF-SW-03 — Framework version binding
- **Statement:** The software interfaces shall be compatible with the pinned framework `eopf == 2.8.1`
  (the CPM API surface provided by the SDE build image). Interface compatibility is bound to that version.
- **Rationale:** The pinned CPM version defines the available API; a change would desynchronise the build
  environment and break the interfaces (RD-1 §<4.3>).

#### REQ-IF-SW-04 — Testable algorithmic core behind the PU wrapper
- **Statement:** The pure algorithmic core of each stage shall be callable independently of the CPM
  wrapper through a plain function/class interface (plain arrays + typed parameters), with the
  `EOProcessingUnit` acting as a thin adapter over it.
- **Rationale:** A framework-independent core interface enables deterministic unit testing and numerical
  verification of the focusing/calibration algorithms without the full CPM runtime (RD-1 §<5.1>), and is
  what makes the synthetic point-target focusing test possible in public CI.

#### <5.3.3> Communication interfaces

#### REQ-IF-COM-01 — Triggering payload (job order) interface
- **Statement:** The processor shall be invocable through the EOPF CPM triggering mechanism via a
  **triggering payload** (JSON job order) that declares, for a run: the input product(s), the ADF set,
  the output target/store, the sensor profile/configuration, the production **mode** (nominal /
  calibration) and the processing parameters/breakpoints. The concrete payload schema is defined in the
  ICD.
- **Rationale:** The triggering payload is the control interface between the orchestration layer (E4)
  and the processor and the single place where a run is fully specified.

#### REQ-IF-COM-02 — URI-referenced, location-transparent I/O
- **Statement:** The triggering and product interfaces shall reference input products, annotation, ADFs,
  DEM and output targets by **URI**, supporting both local (filesystem / Studio VM) and remote
  (object-store) locations, resolved through the EOPF store/mapper at run time.
- **Rationale:** Operational runs use remote stores; verification uses local paths / the Studio VM; the
  interface must be location-transparent.

#### REQ-IF-COM-03 — Local-filesystem fallback for constrained environments
- **Statement:** The communication/I/O interfaces shall provide a local-filesystem path that does not
  require a container runtime, Dask gateway or S3, so that a run (including the synthetic point-target
  test) can be triggered and verified on the CI shell runner.
- **Rationale:** The CI runner lacks those services (§<4.2>); a degraded local path is needed for
  non-blocking verification.

#### <5.3.4> Software-hardware and hardware interfaces

#### REQ-IF-HW-01 — No direct hardware interface
- **Statement:** The processor shall have **no direct hardware interface**; it shall access compute and
  storage resources only through the host operating system and the EOPF store abstraction.
- **Rationale:** `sar-processor` is application-level ground-segment software; dedicated
  software-hardware and hardware interfaces are not applicable (Category C tailoring). Stated explicitly
  to close the Annex C system-interface categories.

#### <5.3.5> Human-machine interface (HMI)

#### REQ-IF-HMI-01 — Non-interactive invocation interface
- **Statement:** The processor shall provide a non-interactive command-line / programmatic invocation
  interface; it shall not require a graphical user interface. Operator interaction is limited to
  supplying the triggering payload and consuming logs and exit status.
- **Rationale:** A batch ground-segment processor is driven by orchestration, not by an interactive UI;
  this keeps the HMI footprint proportionate to a Category C processor.

#### <5.3.6> Security aspects of the external interfaces

#### REQ-IF-SEC-01 — Input identity, integrity and IPF-version match
- **Statement:** The interfaces shall allow verification that the L0 input, annotation, ADFs and sensor
  profile used in a run are exactly those identified (by identifier/version), and the processor shall
  reject or flag inputs whose validity or **IPF version** does not match the selected profile/ADF set.
- **Rationale:** Product correctness and traceability depend on using the right, unaltered, IPF-consistent
  inputs; a mismatched IPF version or calibration must not silently produce a product.

#### REQ-IF-SEC-02 — Confidentiality of private inputs (data policy)
- **Statement:** RAW (L0) inputs and instrument calibration ADFs are private: the interfaces shall
  reference them at run time only (Studio VM data store) and shall never persist them into the public
  source repository or public CI artefacts. Output products shall not embed private calibration
  coefficients beyond the identifiers/versions required for provenance (REQ-IF-CAP-03).
- **Rationale:** Enforces the project data policy (§<4.2>) at the interface boundary.

#### REQ-IF-SEC-03 — Least-privilege access
- **Statement:** The processor shall require only **read** access to its inputs/annotation/ADFs/DEM/profile
  and **write** access to the designated output store; it shall require no other external access.
- **Rationale:** Minimising the access surface limits the impact of misconfiguration and is consistent
  with the immutability requirements (REQ-IF-IN-L0-04, REQ-IF-IN-ADF-04).

### <5.4> Adaptation / missionization requirements

External data that varies according to sensor and operational needs — the **sensor-profile /
configuration interface** (and its complement, the per-acquisition annotation, REQ-IF-IN-L0-02).

#### REQ-IF-AD-01 — Sensor-agnostic chain driven by a profile interface
- **Statement:** The processing chain shall be sensor-agnostic and parametrised through a **sensor
  profile / configuration interface**. All sensor/mode-constant data — carrier frequency/wavelength,
  acquisition mode, polarisation channels, sub-swath static definitions, ADF bindings, supported-IPF
  envelope, and per-stage processing options/thresholds — shall be supplied via the profile and shall
  not be hardcoded. (Per-acquisition parameters come from the annotation, REQ-IF-IN-L0-02.)
- **Rationale:** A single generic processor must serve multiple SAR sensors/modes; externalising all
  sensor-constant content to the profile — and all scene-varying content to the annotation — is the core
  adaptation mechanism (RD-1 §<1>, SSS SYS-ADP-01/02).

#### REQ-IF-AD-02 — Profile identification, versioning and selection
- **Statement:** Each sensor profile shall be uniquely identified and versioned and shall be selectable
  per run via the triggering payload (REQ-IF-COM-01). The first profile instantiated is C-band SAR
  (Sentinel-1 IW/TOPSAR).
- **Rationale:** Reproducibility and traceability require knowing exactly which profile version produced
  a product (REQ-IF-CAP-03); per-run selection enables multi-sensor/mode operation.

#### REQ-IF-AD-03 — Externalised operations-/site-dependent settings
- **Statement:** The profile/configuration interface shall externalise operations- and site-dependent
  settings — output storage target and chunking, processing baseline / IPF-version selection,
  optional-stage enable/disable (e.g. thermal-noise removal), breakpoints, production mode, and
  DEM/orbit source selection — so that the same software runs across operational contexts without code
  change.
- **Rationale:** Portability across deployments (local/Studio-VM verification vs operational) must be a
  configuration concern, not a code concern (RD-1 §<4.1>).

#### REQ-IF-AD-04 — Profile validation at load
- **Statement:** The profile/configuration interface shall be **validated on load**; an incomplete or
  invalid profile shall be rejected with a clear diagnostic. The concrete profile schema is defined in
  the ICD.
- **Rationale:** Failing fast on a malformed profile prevents silently producing an incorrectly
  parametrised product.

## <6> Validation requirements

a. The interface requirements in §<5> are validated to demonstrate that the software interface
   requirements are met. At SRR the interfaces are validated primarily by **inspection** of this IRD and
   **review** of the design/ICD; the data interfaces become test-validatable once the ICD (RD-3) is
   baselined (PDR/CDR) and sample products/ADFs are available for **local** numerical verification (per
   the data policy). Validation methods: **T** Test, **A** Analysis, **I** Inspection, **R** Review of
   design, **D** Demonstration.

b. The validation method applicable to each requirement (requirements-to-validation-method correlation
   table):

| Requirement | Method | Means (and milestone) |
|---|---|---|
| REQ-IF-CAP-01 | T / R | Sub-chain run from/to a breakpoint (SLC, GRD); review of CPM stage decomposition (CDR) |
| REQ-IF-CAP-02 | T / A | Per-burst chunked read/write on a larger-than-memory datatake; memory-footprint analysis (CDR) |
| REQ-IF-CAP-03 | I / T | Inspect provenance metadata (incl. IPF version) against ICD; assert presence in output (CDR) |
| REQ-IF-CAP-04 | T | Re-run identical inputs; decode bit-identical, focusing/geocoding within tolerance (CDR) |
| REQ-IF-CAP-05 | T | Assert completion status + diagnostics/quality flags on success and forced failure |
| REQ-IF-IN-L0-01 | I / T | Inspect L0/ISP interface vs ICD; ingest a sample L0 datatake (local) |
| REQ-IF-IN-L0-02 | I / T | Inspect annotation interface; read burst/DC/FM/steering params from a sample product |
| REQ-IF-IN-L0-03 | I / T | Inspect required selection metadata (incl. IPF version); resolve profile/ADF |
| REQ-IF-IN-L0-04 | A / I | Static analysis / inspection: no write path to L0 input/annotation |
| REQ-IF-IN-ADF-01 | I / T | Inspect ADF interface vs ICD; load AUX_CAL/INS/PP1/orbit/attitude/DEM (local) |
| REQ-IF-IN-ADF-02 | I / T | Inspect ADF id/version/validity/IPF-match; select valid ADF for a given L0 |
| REQ-IF-IN-ADF-03 | I / A | Repository/CI inspection: no ADF content committed; runtime-URI resolution |
| REQ-IF-IN-ADF-04 | A / I | Static analysis / inspection: no write path to ADFs/DEM |
| REQ-IF-OUT-01 | T / I | Produce SLC/GRD/GTC Zarr `EOProduct` via `EOZarrStore`; inspect store output |
| REQ-IF-OUT-02 | I / T | Inspect product structure vs ICD/PSFD; assert complex SLC, burst grouping, masks, geo-ref, metadata |
| REQ-IF-OUT-03 | T | Write to POSIX (CI) and object store (when available); partial/per-burst read |
| REQ-IF-OUT-04 | I / T | Inspect product id (SAFE-style) + baseline + input/ADF/IPF/profile links |
| REQ-IF-SW-01 | R / I | Review CPM computing-model JSON (declared inputs/ADFs/outputs/params) |
| REQ-IF-SW-02 | R / T | Review I/O uses `EOProduct`/`EOZarrStore`; round-trip test |
| REQ-IF-SW-03 | I | Inspect pinned `eopf == 2.8.1` and CI build image |
| REQ-IF-SW-04 | T | Unit-test the algorithmic core (focusing on a point target) without the CPM runtime |
| REQ-IF-COM-01 | I / T | Inspect payload vs ICD; trigger a run (mode + breakpoints) from a sample payload |
| REQ-IF-COM-02 | T | Trigger with local/Studio-VM and remote (when available) URIs |
| REQ-IF-COM-03 | T | Trigger + verify on the CI shell runner via local-filesystem path (point-target test) |
| REQ-IF-HW-01 | I | Inspection — confirm no direct hardware interface (see §<6>c) |
| REQ-IF-HMI-01 | T / I | Invoke via CLI/programmatic entry point; confirm no GUI dependency |
| REQ-IF-SEC-01 | T | Run with mismatched ADF/profile/IPF validity → reject/flag |
| REQ-IF-SEC-02 | I / A | Repository/CI scan: no private inputs persisted; output carries only provenance ids |
| REQ-IF-SEC-03 | A / I | Inspect required access modes (read inputs, write output store only) |
| REQ-IF-AD-01 | R / T | Review profile externalises sensor-constant data; annotation supplies per-acquisition data |
| REQ-IF-AD-02 | I / T | Inspect profile id/version; select profile via payload |
| REQ-IF-AD-03 | I / T | Inspect externalised settings; change a setting (e.g. mode, noise toggle) without code change |
| REQ-IF-AD-04 | T | Load an invalid/incomplete profile → rejected with diagnostic |

c. **Requirements not validated against the requirements baseline.** REQ-IF-HW-01 is a not-applicable
   statement (no direct hardware interface) closed by inspection rather than an active validation
   activity. REQ-IF-COM-03 is a constraint-derived enabling requirement for the constrained CI
   environment; it is verified by demonstration on the shell runner but is not part of the operational
   acceptance criteria. The detailed requirement-to-design/ICD traceability is maintained in the project
   traceability matrix (`compliance/traceability/`).

   > NOTE — The correlation table above is the requirements-to-validation-method matrix required by the
   > IRD DRD. As the project evolves it is split, per project needs, into validation requirements (V&V
   > plan, `compliance/drd/vv-plan.md`) and acceptance requirements (SRelD/AR).

---

*End of IRD. Authored per ECSS-E-ST-40C Rev.1 Annex C. Concrete interface definitions are controlled in
the ICD (Annex E) at PDR/CDR.*
