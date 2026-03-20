"""
Cart routes for Grocery Store Application
"""
from flask import Blueprint, request, jsonify, session

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/', methods=['GET'])
def get_cart():
    """Get cart items for current user/session"""
    try:
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Get cart items
        cart_items = Cart.query.filter(
            (Cart.user_id == user_id) | (Cart.session_id == session_id)
        ).all()
        
        # Calculate totals
        total_items = sum(item.quantity for item in cart_items)
        total_amount = sum(item.quantity * float(item.product.price) for item in cart_items)
        
        return jsonify({
            'cart_items': [item.to_dict() for item in cart_items],
            'total_items': total_items,
            'total_amount': total_amount
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'product_id' not in data:
            return jsonify({'error': 'Product ID is required'}), 400
        
        product_id = data['product_id']
        quantity = data.get('quantity', 1)
        
        # Validate quantity
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        # Check if product exists and is active
        product = Product.query.filter_by(id=product_id, is_active=True).first()
        if not product:
            return jsonify({'error': 'Product not found'}'), 404
        
        # Check if product is in stock
        if product.stock_quantity < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Check if item already exists in cart
        existing_item = Cart.query.filter(
            ((Cart.user_id == user_id) | (Cart.session_id == session_id)) &
            (Cart.product_id == product_id)
        ).first()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                return jsonify({'error': 'Insufficient stock for requested quantity'}), 400
            
            existing_item.quantity = new_quantity
            db.session.commit()
            cart_item = existing_item
        else:
            # Add new item to cart
            cart_item = Cart(
                user_id=user_id,
                session_id=session_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            db.session.commit()
        
        return jsonify({
            'message': 'Item added to cart successfully',
            'cart_item': cart_item.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/update/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        data = request.get_json()
        quantity = data.get('quantity')
        
        if quantity is None or quantity <= 0:
            return jsonify({'error': 'Valid quantity is required'}), 400
        
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Find cart item
        cart_item = Cart.query.filter(
            Cart.id == item_id,
            (Cart.user_id == user_id) | (Cart.session_id == session_id)
        ).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        # Check stock availability
        if cart_item.product.stock_quantity < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Update quantity
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({
            'message': 'Cart item updated successfully',
            'cart_item': cart_item.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Remove item from cart"""
    try:
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Find cart item
        cart_item = Cart.query.filter(
            Cart.id == item_id,
            (Cart.user_id == user_id) | (Cart.session_id == session_id)
        ).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        # Remove item
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from cart successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/clear', methods=['DELETE'])
def clear_cart():
    """Clear all items from cart"""
    try:
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Delete all cart items for this user/session
        Cart.query.filter(
            (Cart.user_id == user_id) | (Cart.session_id == session_id)
        ).delete()
        
        db.session.commit()
        
        return jsonify({'message': 'Cart cleared successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/count', methods=['GET'])
def get_cart_count():
    """Get total number of items in cart"""
    try:
        session_id = get_or_create_session_id()
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Count cart items
        total_items = db.session.query(db.func.sum(Cart.quantity)).filter(
            (Cart.user_id == user_id) | (Cart.session_id == session_id)
        ).scalar() or 0
        
        return jsonify({'total_items': total_items})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
