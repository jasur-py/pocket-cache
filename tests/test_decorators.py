from quickcache.utils.decorators import cached
import time

def test_cached_decorator():
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

def test_cached_decorator_different_args():
    call_count = 0
    
    @cached(ttl=30)
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count == 1
    
    result2 = expensive_function(10)  # Different argument
    assert result2 == 20
    assert call_count == 2  # Should call function again

def test_cached_decorator_expiration():
    call_count = 0
    
    @cached(ttl=1)  # 1 second TTL
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count == 1
    
    time.sleep(1.1)  # Wait for cache to expire
    
    result2 = expensive_function(5)
    assert result2 == 10
    assert call_count == 2  # Should call function again after expiration 