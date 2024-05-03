#!/usr/bin/python3
"""
Create a flask app; and register the blueprint app_views to flask instance
"""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', '5000')
    app.run(hosts=HOST, port=PORT, threaded=True)