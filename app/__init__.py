#!flask/bin/python
from flask import Flask
from app import models
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

Session = sessionmaker(bind=models.engine)
Session.configure(bind=models.engine) 
sql_session = Session()

from app import chatview

