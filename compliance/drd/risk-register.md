# Risk Register

| | |
|---|---|
| **Document** | Risk Register |
| **DRD** | No dedicated DRD — risk attributes per ECSS-M-ST-80C (risk management); contributes to SDP §4.5 |
| **Container** | Management File (MGT) |
| **Project** | `sar-processor` — generic spaceborne SAR data processor |
| **Configuration item** | `gitlab.eopf.copernicus.eu/ipf/sar-processor` |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 / ECSS-E-ST-40C Annex R) |
| **Baselined at** | SRR |
| **Status** | Draft for SRR — skeleton (living document) |

> Software engineering contribution to project risk management. Likelihood (L) and severity (S)
> scored 1–5 per ECSS-M-ST-80C.

---

## <1> Register

| ID | Risk | L | S | Mitigation | Status |
|---|---|---|---|---|---|
| RSK-01 | Public Sentinel-1 **L0 raw data availability/decodability** (FDBAQ decode complexity) blocks real-data validation of the L0 decode stage | 3 | 4 | Early PDR feasibility probe on a real S1 L0 product; fall back to synthetic ISPs generated from L1 (reverse-ladder precedent from the S2 E2ES work) | Open |
| RSK-02 | **Azimuth-focusing algorithm complexity** (range-Doppler/chirp-scaling/ω-k) exceeds single-developer schedule | 3 | 4 | Doc-first ATBD trade-off at PDR; incremental implementation (point-target validation before full scenes); reuse published reference implementations where licence-compatible (record in SRF) | Open |
| RSK-03 | **Single-developer schedule** risk across the full SRR→AR document + code footprint | 4 | 3 | Tailored Category C DRL (SDP <5.5.2>); platform machinery reused from msi-processor (SRF-RU-01..05); milestone scope control | Open |
| RSK-04 | SentiWiki/S1 technical-reference **ingest gaps** leave TBDs unresolved at SRR/PDR | 2 | 3 | Vault ingest in progress; TBD/TBC markers tracked per document; SRR gate checks TBD count | Open |

## <2> Closed risks

None.
