"""Single pipeline driver for sar-processor (skeleton).

Mirrors the msi-processor single-driver convention: one entry point, mode-only
CLI (``nominal`` | ``calibration``), settings via ``S2_DATA_STORE``-style
environment variables (the SAR equivalents are defined in the ICD at PDR).

The phase chains are baselined with the SRS/SDD; until then this driver only
validates its arguments and reports the (empty) phase plan, so the manual CI
jobs ``pipeline-nominal`` / ``pipeline-calibration`` exercise the wiring.
"""

from __future__ import annotations

import argparse
import sys

# Canonical phase order; populated as stages are baselined (SDD <5.3>).
PHASES: list[str] = []
NOMINAL_PHASES: list[str] = []
CALIBRATION_PHASES: list[str] = []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="sar-processor pipeline driver")
    parser.add_argument("store", help="data-store root directory")
    parser.add_argument("--mode", choices=("nominal", "calibration"), default="nominal")
    args = parser.parse_args(argv)

    todo = NOMINAL_PHASES if args.mode == "nominal" else CALIBRATION_PHASES
    print(f"sar-processor driver: store={args.store} mode={args.mode}")
    print(f"phase plan: {todo or '(no stages baselined yet — skeleton)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
