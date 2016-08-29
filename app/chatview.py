from flask import render_template, redirect, request, Flask, jsonify
from app import app, chatmodel, models
from sqlalchemy import text, update, func
from json import loads

@app.route('/')
@app.route('/api')
@app.route('/api/reference')
def renderreferencepage():
	return render_template('reference.html', url = 'http://localhost:5000')

@app.route('/api/MessageThread', methods = ['GET']) 
def getmessagethread():
	messages = []
	
	if request.args.get('user1'):
		user1 = request.args.get('user1')
		if request.args.get('user2'):
			user2 = request.args.get('user2')
			results = chatmodel.getmessagesbyuser(user1, user2)
		else:
			results = chatmodel.getmessagesbyuser(user1)
		for result in results:
			message = { 'thread': result[7]
				, 'message_id': result[0]
				, 'time': result[4]
				, 'from': result[5]
				, 'to': result[6]
				, 'body': result[3]
				}
			messages.append(message)

	return jsonify(messages)
#curl -i "http://localhost:5000/api/MessageThread?user1=[username1]"
#curl -i "http://localhost:5000/api/MessageThread?user1=[username1]&user2=[username2]"

@app.route('/api/MessageThread', methods = ['POST'])
def postmessagethread():
	messages = []
	if request.json['from'] and request.json['to'] and request.json['body']:
		from_user = request.json['from']
		to_user = request.json['to']
		body = request.json['body']
		post = chatmodel.postmessage(from_user = from_user, to_user = to_user, body = body)
		results = chatmodel.getmessagesbyuser(from_user, to_user)
		for result in results:
			message = { 'message_id': result[0]
				, 'time': result[4]
				, 'from': result[5]
				, 'to': result[6]
				, 'body': result[3]
				}
			messages.append(message)

		if post == "success":
			return jsonify(messages)
		else:
			return "Check that you are using valid usernames."
	else:
		return "Check parameters."
#curl -i -H "Content-Type: application/json" -X POST -d '{"from":"[username]", "to": "[username]", "body": "[body text]"}' http://localhost:5000/api/MessageThread

@app.route('/api/User', methods = ['POST'])
def adduser():
	return_message = { 'error': 'Check params'}
	if request.args.get('username') and request.args.get('email') and request.args.get('password'):
		if '@' not in request.args.get('email'):
			return_message = { 'error': 'Check that email is valid'}
		elif ' ' in request.args.get('username'):
			return_message = { 'error': 'Make sure there are no spaces in your username'}
		elif ' ' in request.args.get('password'):
			return_message = { 'error': 'Make sure there are no spaces in your password'}
		else:
			username = request.args.get('username')
			email = request.args.get('email')
			password = request.args.get('password')
			post = chatmodel.addnewuser(username = username, email = email, password = password)
			if post == "success":
				return_message = {'success': 'user successfully created'}

	return return_message
#curl -X POST "http://localhost:5000/api/User?username=[username]&email=[email]&password=[password]






