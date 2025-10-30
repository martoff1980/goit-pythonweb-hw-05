<!-- @format -->

# Послідовність дій:

## 1. Запуск PostgreSQL через Docker:

docker run --name postgres_student -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres

- postgres_student — назва контейнера

- 1234 — пароль для користувача postgres

Перевірити, що контейнер працює

docker ps

## 2. Підготовка Python середовища

Встановити залежності:

pip install -r requirements.txt

## 3. Створення бази даних і таблиць

## Варіант без Alembic:

python seed.py

- seed.py створить таблиці через Base.metadata.create_all(engine)

- заповнить базу випадковими даними (~30 студентів, 3 групи, 4 викладачі, 6 предметів, оцінки)

## Варіант з Alembic:

Ініціалізація Alembic:

alembic init alembic

Створити міграцію:

alembic revision --autogenerate -m "Initial migration"

Застосувати міграцію:

alembic upgrade head

- для файлу env.py:

from models import Base

target_metadata = Base.metadata

- для файлу alembic.ini:

[alembic]

script_location = alembic

sqlalchemy.url = postgresql+psycopg2://postgres:1234@localhost:5432/postgres

## 4. Тестування запитів

python test_selects.py

## 5. (Опціонально) CLI для CRUD

- Створити нового викладача

python main.py -a create -m Teacher -n "Boris Jonson"

- Показати всіх студентів

python main.py -a list -m Student

- Оновити дані групи

python main.py -a update -m Group --id 1 -n "AD-102"

- Видалити студента

python main.py -a remove -m Student --id 5

# Проект готовий до використання:

- Docker PostgreSQL працює

- Таблиці створені

- Дані наповнені Faker

- Тестувати SQLAlchemy-запити
