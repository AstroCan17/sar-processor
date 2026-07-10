# Interface Control Document (ICD)

| Field | Value |
|---|---|
| **Document** | ICD — Interface Control Document |
| **DRD ref** | ECSS-E-ST-40C Rev.1, Annex E |
| **Container** | Technical Specification (TS) — `compliance/drd/` (source), published subset in `docs/` |
| **Project** | `sar-processor` (gitlab.eopf.copernicus.eu/ipf/sar-processor) |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | PDR (preliminary) / **CDR** (final) |
| **Status** | Draft for SRR — skeleton |

> This ICD gives the **concrete field-level interface definitions** implementing the interface
> requirements (`REQ-IF-*`, IRD): input L0 packet/annotation structures, ADF formats, output
> product structure and **product naming/type codes** — all identified as **`ICD-IF-*`**.
> **Product naming and S01 SAR product type codes are fixed in this document at PDR.**
> Content `TBD (PDR)`.

---

## <1> Introduction

`TBD (PDR)`.

## <2> Applicable and reference documents

Per SDP <2>. `TBD (PDR)`.

## <3> Interface definitions (`ICD-IF-*`)

- **<3.1> Input L0** — ISP structure, space-packet framing, annotation records.
  `TBD (PDR — pending SentiWiki S1 ingest)`.
- **<3.2> Auxiliary data files** — ADF formats and URIs. `TBD (PDR)`.
- **<3.3> Output products** — L1 SLC / L1 GRD EOPF/Zarr structure; naming convention and type
  codes `TBD (PDR)`.
- **<3.4> Data-store protocol** — shared `ipf/data-store` fetch/publish, manifest, sha256.
  `TBD (PDR)` (expected verbatim reuse of the msi-processor mechanism; see SRF).

## <4> Traceability

`REQ-IF-*` → `ICD-IF-*` in the traceability matrix. `TBD (PDR)`.
