#!/usr/bin/python3
"""
Users View
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from os import getenv, environ


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def allusers():
    """
    Retrieves all user objects
    """
    return jsonify([s.to_dict() for s in storage.all("User").values()]), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createuser():
    """Creates a user"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if not data.get('email'):
        abort(400, "Missing email")
    if not data.get('password'):
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(user_id=""):
    """User by id get, delete, and put"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    request.method
    output = {}
    if request.method == 'GET':
        output = user.to_dict()
    if request.method == 'DELETE':
        user.delete()
        storage.save()
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        output = user.to_dict()
    return jsonify(output), 200
