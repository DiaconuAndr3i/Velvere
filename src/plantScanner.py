from flask import Blueprint, request, jsonify
import random
from src.constants.status_codes import *
import os
import requests

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

    # os.putenv("currentPlant", f"{plants[nr]}")

    print(plants[0])

    return plants[nr]
