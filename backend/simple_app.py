"""
Simple Flask Application for Grocery Store
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import pymysql

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:3000', 'http://127.0.0.1:3000',
    'http://localhost:5500', 'http://127.0.0.1:5500',
    'http://localhost:8080', 'http://127.0.0.1:8080',
    'https://*.github.io',  # GitHub Pages
    '*'  # Allow all during development - restrict in production
])

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DB', 'grocery_store'),
    'charset': 'utf8mb4'
}

def get_db_connection():
    """Get database connection"""
    return pymysql.connect(**DB_CONFIG)

def query_db(query, params=None):
    """Execute query and return results"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = None
        return result
    finally:
        conn.close()

# Sample data (in case database is not set up) - Indian Market Products
SAMPLE_PRODUCTS = [
    {'id': 1, 'name': 'Onion', 'description': 'Fresh red onions 1kg', 'price': 30.00, 'category_id': 1, 'stock_quantity': 100, 'image_url': 'https://source.unsplash.com/400x400/?onion,vegetable'},
    {'id': 2, 'name': 'Potato', 'description': 'Fresh potatoes 1kg', 'price': 25.00, 'category_id': 1, 'stock_quantity': 150, 'image_url': 'https://source.unsplash.com/400x400/?potato,vegetable'},
    {'id': 3, 'name': 'Tomato', 'description': 'Ripe red tomatoes 1kg', 'price': 28.00, 'category_id': 1, 'stock_quantity': 80, 'image_url': 'https://source.unsplash.com/400x400/?tomato,vegetable'},
    {'id': 4, 'name': 'Apple', 'description': 'Fresh red apples 1kg', 'price': 150.00, 'category_id': 2, 'stock_quantity': 60, 'image_url': 'https://source.unsplash.com/400x400/?apple,fruit'},
    {'id': 5, 'name': 'Banana', 'description': 'Fresh yellow bananas 1 dozen', 'price': 50.00, 'category_id': 2, 'stock_quantity': 120, 'image_url': 'https://source.unsplash.com/400x400/?banana,fruit'},
    {'id': 6, 'name': 'Mango', 'description': 'Sweet ripe mangoes 1kg', 'price': 120.00, 'category_id': 2, 'stock_quantity': 40, 'image_url': 'https://source.unsplash.com/400x400/?mango,fruit'},
    {'id': 7, 'name': 'Basmati Rice', 'description': 'Premium long grain basmati rice 1kg', 'price': 90.00, 'category_id': 3, 'stock_quantity': 100, 'image_url': 'https://source.unsplash.com/400x400/?basmati,rice,grains'},
    {'id': 8, 'name': 'Wheat Atta', 'description': 'Whole wheat flour 1kg', 'price': 55.00, 'category_id': 3, 'stock_quantity': 80, 'image_url': 'https://source.unsplash.com/400x400/?wheat,flour,grains'},
    {'id': 9, 'name': 'Rava', 'description': 'Fine semolina 1kg', 'price': 45.00, 'category_id': 3, 'stock_quantity': 70, 'image_url': 'https://source.unsplash.com/400x400/?rava,semolina,grains'},
    {'id': 10, 'name': 'Toor Dal', 'description': 'Arhar dal toor 1kg', 'price': 140.00, 'category_id': 4, 'stock_quantity': 60, 'image_url': 'https://source.unsplash.com/400x400/?toor,dal,lentils'},
    {'id': 11, 'name': 'Moong Dal', 'description': 'Green gram dal 1kg', 'price': 130.00, 'category_id': 4, 'stock_quantity': 65, 'image_url': 'https://source.unsplash.com/400x400/?moong,dal,lentils'},
    {'id': 12, 'name': 'Chana Dal', 'description': 'Bengal gram dal 1kg', 'price': 110.00, 'category_id': 4, 'stock_quantity': 55, 'image_url': 'https://source.unsplash.com/400x400/?chana,dal,lentils'},
    {'id': 13, 'name': 'Turmeric Powder', 'description': 'Pure turmeric powder 200g', 'price': 40.00, 'category_id': 5, 'stock_quantity': 90, 'image_url': 'https://source.unsplash.com/400x400/?turmeric,spice'},
    {'id': 14, 'name': 'Red Chilli Powder', 'description': 'Kashmiri red chilli powder 200g', 'price': 60.00, 'category_id': 5, 'stock_quantity': 85, 'image_url': 'https://source.unsplash.com/400x400/?chilli,powder,spice'},
    {'id': 15, 'name': 'Garam Masala', 'description': 'Authentic garam masala 100g', 'price': 80.00, 'category_id': 5, 'stock_quantity': 75, 'image_url': 'https://source.unsplash.com/400x400/?garam,masala,spice'},
    {'id': 16, 'name': 'Mustard Oil', 'description': 'Pure mustard oil 1 litre', 'price': 120.00, 'category_id': 6, 'stock_quantity': 50, 'image_url': 'https://source.unsplash.com/400x400/?mustard,oil,cooking'},
    {'id': 17, 'name': 'Refined Sunflower Oil', 'description': 'Sunflower refined oil 1 litre', 'price': 110.00, 'category_id': 6, 'stock_quantity': 45, 'image_url': 'https://source.unsplash.com/400x400/?sunflower,oil,cooking'},
    {'id': 18, 'name': 'Pure Ghee', 'description': 'Desi ghee 500g', 'price': 280.00, 'category_id': 6, 'stock_quantity': 30, 'image_url': 'https://source.unsplash.com/400x400/?ghee,cooking'},
    {'id': 19, 'name': 'Milk', 'description': 'Fresh full cream milk 1 litre', 'price': 28.00, 'category_id': 7, 'stock_quantity': 50, 'image_url': 'https://source.unsplash.com/400x400/?milk,dairy'},
    {'id': 20, 'name': 'Curd', 'description': 'Fresh curd 500g', 'price': 35.00, 'category_id': 7, 'stock_quantity': 45, 'image_url': 'https://source.unsplash.com/400x400/?curd,dairy'},
    {'id': 21, 'name': 'Paneer', 'description': 'Fresh paneer 200g', 'price': 90.00, 'category_id': 7, 'stock_quantity': 30, 'image_url': 'https://source.unsplash.com/400x400/?paneer,dairy'},
]

