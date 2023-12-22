#!/usr/bin/python3
"""users module for API"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Places Reviews objects"""
    if not storage.get(Place, place_id):
        abort(404)
    list_reviews = [
        review.to_dict() for review in
        storage.all(Review).values() if review.place_id == place_id
        ]
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Places Reviews object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Places reviews object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Place Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if "text" not in request.get_json():
        abort(400, "Missing text")
    user = storage.get(User, request.get_json()["user_id"])
    if not user:
        abort(404)
    request.get_json()['place_id'] = place_id
    review = Review(**request.get_json())
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a User object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
