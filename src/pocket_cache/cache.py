"""
Core cache implementation for PocketCache.
"""
from typing import Any, Optional, Type, TypeVar, Callable, Union
from functools import wraps
import time
from datetime import timedelta
import hashlib
import json

from pocket_cache.backends.base import BaseBackend
from pocket_cache.backends.memory import MemoryCache
from pocket_cache.serializers.base import BaseSerializer
from pocket_cache.serializers.json import JSONSerializer
from pocket_cache.utils.key import generate_key
from pocket_cache.utils.validation import validate_ttl

T = TypeVar("T")

class Cache:
    """
    Main cache implementation that handles caching logic and interfaces with backends.
    """
    
    def __init__(
        self,
        backend: Optional[BaseBackend] = None,
        serializer: Optional[BaseSerializer] = None,
        default_ttl: Union[int, timedelta] = 300,
    ):
        """
        Initialize the cache with a backend and serializer.
        
        Args:
            backend: Cache backend to use. Defaults to MemoryCache.
            serializer: Serializer to use. Defaults to JSONSerializer.
            default_ttl: Default time-to-live in seconds or a timedelta. Defaults to 300.
        """
        self.backend = backend or MemoryCache()
        self.serializer = serializer or JSONSerializer()
        self.default_ttl = default_ttl if isinstance(default_ttl, timedelta) else timedelta(seconds=default_ttl)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from the cache.
        
        Args:
            key: Cache key
            default: Default value if key doesn't exist
            
        Returns:
            Cached value or default if not found
        """
        data = self.backend.get(key)
        if data is None:
            return default
        return self.serializer.deserialize(data)
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[Union[int, timedelta]] = None
    ) -> None:
        """
        Store a value in the cache.
        
        Args:
            key: Cache key
            value: Value to store
            ttl: Time-to-live (optional)
        """
        if ttl is None:
            ttl = self.default_ttl
        elif isinstance(ttl, int):
            ttl = timedelta(seconds=ttl)

        serialized = self.serializer.serialize(value)
        self.backend.set(key, serialized, ttl)
    
    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
        """
        self.backend.delete(key)
    
    def clear(self) -> None:
        """Clear all values from the cache."""
        self.backend.clear()
    
    def cached(
        self,
        ttl: Optional[int] = None,
        key_prefix: str = "",
        key_generator: Optional[Callable[..., str]] = None,
    ) -> Callable[[Callable[..., T]], Callable[..., T]]:
        """
        Decorator to cache function results.
        
        Args:
            ttl: Time-to-live in seconds
            key_prefix: Prefix for cache keys
            key_generator: Custom function to generate cache keys
            
        Returns:
            Decorated function
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> T:
                if key_generator:
                    key = key_generator(*args, **kwargs)
                else:
                    key = generate_key(key_prefix, func.__name__, args, kwargs)
                
                result = self.get(key)
                if result is not None:
                    return result
                
                result = func(*args, **kwargs)
                self.set(key, result, ttl)
                return result
            return wrapper
        return decorator 