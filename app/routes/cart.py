from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.extensions import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    current_user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    
    if not cart:
        cart = Cart(user_id=current_user_id)
        db.session.add(cart)
        db.session.commit()
    
    return jsonify(cart.to_dict())

@cart_bp.route('/cart/items', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get or create cart
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    if not cart:
        cart = Cart(user_id=current_user_id)
        db.session.add(cart)
    
    # Get product
    product = Product.query.get_or_404(data['product_id'])
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id
    ).first()
    
    if cart_item:
        cart_item.quantity += data.get('quantity', 1)
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=data.get('quantity', 1)
        )
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify(cart.to_dict())

@cart_bp.route('/cart/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        id=item_id
    ).first_or_404()
    
    cart_item.quantity = data.get('quantity', cart_item.quantity)
    db.session.commit()
    
    return jsonify(cart.to_dict())

@cart_bp.route('/cart/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    current_user_id = get_jwt_identity()
    
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        id=item_id
    ).first_or_404()
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify(cart.to_dict())

@cart_bp.route('/cart', methods=['DELETE'])
@jwt_required()
def clear_cart():
    current_user_id = get_jwt_identity()
    
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()
    
    return jsonify(cart.to_dict()) 