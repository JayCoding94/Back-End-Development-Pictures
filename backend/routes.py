from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((pic for pic in data if pic.get("id") == id), None)
    if picture:
        return jsonify(picture), 200
    abort(404, description="Picture not found")


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture entry"""
    picture = request.get_json()
    picture_id = picture.get("id")

    if any(pic["id"] == picture_id for pic in data):
        return jsonify({"Message": f"picture with id {picture_id} already present"}), 302

    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture entry by ID"""
    update_data = request.get_json()

    # Find the picture with the given ID
    picture = next((pic for pic in data if pic["id"] == id), None)
    
    if not picture:
        return jsonify({"message": "picture not found"}), 404

    # Update the picture with new data
    picture.update(update_data)

    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture entry by ID"""
    global data  # 데이터를 수정해야 하므로 global로 선언

    # Find the picture index by ID
    picture_index = next((index for index, pic in enumerate(data) if pic["id"] == id), None)
    
    if picture_index is None:
        return jsonify({"message": "picture not found"}), 404

    # Remove the picture from the list
    del data[picture_index]

    return "", 204  # 204 No Content (Empty body)