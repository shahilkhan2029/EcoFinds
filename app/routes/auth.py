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
    data = request.get_json()
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': 'Registration successful',
            'user': new_user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    
    return jsonify({'error': 'Invalid email or password'}), 401 