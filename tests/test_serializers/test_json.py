"""Tests for JSON serializer."""
import pytest
from pocket_cache.serializers.json import JSONSerializer, SerializationError

def test_json_serializer_string():
    serializer = JSONSerializer()
    value = "test_string"
    serialized = serializer.serialize(value)
    deserialized = serializer.deserialize(serialized)
    assert deserialized == value

def test_json_serializer_dict():
    serializer = JSONSerializer()
    value = {"key": "value", "number": 42}
    serialized = serializer.serialize(value)
    deserialized = serializer.deserialize(serialized)
    assert deserialized == value

def test_json_serializer_list():
    serializer = JSONSerializer()
    value = [1, "two", {"three": 3}]
    serialized = serializer.serialize(value)
    deserialized = serializer.deserialize(serialized)
    assert deserialized == value 