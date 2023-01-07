#!/usr/bin/python3
"""
States Object method
"""
from api.v1.views import app_views, storage
from flask import Flask, jsonify, request, abort
import json
from models.state import State
app = Flask(__name__)


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_list():
    """
    list all state
    """
    if request.method == "GET":
        all_state = []
        storagest = storage.all("State")
        for state in storagest.values():
            all_state.append(state.to_dict())
            json.dumps(all_state)
        return json.dumps(all_state, sort_keys=True, indent=4)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_select(state_id):
    """
    select state by id
    """
    if request.method == "GET":
        storagest = storage.all("State")
        for state in storagest.values():
            if state.id == state_id:
                state_dict = (state.to_dict())
                return json.dumps(state_dict, sort_keys=True, indent=4)
        return abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    """
    delete state by id
    """
    if request.method == "DELETE":
        for state in storage.all("State").values():
            if state.id == state_id:
                storage.delete(state)
                storage.save()
                return {}
        return abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    create state by id
    """
    new_state = request.get_json(silent=True)
    if not new_state:
        return abort(400, {"Not a JSON"})
    if "name" not in new_state.keys():
        return abort(400, {"Missing name"})
    new_obj = State(name=new_state['name'])
    storage.new(new_obj)
    storage.save()
    return new_obj.to_dict(), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_update(state_id):
    """
    update state by id
    """
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})
    old = storage.get(State, state_id)
    if not old:
        return abort(404)
    for key, value in new.items():
        if key not in ['id', 'created_at']:
            setattr(old, key, value)
    storage.save()
    return jsonify(old.to_dict())
