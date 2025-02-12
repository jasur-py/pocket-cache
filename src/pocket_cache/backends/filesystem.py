"""
File system backend implementation for PocketCache.

This backend stores cache data in files, providing persistent storage
with automatic TTL expiration and proper file management.
"""
import os
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import timedelta

from .base import BaseBackend

class FileSystemCache(BaseBackend):
    """
    File system cache backend that stores cache entries as files.
    
    Each cache entry is stored as a separate file containing both
    the data and metadata (expiration time, creation time).
    """
    
    def __init__(
        self,
        cache_dir: str = ".cache",
        create_dir: bool = True,
        dir_mode: int = 0o700,
        file_mode: int = 0o600,
    ):
        """
        Initialize the file system cache.
        
        Args:
            cache_dir: Directory to store cache files
            create_dir: Whether to create the cache directory if it doesn't exist
            dir_mode: Permission mode for cache directory
            file_mode: Permission mode for cache files
            
        Raises:
            OSError: If create_dir is False and cache_dir doesn't exist
        """
        self.cache_dir = os.path.abspath(cache_dir)
        self.dir_mode = dir_mode
        self.file_mode = file_mode
        
        if not os.path.exists(self.cache_dir):
            if create_dir:
                os.makedirs(self.cache_dir, mode=self.dir_mode, exist_ok=True)
            else:
                raise OSError(f"Cache directory {self.cache_dir} does not exist")
    
    def _get_file_path(self, key: str) -> str:
        """Get the file path for a cache key."""
        # Use hash of key for filename to avoid filesystem issues
        filename = str(hash(key)) + ".cache"
        return os.path.join(self.cache_dir, filename)
    
    def _read_cache_file(self, path: str) -> Optional[Dict[str, Any]]:
        """Read and parse a cache file."""
        try:
            with open(path, 'rb') as f:
                data = json.loads(f.read().decode('utf-8'))
                
            # Check if entry has expired
            if data['expires_at'] is not None and time.time() > data['expires_at']:
                self._remove_file(path)
                return None
                
            return data
        except (IOError, json.JSONDecodeError, KeyError):
            return None
    
    def _write_cache_file(self, path: str, value: bytes, ttl: Optional[timedelta]) -> None:
        """Write data to a cache file."""
        if ttl is not None and ttl.total_seconds() <= 0:
            # Don't write to file if TTL is zero or negative
            return
            
        expires_at = time.time() + ttl.total_seconds() if ttl else None
        
        data = {
            'value': value.decode('utf-8'),
            'created_at': time.time(),
            'expires_at': expires_at
        }
        
        # Write to temporary file first to ensure atomic operation
        temp_path = path + '.tmp'
        try:
            with open(temp_path, 'w') as f:
                json.dump(data, f)
            os.chmod(temp_path, self.file_mode)
            os.replace(temp_path, path)
        except IOError:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise
    
    def _remove_file(self, path: str) -> None:
        """Safely remove a cache file."""
        try:
            os.unlink(path)
        except OSError:
            pass
    
    def get(self, key: str) -> Optional[bytes]:
        """
        Retrieve a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        path = self._get_file_path(key)
        data = self._read_cache_file(path)
        
        if data and 'value' in data:
            return data['value'].encode('utf-8')
        return None
    
    def set(self, key: str, value: bytes, ttl: Optional[timedelta] = None) -> None:
        """
        Store a value in the cache.
        
        Args:
            key: Cache key
            value: Value to store
            ttl: Time-to-live
        """
        if ttl is not None and ttl.total_seconds() <= 0:
            self.delete(key)  # Remove the key if TTL is zero or negative
            return
            
        path = self._get_file_path(key)
        self._write_cache_file(path, value, ttl)
    
    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
        """
        path = self._get_file_path(key)
        self._remove_file(path)
    
    def clear(self) -> None:
        """Clear all values from the cache."""
        if not os.path.exists(self.cache_dir):
            return
            
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    path = os.path.join(self.cache_dir, filename)
                    self._remove_file(path)
        except OSError:
            # Handle permission errors or other OS errors gracefully
            pass
    
    def close(self) -> None:
        """Close the cache backend and clean up resources."""
        # Nothing to close for filesystem cache, but we need to implement
        # this method to satisfy the BaseBackend interface
        pass 