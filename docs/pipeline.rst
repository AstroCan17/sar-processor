.. Copyright 2026 ESA

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Processing pipeline
===================

``sar-processor`` follows the single-driver convention of its sibling
``msi-processor``: one entry point, a mode-only CLI, and all deployment
settings taken from environment variables (defined in the ICD at PDR).

.. code-block:: shell

   python scripts/run_pipeline.py <store> --mode nominal      # L0 → L1 SLC → L1 GRD
   python scripts/run_pipeline.py <store> --mode calibration  # calibration products

Modes
-----

.. list-table::
   :header-rows: 1

   * - Mode
     - Phase chain
     - Products
   * - ``nominal``
     - TBD (PDR) — L0 decode → Doppler-centroid estimation → range compression →
       azimuth focusing → radiometric calibration → multilook/detection → geocoding
     - TBD — S01 SAR product type codes fixed in the ICD at PDR
   * - ``calibration``
     - TBD (PDR)
     - TBD

The phase chains are baselined with the SRS/SDD; until then the driver only
validates its arguments and reports the (empty) phase plan.
