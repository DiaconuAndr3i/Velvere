from flask import Blueprint, request, jsonify
from src.constants.status_codes import *
from src.database import Utilities, db
from flask_jwt_extended import jwt_required

utilities = Blueprint("utilities", __name__, url_prefix="/api/utilities")


@utilities.post("/addUtilities")
@jwt_required()
def addUtilities():
    name = request.json["name"]
    quantity = request.json["quantity"]
    unit_measure = request.json["unit_measure"]

    if Utilities.query.filter_by(name=name).first() is not None:
        return jsonify({'error': 'Utility already exist'}), HTTP_409_CONFLICT

    utility = Utilities(name=name, quantity=quantity, unit_measure=unit_measure)

    db.session.add(utility)
    db.session.commit()

    return jsonify({
        "response": "Utility created"
    }), HTTP_201_CREATED


@utilities.get("/getUtilities")
@jwt_required()
def getUtilities():
    allUtilities = Utilities.query.all()
    listUtilities = []
    for item in allUtilities:
        obj = {
            'name': item.name,
            'quantity': item.quantity,
            'unit_measure': item.unit_measure,
            'last_date': item.last_date}

        listUtilities.append(obj)

    return jsonify({
        'Utilities': listUtilities
    }), HTTP_200_OK


@utilities.put("/updateUtility")
@jwt_required()
def updateUtility():
    name = request.json["name"]
    quantity = request.json["quantity"]
    utility = Utilities.query.filter_by(name=name).first()
    utility.quantity = quantity
    db.session.commit()

    return jsonify({
        "response": "Utility updated"
    }), HTTP_200_OK
