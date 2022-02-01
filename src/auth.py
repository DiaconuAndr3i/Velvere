from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.status_codes import *
from src.database import User, db
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import  swag_from


auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.post('/register')
@swag_from('./docs/auth/register.yml')
def register():
    nickname = request.json["nickname"]
    email = request.json["email"]
    password = request.json["password"]

    if len(password) < 6:
        return jsonify({'error': 'Password is too short'}), HTTP_400_BAD_REQUEST

    if len(nickname) < 3:
        return jsonify({'error': 'Nickname is too short'}), HTTP_400_BAD_REQUEST

    if not nickname.isalnum() < 3:
        return jsonify({'error': 'Nickname is not alphanumeric'}), HTTP_400_BAD_REQUEST

    if " " in nickname:
        return jsonify({'error': 'Nickname cannot contain spaces'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'Email is invalid'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email is taken'}), HTTP_409_CONFLICT

    if User.query.filter_by(nickname=nickname).first() is not None:
        return jsonify({'error': 'Nickname is taken'}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(nickname=nickname, password=pwd_hash, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created',
        'user': {
            'nickname': nickname,
            'email': email
        }
    }), HTTP_201_CREATED


@auth.post("/login")
@swag_from('./docs/auth/login.yml')
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id_user)
            access = create_access_token(identity=user.id_user)

            return jsonify({
                'user':
                    {
                        'refresh': refresh,
                        'access': access,
                        'nickname': user.nickname,
                        'email': user.email
                    }
            }), HTTP_200_OK
    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.get('/refresh/token')
@jwt_required(refresh=True)
@swag_from('./docs/auth/refreshToken.yml')
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK
