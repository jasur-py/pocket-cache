# QuickCache

A fast and flexible API response caching library for Python.

## Features

- Multiple backend support (Memory, Redis, File System)
- Flexible serialization (JSON, Pickle)
- Decorator-based caching
- TTL (Time-To-Live) support
- Async support
- Type hints
- Extensive test coverage
- Comprehensive documentation

## Installation

```bash
pip install quickcache
```

## Quick Start

```python
from quickcache import Cache
from quickcache.utils.decorators import cached

# Create a cache instance
cache = Cache()

# Basic usage
cache.set("my_key", "my_value", ttl=300)  # Cache for 5 minutes
value = cache.get("my_key")

# Decorator usage
@cached(ttl=300)
def expensive_operation(x):
    # This result will be cached for 5 minutes
    return x * 2

# Using with Redis backend
from quickcache.backends.redis import RedisCache
from redis import Redis

redis_client = Redis(host='localhost', port=6379)
cache = Cache(backend=RedisCache(redis_client))
```

## Configuration

QuickCache can be configured with different backends and serializers:

```python
from quickcache import Cache
from quickcache.backends.redis import RedisCache
from quickcache.serializers.pickle import PickleSerializer
from datetime import timedelta

cache = Cache(
    backend=RedisCache(redis_client),
    serializer=PickleSerializer(),
    default_ttl=timedelta(minutes=5)
)
```

## Advanced Usage

### Custom Backend

```python
from quickcache.backends.base import BaseCacheBackend
from datetime import timedelta

class MyCustomBackend(BaseCacheBackend):
    def get(self, key: str) -> Optional[bytes]:
        # Implementation
        pass

    def set(self, key: str, value: bytes, ttl: timedelta) -> None:
        # Implementation
        pass

    def delete(self, key: str) -> None:
        # Implementation
        pass

    def clear(self) -> None:
        # Implementation
        pass
```

### Custom Serializer

```python
from quickcache.serializers.base import BaseSerializer
import msgpack

class MsgPackSerializer(BaseSerializer):
    def serialize(self, value: Any) -> bytes:
        return msgpack.packb(value)

    def deserialize(self, value: bytes) -> Any:
        return msgpack.unpackb(value)
```

## Development

### Setting up the development environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quickcache.git
cd quickcache
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev,test,docs]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=quickcache

# Run specific test file
pytest tests/test_cache.py
```

### Code Quality

The project uses several tools to maintain code quality:

- `black` for code formatting
- `isort` for import sorting
- `flake8` for style guide enforcement
- `mypy` for static type checking

Run them using:
```bash
# Format code
black src tests examples
isort src tests examples

# Check types
mypy src tests examples

# Check style
flake8 src tests examples
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run the tests (`pytest`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Documentation

Full documentation is available at [https://quickcache.readthedocs.io/](https://quickcache.readthedocs.io/) 