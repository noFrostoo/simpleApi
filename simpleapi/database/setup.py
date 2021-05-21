from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import os


url = os.getenv("DATABASE_URL")

urls = url.split("://")
urls[0] = "postgresql+psycopg2://"

SQLALCHEMY_DATABASE_URL = urls[0] + urls[1]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()