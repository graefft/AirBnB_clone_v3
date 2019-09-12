#!/usr/bin/python3
"""
States View
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from os import getenv, environ


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allstates():
    """
    Retrieves all state objects
    """
    return jsonify([s.to_dict() for s in storage.all("State").values()]), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """Creates a state"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if not data.get('name'):
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state(state_id=" "):
    """State by id get, delete, and put"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    request.method
    output = {}
    if request.method == 'GET':
        output = state.to_dict()
    if request.method == 'DELETE':
        state.delete()
        storage.save()
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        output = state.to_dict()
    return jsonify(output), 200
