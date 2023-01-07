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
app = Flask(__name__)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_select(place_id):
    """
    select place by id
    """
    if request.method == "GET":
        storagest = storage.all("Place")
        for place in storagest.values():
            if place.id == place_id:
                place_dict = (place.to_dict())
                return json.dumps(place_dict, sort_keys=True, indent=4)
        return abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def place_delete(place_id):
    """
    delete place by id
    """
    if request.method == "DELETE":
        for place in storage.all("Place").values():
            if place.id == place_id:
                storage.delete(place)
                storage.save()
                return {}
        return abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_update(place_id):
    """
    update place by id
    """
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})
    old = storage.get(Place, place_id)
    if not old:
        return abort(404)
    for key, value in new.items():
        if key not in ['id', 'created_at']:
            setattr(old, key, value)
    storage.save()
    return jsonify(old.to_dict())


@app_views.route("cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def city_place_list(city_id):
    """
    list all place of a city
    """
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    all_place = []
    storagest = storage.all("Place")
    for place in storagest.values():
        if place.city_id == city_id:
            all_place.append(place.to_dict())
            json.dumps(all_place)
    return json.dumps(all_place, sort_keys=True, indent=4)


@app_views.route("cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def place_create(city_id):
    """
    create place by id
    """
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    new_place = request.get_json(silent=True)
    if not new_place:
        return abort(400, {"Not a JSON"})
    if "name" not in new_place.keys():
        return abort(400, {"Missing name"})
    if "user_id" not in new_place.keys():
        return abort(400, {"Missing user id"})
    user = storage.get(User, new_place['user_id'])
    print("zzzzzzzzzzzz: {}".format(new_place.keys()))
    if user is None:
        return abort(404)
    new_obj = Place(name=new_place['name'],
                    user_id=new_place['user_id'],
                    city_id=city_id)
    storage.new(new_obj)
    storage.save()
    return new_obj.to_dict(), 201
