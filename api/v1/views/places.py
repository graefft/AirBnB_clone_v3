#!/usr/bin/python3
"""
Cities View
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from os import getenv, environ


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def all_places(place_id):
    '''retrieves a Place object'''
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places_in_city(city_id):
    """
    Retrieves all place objects of a city
    """
    place_list = []
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    else:
        places = city.places
        for place in places:
            place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    '''place by id delete'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    '''creates a Place'''
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    if not data.get('name'):
        abort(400, 'Missing name')
    user = storage.get('User', data['user_id'])
    if not user:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    '''sends PUT request on place by id'''
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    output = {}
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    output = place.to_dict()
    return jsonify(output), 200
