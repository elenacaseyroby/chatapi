#!flask/bin/python
from app import app
import os

#if 'HEROKU_CHECK' in os.environ:
	#print("heroku check")
app.run(host='0.0.0.0', port=int(os.environ.get("PORT"))) 

#else:
	#print("local")
	#app.run(debug=True)