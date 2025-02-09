"""
QuickCache - A fast and flexible caching library for Python.
"""

from quickcache.cache import Cache
from quickcache.backends import MemoryBackend, RedisBackend, FilesystemBackend
from quickcache.serializers import JSONSerializer, PickleSerializer

__version__ = "0.1.0"

__all__ = [
    "Cache",
    "MemoryBackend",
    "RedisBackend",
    "FilesystemBackend",
    "JSONSerializer",
    "PickleSerializer",
] 