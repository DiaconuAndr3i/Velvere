from flask import Blueprint, request, jsonify
from src.constants.status_codes import *
from src.database import Sensor, db, Plant
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import os
import json

humidityTemperatureSensor = Blueprint("humidityTemperatureSensor", __name__, url_prefix="/api/humidityTemperatureSensor")


@humidityTemperatureSensor.post("/sensorForFertilizer")
@jwt_required()
def sensorForFertilizer():
    current_user = get_jwt_identity()
    humidity = request.json["humidity"]
    temperature = request.json["temperature"]
    namePlant = json.loads(os.environ.get('currentPlant'))["name"]
    plant = Plant.query.filter_by(name=namePlant).first()
    if plant is None:
        return jsonify({
            "response": "Doesn't exist plant in the database."
        }), HTTP_404_NOT_FOUND
    sensorRecord = Sensor(humidity=humidity, temperature=temperature, id_user = current_user, id_plant=plant.id_plant)

    db.session.add(sensorRecord)
    db.session.commit()

    return jsonify({
        "response": "Response of the sensor it was recorded"
    }), HTTP_201_CREATED

