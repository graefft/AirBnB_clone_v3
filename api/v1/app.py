#!/usr/bin/python3
'''Flask module to return status of API'''
from flask import Flask, Blueprint, jsonify, session
from models import storage
from api.v1.views import app_views
from os import getenv, environ
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def clean_up(self):
    '''closes storage'''
    storage.close()


@app.errorhandler(404)
def not_found(e):
    '''returns not found on 404'''
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    if environ.get('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    if environ.get('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
