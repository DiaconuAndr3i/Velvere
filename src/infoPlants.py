from flask import Blueprint, request, jsonify
from src.constants.status_codes import *
from src.database import Plant, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import os

infoPlants = Blueprint("infoPlants", __name__, url_prefix="/api/infoPlants")

@infoPlants.post("/insert")
@jwt_required()
def insertPlant():
    name = request.json["name"]
    origin_country = request.json["origin_country"]
    opt_humidity = request.json["opt_humidity"]
    opt_temperature = request.json["opt_temperature"]

    plant = Plant(name=name, origin_country=origin_country,
                  opt_humidity=opt_humidity, opt_temperature=opt_temperature)

    db.session.add(plant)
    db.session.commit()

    plantGreenHouse = {
        "name": name,
        "origin_country": origin_country,
        "opt_humidity": opt_humidity,
        "opt_temperature": opt_temperature
    }

    os.environ['currentPlant'] = f"{plantGreenHouse}"

    return jsonify({
        'message': 'Plant inserted',
        'plant': {
            'name': name,
            'origin_country': origin_country,
            'opt_humidity': opt_humidity,
            'opt_temperature': opt_temperature
        }
    }), HTTP_201_CREATED


@infoPlants.get("/getPlants")
def getPlants():
    plants = Plant.query.all()
    listPlants = []
    for item in plants:

        obj = {
            'name': item.name,
            'origin_country': item.origin_country,
            'opt_humidity': item.opt_humidity,
            'opt_temperature': item.opt_temperature}

        listPlants.append(obj)

    return jsonify({
        'plants': listPlants
    }), HTTP_200_OK