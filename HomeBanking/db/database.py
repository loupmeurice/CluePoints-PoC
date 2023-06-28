from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from db.variables import *

try:
    MYSQL_HOST = os.environ["MYSQL_HOST"]
    MYSQL_PORT = os.environ["MYSQL_PORT"]
    MYSQL_USER = os.environ["MYSQL_USER"]
    MYSQL_PWD = os.environ["MYSQL_PWD"]
    MYSQL_DB = os.environ["MYSQL_DB"]

    SQLALCHEMY_DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )

except KeyError:
    SQLALCHEMY_DATABASE_URL = settings.db_url  # default database url


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    return SessionLocal()
