"""Typed exception hierarchy for sar_processor."""

from sar_processor.exceptions.errors import InputValidationError, SarProcessorError

__all__ = ["SarProcessorError", "InputValidationError"]
