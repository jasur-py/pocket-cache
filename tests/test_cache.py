"""
Tests for the core cache functionality.
"""
import pytest
from time import sleep
from datetime import timedelta
import time

from pocket_cache import Cache
from pocket_cache.backends.memory import MemoryCache
from pocket_cache.serializers.json import JSONSerializer

@pytest.fixture
def cache():
    """Create a cache instance for testing."""
    return Cache(
        backend=MemoryCache(),
        serializer=JSONSerializer(),
        default_ttl=60
    )

def test_cache_initialization():
    """Test cache initialization with different parameters."""
    # Default initialization
    cache1 = Cache()
    assert isinstance(cache1.backend, MemoryCache)
    assert isinstance(cache1.serializer, JSONSerializer)
    assert cache1.default_ttl == timedelta(seconds=300)

    # Custom TTL with int
    cache2 = Cache(default_ttl=60)
    assert cache2.default_ttl == timedelta(seconds=60)

    # Custom TTL with timedelta
    cache3 = Cache(default_ttl=timedelta(minutes=5))
    assert cache3.default_ttl == timedelta(minutes=5)

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

def test_ttl_variations(cache):
    """Test different TTL specifications."""
    # Test with int TTL
    cache.set("key1", "value1", ttl=1)
    assert cache.get("key1") == "value1"
    sleep(1.1)
    assert cache.get("key1") is None

    # Test with timedelta TTL
    cache.set("key2", "value2", ttl=timedelta(seconds=1))
    assert cache.get("key2") == "value2"
    sleep(1.1)
    assert cache.get("key2") is None

    # Test with default TTL
    cache.set("key3", "value3")  # Uses default_ttl
    assert cache.get("key3") == "value3"

def test_clear(cache):
    """Test cache clearing."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None

def test_cached_decorator_variations(cache):
    """Test different variations of the @cached decorator."""
    call_count = 0
    
    # Basic caching
    @cache.cached()
    def func1(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    # Custom TTL
    @cache.cached(ttl=1)
    def func2(x):
        nonlocal call_count
        call_count += 1
        return x * 3

    # Custom key prefix
    @cache.cached(key_prefix="custom")
    def func3(x):
        nonlocal call_count
        call_count += 1
        return x * 4

    # Custom key generator
    def custom_key_gen(*args, **kwargs):
        return f"custom_key:{args[0]}"

    @cache.cached(key_generator=custom_key_gen)
    def func4(x):
        nonlocal call_count
        call_count += 1
        return x * 5

    # Test basic caching
    assert func1(5) == 10
    assert func1(5) == 10
    assert call_count == 1

    # Test custom TTL
    assert func2(5) == 15
    assert func2(5) == 15
    sleep(1.1)
    assert func2(5) == 15  # Should recompute
    assert call_count == 3

    # Test custom key prefix
    assert func3(5) == 20
    assert func3(5) == 20
    assert call_count == 4

    # Test custom key generator
    assert func4(5) == 25
    assert func4(5) == 25
    assert call_count == 5

def test_complex_data_types(cache):
    """Test caching of complex data types."""
    # Dictionary
    data_dict = {"a": 1, "b": [1, 2, 3], "c": {"nested": True}}
    cache.set("dict_key", data_dict)
    assert cache.get("dict_key") == data_dict

    # List
    data_list = [1, "two", {"three": 3}, [4, 5, 6]]
    cache.set("list_key", data_list)
    assert cache.get("list_key") == data_list

    # Mixed data
    data_mixed = {
        "string": "value",
        "number": 42,
        "list": [1, 2, 3],
        "dict": {"a": 1},
        "boolean": True,
        "null": None
    }
    cache.set("mixed_key", data_mixed)
    assert cache.get("mixed_key") == data_mixed

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