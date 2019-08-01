import logging
from functools import wraps


logger = logging.getLogger('decorators')

def debug_log(func):
    # @wraps
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{func.__name__}({request})')
        return func(request, *args, **kwargs)
    return wrapper

def trace_log(func):
    # @wraps
    def wrapper(*args, **kwargs):
        logger.debug(f'{func.__name__} called')
        return func(*args, **kwargs)
    return wrapper
