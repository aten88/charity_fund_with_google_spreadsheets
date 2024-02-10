# Кошачий благотворительный фонд QRKot

## Возможности проекта

- Создание администратором благотворительных проектов для поддержания кошачьей популяции
- Внесение пожертвований зарегистрированными пользователями
- Автоматическое инвестирование поступающих средств в открытые проекты
- Регистрация пользователей реализовано при помощи FastAPI Users
- Возможность получить отчет о проектах в Google Sheets

## Технологии

- Python 3.9
- FastAPI 0.78.0
- SQLAlchemy 1.4.36
- pydantic 1.9.1
- Alembic 1.7.7
- Google API

## Установка и запуск проекта
- Скачать репозиторий
git clone git@github.com:aten88/cat_charity_fund.git
- В корневом каталоге создайте файл *.env* и добавьте в него данные (при необходимости):

```
APP_TITLE=Some Fund Name                            # Название фонда
APP_DESCRIPTION=Some description                    # Описание фонда
DATABASE_URL=type_db+somemodule_db:///./somename.db # Путь подключения к БД
SECRET=SOMESECRETKEY                                # Ключ для генерации хэша
FIRST_SUPERUSER_EMAIL=some_superuser@mail.ru        # Почта для суперюзера по умолчанию(при желании)
FIRST_SUPERUSER_PASSWORD=SomeXXXSECRETPass##**      # Пароль для суперюзера по умолчанию(при желании)
```
- Установите и активируйте виртуальное окружение:

  ```
  py3.9 -m venv venv

  Windows:
    source/venv/scripts/activate
  Linux/Mac OS:
    source/venv/bin/activate
  ```

- Установите зависимости:

  ```
  pip install -r requirements.txt
  ```

- Создайте миграции:

```
alembic revision --autogenerate -m "First migration" 
```

- Примените миграции:

```shell
alembic upgrade head
```

- Запустите проект:

```shell
uvicorn app.main:app  --reload
```

## Документации проекта QRKot

При запущенном проекте откройте одну из ссылкок в браузере:

Swagger:

```shell
http://127.0.0.1:8000/docs
```
Redoc:

```shell
http://127.0.0.1:8000/redoc
```
## Автор
Алексей Тен.
