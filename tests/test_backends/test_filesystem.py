"""Tests for filesystem cache backend."""
import os
import time
import json
import shutil
import tempfile
from datetime import timedelta
import pytest
from pathlib import Path

from pocket_cache.backends.filesystem import FileSystemCache

@pytest.fixture
def cache_dir():
    """Create a temporary directory for cache files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def fs_cache(cache_dir):
    """Create a filesystem cache instance."""
    return FileSystemCache(cache_dir=cache_dir)

def test_filesystem_cache_init(cache_dir):
    """Test filesystem cache initialization."""
    # Test with default settings
    cache = FileSystemCache(cache_dir)
    assert os.path.exists(cache_dir)
    assert os.path.isdir(cache_dir)
    
    # Test with custom permissions
    custom_dir = os.path.join(cache_dir, "custom")
    cache = FileSystemCache(custom_dir, dir_mode=0o755, file_mode=0o644)
    assert os.path.exists(custom_dir)
    assert oct(os.stat(custom_dir).st_mode)[-3:] == "755"

    # Test with existing directory
    existing_dir = os.path.join(cache_dir, "existing")
    os.makedirs(existing_dir, mode=0o755)
    cache = FileSystemCache(existing_dir, create_dir=False)
    assert os.path.exists(existing_dir)

    # Test with create_dir=False and non-existent directory
    non_existent_dir = os.path.join(cache_dir, "nonexistent")
    with pytest.raises(OSError):
        FileSystemCache(non_existent_dir, create_dir=False)

def test_filesystem_cache_set_get(fs_cache):
    """Test basic set and get operations."""
    # Test with string value
    fs_cache.set("key1", b"value1")
    assert fs_cache.get("key1") == b"value1"
    
    # Test with bytes value
    fs_cache.set("key2", b"value2")
    assert fs_cache.get("key2") == b"value2"
    
    # Test non-existent key
    assert fs_cache.get("nonexistent") is None

    # Test with empty value
    fs_cache.set("empty_key", b"")
    assert fs_cache.get("empty_key") == b""

    # Test with special characters in key
    special_key = "!@#$%^&*()_+"
    fs_cache.set(special_key, b"special")
    assert fs_cache.get(special_key) == b"special"

def test_filesystem_cache_ttl(fs_cache):
    """Test TTL functionality."""
    # Set with TTL
    fs_cache.set("key1", b"value1", ttl=timedelta(seconds=1))
    assert fs_cache.get("key1") == b"value1"
    
    # Wait for expiration
    time.sleep(1.1)
    assert fs_cache.get("key1") is None
    
    # Test with no TTL
    fs_cache.set("key2", b"value2")
    assert fs_cache.get("key2") == b"value2"
    time.sleep(1.1)
    assert fs_cache.get("key2") == b"value2"

    # Test with zero TTL
    fs_cache.set("key3", b"value3", ttl=timedelta(seconds=0))
    assert fs_cache.get("key3") is None

def test_filesystem_cache_delete(fs_cache):
    """Test delete operation."""
    fs_cache.set("key1", b"value1")
    assert fs_cache.get("key1") == b"value1"
    
    fs_cache.delete("key1")
    assert fs_cache.get("key1") is None
    
    # Delete non-existent key should not raise error
    fs_cache.delete("nonexistent")

    # Delete and verify file is removed
    fs_cache.set("key2", b"value2")
    file_path = fs_cache._get_file_path("key2")
    assert os.path.exists(file_path)
    fs_cache.delete("key2")
    assert not os.path.exists(file_path)

def test_filesystem_cache_clear(fs_cache):
    """Test clear operation."""
    # Set multiple values
    fs_cache.set("key1", b"value1")
    fs_cache.set("key2", b"value2")
    
    # Clear cache
    fs_cache.clear()
    
    # Verify all values are cleared
    assert fs_cache.get("key1") is None
    assert fs_cache.get("key2") is None

    # Test clear on empty cache
    fs_cache.clear()  # Should not raise any errors

    # Test clear with non-cache files in directory
    non_cache_file = os.path.join(fs_cache.cache_dir, "not_a_cache_file.txt")
    with open(non_cache_file, 'w') as f:
        f.write("test")
    fs_cache.clear()
    assert os.path.exists(non_cache_file)  # Non-cache file should remain

def test_filesystem_cache_file_content(fs_cache, cache_dir):
    """Test the structure and content of cache files."""
    fs_cache.set("key1", b"value1", ttl=timedelta(seconds=60))
    
    # Get the cache file path
    filename = str(hash("key1")) + ".cache"
    file_path = os.path.join(cache_dir, filename)
    
    # Verify file exists and has correct permissions
    assert os.path.exists(file_path)
    assert oct(os.stat(file_path).st_mode)[-3:] == "600"
    
    # Verify file content structure
    with open(file_path, 'r') as f:
        data = json.load(f)
        assert 'value' in data
        assert 'created_at' in data
        assert 'expires_at' in data
        assert data['value'] == "value1"
        assert isinstance(data['created_at'], float)
        assert isinstance(data['expires_at'], float)

def test_filesystem_cache_concurrent_access(fs_cache):
    """Test concurrent access handling."""
    # Write same key multiple times
    for i in range(100):
        fs_cache.set("concurrent_key", f"value{i}".encode())
    
    # Verify we can still read the value
    value = fs_cache.get("concurrent_key")
    assert value is not None
    assert value.startswith(b"value")

def test_filesystem_cache_invalid_files(fs_cache, cache_dir):
    """Test handling of invalid cache files."""
    # Create an invalid cache file
    filename = str(hash("invalid_key")) + ".cache"
    file_path = os.path.join(cache_dir, filename)
    
    with open(file_path, 'w') as f:
        f.write("invalid json")
    
    # Reading invalid file should return None
    assert fs_cache.get("invalid_key") is None

    # Test with corrupted JSON structure
    filename2 = str(hash("corrupted_key")) + ".cache"
    file_path2 = os.path.join(cache_dir, filename2)
    with open(file_path2, 'w') as f:
        f.write('{"value": "test", "created_at": "invalid"}')
    assert fs_cache.get("corrupted_key") is None

def test_filesystem_cache_large_values(fs_cache):
    """Test handling of large values."""
    large_value = b"x" * 1024 * 1024  # 1MB
    fs_cache.set("large_key", large_value)
    assert fs_cache.get("large_key") == large_value

def test_filesystem_cache_error_handling(fs_cache, cache_dir):
    """Test error handling in various scenarios."""
    # Test with read-only directory
    readonly_dir = os.path.join(cache_dir, "readonly")
    os.makedirs(readonly_dir, mode=0o555)
    readonly_cache = FileSystemCache(readonly_dir)
    
    # Attempt to write to read-only directory
    with pytest.raises(IOError):
        readonly_cache.set("key", b"value")

    # Test with invalid file permissions
    fs_cache.set("perm_key", b"value")
    file_path = fs_cache._get_file_path("perm_key")
    os.chmod(file_path, 0o000)  # Remove all permissions
    assert fs_cache.get("perm_key") is None

    # Test with corrupted temporary file
    key = "temp_key"
    fs_cache.set(key, b"value")
    temp_path = fs_cache._get_file_path(key) + '.tmp'
    
    # Create a corrupted temp file
    with open(temp_path, 'w') as f:
        f.write('corrupted')
    
    # Attempt to write, should handle temp file cleanup
    fs_cache.set(key, b"new_value")
    assert not os.path.exists(temp_path)
    assert fs_cache.get(key) == b"new_value"

def test_filesystem_cache_close(fs_cache):
    """Test close method."""
    # close() should not raise any errors
    fs_cache.close()
    
    # Operations should still work after close
    fs_cache.set("key", b"value")
    assert fs_cache.get("key") == b"value"

def test_filesystem_cache_clear_error_handling(fs_cache, cache_dir):
    """Test error handling during clear operation."""
    # Create some cache files
    fs_cache.set("key1", b"value1")
    fs_cache.set("key2", b"value2")
    
    # Create a directory that can't be listed
    no_access_dir = os.path.join(cache_dir, "no_access")
    os.makedirs(no_access_dir)
    no_access_cache = FileSystemCache(no_access_dir)
    
    try:
        os.chmod(no_access_dir, 0o000)  # Remove all permissions
        # Clear should handle permission errors gracefully
        no_access_cache.clear()  # Should not raise exception
    finally:
        # Restore permissions for cleanup
        os.chmod(no_access_dir, 0o700)

def test_filesystem_cache_read_errors(fs_cache):
    """Test various read error scenarios."""
    # Test with file that exists but can't be read
    key = "unreadable"
    fs_cache.set(key, b"value")
    file_path = fs_cache._get_file_path(key)
    os.chmod(file_path, 0o200)  # Write-only permissions
    assert fs_cache.get(key) is None

    # Test with file that becomes inaccessible
    key2 = "disappearing"
    fs_cache.set(key2, b"value")
    file_path2 = fs_cache._get_file_path(key2)
    os.unlink(file_path2)  # Remove file after setting
    assert fs_cache.get(key2) is None 