#!/usr/bin/python3
"""
amenitys Object method
"""
from api.v1.views import app_views, storage
from flask import jsonify, request, abort, Flask
import json
from models.amenity import Amenity

app = Flask(__name__)


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_list():
    """
    list all amenity
    """
    if request.method == "GET":
        all_amenity = []
        storagest = storage.all("Amenity")
        for amenity in storagest.values():
            all_amenity.append(amenity.to_dict())
        return jsonify(all_amenity), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_select(amenity_id):
    """
    select amenity by id
    """
    if request.method == "GET":
        storagest = storage.all("Amenity")
        storageamen = storagest.get('Amenity' + "." + amenity_id)
        if storageamen is None:
            abort(404)
        else:
            return jsonify(storageamen.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """
    delete amenity by id
    """
    if request.method == "DELETE":
        for amenity in storage.all("Amenity").values():
            if amenity.id == amenity_id:
                storage.delete(amenity)
                storage.save()
                return {}
        return abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    create amenity by id
    """
    new_amenity = request.get_json(silent=True)
    if not new_amenity:
        return abort(400, {"Not a JSON"})
    if "name" not in new_amenity.keys():
        return abort(400, {"Missing name"})
    new_obj = Amenity(name=new_amenity['name'])
    storage.new(new_obj)
    storage.save()
    return new_obj.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """
    update amenity by id
    """
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})
    old = storage.get(Amenity, amenity_id)
    if not old:
        return abort(404)
    for key, value in new.items():
        if key not in ['id', 'created_at']:
            setattr(old, key, value)
    storage.save()
    return jsonify(old.to_dict())
