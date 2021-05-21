from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Path('testdata').mkdir(exist_ok=True)

TEST_SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdata/db.sqlite'

testengine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=testengine)