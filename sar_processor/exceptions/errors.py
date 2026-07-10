"""Typed error hierarchy (grows with the stage set; see SDD <5.2>)."""


class SarProcessorError(Exception):
    """Base class for all sar-processor errors."""


class InputValidationError(SarProcessorError):
    """An input product or parameter failed validation."""
