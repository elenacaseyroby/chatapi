from flask import render_template, redirect, request, Flask, jsonify, abort, make_response
from app import app, chatmodel, models
from sqlalchemy import text, update, func
from json import loads

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad Request. The browser (or proxy) sent a request that this server could not understand.'}), 400)



@app.route('/')
@app.route('/api')
@app.route('/api/reference')
def renderreferencepage():
	return render_template('reference.html', url = 'http://localhost:5000')

@app.route('/api/MessageThread', methods = ['GET']) 
def getmessagethread():
	messages = []
	if request.json.get('user1'):
		user1 = request.json.get('user1')
		if request.json.get('user2'):
			user2 = request.json.get('user2')
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
	else:
		abort(400)
	if len(messages) == 0:
		messages = [{'success': 'Request succeeded but yielded no results.'}]
	return jsonify(messages)
#curl -i -H 'Content-Type: application/json' -X GET -d '{"user1":"ecroby","user2":"user2"}' http://localhost:5000/api/MessageThread
#works!

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
			abort(400)
	else:
		abort(400)
#curl -i -H "Content-Type: application/json" -X POST -d '{"from":"[username]", "to": "[username]", "body": "[body text]"}' http://localhost:5000/api/MessageThread

@app.route('/api/User', methods = ['POST'])
def adduser():
	message = []
	if request.json['username'] and request.json['email'] and request.json['password']:
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

#curl -X POST "http://localhost:5000/api/User?username=[username]&email=[email]&password=[password]"
#curl -i -H "Content-Type: application/json" -X POST -d '{"username":"[username]", "email": "[email]", "password": "[password]"}' http://localhost:5000/api/User





