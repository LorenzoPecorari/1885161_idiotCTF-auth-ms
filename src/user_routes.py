from flask import Blueprint, request, jsonify
from models import db, User
from datetime import datetime
from token_utils import Token
from mail_sender_utils import MailSender

bp_user=Blueprint("user_routes", __name__)

@bp_user.route("/user/getusers", methods=["GET"])
def get_user():
    users=User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp_user.route("/user/add", methods=["POST"])
def add_user():
    data=request.json
    matricola=data["matricola"]
    user=User.query.get(matricola)
    if user:
        return jsonify({'error': f'An user with matricola {matricola} is already present. Please use a different matricola number'}), 400
    
    email=data["email"]
    user=User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': f'An user with email {email} is already present. Please use a different email'}), 400

    newUser=User(matricola=data["matricola"], name=data["name"], surname=data["surname"],
                 email=data["email"], gender=data["gender"], dob=datetime.strptime(data["dob"], "%d/%m/%Y"),
                 password=data["password"], university=data["university"], role=data["role"])
    db.session.add(newUser)
    db.session.commit()
    ms = MailSender()
    ms.user_activation(email)
    return jsonify(newUser.to_dict()), 201

@bp_user.route("/user/getuserbyid/<int:id>",methods=["GET"])
def get_user_by_id(id):
    user=User.query.get(id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': "User not found"}), 404

@bp_user.route("/user/getusersbyuniversity/<string:university>", methods=['GET'])
def get_users_by_university(university):
    users=User.query.filter_by(university=university).all()
    if users:
        return jsonify([user.to_dict() for user in users]), 200
    else:
        return jsonify({'error': f'There are no users for \'{university}\''}), 404
    
@bp_user.route("/user/getuserrole", methods=["GET"])
def get_user_role():
    token=request.headers.get("Authorization").replace("Bearer ", "")
    email=Token.get_email(token)
    print(email)
    if '@' in email:
        user=User.query.filter_by(email=email).first()
        if user:
            return jsonify({'role': user.role}), 200
        else:
            return jsonify({'error': f'User with email {email} not found'}), 404
    else:
        return jsonify({'error': 'Error in token decode'}), 400
    
@bp_user.route("/user/getuserbytoken", methods=["GET"])
def get_id_by_token():
    token=request.headers.get("Authorization").replace("Bearer ", "")
    email=Token.get_email(token)
    if '@' in email:
        user=User.query.filter_by(email=email).first()
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({'error': f'User with email {email} not found'}), 404
    else:
        return jsonify({'error': 'Error in token decode'}), 400
    
@bp_user.route("/user/isactivated/<string:email>", methods=["GET"])
def is_user_activated(email):
    user=User.query.filter_by(email=email).first()
    if user:
        return jsonify({'is_activated': user.is_activated}), 200
    else:
        return jsonify({'error': f'User with email {email} not found'}), 404