from flask import render_template, redirect, request, Flask, jsonify
from app import app, models
from sqlalchemy import text, update, func
from json import loads

@app.route('/api/messages', methods = ['GET'])
def getmessages():
	messages = []
	if request.args.get('user1'):
		user1 = request.args.get('user1')
		#if 2 users specified, then get specific convo
		if request.args.get('user2'):
			user2 = request.args.get('user2')
			where = "WHERE (messages.from_user = "+user1+" AND messages.to_user = "+user2+") OR (messages.from_user = "+user2+" AND messages.to_user = "+user1+")"
		#else get all convos for one user
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

	return jsonify(messages)

@app.route('/api/messages', methods = ['POST'])
def postmessages():
    return "success"

@app.route('/api/messages', methods = ['PUT'])
def updatemessages():

    return "success"

@app.route('/api/messages', methods = ['DELETE'])
def deletemessages():

    return "success"

@app.route('/api/user', methods = ['POST'])
def adduser():

    return "success"


