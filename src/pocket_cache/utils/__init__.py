"""
Utility functions for QuickCache.
"""
from .key import generate_key
from .validation import validate_ttl

__all__ = ['generate_key', 'validate_ttl']