#!/usr/bin/python
# -*- mode: python -*-

from app import models, sql_session
from app.views import viewsClasses
from sqlalchemy import text, update, func
from flask import session, request

"""
def getartists(artist_id=None):
  where = ""
  if artist_id:
    where = "WHERE artist_id = "+artist_id
  sql= text(""""""SELECT *
    FROM artists
   """ """+where+";")
  result = models.engine.execute(sql)
  return result
 """