"""Tests for validation utilities."""
from datetime import timedelta

import pytest

from pocket_cache.utils.validation import validate_ttl


def test_validate_ttl_none():
    """Test that None TTL is handled correctly."""
    assert validate_ttl(None) is None


def test_validate_ttl_positive_int():
    """Test positive integer TTL."""
    result = validate_ttl(60)
    assert isinstance(result, timedelta)
    assert result.total_seconds() == 60


def test_validate_ttl_zero_int():
    """Test zero integer TTL."""
    result = validate_ttl(0)
    assert isinstance(result, timedelta)
    assert result.total_seconds() == 0


def test_validate_ttl_negative_int():
    """Test that negative integer TTL raises ValueError."""
    with pytest.raises(ValueError, match="TTL cannot be negative"):
        validate_ttl(-1)


def test_validate_ttl_positive_timedelta():
    """Test positive timedelta TTL."""
    td = timedelta(minutes=5)
    result = validate_ttl(td)
    assert result == td


def test_validate_ttl_zero_timedelta():
    """Test zero timedelta TTL."""
    td = timedelta()
    result = validate_ttl(td)
    assert result == td


def test_validate_ttl_negative_timedelta():
    """Test that negative timedelta TTL raises ValueError."""
    td = timedelta(seconds=-1)
    with pytest.raises(ValueError, match="TTL cannot be negative"):
        validate_ttl(td)


def test_validate_ttl_invalid_type():
    """Test that invalid TTL type raises ValueError."""
    with pytest.raises(ValueError, match="Invalid TTL type"):
        validate_ttl("60")  # type: ignore


def test_validate_ttl_float():
    """Test that float TTL raises ValueError."""
    with pytest.raises(ValueError, match="Invalid TTL type"):
        validate_ttl(60.0)  # type: ignore
