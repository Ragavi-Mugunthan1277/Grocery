"""
Helper functions for Grocery Store Application
"""
from flask import session
import uuid

def get_or_create_session_id():
    """Get existing session ID or create a new one"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    import re
    # Remove all non-digit characters
    cleaned = re.sub(r'\D', '', phone)
    # Check if it's 10 digits (US format) or has country code
    return len(cleaned) == 10 or (len(cleaned) > 10 and len(cleaned) <= 15)

def format_currency(amount):
    """Format amount as currency"""
    return f"₹{amount:.2f}"

def generate_order_number():
    """Generate unique order number"""
    from datetime import datetime
    import uuid
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"ORD-{timestamp}-{unique_id}"

def paginate_query(query, page, per_page):
    """Paginate a SQLAlchemy query"""
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def calculate_cart_total(cart_items):
    """Calculate total amount for cart items"""
    total = 0
    for item in cart_items:
        total += item.quantity * float(item.product.price)
    return total

def check_stock_availability(product_id, requested_quantity):
    """Check if product has sufficient stock"""
    from models.models import Product
    
    product = Product.query.get(product_id)
    if not product:
        return False, "Product not found"
    
    if product.stock_quantity < requested_quantity:
        return False, f"Insufficient stock. Available: {product.stock_quantity}, Requested: {requested_quantity}"
    
    return True, "Stock available"

def update_product_stock(product_id, quantity_change):
    """Update product stock quantity"""
    from models.models import Product
    
    product = Product.query.get(product_id)
    if product:
        product.stock_quantity += quantity_change
        if product.stock_quantity < 0:
            product.stock_quantity = 0
        return True
    return False
