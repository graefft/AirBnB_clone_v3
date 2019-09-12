#!/usr/bin/python3
"""
Cities View
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from os import getenv, environ


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def all_reviews(review_id):
    '''retrieves a Review object'''
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews_in_place(place_id):
    """
    Retrieves all review objects of a place
    """
    review_list = []
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    else:
        reviews = place.reviews
        for review in reviews:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    '''review by id delete'''
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    '''creates a Review'''
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    if not data.get('text'):
        abort(400, 'Missing text')
    user = storage.get('User', data['user_id'])
    if not user:
        abort(404)
    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    '''sends PUT request on review by id'''
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    output = {}
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    output = review.to_dict()
    return jsonify(output), 200
