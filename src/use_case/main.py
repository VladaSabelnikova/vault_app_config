"""
Модуль содержит demo код.

Получение переменных (хоста и порта) из Vault.
Обратите внимание, хост может иметь разные значения,
в зависимости от DEV_MODE=True/False константы src/config/settings.py.
"""
from src.config.settings import config

host = config.app_host
port = config.app_port

print(host, port)  # noqa: WPS421
