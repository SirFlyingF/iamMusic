from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Commons.BuildDB import builddb

engine = create_engine('mysql+pymysql://root:bunny1234@localhost/iammusic')

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


#init_db()
