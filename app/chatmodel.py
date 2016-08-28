#!/usr/bin/python
# -*- mode: python -*-

from app import models, sql_session
from sqlalchemy import text, update, func
from flask import session, request

def getmessagesbyuser(user1, user2 = None):
	messages = []
	# if user1 and user2 set, get convos between user1 and user2
	if user2:
		where = "WHERE (messages.from_user = "+user1+" AND messages.to_user = "+user2+") OR (messages.from_user = "+user2+" AND messages.to_user = "+user1+")"
	# if user1 set, get all convos involving user1
	else:
		where = "WHERE messages.from_user = "+user1+" OR messages.to_user = "+user1

	sql = text("""SELECT messages.time_sent
		, messages.body
		, u.username as `from`
		, u2.username as `to`
		FROM messages
		JOIN users u ON messages.from_user = u.id
		JOIN users u2 ON messages.to_user = u2.id
		"""+where+"""
		ORDER BY messages.time_sent;""")
	results = models.engine.execute(sql)
	for result in results:
		message = { 'time': result[0]
			, 'from': result[2]
			, 'to': result[3]
			, 'body': result[1]
			}
		messages.append(message)

	return messages
def postmessage(from_user, to_user, body):
	#check for users
	from_user_in_db = sql_session.query(models.User).filter_by(username = from_user).first()
	if from_user_in_db:
		from_user_id = from_user_in_db.id
		to_user_in_db = sql_session.query(models.User).filter_by(username = to_user).first()
		if to_user_in_db:
			to_user_id = to_user_in_db.id
	if from_user_id and to_user_id:
			new_message = models.Message(from_user = int(from_user_id), to_user = int(to_user_id), body = str(body))
			sql_session.add(new_message)
			sql_session.commit()
			return "success"
	else:
		return "failure"

def addnewuser(username, email, password):
	username_in_db = sql_session.query(models.User).filter_by(username = from_user).first()
	if username_in_db:
		return "failure"
	else:
		new_user = models.User(username = username, email = email, password = password)
		sql_session.add(new_user)
		sql_session.commit()
		return "success"





