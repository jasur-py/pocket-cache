"""Tests for cache decorators."""
from datetime import timedelta
import time
import pytest
from pocket_cache import Cache
from pocket_cache.utils.decorators import cached

def test_cached_decorator():
    """Test basic cached decorator functionality."""
    call_count = 0
    
    @cached(ttl=30)
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call should execute the function
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count == 1
    
    # Second call should use cached result
    result2 = expensive_function(5)
    assert result2 == 10
    assert call_count == 1  # Call count shouldn't increase
    
    # Different argument should compute
    result3 = expensive_function(10)
    assert result3 == 20
    assert call_count == 2

def test_cached_decorator_different_args():
    """Test cached decorator with different argument types."""
    call_count = 0
    
    @cached()
    def func_with_args(a, b=None, *args, **kwargs):
        nonlocal call_count
        call_count += 1
        return f"{a}:{b}:{args}:{sorted(kwargs.items())}"
    
    # Test with different argument combinations
    result1 = func_with_args(1)
    result2 = func_with_args(1)  # Should use cache
    assert result1 == result2
    assert call_count == 1
    
    result3 = func_with_args(1, 2)  # Different args
    result4 = func_with_args(1, 2)  # Should use cache
    assert result3 == result4
    assert call_count == 2
    
    result5 = func_with_args(1, 2, 3, 4)  # Variable args
    result6 = func_with_args(1, 2, 3, 4)  # Should use cache
    assert result5 == result6
    assert call_count == 3
    
    result7 = func_with_args(1, x=2, y=3)  # Keyword args
    result8 = func_with_args(1, x=2, y=3)  # Should use cache
    assert result7 == result8
    assert call_count == 4

def test_cached_decorator_expiration():
    """Test cached decorator with TTL expiration."""
    call_count = 0
    
    @cached(ttl=1)  # 1 second TTL
    def func_with_ttl(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call
    result1 = func_with_ttl(5)
    assert result1 == 10
    assert call_count == 1
    
    # Call before expiration
    result2 = func_with_ttl(5)
    assert result2 == 10
    assert call_count == 1
    
    # Wait for TTL to expire
    time.sleep(1.1)
    
    # Call after expiration
    result3 = func_with_ttl(5)
    assert result3 == 10
    assert call_count == 2

def test_cached_decorator_with_custom_cache():
    """Test cached decorator with custom cache instance."""
    call_count = 0
    custom_cache = Cache(default_ttl=60)
    
    @cached(cache=custom_cache)
    def func_with_custom_cache(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call
    result1 = func_with_custom_cache(5)
    assert result1 == 10
    assert call_count == 1
    
    # Second call should use cache
    result2 = func_with_custom_cache(5)
    assert result2 == 10
    assert call_count == 1

def test_cached_decorator_with_key_prefix():
    """Test cached decorator with custom key prefix."""
    call_count = 0
    
    @cached(key_prefix="test_prefix")
    def func_with_prefix(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call
    result1 = func_with_prefix(5)
    assert result1 == 10
    assert call_count == 1
    
    # Second call should use cache
    result2 = func_with_prefix(5)
    assert result2 == 10
    assert call_count == 1

def test_cached_decorator_with_timedelta():
    """Test cached decorator with timedelta TTL."""
    call_count = 0
    
    @cached(ttl=timedelta(seconds=1))
    def func_with_timedelta(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call
    result1 = func_with_timedelta(5)
    assert result1 == 10
    assert call_count == 1
    
    # Call before expiration
    result2 = func_with_timedelta(5)
    assert result2 == 10
    assert call_count == 1
    
    # Wait for TTL to expire
    time.sleep(1.1)
    
    # Call after expiration
    result3 = func_with_timedelta(5)
    assert result3 == 10
    assert call_count == 2 