from flask import Blueprint, request, jsonify
from models import db, User
from datetime import datetime
from token_utils import Token

bp_auth=Blueprint("auth_routes", __name__)

@bp_auth.route("/auth/login", methods=["POST"])
def user_authentication():
    data=request.json
    email=data["email"]
    password=data["password"]
    user=User.query.filter_by(email=email).first()
    if user:
        if not user.is_activated:
            return jsonify({'error': 'User is not activated, check your email'}), 400
        elif password==user.password:
            token=Token.token_generation(email=email)
            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Password wrong'}), 400
    else:
        return jsonify({'error': f'User with email {email} is not present in the database'}), 404
    
@bp_auth.route("/auth/isvalid", methods=["POST"])
def token_is_valid():
    token=request.headers.get("Authorization").replace("Bearer ", "")
    response=Token.token_is_valid(token=token)
    if response:
        return jsonify({'message':'Token is valid'}), 200
    else:
        return jsonify({'error': 'Token is not valid'}), 400
    
@bp_auth.route("/auth/useractivation", methods=["POST"])
def user_activation():
    body=request.json
    email=body["email"]
    user=User.query.filter_by(email=email).first()
    if user:
        if user.is_activated:
            return jsonify({'error': 'User already activated'}), 400
        else:
            user.is_activated=True
            db.session.commit()
            return jsonify({'message': 'User activated'}), 200
    else:
        return jsonify({'error': f'User with email {email} not found'}), 404