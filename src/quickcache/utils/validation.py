"""
Validation utilities for cache operations.
"""
from typing import Union, Optional
from datetime import timedelta

def validate_ttl(ttl: Optional[Union[int, timedelta]]) -> Optional[timedelta]:
    """
    Validate and convert TTL to timedelta.
    
    Args:
        ttl: Time-to-live value (int seconds or timedelta)
        
    Returns:
        Validated timedelta object or None
        
    Raises:
        ValueError: If TTL is negative or invalid type
    """
    if ttl is None:
        return None
        
    if isinstance(ttl, int):
        if ttl < 0:
            raise ValueError("TTL cannot be negative")
        return timedelta(seconds=ttl)
        
    if isinstance(ttl, timedelta):
        if ttl.total_seconds() < 0:
            raise ValueError("TTL cannot be negative")
        return ttl
        
    raise ValueError(f"Invalid TTL type: {type(ttl)}. Must be int or timedelta.")