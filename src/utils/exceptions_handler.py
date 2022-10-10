"""Модуль содержит избирательную функцию backoff для определённых ошибок."""
from functools import wraps
from logging import getLogger
from time import sleep
from typing import Callable, Any, Union

from requests.exceptions import ConnectionError


def exceptions_handler(
    max_timeout: Union[int, float],
    logger_name: str,
    start_sleep_time: Union[int, float] = 0.1,
    factor: Union[int, float] = 2,
) -> Callable:
    """
    Параметрический декоратор — backoff, срабатывающая ТОЛЬКО на ошибки сети.

    Если ошибка связана с подключением к серверу — пробует повторно обратиться через некоторое время.
    Иначе прекращает работу программы.
    Прекращает работу программы при достижении лимита таймаута.

    Args:
        max_timeout: предел ожидания ответа, после которого вызывается исключение
        logger_name: имя логгера
        start_sleep_time: начальное время задержки перед повтором
        factor: во сколько раз нужно увеличить время ожидания при следующем повторе

    Returns:
        Вернёт декоратор.
    """
    logger = getLogger(logger_name)

    def func_wrapper(func: Callable) -> Callable:
        """
        Декоратор функций.

        Args:
            func: функция, которая подключается к сервису

        Returns:
            Пробует выполнить функцию func и, если что-то пошло не так, «засыпает» на какое-то время.
        """
        @wraps(func)
        def inner(*args: tuple, **kwargs: dict) -> Any:
            """
            Возвращаемая декоратором функция.
            При неудачном подключении к сервису повторяет попытку через start_sleep_time.

            Args:
                args: все позиционные аргументы, нужные func
                kwargs: все непозиционные аргументы, нужные для func

            Returns:
                Результат выполнения func

            Raises:
                SystemExit:
                    для завершения работы программы, поскольку её продолжение невозможно.
            """
            nonlocal start_sleep_time  # Переменная точно не глобальная, но и не локальная вроде :)
            execution_time: float = 0

            while True:
                try:
                    return func(*args, **kwargs)

                except ConnectionError as error:
                    # Проблема связана с соединением, значит еще не всё потеряно.
                    if execution_time < max_timeout:
                        logger.warning(f'waiting for {start_sleep_time} sec | {error}')
                        sleep(start_sleep_time)
                        execution_time += start_sleep_time
                        start_sleep_time = min(start_sleep_time * factor, max_timeout - execution_time)

                    else:
                        raise SystemExit('Connection timeout')

                except Exception as error:
                    # Любые другие ошибки означают, что сразу прекращаем работу программы.
                    logger.error('FAILED RUN %s.%s | ERROR %s', func.__module__, func.__name__, error)
                    raise SystemExit('Program stopped')

        return inner

    return func_wrapper
