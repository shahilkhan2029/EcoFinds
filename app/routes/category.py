from flask import Blueprint, jsonify, request
from app.models.category import Category
from app.extensions import db
from app.config.settings import messages

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@category_bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict())

@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category with this name already exists'}), 400
    
    category = Category(
        name=data['name'],
        description=data.get('description'),
        icon=data.get('icon')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category.to_dict()), 201

@category_bp.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data and data['name'] != category.name:
        if Category.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Category with this name already exists'}), 400
        category.name = data['name']
    
    if 'description' in data:
        category.description = data['description']
    if 'icon' in data:
        category.icon = data['icon']
    
    db.session.commit()
    return jsonify(category.to_dict())

@category_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return '', 204 