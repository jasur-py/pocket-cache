"""Tests for decorator edge cases."""
import pytest
from pocket_cache.utils.decorators import cached
from pocket_cache.cache import Cache
from pocket_cache.utils.key import generate_key

def test_cached_without_cache_instance():
    """Test cached decorator without providing a cache instance."""
    
    @cached()
    def test_func(x):
        return x * 2
    
    # First call should create cache and store result
    result1 = test_func(5)
    assert result1 == 10
    
    # Second call should use cached result
    result2 = test_func(5)
    assert result2 == 10
    
    # Different input should calculate new result
    result3 = test_func(7)
    assert result3 == 14

def test_cached_with_custom_prefix():
    """Test cached decorator with custom key prefix."""
    
    @cached(key_prefix="custom")
    def test_func(x):
        return x * 2
    
    # Call function and verify it works with custom prefix
    result = test_func(5)
    assert result == 10

def test_cached_with_existing_cache():
    """Test cached decorator with an existing cache instance."""
    cache = Cache()
    
    @cached(cache=cache)
    def test_func(x):
        return x * 2
    
    # Call function and verify it uses the provided cache
    result = test_func(5)
    assert result == 10
    
    # Verify the result is in the cache with the correct key
    # The key format is: prefix:function_name:arg1,arg2,...
    assert cache.get(":test_func:5") == 10 