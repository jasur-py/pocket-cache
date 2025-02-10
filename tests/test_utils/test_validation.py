"""Tests for validation utilities."""
import pytest
from datetime import timedelta
from pocket_cache.utils.validation import validate_ttl

def test_validate_ttl_none():
    """Test that None TTL returns None."""
    assert validate_ttl(None) is None

def test_validate_ttl_positive_int():
    """Test that positive integer TTL is converted to timedelta."""
    result = validate_ttl(60)
    assert isinstance(result, timedelta)
    assert result.total_seconds() == 60

def test_validate_ttl_negative_int():
    """Test that negative integer TTL raises ValueError."""
    with pytest.raises(ValueError, match="TTL cannot be negative"):
        validate_ttl(-60)

def test_validate_ttl_positive_timedelta():
    """Test that positive timedelta TTL is returned as is."""
    td = timedelta(minutes=5)
    result = validate_ttl(td)
    assert result == td

def test_validate_ttl_negative_timedelta():
    """Test that negative timedelta TTL raises ValueError."""
    td = timedelta(seconds=-60)
    with pytest.raises(ValueError, match="TTL cannot be negative"):
        validate_ttl(td)

def test_validate_ttl_invalid_type():
    """Test that invalid TTL type raises ValueError."""
    with pytest.raises(ValueError, match="Invalid TTL type"):
        validate_ttl("60") 