#!/usr/bin/python3
"""
Cities Object method
"""
from api.v1.views import app_views, storage
from flask import Flask, jsonify, request, abort
import json
from models.city import City
from models.state import State


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_select(city_id):
    """
    select city by id
    """
    if request.method == "GET":
        storagest = storage.all("City")
        for city in storagest.values():
            if city.id == city_id:
                city_dict = (city.to_dict())
                return json.dumps(city_dict, sort_keys=True, indent=4)
        return abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_delete(city_id):
    """
    delete city by id
    """
    if request.method == "DELETE":
        for city in storage.all("City").values():
            if city.id == city_id:
                storage.delete(city)
                storage.save()
                return {}
        return abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_update(city_id):
    """
    update city by id
    """
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})
    old = storage.get(City, city_id)
    if not old:
        return abort(404)
    for key, value in new.items():
        if key not in ['id', 'created_at']:
            setattr(old, key, value)
    storage.save()
    return jsonify(old.to_dict())


@app_views.route("states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def state_city_list(state_id):
    """
    list all city of a state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_city = []
    storagest = storage.all("City")
    for city in storagest.values():
        if city.state_id == state_id:
            all_city.append(city.to_dict())
            json.dumps(all_city)
    return json.dumps(all_city, sort_keys=True, indent=4)


@app_views.route("states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def city_create(state_id):
    """
    create city by id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    new_city = request.get_json(silent=True)
    if not new_city:
        return abort(400, {"Not a JSON"})
    if "name" not in new_city.keys():
        return abort(400, {"Missing name"})
    new_obj = City(name=new_city['name'], state_id=state_id)
    storage.new(new_obj)
    storage.save()
    return new_obj.to_dict(), 201
