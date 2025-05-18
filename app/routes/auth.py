from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db, mail
from flask_mail import Message
from app.config.settings import messages, features

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    if not features['enableRegistration']:
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': messages['errors']['emailExists']}), 400
    
    user = User(
        email=data['email'],
        password=generate_password_hash(data['password']),
        role='user'
    )
    
    db.session.add(user)
    db.session.commit()
    
    msg = Message(
        'Welcome to PrimeHomes',
        recipients=[user.email]
    )
    msg.body = f"Welcome to PrimeHomes! We're excited to have you on board."
    mail.send(msg)
    
    return jsonify({'message': messages['success']['registration']}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'error': messages['errors']['invalidCredentials']}), 401 