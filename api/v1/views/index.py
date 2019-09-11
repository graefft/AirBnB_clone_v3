#!/usr/bin/python3
''' Imports app_views and creates /status route on app_views'''
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/stats', strict_slashes=False)
def stats():
    '''creates endpoint that retrieves number of each object by type'''
    classes = {'amenities':  storage.count(Amenity),
               'cities':  storage.count(City),
               'places':  storage.count(Place),
               'reviews':  storage.count(Review),
               'states':  storage.count(State),
               'users':  storage.count(User)}
    return jsonify(classes)


@app_views.route('/status', strict_slashes=False)
def status():
    '''returns JSON: "status": OK'''
    result = {'status':  'OK'}
    return jsonify(result), 200
