"""
Basic usage examples for PocketCache.
"""
from pocket_cache import Cache
from pocket_cache.backends import MemoryBackend, RedisBackend
from pocket_cache.serializers import JSONSerializer

def basic_cache_operations():
    # Create a cache with default memory backend
    cache = Cache()
    
    # Set a value
    cache.set("greeting", "Hello, World!")
    
    # Get the value
    value = cache.get("greeting")
    print(f"Retrieved value: {value}")  # Output: Retrieved value: Hello, World!
    
    # Delete the value
    cache.delete("greeting")
    
    # Get a non-existent value
    value = cache.get("greeting")
    print(f"After deletion: {value}")  # Output: After deletion: None

def cache_decorator_example():
    cache = Cache(default_ttl=60)  # 1 minute TTL
    
    @cache.cached(ttl=300)  # 5 minutes TTL
    def fibonacci(n: int) -> int:
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    # First call will compute
    result1 = fibonacci(10)
    print(f"First call result: {result1}")
    
    # Second call will use cached value
    result2 = fibonacci(10)
    print(f"Second call result (from cache): {result2}")

def redis_backend_example():
    # Create a cache with Redis backend
    redis_backend = RedisBackend(host="localhost", port=6379)
    cache = Cache(backend=redis_backend)
    
    # Use the cache with Redis
    cache.set("user:1", {"name": "John", "age": 30})
    user = cache.get("user:1")
    print(f"User from Redis: {user}")

if __name__ == "__main__":
    print("Basic cache operations example:")
    basic_cache_operations()
    print("\nCache decorator example:")
    cache_decorator_example()
    print("\nRedis backend example:")
    try:
        redis_backend_example()
    except Exception as e:
        print(f"Redis example failed (Redis server not running?): {e}") 