"""Tests for key generation utilities."""
import pytest
from pocket_cache.utils.key import generate_key

def test_generate_key_basic():
    """Test basic key generation with prefix and function name only."""
    key = generate_key("test", "my_func", (), {})
    assert key == "test:my_func"

def test_generate_key_with_args():
    """Test key generation with positional arguments."""
    key = generate_key("test", "my_func", (1, "two", 3.0), {})
    assert "test:my_func" in key
    assert "1" in key
    assert "two" in key
    assert "3.0" in key

def test_generate_key_with_kwargs():
    """Test key generation with keyword arguments."""
    key = generate_key("test", "my_func", (), {"a": 1, "b": "two"})
    assert "test:my_func" in key
    assert "a" in key
    assert "b" in key
    assert "1" in key
    assert "two" in key

def test_generate_key_with_args_and_kwargs():
    """Test key generation with both positional and keyword arguments."""
    key = generate_key("test", "my_func", (1, 2), {"a": "b"})
    assert "test:my_func" in key
    assert "1" in key
    assert "2" in key
    assert "a" in key
    assert "b" in key

def test_generate_key_complex_objects():
    """Test key generation with complex objects."""
    args = ({"nested": {"dict": True}}, [1, 2, {"list": "item"}])
    kwargs = {"complex": {"nested": ["list", "items"]}}
    key = generate_key("test", "my_func", args, kwargs)
    assert "test:my_func" in key
    assert "nested" in key
    assert "dict" in key
    assert "list" in key

def test_generate_key_long_input():
    """Test key generation with very long input that triggers hashing."""
    long_string = "x" * 300  # Create a string longer than 250 chars
    key = generate_key("test", "my_func", (long_string,), {})
    # The result should be a SHA-256 hash (64 characters)
    assert len(key) == 64
    assert all(c in "0123456789abcdef" for c in key) 