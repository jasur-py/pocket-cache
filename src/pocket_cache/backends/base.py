"""
Base class for cache backend implementations.
"""
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

class BaseBackend(ABC):
    """Abstract base class for cache backends."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[bytes]:
        """
        Retrieve a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value as bytes or None if not found
        """
        pass

    @abstractmethod
    def set(self, key: str, value: bytes, ttl: timedelta) -> None:
        """
        Store a value in the cache.
        
        Args:
            key: Cache key
            value: Value to store as bytes
            ttl: Time-to-live
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all values from the cache."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close any resources used by the backend."""
        pass