"""
JSON serializer implementation.
"""
import json
from typing import Any
from .base import BaseSerializer

class JSONSerializer(BaseSerializer):
    """
    JSON serializer implementation.
    
    Note: Only supports JSON-serializable objects.
    """
    
    def serialize(self, value: Any) -> bytes:
        """
        Serialize a Python object to JSON bytes.
        
        Args:
            value: Python object to serialize
            
        Returns:
            JSON-encoded bytes
            
        Raises:
            SerializationError: If value is not JSON-serializable
        """
        try:
            return json.dumps(value).encode('utf-8')
        except (TypeError, ValueError) as e:
            raise SerializationError(f"Failed to serialize value to JSON: {e}")
    
    def deserialize(self, value: bytes) -> Any:
        """
        Deserialize JSON bytes to a Python object.
        
        Args:
            value: JSON bytes to deserialize
            
        Returns:
            Deserialized Python object
            
        Raises:
            SerializationError: If value is not valid JSON
        """
        try:
            return json.loads(value.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise SerializationError(f"Failed to deserialize JSON: {e}")

class SerializationError(Exception):
    """Raised when serialization or deserialization fails."""
    pass 