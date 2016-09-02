#!flask/bin/python
from app import app
import os

if 'heroku' in os.environ.get("PATH"):
		app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT"))) 
else:
	app.run(debug=True)