SAMPLE_CATEGORIES = [
    {'id': 1, 'name': 'Vegetables', 'description': 'Fresh vegetables'},
    {'id': 2, 'name': 'Fruits', 'description': 'Fresh fruits'},
    {'id': 3, 'name': 'Rice & Grains', 'description': 'Rice, wheat and grains'},
    {'id': 4, 'name': 'Pulses & Dals', 'description': 'Various dals and pulses'},
    {'id': 5, 'name': 'Spices', 'description': 'Indian spices and masalas'},
    {'id': 6, 'name': 'Oils & Ghee', 'description': 'Cooking oils and ghee'},
    {'id': 7, 'name': 'Dairy Products', 'description': 'Milk, curd, paneer and more'},
]

# In-memory cart storage
cart_storage = {}
order_storage = {}

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Grocery Store API',
        'version': '1.0.0',
        'endpoints': {
            'products': '/api/products',
            'categories': '/api/products/categories',
            'health': '/api/health'
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Grocery Store API is running',
        'version': '1.0.0'
    })

@app.route('/api/products/categories')
def get_categories():
    """Get all categories"""
    try:
        # Try to get from database with correct column names
        query = "SELECT category_id as id, category_name as name, image_url FROM categories"
        categories = query_db(query)
        if categories:
            return jsonify(categories)
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback to sample data
        return jsonify(SAMPLE_CATEGORIES)

