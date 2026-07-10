# Software Product Assurance Plan (SPAP)

| | |
|---|---|
| **Document** | Software Product Assurance Plan (SPAP) |
| **DRD** | ECSS-Q-ST-80C Rev.2 (30 April 2025), Annex B |
| **Container** | Product Assurance File (PAF) |
| **Project** | `sar-processor` — generic spaceborne SAR data processor |
| **Configuration item** | `gitlab.eopf.copernicus.eu/ipf/sar-processor` |
| **Software criticality** | Category C (ECSS-Q-ST-80C Rev.2 Annex D / ECSS-E-ST-40C Rev.1 Annex R) |
| **Baselined at** | SRR |
| **Status** | Draft for SRR — skeleton |

> This SPAP is the software product assurance constituent of the Product Assurance File for the
> `sar-processor` project, tailored to Category C, single-developer scope. PA mechanisms are the
> automated CI quality gates plus the review milestones. Content `TBD (SRR)`.

---

## <1> Introduction

`TBD (SRR)`.

## <2> Product assurance programme

- **Automated gates (every MR):** flake8/black/isort (120 cols), mypy strict, bandit + pip-audit,
  pytest unit tier with coverage, docstring-coverage and complexity (non-blocking), SonarQube.
- **Reviews:** milestone reviews per SRevP; MR review checklist (`.gitlab/merge_request_templates/`).
- **Configuration management:** GitLab, protected `main`, SemVer tags, CIDL/SCF at QR.

## <3> Criticality and tailoring

Category C justification and Annex D tailoring table. `TBD (SRR)`.

## <4> Compliance matrix

ECSS-Q-ST-80C Rev.2 clause compliance. `TBD (SRR)`.
