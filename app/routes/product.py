from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product import Product
from app.models.user import User
from app.extensions import db
from werkzeug.utils import secure_filename
import os

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    # Get query parameters
    category = request.args.get('category')
    search = request.args.get('search')
    
    # Base query
    query = Product.query
    
    # Apply filters
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.title.ilike(f'%{search}%'))
    
    # Get products
    products = query.order_by(Product.created_at.desc()).all()
    return jsonify([product.to_dict() for product in products])

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    current_user_id = get_jwt_identity()
    data = request.form
    
    # Handle image upload
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('public/uploads', filename))
            image_url = f'/uploads/{filename}'
    
    # Create product
    product = Product(
        title=data['title'],
        description=data['description'],
        price=float(data['price']),
        category=data['category'],
        image_url=image_url,
        seller_id=current_user_id
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify(product.to_dict()), 201

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_user_id = get_jwt_identity()
    product = Product.query.get_or_404(product_id)
    
    # Check ownership
    if product.seller_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.form
    
    # Update fields
    if 'title' in data:
        product.title = data['title']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = float(data['price'])
    if 'category' in data:
        product.category = data['category']
    
    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('public/uploads', filename))
            product.image_url = f'/uploads/{filename}'
    
    db.session.commit()
    return jsonify(product.to_dict())

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    current_user_id = get_jwt_identity()
    product = Product.query.get_or_404(product_id)
    
    # Check ownership
    if product.seller_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(product)
    db.session.commit()
    return '', 204

@product_bp.route('/products/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Product.category).distinct().all()
    return jsonify([category[0] for category in categories]) 