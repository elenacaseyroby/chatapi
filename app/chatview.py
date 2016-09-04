from flask import render_template, redirect, request, Flask, jsonify, abort, make_response
from app import app, chatmodel, models
from sqlalchemy import text, update, func
from json import loads

@app.teardown_request
def session_clear(exception=None):

	if exception and Session.is_active:
		Session.rollback()

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad Request. The browser (or proxy) sent a request that this server could not understand.'}), 400)

@app.route('/')
@app.route('/reference')
def renderreferencepage():
	return render_template('reference.html', url = 'http://caseys-chat-api.herokuapp.com')

@app.route('/api/v1/MessageThreads', methods = ['GET']) 
def getmessagethread():
	messages = []
	#set time param
	if request.args.get('timeSent'):
		if request.args.get('timeSent') == 'today':
			time_sent = 'today'
		elif request.args.get('timeSent') == 'week':
			time_sent = 'week'
		elif request.args.get('timeSent') == 'month':
			time_sent = 'month'
		else:
			abort(400)
	else: 
		time_sent = None
	#set user2
	if request.args.get('user2'):
		user2 = request.args.get('user2')
	else:
		user2 = None
		
	if request.args.get('user1'):
		user1 = request.args.get('user1')
		if request.args.get('listThreads'):
			if request.args.get('listThreads') == 'true':
				results = chatmodel.getthreadsbyuser(user1 = user1, user2 = user2, time_sent = time_sent)
				previously_listed_threads = []
				for result in results:
					if result[7] not in previously_listed_threads:
						message = { 'thread': result[7]}
						messages.append(message)
					previously_listed_threads.append(result[7])
			else:
				abort(400)
		else:
			results = chatmodel.getthreadsbyuser(user1 = user1, user2 = user2, time_sent = time_sent)
			for result in results:
				message = { 'thread': result[7]
					, 'messageId': result[0]
					, 'time': result[4]
					, 'from': result[5]
					, 'to': result[6]
					, 'body': result[3]
					}
				messages.append(message)
	else:
		abort(400)
	if len(messages) == 0:
		messages = [{'success': 'Request succeeded but yielded no results.'}]
	return jsonify(messages)

@app.route('/api/v1/MessageThreads', methods = ['POST'])
def postmessagethread():
	messages = []
	params = request.get_json()
	if ('from' in params) and ('to' in params) and ('body' in params):
		from_user = request.json['from']
		to_user = request.json['to']
		body = request.json['body']
		post = chatmodel.postmessage(from_user = from_user, to_user = to_user, body = body)
		results = chatmodel.getthreadsbyuser(user1 = from_user, user2 = to_user)
		for result in results:
			message = { 'messageId': result[0]
				, 'time': result[4]
				, 'from': result[5]
				, 'to': result[6]
				, 'body': result[3]
				}
			messages.append(message)

		if post == "success":
			if ('returnThread' in params):
				if request.json['returnThread'] == 'true':
					return jsonify(messages)
				else:
					abort(400)
			else:
				return jsonify(message)
		else:
			abort(400)
	else:
		abort(400)

@app.route('/api/v1/Users', methods = ['GET'])
def getusers():
	messages = []
	results = chatmodel.getallusers()
	for result in results:
		message = { 'user':result[1]
			}
		messages.append(message)
	return jsonify(messages)

@app.route('/api/v1/Users', methods = ['POST'])
def adduser():
	message = []
	params = request.get_json()
	if ('username' in params) and ('email' in params) and ('password' in params):
		if '@' not in request.json['email']:
			abort(400)
		elif ' ' in request.json['username']:
			abort(400)
		elif ' ' in request.json['password']:
			abort(400)
		else:
			username = request.json['username']
			email = request.json['email']
			password = request.json['password']
			post = chatmodel.addnewuser(username = username, email = email, password = password)
			if post == "success":
				message = [{'message': 'added user successfully'
				, 'username': username
				, 'email': email
				, 'password': '***'}]
			else:
				message = [{'error':'Bad Request. Username is taken. Please try a different one.'}]
			return jsonify(message)
	else:
		abort(400)





