from flask import Blueprint, request, jsonify
import random
from src.constants.status_codes import *
import os
import requests
from src.database import Plant
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

plantScanner = Blueprint("plantScanner", __name__, url_prefix="/api/plantScanner")


@plantScanner.get("/scanResponse")
def scanResponse():
    response = requests.get("http://127.0.0.1:5000/api/infoPlants/getPlants")
    plants = response.json()['plants']

    nr = random.randrange(0, len(plants) + 1)

    if nr == len(plants):
        return jsonify({
            "response": "The scanned plant doesn't exist in database. Please insert or choose the plant!"
        }), HTTP_404_NOT_FOUND

    os.environ['currentPlant'] = f"{plants[nr]}"

    return plants[nr]


@plantScanner.get("/showPlantFromGreenHouse")
def showPlantFromGreenHouse():
    if os.environ.get('currentPlant') is None:
        return jsonify({
            "result": "Doesn't exist plant in the greenhouse."
        }), HTTP_404_NOT_FOUND
    return jsonify({
        "result": os.environ.get('currentPlant')
    }), HTTP_200_OK


@plantScanner.post("/putPlantInGreenHouse")
@jwt_required()
def putPlantInGreenHouse():
    name = request.json["name"]
    origin_country = request.json["origin_country"]
    opt_humidity = request.json["opt_humidity"]
    opt_temperature = request.json["opt_temperature"]

    plant = '{"name": "' + name + '", "origin_country": "' + origin_country \
            + '", "opt_humidity": "' + opt_humidity + '", "opt_temperature": "' + opt_temperature + '"}'

    os.environ['currentPlant'] = f"{plant}"

    return jsonify({
        "response": "Plant added"
    })