@app.route('/api/products')
def get_products():
    """Get all products with optional filtering and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        print(f"DEBUG: search='{search}', category_id={category_id}, min_price={min_price}, max_price={max_price}")
        
        # Try to get from database with correct column names
        query = "SELECT product_id as id, product_name as name, price, category_id, image_url FROM products"
        params = []
        
        if category_id:
            query += " WHERE category_id = %s"
            params.append(category_id)
        
        if search:
            if category_id:
                query += " AND (product_name LIKE %s)"
            else:
                query += " WHERE (product_name LIKE %s)"
            params.extend([f'%{search}%'])
            print(f"DEBUG: Search query={query}, params={params}")
        
        if min_price is not None:
            if category_id or search:
                query += " AND price >= %s"
            else:
                query += " WHERE price >= %s"
            params.append(min_price)
        
        if max_price is not None:
            if category_id or search or min_price is not None:
                query += " AND price <= %s"
            else:
                query += " WHERE price <= %s"
            params.append(max_price)
        
        query += " LIMIT %s OFFSET %s"
        offset = (page - 1) * per_page
        params.extend([per_page, offset])
        
        products = query_db(query, params)
        print(f"DEBUG: Found {len(products) if products else 0} products in database")
        
        if products:
            # Convert price to float for JSON serialization
            for product in products:
                product['price'] = float(product['price'])
                # Add description for frontend compatibility
                product['description'] = f"Fresh {product['name']}"
                product['stock_quantity'] = 100  # Default stock
            
            return jsonify({
                'products': products,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': len(products),
                    'pages': 1
                }
            })
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback to sample data
        filtered_products = SAMPLE_PRODUCTS
        print(f"DEBUG: Using sample data, total products={len(filtered_products)}")
        
        if category_id:
            filtered_products = [p for p in filtered_products if p['category_id'] == category_id]
            print(f"DEBUG: After category filter, products={len(filtered_products)}")
        
        if search:
            search_lower = search.lower()
            filtered_products = [p for p in filtered_products 
                            if search_lower in p['name'].lower() or search_lower in p['description'].lower()]
            print(f"DEBUG: Search term '{search_lower}' found {len(filtered_products)} products")
            for p in filtered_products:
                print(f"DEBUG: Matched product: {p['name']}")
        
        if min_price is not None:
            filtered_products = [p for p in filtered_products if p['price'] >= min_price]
        
        if max_price is not None:
            filtered_products = [p for p in filtered_products if p['price'] <= max_price]
        
        # Create local image URLs that will definitely work
        for product in filtered_products:
            product['image_url'] = f'http://localhost:5000/api/product-image/{product["id"]}'
        
        print(f"DEBUG: Final result: {len(filtered_products)} products")
        return jsonify({
            'products': filtered_products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(filtered_products),
                'pages': 1
            }
        })

@app.route('/api/product-image/<int:product_id>')
def get_product_image(product_id):
    """Serve local product images if available, otherwise fallback to Picsum"""
    product = next((p for p in SAMPLE_PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    
    # Try to serve local image first
    local_image_path = f"images/product_{product_id}.jpg"
    try:
        if os.path.exists(local_image_path):
            return send_from_directory('.', local_image_path)
    except:
        pass
    
    # Fallback to Picsum images if local image doesn't exist
    product_images = {
        # Vegetables
        1: "https://picsum.photos/seed/onion-vegetable/400/400.jpg",        # Onion
        2: "https://picsum.photos/seed/potato-vegetable/400/400.jpg",      # Potato
        3: "https://picsum.photos/seed/tomato-vegetable/400/400.jpg",       # Tomato

        # Fruits
        4: "https://picsum.photos/seed/apple-fruit/400/400.jpg",           # Apple
        5: "https://picsum.photos/seed/banana-fruit/400/400.jpg",          # Banana
        6: "https://picsum.photos/seed/mango-fruit/400/400.jpg",           # Mango

        # Rice & Grains
        7: "https://picsum.photos/seed/basmati-rice/400/400.jpg",        # Basmati Rice
        8: "https://picsum.photos/seed/wheat-atta/400/400.jpg",          # Wheat Atta
        9: "https://picsum.photos/seed/rava-semolina/400/400.jpg",        # Rava

        # Pulses & Dals
        10: "https://picsum.photos/seed/toor-dal/400/400.jpg",           # Toor Dal
        11: "https://picsum.photos/seed/moong-dal/400/400.jpg",           # Moong Dal
        12: "https://picsum.photos/seed/chana-dal/400/400.jpg",           # Chana Dal

        # Spices
        13: "https://picsum.photos/seed/turmeric-spice/400/400.jpg",       # Turmeric Powder
        14: "https://picsum.photos/seed/chilli-powder/400/400.jpg",       # Red Chilli Powder
        15: "https://picsum.photos/seed/garam-masala/400/400.jpg",       # Garam Masala

        # Oils & Ghee
        16: "https://picsum.photos/seed/mustard-oil/400/400.jpg",         # Mustard Oil
        17: "https://picsum.photos/seed/sunflower-oil/400/400.jpg",       # Sunflower Oil
        18: "https://picsum.photos/seed/pure-ghee/400/400.jpg",          # Pure Ghee

        # Dairy
        19: "https://picsum.photos/seed/fresh-milk/400/400.jpg",          # Milk
        20: "https://picsum.photos/seed/fresh-curd/400/400.jpg",          # Curd
        21: "https://picsum.photos/seed/fresh-paneer/400/400.jpg"        # Paneer
    }
    
    # Get the image URL for this product
    image_url = product_images.get(product_id, f"https://picsum.photos/seed/{product['name'].replace(' ', '-')}/400/400.jpg")
    
    # Redirect to the actual image
    from flask import redirect
    return redirect(image_url)

@app.route('/images/<filename>')
def serve_image(filename):
    """Serve local images from the images folder"""
    return send_from_directory('images', filename)

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    """Get a single product by ID"""
    try:
        query = "SELECT * FROM products WHERE id = %s AND is_active = TRUE"
        products = query_db(query, (product_id,))
        
        if products:
            product = products[0]
            product['price'] = float(product['price'])
            return jsonify(product)
        else:
            # Fallback to sample data
            product = next((p for p in SAMPLE_PRODUCTS if p['id'] == product_id), None)
            if product:
                return jsonify(product)
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback to sample data
        product = next((p for p in SAMPLE_PRODUCTS if p['id'] == product_id), None)
        if product:
            return jsonify(product)
        return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products/featured')
def get_featured_products():
    """Get featured products"""
    try:
        query = "SELECT * FROM products WHERE is_active = TRUE AND stock_quantity > 20 ORDER BY created_at DESC LIMIT 8"
        products = query_db(query)
        
        if products:
            for product in products:
                product['price'] = float(product['price'])
            return jsonify(products)
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback to sample data
        featured = [p for p in SAMPLE_PRODUCTS if p['stock_quantity'] > 20]
        return jsonify(featured[:8])

@app.route('/api/test/session')
def test_session():
    """Test session management"""
    session_id = request.headers.get('X-Session-ID', 'default-session')
    return jsonify({
        'session_id': session_id,
        'available_sessions': list(cart_storage.keys()),
        'cart_storage': cart_storage
    })

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get cart items"""
    session_id = request.headers.get('X-Session-ID', 'default-session')
    print(f"DEBUG: Get cart for session ID: {session_id}")
    print(f"DEBUG: Available sessions: {list(cart_storage.keys())}")
    
    cart_items = cart_storage.get(session_id, [])
    print(f"DEBUG: Cart items for session {session_id}: {cart_items}")
    
    total_items = sum(item['quantity'] for item in cart_items)
    total_amount = sum(item['quantity'] * item['product']['price'] for item in cart_items)
    
    return jsonify({
        'cart_items': cart_items,
        'total_items': total_items,
        'total_amount': total_amount
    })

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    print(f"DEBUG: Cart add request data: {data}")
    
    if not data or 'product_id' not in data:
        return jsonify({'error': 'Product ID is required'}), 400
    
    product_id = data['product_id']
    quantity = data.get('quantity', 1)
    
    # Find product
    product = next((p for p in SAMPLE_PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    session_id = request.headers.get('X-Session-ID', 'default-session')
    print(f"DEBUG: Session ID: {session_id}")
    
    if session_id not in cart_storage:
        cart_storage[session_id] = []
        print(f"DEBUG: Created new cart for session {session_id}")
    
    print(f"DEBUG: Current cart items: {cart_storage[session_id]}")
    
    # Check if item already in cart
    existing_item = next((item for item in cart_storage[session_id] if item['product_id'] == product_id), None)
    
    if existing_item:
        existing_item['quantity'] += quantity
        print(f"DEBUG: Updated existing item quantity to {existing_item['quantity']}")
    else:
        cart_storage[session_id].append({
            'id': len(cart_storage[session_id]) + 1,
            'product_id': product_id,
            'product': product,
            'quantity': quantity,
            'created_at': datetime.utcnow().isoformat()
        })
        print(f"DEBUG: Added new item to cart")
    
    print(f"DEBUG: Final cart: {cart_storage[session_id]}")
    
    return jsonify({'message': 'Item added to cart successfully'})

@app.route('/api/cart/count', methods=['GET'])
def get_cart_count():
    """Get cart item count"""
    session_id = request.headers.get('X-Session-ID', 'default-session')
    print(f"DEBUG: Get cart count for session ID: {session_id}")
    
    cart_items = cart_storage.get(session_id, [])
    total_items = sum(item['quantity'] for item in cart_items)
    
    print(f"DEBUG: Cart count for session {session_id}: {total_items}")
    
    return jsonify({
        'total_items': total_items
    })

@app.route('/api/cart/update/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    """Update cart item quantity"""
    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Quantity is required'}), 400

    quantity = data['quantity']
    session_id = request.headers.get('X-Session-ID', 'default-session')
    cart_items = cart_storage.get(session_id, [])

    item = next((i for i in cart_items if i['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    if quantity < 1:
        cart_items.remove(item)
    else:
        item['quantity'] = quantity

    cart_storage[session_id] = cart_items
    return jsonify({'message': 'Cart updated successfully'})


@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Remove item from cart"""
    session_id = request.headers.get('X-Session-ID', 'default-session')
    cart_items = cart_storage.get(session_id, [])

    item = next((i for i in cart_items if i['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    cart_items.remove(item)
    cart_storage[session_id] = cart_items
    return jsonify({'message': 'Item removed from cart'})


@app.route('/api/cart/clear', methods=['DELETE'])
def clear_cart():
    """Clear all items from cart"""
    session_id = request.headers.get('X-Session-ID', 'default-session')
    cart_storage[session_id] = []
    return jsonify({'message': 'Cart cleared successfully'})


@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Order data is required'}), 400
    
    shipping_address = data.get('shipping_address')
    payment_method = data.get('payment_method')
    
    if not shipping_address or not payment_method:
        return jsonify({'error': 'Shipping address and payment method are required'}), 400
    
    session_id = request.headers.get('X-Session-ID', 'default-session')
    cart_items = cart_storage.get(session_id, [])
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    total_amount = sum(item['quantity'] * item['product']['price'] for item in cart_items)
    
    order = {
        'id': len(order_storage) + 1,
        'order_number': f"ORD-{datetime.now().strftime('%Y%m%d')}-{len(order_storage) + 1:04d}",
        'total_amount': total_amount,
        'status': 'pending',
        'shipping_address': shipping_address,
        'payment_method': payment_method,
        'notes': data.get('notes', ''),
        'created_at': datetime.utcnow().isoformat(),
        'order_items': [
            {
                'id': item['id'],
                'product_id': item['product_id'],
                'product': item['product'],
                'quantity': item['quantity'],
                'price_per_unit': item['product']['price'],
                'total_price': item['quantity'] * item['product']['price']
            }
            for item in cart_items
        ]
    }
    
    order_storage[len(order_storage) + 1] = order
    cart_storage[session_id] = []  # Clear cart
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order
    })

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by ID"""
    order = order_storage.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')
