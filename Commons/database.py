from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

from Commons.BuildDB import builddb

db_host = os.environ['db_host']
db_user = os.environ['db_user']
db_port = os.environ['db_port']
db_name = os.environ['db_name']

# mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
engine = create_engine(f'mysql+pymysql://{db_user}:1Madar2chod#@{db_host}:{db_port}/{db_name}')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()

from .models import * #models
Base.metadata.create_all(bind=engine)

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise
    # you will have to import them first before calling init_db()
    from . import models
    Base.metadata.create_all(bind=engine)
    builddb() #Use this method to insert Foundation data like Super User


init_db()

