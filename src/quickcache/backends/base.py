"""
Abstract base class for cache backends.
"""
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional, Any

class BaseCacheBackend(ABC):
    """Abstract base class for cache backends."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[bytes]:
        """Retrieve a value from the cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: bytes, ttl: timedelta) -> None:
        """Store a value in the cache."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all values from the cache."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close any connections or resources."""
        pass 