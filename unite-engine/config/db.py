from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mariadb+mariadbconnector://dev:password@localhost:3306/storedb")

meta = MetaData()

Base = declarative_base(metadata=meta)

Session = sessionmaker(bind=engine, autoflush=True)