#!/usr/bin/python3
"""
Amenitys View
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from os import getenv, environ


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def allamenities():
    """
    Retrieves all amenity objects
    """
    return jsonify([a.to_dict() for a in storage.all("Amenity").values()]), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createamenity():
    """Creates a amenity"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if not data.get('name'):
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id=""):
    """Amenity by id get, delete, and put"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    request.method
    output = {}
    if request.method == 'GET':
        output = amenity.to_dict()
    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        output = amenity.to_dict()
    return jsonify(output), 200
