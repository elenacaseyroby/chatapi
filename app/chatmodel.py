#!/usr/bin/python
# -*- mode: python -*-

from app import models, sql_session
from sqlalchemy import text, update, func
from flask import session, request
import datetime

def getthreadsbyuser(user1, user2 = None, time_sent = None):
	messages = []
	# if user1 and user2 set, get threads between user1 and user2
	if user2:
		where = "WHERE (u.username = '"+user1+"' AND u2.username = '"+user2+"') OR (u.username = '"+user2+"' AND u2.username = '"+user1+"')"
	# if user1 set, get all threads involving user1
	else:
		where = "WHERE (u.username = '"+user1+"' OR u2.username = '"+user1+"') "

	now = datetime.datetime.now()
	today = now.strftime("%Y-%m-%d %H:%M:%S") 
	if time_sent == 'today':
		where = where + " AND messages.time_sent >= '"+today+"' "
	elif time_sent == 'week':
		oneweekago = datetime.date.today() - datetime.timedelta(days=7)
		oneweekago = oneweekago.strftime("%Y-%m-%d %H:%M:%S")
		where = where + " AND messages.time_sent >= '"+oneweekago+"' "
	elif time_sent == 'month':
		onemonthago = datetime.date.today() - datetime.timedelta(month=1)
		onemonthago = onemonthago.strftime("%Y-%m-%d %H:%M:%S")
		where = where + " AND messages.time_sent >= '"+onemonthago+"' "

	sql = text("""SELECT messages.*
		, u.username as `from`
		, u2.username as `to`
		, CASE WHEN messages.from_user > messages.to_user THEN CONCAT(u2.username," - ",u.username)
			ELSE CONCAT(u.username," - ",u2.username) 
			END AS `thread`
		FROM messages
		JOIN users u ON messages.from_user = u.id
		JOIN users u2 ON messages.to_user = u2.id
		"""+where+""" 
		ORDER BY thread, messages.time_sent;""")
	results = models.engine.execute(sql)
	print(sql)
	return results

def getthreadlistbyuser(user):
	sql = text("""SELECT CASE WHEN messages.from_user > messages.to_user THEN CONCAT(u2.username," - ",u.username)
			ELSE CONCAT(u.username," - ",u2.username) 
			END AS `thread`
		FROM messages
		JOIN users u ON messages.from_user = u.id
		JOIN users u2 ON messages.to_user = u2.id
		WHERE u.username = '"""+user+"' OR u2.username = '"+user+"""'  
UNION
SELECT CASE WHEN messages.from_user > messages.to_user THEN CONCAT(u2.username," - ",u.username)
			ELSE CONCAT(u.username," - ",u2.username) 
			END AS `thread`
		FROM messages
		JOIN users u ON messages.from_user = u.id
		JOIN users u2 ON messages.to_user = u2.id
		WHERE u.username = '"""+user+"' OR u2.username = '"+user+"""';""")
	results = models.engine.execute(sql)
	return results

def getallusers(user = None):
	where = ""
	if user:
		where = "WHERE username != '"+user+"'"
	sql = text("""SELECT *
		FROM users
		"""+where+"""
		ORDER BY username;""")
	results = models.engine.execute(sql)
	return results

def postmessage(from_user, to_user, body):
	#check for users
	from_user_in_db = sql_session.query(models.User).filter_by(username = from_user).first()
	if from_user_in_db:
		from_user_id = from_user_in_db.id
	to_user_in_db = sql_session.query(models.User).filter_by(username = to_user).first()
	if to_user_in_db:
		to_user_id = to_user_in_db.id
	if from_user_in_db and to_user_in_db:
			new_message = models.Message(from_user = int(from_user_id), to_user = int(to_user_id), body = str(body))
			sql_session.add(new_message)
			sql_session.commit()
			return "success"
	else:
		return "failure"

def addnewuser(username, email, password):
	username_in_db = sql_session.query(models.User).filter_by(username = username).first()
	if username_in_db:
		return "failure"
	else:
		new_user = models.User(username = username, email = email, password = password)
		sql_session.add(new_user)
		sql_session.commit()
		return "success"





