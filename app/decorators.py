import time
from functools import wraps


def logger_method(logger):
    def logger_method_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f'Метод {func.__name__} начал работу.')
            start_method = time.time()
            result = func(*args, **kwargs)
            end_method = time.time()
            logger.debug(f'Метод {func.__name__} завершил работу за {round(end_method - start_method, 2)} c.')
            return result
        return wrapper
    return logger_method_func
