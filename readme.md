<!-- @format -->

# Послідовність дій:

1. Запуск PostgreSQL через Docker:

docker run --name postgres_student -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres

Перевірити, що контейнер працює

- docker ps

- postgres_student — назва контейнера

- 1234 — пароль для користувача postgres

2. Підготовка Python середовища

- Встановити залежності

pip install -r requirements.txt

3. Створення бази даних і таблиць

## Варіант A: без Alembic

python seed.py

- seed.py створить таблиці через Base.metadata.create_all(engine)

- Заповнить базу випадковими даними (~30 студентів, 3 групи, 4 викладачі, 6 предметів, оцінки)

## Варіант B: з Alembic

Ініціалізація Alembic:

alembic init alembic

# Налаштувати alembic.ini (SQLAlchemy URL) та env.py (імпорт Base)

# Створити міграцію

alembic revision --autogenerate -m "Initial migration"

# Застосувати міграцію

alembic upgrade head

5️⃣ Тестування запитів

python test_selects.py

6️⃣ (Опціонально) CLI для CRUD

# Створити нового викладача

python main.py -a create -m Teacher -n "Boris Jonson"

# Показати всіх студентів

python main.py -a list -m Student

# Оновити дані групи

python main.py -a update -m Group --id 1 -n "AD-102"

# Видалити студента

python main.py -a remove -m Student --id 5

✅ Проект готовий до використання:

Docker PostgreSQL працює

Таблиці створені

Дані наповнені Faker

SQLAlchemy-запити можна тестувати

# Запустити контейнер PostgreSQL

docker run --name postgres_student -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres

# Ініциалізація Alembic:

py -m alembic init alembic

py -m alembic revision --autogenerate -m "Initial"

alembic upgrade head

для env.py:

## from models import Base

## target_metadata = Base.metadata

для alembic.ini:

## [alembic]

## script_location = alembic

## sqlalchemy.url = postgresql+psycopg2://postgres:1234@localhost:5432/postgres
