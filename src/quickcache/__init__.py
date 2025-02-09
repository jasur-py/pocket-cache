"""QuickCache - A fast and flexible API response caching library."""

from .cache import Cache
from .backends.base import BaseBackend
from .backends.memory import MemoryCache

__version__ = "0.1.0"
__all__ = ['Cache', 'BaseBackend', 'MemoryCache']