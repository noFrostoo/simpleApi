from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2



SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://wlnnklplkclits:42e68a26e2ab7b8991326275cd7a340fdada5976f2c78457dba0247fef5c4c9f@ec2-54-228-99-58.eu-west-1.compute.amazonaws.com:5432/d7gkavdfkrib31'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()