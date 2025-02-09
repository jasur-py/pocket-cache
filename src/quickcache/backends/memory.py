"""
In-memory cache backend implementation.
"""
from typing import Optional, Dict, Tuple
import time
import threading
from datetime import datetime, timedelta

from quickcache.backends.base import BaseBackend

class MemoryBackend(BaseBackend):
    """
    Simple in-memory cache backend using a dictionary.
    Thread-safe implementation.
    """
    
    def __init__(self):
        """Initialize the memory cache."""
        self._cache: Dict[str, Tuple[bytes, datetime]] = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[bytes]:
        """
        Retrieve a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value as bytes or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            value, expiry = self._cache[key]
            if expiry < datetime.now():
                del self._cache[key]
                return None
            
            return value
    
    def set(self, key: str, value: bytes, ttl: timedelta) -> None:
        """
        Store a value in the cache.
        
        Args:
            key: Cache key
            value: Value to store as bytes
            ttl: Time-to-live in seconds
        """
        expiry = datetime.now() + ttl
        with self._lock:
            self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
        """
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all values from the cache."""
        with self._lock:
            self._cache.clear()
    
    def close(self) -> None:
        """No resources to close for memory backend."""
        pass 