"""Processing-stage packages (C-PU-*): one subpackage per SAR processing stage.

The stage set (L0 decode, range compression, azimuth focusing, radiometric
calibration, multilook/detection, geocoding, ...) is baselined at PDR/CDR via
the SRS/SDD; stages are added here only after their requirements exist
(doc-first). Each stage follows the msi-processor convention:
``core.py`` (pure numpy algorithm, CPM-free) + ``unit.py`` (EOProcessingUnit).
"""
