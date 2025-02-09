from functools import wraps
from typing import Any, Callable, Optional, Union
from datetime import timedelta

from ..cache import Cache

def cached(
    ttl: Optional[Union[int, timedelta]] = None,
    key_prefix: str = "",
    cache: Optional[Cache] = None,
) -> Callable:
    """
    Decorator for caching function results.
    
    Args:
        ttl: Time-to-live for cached values
        key_prefix: Prefix for cache keys
        cache: Cache instance to use (creates new one if not provided)
        
    Returns:
        Decorated function
    """
    if cache is None:
        cache = Cache()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate cache key from function name, args, and kwargs
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)

            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result

            # If not in cache, call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        return wrapper

    return decorator 