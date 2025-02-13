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

def test_json_serializer_complex_types():
    """Test serializing complex nested types."""
    serializer = JSONSerializer()
    value = {
        "null": None,
        "bool": True,
        "int": 42,
        "float": 3.14,
        "list": [1, 2, 3],
        "dict": {"nested": {"deep": True}},
        "mixed": [{"a": 1}, None, True, 2.5]
    }
    serialized = serializer.serialize(value)
    deserialized = serializer.deserialize(serialized)
    assert deserialized == value

def test_json_serializer_empty_values():
    """Test serializing empty values."""
    serializer = JSONSerializer()
    # Test empty string
    assert serializer.deserialize(serializer.serialize("")) == ""
    # Test empty list
    assert serializer.deserialize(serializer.serialize([])) == []
    # Test empty dict
    assert serializer.deserialize(serializer.serialize({})) == {}
    # Test empty bytes
    with pytest.raises(SerializationError, match="Failed to deserialize JSON"):
        serializer.deserialize(b"")

def test_json_serializer_unicode():
    """Test serializing Unicode strings."""
    serializer = JSONSerializer()
    value = "Hello, 世界! 🌍"
    serialized = serializer.serialize(value)
    deserialized = serializer.deserialize(serialized)
    assert deserialized == value

def test_json_serializer_type_error():
    """Test serializing objects that raise TypeError."""
    class Unserializable:
        pass
    
    serializer = JSONSerializer()
    with pytest.raises(SerializationError, match="Failed to serialize value to JSON"):
        serializer.serialize(Unserializable())

def test_json_serializer_value_error():
    """Test serializing objects that raise ValueError."""
    serializer = JSONSerializer()
    # Create a circular reference that will cause ValueError
    circular = []
    circular.append(circular)
    with pytest.raises(SerializationError, match="Failed to serialize value to JSON"):
        serializer.serialize(circular) 