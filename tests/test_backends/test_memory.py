from datetime import timedelta
import time
import pytest
from pocket_cache.backends.memory import MemoryCache

def test_memory_backend_set_get():
    backend = MemoryCache()
    backend.set("test_key", b"test_value", ttl=timedelta(seconds=1))
    assert backend.get("test_key") == b"test_value"

def test_memory_backend_expiration():
    backend = MemoryCache()
    backend.set("test_key", b"test_value", ttl=timedelta(seconds=1))
    time.sleep(1.1)
    assert backend.get("test_key") is None

def test_memory_backend_delete():
    backend = MemoryCache()
    backend.set("test_key", b"test_value", ttl=timedelta(seconds=30))
    backend.delete("test_key")
    assert backend.get("test_key") is None 