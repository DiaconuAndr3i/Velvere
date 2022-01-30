from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    sensors = db.relationship('Sensor', backref="user")



class Plant(db.Model):
    id_plant = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    origin_country = db.Column(db.String(200), nullable=False)
    opt_humidity = db.Column(db.Float(), nullable=False)
    opt_temperature = db.Column(db.Float(), nullable=False)
    plants = db.relationship('Sensor', backref="plant")


class Sensor(db.Model):
    id_sensor = db.Column(db.Integer, primary_key=True)
    humidity = db.Column(db.Float(), nullable=False)
    temperature = db.Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'))
    id_plant = db.Column(db.Integer, db.ForeignKey('plant.id_plant'))



class Utilities(db.Model):
    id_utility = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    quantity = db.Column(db.Float(), nullable=False)
    unit_measure = db.Column(db.String(200), nullable=False)
    last_date = db.Column(db.DateTime, default=datetime.now())

