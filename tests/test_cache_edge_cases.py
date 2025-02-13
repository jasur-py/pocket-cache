"""Tests for cache edge cases."""
import pytest
from datetime import timedelta
from pocket_cache.cache import Cache
from pocket_cache.backends.memory import MemoryCache

def test_set_with_integer_ttl():
    """Test setting cache with integer TTL."""
    cache = Cache(backend=MemoryCache())
    key = "test_key"
    value = "test_value"
    
    # Set with integer TTL (seconds)
    cache.set(key, value, ttl=60)
    
    # Verify value was stored
    assert cache.get(key) == value

def test_cache_with_custom_key_generator():
    """Test cache decorator with custom key generator."""
    cache = Cache(backend=MemoryCache())
    
    def key_generator(*args, **kwargs):
        return "custom_key"
    
    @cache.cached(key_generator=key_generator)
    def test_func(x, y):
        return x + y
    
    # First call should cache the result
    result1 = test_func(1, 2)
    assert result1 == 3
    
    # Second call should return cached result
    result2 = test_func(3, 4)  # Different args, but same key
    assert result2 == 3  # Should return cached result from first call

def test_set_with_none_ttl():
    """Test setting cache with None TTL."""
    cache = Cache(backend=MemoryCache(), default_ttl=timedelta(seconds=60))
    key = "test_key"
    value = "test_value"
    
    # Set with None TTL (should use default)
    cache.set(key, value, ttl=None)
    
    # Verify value was stored
    assert cache.get(key) == value 