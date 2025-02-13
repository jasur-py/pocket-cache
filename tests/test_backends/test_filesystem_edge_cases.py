"""Tests for filesystem backend edge cases."""
import os
import tempfile
import time
from datetime import timedelta
import pytest
from pocket_cache.backends.filesystem import FileSystemCache

@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def test_zero_ttl(temp_cache_dir):
    """Test that values with zero TTL are not written to file."""
    backend = FileSystemCache(temp_cache_dir)
    key = "test_key"
    value = b"test_value"
    
    # Try to set with zero TTL
    backend.set(key, value, ttl=timedelta(seconds=0))
    
    # Verify file wasn't created
    path = os.path.join(temp_cache_dir, str(hash(key)) + ".cache")
    assert not os.path.exists(path)

def test_negative_ttl(temp_cache_dir):
    """Test that values with negative TTL are not written to file."""
    backend = FileSystemCache(temp_cache_dir)
    key = "test_key"
    value = b"test_value"
    
    # Try to set with negative TTL
    backend.set(key, value, ttl=timedelta(seconds=-1))
    
    # Verify file wasn't created
    path = os.path.join(temp_cache_dir, str(hash(key)) + ".cache")
    assert not os.path.exists(path)

def test_clear_nonexistent_directory(temp_cache_dir):
    """Test clearing cache when directory doesn't exist."""
    nonexistent_dir = os.path.join(temp_cache_dir, "nonexistent")
    backend = FileSystemCache(nonexistent_dir)
    
    # Should not raise any exception
    backend.clear()

def test_clear_with_io_error(temp_cache_dir):
    """Test clear() when there's an IO error."""
    backend = FileSystemCache(temp_cache_dir)
    
    # Create a test cache file
    key = "test_key"
    value = b"test_value"
    backend.set(key, value, ttl=timedelta(seconds=60))
    
    # Create a directory that will cause OSError during listdir
    os.chmod(temp_cache_dir, 0o000)
    
    try:
        # Should not raise exception even if clearing fails
        backend.clear()
    finally:
        # Restore permissions so the temporary directory can be cleaned up
        os.chmod(temp_cache_dir, 0o755)

def test_write_with_io_error_cleanup(temp_cache_dir):
    """Test cleanup of temporary file when write fails."""
    backend = FileSystemCache(temp_cache_dir)
    key = "test_key"
    value = b"test_value"
    
    # Create a temp file that will cause IOError during write
    temp_path = os.path.join(temp_cache_dir, str(hash(key)) + ".cache.tmp")
    with open(temp_path, 'w') as f:
        f.write('dummy')
    
    # Make the temp file read-only
    os.chmod(temp_path, 0o444)
    
    try:
        # Should raise IOError and clean up temp file
        with pytest.raises(IOError):
            backend.set(key, value, ttl=timedelta(seconds=60))
            
        # Verify temp file was cleaned up
        assert not os.path.exists(temp_path)
    finally:
        # Restore permissions and cleanup if needed
        if os.path.exists(temp_path):
            os.chmod(temp_path, 0o644)
            os.unlink(temp_path)

def test_write_with_zero_ttl_early_return(temp_cache_dir):
    """Test that _write_cache_file returns early with zero TTL."""
    backend = FileSystemCache(temp_cache_dir)
    key = "test_key"
    value = b"test_value"
    
    # Set with zero TTL
    backend.set(key, value, ttl=timedelta(seconds=0))
    
    # Verify no files were created
    cache_file = os.path.join(temp_cache_dir, str(hash(key)) + ".cache")
    temp_file = os.path.join(temp_cache_dir, str(hash(key)) + ".cache.tmp")
    assert not os.path.exists(cache_file)
    assert not os.path.exists(temp_file)

def test_clear_with_permission_error(temp_cache_dir):
    """Test clear() when there's a permission error on a file."""
    backend = FileSystemCache(temp_cache_dir)
    
    # Create a test cache file
    key = "test_key"
    value = b"test_value"
    backend.set(key, value, ttl=timedelta(seconds=60))
    
    # Make the cache file read-only and make the directory read-only
    cache_file = os.path.join(temp_cache_dir, str(hash(key)) + ".cache")
    os.chmod(cache_file, 0o444)
    os.chmod(temp_cache_dir, 0o555)  # r-xr-xr-x
    
    try:
        # Should not raise exception even if file deletion fails
        backend.clear()
        
        # File should still exist since we couldn't delete it
        assert os.path.exists(cache_file)
    finally:
        # Restore permissions for cleanup
        os.chmod(temp_cache_dir, 0o755)
        if os.path.exists(cache_file):
            os.chmod(cache_file, 0o644)

def test_write_with_zero_ttl_direct(temp_cache_dir):
    """Test that _write_cache_file returns early with zero TTL."""
    backend = FileSystemCache(temp_cache_dir)
    key = "test_key"
    value = b"test_value"
    path = os.path.join(temp_cache_dir, str(hash(key)) + ".cache")
    
    # Call _write_cache_file directly with zero TTL
    backend._write_cache_file(path, value, ttl=timedelta(seconds=0))
    
    # Verify no files were created
    assert not os.path.exists(path)
    assert not os.path.exists(path + ".tmp") 