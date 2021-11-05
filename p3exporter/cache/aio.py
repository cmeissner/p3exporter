"""Module that defines async command execution combined with caching"""
from datetime import datetime, timedelta
from functools import lru_cache, wraps

async def async_command_with_cache(lifetime: int = 3600, maxsize: int = 128):

    async def wrapper_async(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=lifetime)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        async def wrapped_func(*args, **kwargs):

            return func(*args, **kwargs)

        return await wrapped_func()

    return wrapper_async
