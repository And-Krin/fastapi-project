# FastApi project
### Основные разделы:
* **Структура проекта**
* **Запуск проекта**
  * Подготовка environment
  * Создание контейнеров базы данных и проекта
  * Создание таблиц базы данных
  * Создание superuser
* **Тестирование**
  * Создание тестовой базы данных
  * Запуск тестов
## Структура проекта
___
```
code
├── migrations/
├── requirements
│   └── dev.txt
├── src
│   ├── auth
│   │   ├── base_config.py
│   │   └── manager.py
│   ├── commands
│   │   ├── check.py
│   │   └── crud.py
│   ├── items
│   │   ├── router.py
│   │   └── schemas.py
│   ├── tests
│   │   ├── conftest.py
│   │   └── test_auth.py
│   ├── users
│   │   ├── responses.py
│   │   ├── router.py
│   │   └── schemas.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── manage.py 
│   ├── models.py 
│   ├── role.py
│   └── settings.py
├── .dockerignore
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```
## Запуск проекта
___
* Подготовка environment
* Создание контейнеров базы данных и проекта
* Создание таблиц базы данных
* Создание superuser
### Подготовка environment
При необходимости подставьте свои значения в файле .env:
```
DB_USER=postgres
DB_PASS=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=db_dev

DB_USER_TEST=postgres
DB_PASS_TEST=postgres
DB_HOST_TEST=db
DB_PORT_TEST=5432
DB_NAME_TEST=db_test

SECRET=SECRET
```
#### Внимание!
*Важно понимать, что в этом проекте тестовая база данных находится в том же
контейнере, что и база данных разработки. Поэтому все поля кроме имён 
(DB_NAME и DB_NAME_TEST) должны совпадать.*
### Создание контейнеров базы данных и проекта 
Для инициализации контейнеров воспользуйтесь следующей командой:
```
docker-compose up
```
### Создание таблиц базы данных
После создания контейнеров следует перейти в консоль контейнера app:
```
docker exec -it app bash
```
Внутри него обратившись к alembic делаем ревизию:
```
alembic revision --autogenerate -m "Create tables"
```
И применяем изменения:
```
alembic upgrade head
```
### Создание superuser
Для создание superuser необходимо в консоли контейнера app
прописать следующую команду:
```
python manage.py create superuser
```
Или:
```
typer manage.py run create superuser
```
*Для выхода из консоли контейнера воспользуйтесь командой* exit
## Тестирование
___
* Создание тестовой базы данных
* Запуск тестов
### Создание тестовой базы данных
Переходим в консоль контейнера db:
```
docker exec -it db bash
```
Проходим аутентификацию пользователя postgres с паролем postgres:
```
psql -U postgres -W
```
И создаем новую базу данных с именем db_test:
```
create database db_test;
```
*Для выхода из консоли Postgresql воспользуйтесь командой* \q
### Запуск тестов
Запускаем тестирование (из консоли контейнера app):
```
pytest -v
```