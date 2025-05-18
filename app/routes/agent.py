from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.agent import Agent
from app.models.user import User
from app.extensions import db
from app.config.settings import messages, features

agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/agents', methods=['GET'])
def get_agents():
    agents = Agent.query.all()
    return jsonify([a.to_dict() for a in agents]), 200

@agent_bp.route('/agents/<int:id>', methods=['GET'])
def get_agent(id):
    agent = Agent.query.get_or_404(id)
    return jsonify(agent.to_dict()), 200

@agent_bp.route('/agents', methods=['POST'])
@jwt_required()
def create_agent():
    if not features['enableAgentRegistration']:
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'user':
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    data = request.get_json()
    agent = Agent(
        user_id=current_user_id,
        full_name=data['full_name'],
        title=data['title'],
        phone=data['phone'],
        bio=data['bio'],
        specialization=data['specialization'],
        languages=data['languages']
    )
    
    user.role = 'agent'
    db.session.add(agent)
    db.session.commit()
    
    return jsonify(agent.to_dict()), 201

@agent_bp.route('/agents/<int:id>', methods=['PUT'])
@jwt_required()
def update_agent(id):
    current_user_id = get_jwt_identity()
    agent = Agent.query.get_or_404(id)
    
    if agent.user_id != current_user_id:
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    data = request.get_json()
    for key, value in data.items():
        setattr(agent, key, value)
    
    db.session.commit()
    return jsonify(agent.to_dict()), 200 