"""
Tests for the core cache functionality.
"""
import pytest
from time import sleep
from datetime import timedelta
import time

from quickcache import Cache
from quickcache.backends.memory import MemoryCache
from quickcache.serializers.json import JSONSerializer

@pytest.fixture
def cache():
    """Create a cache instance for testing."""
    return Cache(
        backend=MemoryCache(),
        serializer=JSONSerializer(),
        default_ttl=60
    )

def test_basic_operations(cache):
    """Test basic cache operations."""
    # Test set and get
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    
    # Test default value for non-existent key
    assert cache.get("non_existent") is None
    assert cache.get("non_existent", "default") == "default"
    
    # Test delete
    cache.delete("key1")
    assert cache.get("key1") is None

def test_ttl(cache):
    """Test time-to-live functionality."""
    cache.set("key1", "value1", ttl=1)  # 1 second TTL
    assert cache.get("key1") == "value1"
    
    sleep(1.1)  # Wait for TTL to expire
    assert cache.get("key1") is None

def test_clear(cache):
    """Test cache clearing."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None

def test_cached_decorator(cache):
    """Test the @cached decorator."""
    call_count = 0
    
    @cache.cached(ttl=60)
    def expensive_operation(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call should compute
    assert expensive_operation(5) == 10
    assert call_count == 1
    
    # Second call should use cache
    assert expensive_operation(5) == 10
    assert call_count == 1  # Call count shouldn't increase
    
    # Different argument should compute
    assert expensive_operation(10) == 20
    assert call_count == 2

def test_cache_set_get():
    cache = Cache()
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"

def test_cache_ttl():
    cache = Cache()
    cache.set("test_key", "test_value", ttl=1)
    assert cache.get("test_key") == "test_value"
    time.sleep(1.1)
    assert cache.get("test_key") is None

def test_cache_delete():
    cache = Cache()
    cache.set("test_key", "test_value")
    cache.delete("test_key")
    assert cache.get("test_key") is None

def test_cache_clear():
    cache = Cache()
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None

def test_cache_default_value():
    cache = Cache()
    assert cache.get("nonexistent", default="default") == "default" 