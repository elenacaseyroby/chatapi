#!/usr/bin/python
# -*- mode: python -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref 
import os

print("~~~~~~~~~~~~~~~~~~~~~~~")
print(os.environ)
print("~~~~~~~~~~~~~~~~~~~~~~~")


if 'CLEARDB_DATABASE_URL' in os.environ and os.environ['CLEARDB_DATABASE_URL']:
    db_url = os.environ['CLEARDB_DATABASE_URL']
    db_url = db_url.replace("?reconnect=true", "")
else:
	db_url = 'mysql+pymysql://root:@127.0.0.1:3306/chatdb'

engine = create_engine(db_url+'?charset=utf8', convert_unicode=True, echo=False)

Base = declarative_base()
Base.metadata.reflect(engine)

class Message(Base):
	__table__ = Base.metadata.tables['messages']

class User(Base):
	__table__ = Base.metadata.tables['users']