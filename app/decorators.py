import sys
from pathlib import Path
import logging
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


def create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(Path(__file__).parent / 'logs/app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
