"""Tests for key generation utilities."""
from pocket_cache.utils.key import generate_key


def test_generate_key_basic():
    """Test basic key generation."""
    key = generate_key("test", "func", (), {})
    assert key == "test:func"


def test_generate_key_with_args():
    """Test key generation with positional arguments."""
    key = generate_key("test", "func", (1, "two", 3.0), {})
    assert "test:func" in key
    assert '[1, "two", 3.0]' in key


def test_generate_key_with_kwargs():
    """Test key generation with keyword arguments."""
    key = generate_key("test", "func", (), {"a": 1, "b": 2})
    assert "test:func" in key
    assert '{"a": 1, "b": 2}' in key


def test_generate_key_with_args_and_kwargs():
    """Test key generation with both args and kwargs."""
    key = generate_key("test", "func", (1, 2), {"a": 3, "b": 4})
    assert "test:func" in key
    assert "[1, 2]" in key
    assert '{"a": 3, "b": 4}' in key


def test_generate_key_empty_prefix():
    """Test key generation with empty prefix."""
    key = generate_key("", "func", (1,), {})
    assert key == ":func:[1]"


def test_generate_key_none_values():
    """Test key generation with None values."""
    key = generate_key("test", "func", (None,), {"null": None})
    assert "test:func" in key
    assert "[null]" in key
    assert '{"null": null}' in key


def test_generate_key_nested_structures():
    """Test key generation with nested data structures."""
    args = ([1, 2, {"inner": [3, 4]}],)
    kwargs = {"dict": {"a": [1, 2], "b": {"c": 3}}}
    key = generate_key("test", "func", args, kwargs)
    assert "test:func" in key
    assert "inner" in key
    assert "dict" in key


def test_generate_key_long_key():
    """Test key generation with very long input that requires hashing."""
    long_string = "x" * 300
    key = generate_key("test", "func", (long_string,), {})
    assert len(key) == 64  # SHA-256 hexdigest length
    assert all(c in "0123456789abcdef" for c in key)


def test_generate_key_special_characters():
    """Test key generation with special characters."""
    key = generate_key("test", "func", ("!@#$%^&*",), {"key:with:colons": "value"})
    assert "test:func" in key
    assert "!@#$%^&*" in key
    assert "key:with:colons" in key


def test_generate_key_unicode():
    """Test key generation with Unicode characters."""
    key = generate_key("test", "func", ("你好",), {"emoji": "🐍"})
    assert "test:func" in key
    # Check for escaped Unicode sequences
    assert "\\u4f60\\u597d" in key  # Escaped form of "你好"
    assert "\\ud83d\\udc0d" in key  # Escaped form of "🐍"
