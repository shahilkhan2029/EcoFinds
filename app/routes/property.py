from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.property import Property
from app.models.user import User
from app.extensions import db
from app.config.settings import messages, features
import os

property_bp = Blueprint('property', __name__)

@property_bp.route('/properties', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    return jsonify([p.to_dict() for p in properties]), 200

@property_bp.route('/properties/<int:id>', methods=['GET'])
def get_property(id):
    property = Property.query.get_or_404(id)
    return jsonify(property.to_dict()), 200

@property_bp.route('/properties', methods=['POST'])
@jwt_required()
def create_property():
    if not features['enablePropertyCreation']:
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'agent':
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    data = request.get_json()
    property = Property(
        title=data['title'],
        type=data['type'],
        price=data['price'],
        location=data['location'],
        description=data['description'],
        bedrooms=data['bedrooms'],
        bathrooms=data['bathrooms'],
        area=data['area'],
        agent_id=current_user_id
    )
    
    db.session.add(property)
    db.session.commit()
    
    return jsonify(property.to_dict()), 201

@property_bp.route('/properties/<int:id>', methods=['PUT'])
@jwt_required()
def update_property(id):
    current_user_id = get_jwt_identity()
    property = Property.query.get_or_404(id)
    
    if property.agent_id != current_user_id:
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    data = request.get_json()
    for key, value in data.items():
        setattr(property, key, value)
    
    db.session.commit()
    return jsonify(property.to_dict()), 200

@property_bp.route('/properties/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_property(id):
    current_user_id = get_jwt_identity()
    property = Property.query.get_or_404(id)
    
    if property.agent_id != current_user_id:
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    db.session.delete(property)
    db.session.commit()
    
    return jsonify({'message': messages['success']['deletion']}), 200 