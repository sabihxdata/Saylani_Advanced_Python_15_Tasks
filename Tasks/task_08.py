
import time
from functools import wraps


def ttl_cache(seconds):
    if seconds < 0:
        raise ValueError("Cache duration cannot be negative")

    def decorator(function):
        cache = {}
        hits = 0
        misses = 0

        @wraps(function)
        def wrapper(*args, **kwargs):
            nonlocal hits, misses

            
            try:
                key = (args, tuple(sorted(kwargs.items())))
                hash(key)
            except TypeError:
                
                misses += 1
                return function(*args, **kwargs)

            current_time = time.monotonic()

            
            if key in cache:
                result, expiry_time = cache[key]

                if current_time < expiry_time:
                    hits += 1
                    return result

                
                del cache[key]

            
            misses += 1
            result = function(*args, **kwargs)
            cache[key] = (result, time.monotonic() + seconds)

            return result

        @wraps(function)
        def cache_info():
            return {
                "hits": hits,
                "misses": misses,
                "size": len(cache)
            }

        def cache_clear():
            nonlocal hits, misses
            cache.clear()
            hits = 0
            misses = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear

        return wrapper

    return decorator




@ttl_cache(seconds=5)
def add(x, y):
    print("Calculating result...")
    return x + y


print("TEST 1: CACHE")
print("First call:", add(x=2, y=3))
print("Second call:", add(y=3, x=2))
print("Cache information:", add.cache_info())




print("\nTEST 2: DIFFERENT ARGUMENTS")
print("Result:", add(10, 20))
print("Cache information:", add.cache_info())




@ttl_cache(seconds=5)
def calculate_total(numbers):
    print("Calculating total...")
    return sum(numbers)


print("\nTEST 3: UNHASHABLE INPUT")
print("Result:", calculate_total([1, 2, 3]))
print("Result:", calculate_total([1, 2, 3]))
print("Cache information:", calculate_total.cache_info())




@ttl_cache(seconds=0)
def multiply(x, y):
    print("Calculating multiplication...")
    return x * y


print("\nTEST 4: EXPIRATION")
print("First call:", multiply(4, 5))
print("Second call:", multiply(4, 5))
print("Cache information:", multiply.cache_info())




print("\nTEST 5: FUNCTION METADATA")
print("Function name:", add.__name__)




print("\nTEST 6: CLEAR CACHE")
add.cache_clear()
print("Cache information after clearing:", add.cache_info())
