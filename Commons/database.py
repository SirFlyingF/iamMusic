from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

# mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
DB_STR = getenv('DB_STR')
engine = create_engine(f'mysql+pymysql://{DB_STR}')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()

# Use database.sql file to create tables instead of create_all()

