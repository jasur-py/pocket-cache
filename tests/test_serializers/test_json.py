"""Tests for JSON serializer."""
import pytest
from pocket_cache.serializers.json import JSONSerializer, SerializationError

def test_json_serializer_string():
    """Test serializing and deserializing a string."""
    serializer = JSONSerializer()
    value = "test_string"
    serialized = serializer.serialize(value)
    deserialized = serializer.deserialize(serialized)
    assert deserialized == value

def test_json_serializer_dict():
    """Test serializing and deserializing a dictionary."""
    serializer = JSONSerializer()
    value = {"key": "value", "number": 42}
    serialized = serializer.serialize(value)
    deserialized = serializer.deserialize(serialized)
    assert deserialized == value

def test_json_serializer_list():
    """Test serializing and deserializing a list."""
    serializer = JSONSerializer()
    value = [1, "two", {"three": 3}]
    serialized = serializer.serialize(value)
    deserialized = serializer.deserialize(serialized)
    assert deserialized == value

def test_json_serializer_non_serializable():
    """Test serializing a non-JSON-serializable object."""
    serializer = JSONSerializer()
    with pytest.raises(SerializationError, match="Failed to serialize value to JSON"):
        serializer.serialize(set([1, 2, 3]))

def test_json_serializer_invalid_json():
    """Test deserializing invalid JSON."""
    serializer = JSONSerializer()
    with pytest.raises(SerializationError, match="Failed to deserialize JSON"):
        serializer.deserialize(b"invalid json")

def test_json_serializer_invalid_utf8():
    """Test deserializing invalid UTF-8 bytes."""
    serializer = JSONSerializer()
    with pytest.raises(SerializationError, match="Failed to deserialize JSON"):
        serializer.deserialize(b'\xff\xff\xff\xff') 