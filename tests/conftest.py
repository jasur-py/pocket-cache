import pytest
from pocket_cache import Cache
from pocket_cache.backends.memory import MemoryCache
from pocket_cache.serializers.json import JSONSerializer

@pytest.fixture
def cache():
    return Cache(
        backend=MemoryCache(),
        serializer=JSONSerializer(),
    ) 