"""Модуль с абстрактными классами для работы с хранилищем секретов."""
from abc import ABC, abstractmethod
from typing import Optional


class AbstractAppConfig(ABC):

    """Класс для конфигурирования приложения из хранилища секретов."""

    @abstractmethod
    def get_setting(self, key: str, dev_mode_value: Optional[str] = None) -> str:  # noqa:WPS463
        """
        Метод достаёт значение ключа из хранилища.

        Args:
            key: ключ
            dev_mode_value: значение ключа для dev mode

        Returns:
            Возвращает значение в виде строки
        """
        pass
