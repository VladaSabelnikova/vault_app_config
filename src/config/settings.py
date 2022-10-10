"""Модуль содержит настройки приложения."""

from pydantic import BaseSettings

from src.vault_service.env_config import env
from src.vault_service.vault_app_config import VaultAppConfig
from src.vault_service.vault_client import client

# Режим разработки для запуска приложения с локальными настройками dev_mode_value вместо значений из vault
# Удобно использовать для быстрого переключения настроек между compose и локальной машиной,
# меняя хосты контейнеров
DEV_MODE = False

vault = VaultAppConfig(vault_client=client, app_name=env.vault_app_name, dev_mode=DEV_MODE)


class Config(BaseSettings):

    """Класс с конфигурацией проекта."""

    app_host: str = vault.get_setting(key='app_host', dev_mode_value='localhost')
    app_port: int = vault.get_setting(key='app_port')


config = Config()
