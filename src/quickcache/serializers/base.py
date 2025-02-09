"""
Abstract base class for cache serializers.
"""
from abc import ABC, abstractmethod
from typing import Any

class BaseSerializer(ABC):
    """
    Abstract base class for serializers.
    """
    
    @abstractmethod
    def serialize(self, value: Any) -> bytes:
        """
        Serialize a value to bytes.
        
        Args:
            value: Python object to serialize
            
        Returns:
            Serialized value as bytes
            
        Raises:
            SerializationError: If serialization fails
        """
        pass
    
    @abstractmethod
    def deserialize(self, value: bytes) -> Any:
        """
        Deserialize bytes to a value.
        
        Args:
            value: Bytes to deserialize
            
        Returns:
            Deserialized Python object
            
        Raises:
            SerializationError: If deserialization fails
        """
        pass 