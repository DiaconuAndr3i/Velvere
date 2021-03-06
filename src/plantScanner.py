from flask import Blueprint, request, jsonify
import random
from src.constants.status_codes import *
import os
import requests
from src.database import Plant
import json
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import paho.mqtt.client as mqtt
from flasgger import swag_from

plantScanner = Blueprint("plantScanner", __name__, url_prefix="/api/plantScanner")


mqttBroker = "broker.hivemq.com"
client_temp = mqtt.Client("Optimum_Temperature")
client_temp.connect(mqttBroker)
client_hum = mqtt.Client("Optimum_Humidity")
client_hum.connect(mqttBroker)


@plantScanner.get("/scanResponse")
@swag_from('./docs/plantScanner/scanResponse.yml')
def scanResponse():
    response = requests.get("http://127.0.0.1:5000/api/infoPlants/getPlants")
    plants = response.json()['plants']

    nr = random.randrange(0, len(plants) + 1)

    if nr == len(plants):
        return jsonify({
            "response": "The scanned plant doesn't exist in database. Please insert or choose the plant!"
        }), HTTP_404_NOT_FOUND

    plantForEnv = '{"name": "' + plants[nr]['name'] + '", "origin_country": "' + plants[nr]['origin_country'] \
                  + '", "opt_humidity": "' + str(plants[nr]['opt_humidity']) + '", "opt_temperature": "' + str(plants[nr][
                      'opt_temperature']) + '"}'
    os.environ['currentPlant'] = plantForEnv

    client_temp.publish("OPTIMUM_TEMPERATURE", 'OptimumTem: ' + str(plants[nr]['opt_temperature']))
    client_hum.publish("OPTIMUM_HUMIDITY", 'OptimumHum: ' + str(plants[nr]['opt_humidity']))

    return plants[nr], HTTP_200_OK


@plantScanner.get("/showPlantFromGreenHouse")
@swag_from('./docs/plantScanner/showPlantFromGreenhouse.yml')
def showPlantFromGreenHouse():
    if os.environ.get('currentPlant') is None:
        return jsonify({
            "result": "Doesn't exist plant in the greenhouse."
        }), HTTP_404_NOT_FOUND
    return jsonify({
        "result": json.loads(os.environ.get('currentPlant'))
    }), HTTP_200_OK


@plantScanner.post("/putPlantInGreenHouse")
@jwt_required()
@swag_from('./docs/plantScanner/putPlantInGreenhouse.yml')
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
    }), HTTP_200_OK
