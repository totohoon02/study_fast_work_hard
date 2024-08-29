from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# DB CONF
drivername = "mysql"
username = "root"
password = "admin"
host = "127.0.0.1"
database = "mydb"

DATABASE_URL = f"{drivername}://{username}:{password}@{host}/{database}?charset=utf8"
engine = create_engine(DATABASE_URL, echo=True)

session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))


Base = declarative_base()


def init_db():
    Base.metadata.create_all(engine)
