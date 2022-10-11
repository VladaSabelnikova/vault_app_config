## Интерфейс для конфигурации проектов с помощью HashiCorp Vault

### Зачем вам Vault для конфигурирования проекта?
1. Безопасно хранит секреты (джун больше не выгрузит секреты в репозиторий)
2. Реализует паттерн Externalized configuration (никакого зоопарка из .env файлов)
3. Отныне и навсегда .env файл приложения состоит из 3-х строчек


### Интерфейс позволяет:
1. Хранить все константы, настройки и секреты в Vault
2. Создавать удобный для использования конфиг
3. Работать в dev mode (удобно для локальной разработки)


### Инструкция по развёртыванию:
1. Клонировать проект
2. Установить зависимости `poetry install`
3. В папке vault/ создать .env файл (образец в vault/.env_example)
4. Запустить Vault `docker-compose up -d`
5. В консоли Vault-а выполнить инструкции из vault/example_vault_init
6. В консоли Vault-а сохранить demo секреты по инструкции из src/vault_service/example_vault_keys
7. В папке src/use_case создать .env файл (образец в src/use_case/.env_example)


После этого можно запустить демонстрационный файл src/use_case/main.py

### Планы по доработке:

1. Вместо библиотеки hvac (громоздкой для данной ситуации) использовать прямое обращение к API Vault.
