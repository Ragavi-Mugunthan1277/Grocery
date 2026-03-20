"""
Product routes for Grocery Store Application
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import or_

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

@products_bp.route('/', methods=['GET'])
def get_products():
    """Get all products with optional filtering and pagination"""
    try:
        from models.models import db, Product, Category
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Build query
        query = Product.query.filter_by(is_active=True)
        
        # Apply filters
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        # Apply pagination
        products = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': products.total,
                'pages': products.pages,
                'has_next': products.has_next,
                'has_prev': products.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        product = Product.query.filter_by(id=product_id, is_active=True).first()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify(product.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/featured', methods=['GET'])
def get_featured_products():
    """Get featured products (products with high stock or recent additions)"""
    try:
        limit = request.args.get('limit', 8, type=int)
        
        # Get products with high stock or recent additions
        featured_products = Product.query.filter_by(is_active=True)\
            .filter(Product.stock_quantity > 20)\
            .order_by(Product.created_at.desc())\
            .limit(limit)\
            .all()
        
        return jsonify([product.to_dict() for product in featured_products])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/category/<int:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    """Get products by category"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Check if category exists
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Get products in this category
        products = Product.query.filter_by(category_id=category_id, is_active=True)\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'category': category.to_dict(),
            'products': [product.to_dict() for product in products.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': products.total,
                'pages': products.pages,
                'has_next': products.has_next,
                'has_prev': products.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
