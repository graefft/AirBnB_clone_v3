#!/usr/bin/python3
"""
Cities View
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from os import getenv, environ


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def all_cities(city_id):
    '''retrieves a City object'''
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities_in_state(state_id):
    """
    Retrieves all city objects of a state
    """
    city_list = []
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    else:
        cities = state.cities
        for city in cities:
            city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id):
    '''city by id delete'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    '''creates a City'''
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('name'):
        abort(400, 'Missing name')
    city = City(name=data['name'], state_id=state_id)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    '''sends PUT request on city by id'''
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    output = {}
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    output = city.to_dict()
    return jsonify(output), 200
