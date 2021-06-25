"""Module that defines async command execution combined with caching"""
from datetime import datetime, timedelta
from functools import lru_cache, wraps

def async_command_with_cache(lifetime: int = 3600, maxsize: int = 128):

    def wrapper_async(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=lifetime)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):

            return func(*args, **kwargs)

        return wrapped_func()

    return wrapper_async
