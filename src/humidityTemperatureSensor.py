from flask import Blueprint, request, jsonify
from src.constants.status_codes import *
from src.database import Sensor, db, Plant
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import os
import json
import paho.mqtt.client as mqtt

humidityTemperatureSensor = Blueprint("humidityTemperatureSensor", __name__,
                                      url_prefix="/api/humidityTemperatureSensor")

mqttBroker = "broker.hivemq.com"
client_temp = mqtt.Client("Temperature")
client_temp.connect(mqttBroker)
client_hum = mqtt.Client("Humidity")
client_hum.connect(mqttBroker)


@humidityTemperatureSensor.post("/sensorForHumidityTemperature")
@jwt_required()
def sensorForHumidityTemperature():
    current_user = get_jwt_identity()
    humidity = request.json["humidity"]
    temperature = request.json["temperature"]
    namePlant = json.loads(os.environ.get('currentPlant'))["name"]
    plant = Plant.query.filter_by(name=namePlant).first()

    client_temp.publish("AMBIENT_TEMPERATURE", f'Tem: {temperature}')
    client_hum.publish("AMBIENT_HUMIDITY", f'Hum: {humidity}')

    if plant is None:
        return jsonify({
            "response": "Doesn't exist plant in the database."
        }), HTTP_404_NOT_FOUND
    sensorRecord = Sensor(humidity=humidity, temperature=temperature, id_user=current_user, id_plant=plant.id_plant)

    db.session.add(sensorRecord)
    db.session.commit()

    return jsonify({
        "temperature": temperature,
        "humidity": humidity
    }), HTTP_201_CREATED
