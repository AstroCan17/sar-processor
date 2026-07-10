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
| **Status** | Draft for SRR — living document |

> Software engineering contribution to project risk management. Likelihood (L) and severity (S) scored
> 1–5 per ECSS-M-ST-80C; risk index = L×S. PA-originated and engineering risks are raised as GitLab
> issues (`Risk` template) linked to their mitigation merge requests, and reviewed at each milestone.
> The technical rationale for RSK-05..RSK-11 is developed in the project implementation plan
> (`vault-a-s1-sar-*` plan, risks R1–R7).

---

## <1> Register

| ID | Risk | L | S | Idx | Mitigation | Owner gate | Status |
|---|---|---|---|---|---|---|---|
| RSK-01 | Public Sentinel-1 **L0 raw decodability** (FDBAQ Huffman/BAQ complexity) blocks real-data validation of the L0 decode stage | 3 | 4 | 12 | Extract & study the ESA MPC **L0 Decoding Package** (DI-MPC-TN-0474) early; bit-exact decode test vs its reference decoded vectors (Inc 1); fall back to reverse-generated ISPs (S2-E2ES reverse-ladder precedent) if reference vectors are insufficient | PDR / Inc 1 | Open |
| RSK-02 | **Azimuth-focusing complexity** (Range-Doppler: SRC, RCMC, TOPSAR deramp/UFR/deburst) exceeds single-developer schedule / correctness reach | 4 | 4 | 16 | Doc-first ATBD (public IPFDPM basis, RD-05); **fundamentals-first increments** (single-burst point-target validation before TOPSAR); reuse published reference formulations where licence-compatible (SRF) | PDR / Inc 2–4 | Open |
| RSK-03 | **Single-developer schedule** across the full SRR→AR document + code footprint | 4 | 3 | 12 | Tailored Category C DRL (SDP §5.5.2); sensor-agnostic scaffold reused from msi-processor (SRF-RU-01..05); milestone scope control; teaching-hybrid keeps doc + prototype in lockstep | all | Open |
| RSK-04 | SentiWiki/S1 technical-reference **ingest gaps** leave TBDs unresolved at SRR/PDR | 2 | 3 | 6 | Vault ingest largely complete (ATBD-grade S1 corpus present); TBD/TBC markers tracked per document; SRR gate checks TBD count | SRR/PDR | Open |
| RSK-05 | **EOPF Zarr model for complex / burst data** — `EOZarrStore`/`EOVariable` may not natively represent `complex64` or per-burst grouping (plan R1) | 3 | 4 | 12 | Feasibility probe on `eopf == 2.8.1` before Inc 2; define a documented complex-split / burst-group convention if native support is absent; record in ICD/SDD | PDR / before Inc 2 | Open |
| RSK-06 | **Ground-truth scene** — the chosen IW datatake may lack corner reflectors / a transponder / a stable-σ0 site, or a matching-IPF SLC+GRD+ADF set, blocking tolerance validation (plan R2) | 3 | 4 | 12 | Select the datatake against a documented cal-site catalogue; source the matched product+ADF set from the Studio VM store; keep the synthetic point-target test as the always-available fallback for focusing correctness | PDR / before Inc 2 | Open |
| RSK-07 | **L0 Decoding Package completeness** — the package may ship only the spec, not decoded reference vectors sufficient for a bit-exact decode test (plan R3) | 2 | 3 | 6 | Inventory the extracted package early; if vectors are absent, derive a reference by round-tripping a real L1→L0 or accept a tolerance-based decode check with documented rationale | Inc 1 | Open |
| RSK-08 | **DEM choice / licensing / datum** — Copernicus DEM vs GETASSE30, ellipsoidal-vs-orthometric geoid handling for GTC (plan R4) | 2 | 3 | 6 | Fix the DEM source + datum convention in the ICD at PDR; unit-test the geoid handling; source DEM from the Studio VM store | PDR / Inc 7 | Open |
| RSK-09 | **Compute / memory** — full IW-datatake focusing may exceed the SDE shell runner / local memory (plan R6) | 3 | 3 | 9 | Per-burst / per-sub-swath chunking (SSS SYS-RES-03); Dask strategy (repo has dask scaffolding); CI Tier-A limited to single-burst / point-target; heavy runs on the Studio VM | CDR / Inc 4 | Open |
| RSK-10 | **IPF-version gating scope** — the matrix of version-gated corrections (EAP phase, noise-vector form, GRD fill) could sprawl (plan R7) | 2 | 3 | 6 | Pin a single supported IPF version for v1 (profile `supported_ipf_versions`); bound the gating matrix; extend by profile/data later without core changes (SSS SYS-MNT-02) | PDR | Open |
| RSK-11 | **`product/` subpackage scope** — the SAR-specific SAFE/annotation/LUT/orbit I/O layer (a divergence from msi) could grow unbounded or leak framework types into cores | 2 | 2 | 4 | Keep `core.py` framework-free (arrays + typed params); confine SAFE/annotation parsing to `product/`; record reuse-vs-new boundary in the SRF (RD-12); design review at CDR | CDR | Open |
| RSK-12 | **Bit-identical-reproduction expectation gap** — stakeholders may expect pixel-identical reproduction of ESA SLC, which is infeasible without the reference IPF binary | 1 | 3 | 3 | Explicit in SSS §4.3 / SYS-VV-04 and IRD REQ-IF-CAP-04: tolerance-based validation (PSLR/ISLR/IRW, ALE, σ0, burst-overlap phase); bit-exact only for FDBAQ decode | SRR (closed by doc) | Open |

**Scoring key.** L/S: 1 = very low … 5 = very high. Idx = L×S (1–25). Idx ≥ 12 → actively tracked with a
milestone gate; Idx 6–11 → monitored; Idx ≤ 5 → accepted/watch.

## <2> Closed risks

None.

---

*Living document — updated at each milestone review (SRevP) and whenever a risk is opened, mitigated or
closed via a linked GitLab issue/MR.*
