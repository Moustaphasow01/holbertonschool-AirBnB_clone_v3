#!/usr/bin/python3
"""
Places Object method
"""
from api.v1.views import app_views, storage
from flask import Flask, jsonify, request, abort
import json
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
app = Flask(__name__)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def review_select(review_id):
    """
    select place by id
    """
    if request.method == "GET":
        storagest = storage.all("Review")
        for review in storagest.values():
            if review.id == review_id:
                review_dict = (review.to_dict())
                return json.dumps(review_dict, sort_keys=True, indent=4)
        return abort(404)


@app_views.route("places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def review__select_by_place(place_id):
    """Returns JSON reviews of given place"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    all_review = []
    storagest = storage.all("Review")
    for review in storagest.values():
        if review.place_id == place_id:
            all_review.append(review.to_dict())
            json.dumps(all_review)
    return json.dumps(all_review, sort_keys=True, indent=4)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def review_delete(review_id):
    """
    delete review by id
    """
    if request.method == "DELETE":
        for review in storage.all("Review").values():
            if review.id == review_id:
                storage.delete(review)
                storage.save()
                return {}
        return abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def review_update(review_id):
    """
    update review by id
    """
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})
    old = storage.get(Review, review_id)
    if not old:
        return abort(404)
    for key, value in new.items():
        if key not in ['id',
                       'created_at',
                       'updated_at',
                       'user_id',
                       'place_id']:
            setattr(old, key, value)
    storage.save()
    return jsonify(old.to_dict())


@app_views.route("places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def review_create(place_id):
    """
    create review by id
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    new_review = request.get_json(silent=True)
    if not new_review:
        return abort(400, {"Not a JSON"})
    if "text" not in new_review.keys():
        return abort(400, {"Missing text"})
    if "user_id" not in new_review.keys():
        return abort(400, {"Missing user id"})
    user = storage.get(User, new_review['user_id'])
    if user is None:
        return abort(404)
    new_obj = Review(text=new_review['text'],
                     user_id=new_review['user_id'],
                     place_id=place_id)
    storage.new(new_obj)
    storage.save()
    return new_obj.to_dict(), 201
