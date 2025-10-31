import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from logging.config import fileConfig
from alembic import context


# Загружаемо змінні оточення
load_dotenv()

# Конфиг Alembic
config = context.config

# Настройка логирования Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/postgres"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
