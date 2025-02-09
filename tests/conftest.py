import pytest
from quickcache import Cache
from quickcache.backends.memory import MemoryCache
from quickcache.serializers.json import JSONSerializer

@pytest.fixture
def cache():
    return Cache(
        backend=MemoryCache(),
        serializer=JSONSerializer(),
    ) 