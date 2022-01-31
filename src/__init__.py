from flask import Flask
import os
from src.auth import auth
from src.infoPlants import infoPlants
from src.plantScanner import plantScanner
from src.utilities import utilities
from src.humidityTemperatureSensor import humidityTemperatureSensor
from src.database import db
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLACLHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    create_databse(app)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(infoPlants)
    app.register_blueprint(plantScanner)
    app.register_blueprint(utilities)
    app.register_blueprint(humidityTemperatureSensor)

    return app


def create_databse(app):
    if not os.path.exists('src/' + os.environ.get('DATABASE_NAME')):
        db.create_all(app=app)
        print('Created database!')
