from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.extensions import db

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    current_user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=current_user_id).order_by(Order.created_at.desc()).all()
    return jsonify([order.to_dict() for order in orders])

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    current_user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=current_user_id).first_or_404()
    return jsonify(order.to_dict())

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    current_user_id = get_jwt_identity()
    
    # Get user's cart
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    if not cart or not cart.items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart.items)
    
    # Create order
    order = Order(
        user_id=current_user_id,
        total_amount=total_amount,
        status='completed'
    )
    db.session.add(order)
    
    # Create order items
    for cart_item in cart.items:
        order_item = OrderItem(
            order=order,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price_at_time=cart_item.product.price
        )
        db.session.add(order_item)
    
    # Clear cart
    CartItem.query.filter_by(cart_id=cart.id).delete()
    
    db.session.commit()
    return jsonify(order.to_dict()), 201

@order_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    current_user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=current_user_id).first_or_404()
    
    if order.status != 'pending':
        return jsonify({'error': 'Cannot cancel completed order'}), 400
    
    order.status = 'cancelled'
    db.session.commit()
    
    return jsonify(order.to_dict()) 