"""
Utilities for generating cache keys.
"""
from typing import Any, Dict, Tuple
import hashlib
import json

def generate_key(prefix: str, func_name: str, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> str:
    """
    Generate a cache key from function arguments.
    
    Args:
        prefix: Key prefix
        func_name: Function name
        args: Positional arguments
        kwargs: Keyword arguments
        
    Returns:
        Cache key string
    """
    # Convert args and kwargs to a string representation
    key_parts = [prefix, func_name]
    
    # Add args to key parts
    if args:
        args_str = json.dumps(args, sort_keys=True)
        key_parts.append(args_str)
    
    # Add kwargs to key parts
    if kwargs:
        kwargs_str = json.dumps(kwargs, sort_keys=True)
        key_parts.append(kwargs_str)
    
    # Join parts with colon
    key = ":".join(key_parts)
    
    # If key is too long, hash it
    if len(key) > 250:
        key = hashlib.sha256(key.encode()).hexdigest()
    
    return key
