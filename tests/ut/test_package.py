"""Smoke tests for the package skeleton (keeps the CI unit-tests gate green)."""

import pytest

import sar_processor
from sar_processor.exceptions import InputValidationError, SarProcessorError


@pytest.mark.unit
def test_version_is_set() -> None:
    assert sar_processor.__version__


@pytest.mark.unit
def test_error_hierarchy() -> None:
    assert issubclass(InputValidationError, SarProcessorError)
    assert issubclass(SarProcessorError, Exception)
