from functools import wraps


def logger_method(logger):
    def logger_method_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f'Метод {func.__name__} начал работу.')
            result = func(*args, **kwargs)
            logger.debug(f'Метод {func.__name__} завершил работу.')
            return result
        return wrapper
    return logger_method_func
