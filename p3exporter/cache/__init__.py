"""Module that defines all needed classes and functions for caching facility."""
import asyncio

from functools import lru_cache, wraps
from datetime import datetime, timedelta


# found on https://bit.ly/39vlEXs
# thanks https://realpython.com/team/svaldarrama/ for your awsome article about caching in python
# has been adapted by us to meet our requirements
def timed_lru_cache(lifetime: int = 3600, maxsize: int = 128):
    """Provide cache with a given lifetime.

    This function has to be used as decorator.

    Each time the the cache will be accessed the decorator checks current date is past experation date.
    If so, the cache will cleared and the new expiration data will be recomputed. If not the cache entry
    will be delivered.

    :param lifetime: The lifetime of cache in seconds, defaults to 3600
    :type lifetime: int, optional
    :param maxsize: The maximum number of cache items, defaults to 128
    :type maxsize: int, optional
    """
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=lifetime)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


# Define a method to use as a decorator for the Cache class
def async_cache(key: str = None, lifetime: int = 3600, maxsize: int = 128):
    """Provide async cache for a given cache key.

    This methode provide an async cache.
    It needs a cache key where to store and resolve the value.
    """

    def decorator(func):
        cache = lru_cache(maxsize=maxsize)(func)
        cache.lifetime = timedelta(seconds=lifetime)
        cache.expiration = datetime.utcnow() + func.lifetime

        async def wrapper(cache):
            # Check if the metric value is already in the cache
            value = cache.get(key)
            # Start a new background task to collect the new cache value
            asyncio.create_task(func())

            # Return default value
            return value
        return wrapper
    return decorator
