"""
Order routes for Grocery Store Application
"""
from flask import Blueprint, request, jsonify, session
from models.models import db, Order, OrderItem, Cart, Product
from utils.helpers import get_or_create_session_id
from datetime import datetime
import uuid

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@orders_bp.route('/', methods=['POST'])
def create_order():
    """Create a new order from cart items"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Order data is required'}), 400
        
        shipping_address = data.get('shipping_address')
        payment_method = data.get('payment_method')
        notes = data.get('notes', '')
        
        if not shipping_address:
            return jsonify({'error': 'Shipping address is required'}), 400
        
        if not payment_method:
            return jsonify({'error': 'Payment method is required'}), 400
        
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Get cart items
        cart_items = Cart.query.filter(
            (Cart.user_id == user_id) | (Cart.session_id == session_id)
        ).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total amount and check stock
        total_amount = 0
        order_items_data = []
        
        for cart_item in cart_items:
            product = cart_item.product
            
            # Check stock availability
            if product.stock_quantity < cart_item.quantity:
                return jsonify({
                    'error': f'Insufficient stock for {product.name}. Available: {product.stock_quantity}, Requested: {cart_item.quantity}'
                }), 400
            
            item_total = cart_item.quantity * float(product.price)
            total_amount += item_total
            
            order_items_data.append({
                'product_id': product.id,
                'quantity': cart_item.quantity,
                'price_per_unit': float(product.price),
                'total_price': item_total
            })
        
        # Generate unique order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Create order
        order = Order(
            user_id=user_id,
            session_id=session_id,
            order_number=order_number,
            total_amount=total_amount,
            shipping_address=shipping_address,
            payment_method=payment_method,
            notes=notes,
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Create order items and update stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price_per_unit=item_data['price_per_unit'],
                total_price=item_data['total_price']
            )
            db.session.add(order_item)
            
            # Update product stock
            product = Product.query.get(item_data['product_id'])
            product.stock_quantity -= item_data['quantity']
        
        # Clear cart
        Cart.query.filter(
            (Cart.user_id == user_id) | (Cart.session_id == session_id)
        ).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """Get orders for current user/session"""
    try:
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Get orders
        orders = Order.query.filter(
            (Order.user_id == user_id) | (Order.session_id == session_id)
        ).order_by(Order.created_at.desc()).all()
        
        return jsonify([order.to_dict() for order in orders])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by ID"""
    try:
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Find order
        order = Order.query.filter(
            Order.id == order_id,
            (Order.user_id == user_id) | (Order.session_id == session_id)
        ).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify(order.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """Cancel an order"""
    try:
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Find order
        order = Order.query.filter(
            Order.id == order_id,
            (Order.user_id == user_id) | (Order.session_id == session_id)
        ).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Check if order can be cancelled
        if order.status not in ['pending', 'confirmed']:
            return jsonify({'error': 'Order cannot be cancelled in current status'}), 400
        
        # Update order status
        order.status = 'cancelled'
        
        # Restore stock for cancelled order
        for order_item in order.order_items:
            product = Product.query.get(order_item.product_id)
            if product:
                product.stock_quantity += order_item.quantity
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/stats', methods=['GET'])
def get_order_stats():
    """Get order statistics for current user"""
    try:
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Get order counts by status
        stats = db.session.query(
            Order.status,
            db.func.count(Order.id).label('count')
        ).filter(
            (Order.user_id == user_id) | (Order.session_id == session_id)
        ).group_by(Order.status).all()
        
        # Get total spent
        total_spent = db.session.query(
            db.func.sum(Order.total_amount)
        ).filter(
            (Order.user_id == user_id) | (Order.session_id == session_id),
            Order.status != 'cancelled'
        ).scalar() or 0
        
        # Format stats
        stats_dict = {status: count for status, count in stats}
        
        return jsonify({
            'stats': stats_dict,
            'total_orders': sum(stats_dict.values()),
            'total_spent': float(total_spent)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
