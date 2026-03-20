"""
Main Flask Application for Grocery Store
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config.config import config
from models.models import db, Product, Category
from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp
import os

def create_app(config_name='default'):
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Grocery Store API is running',
            'version': '1.0.0'
        })
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'Grocery Store API',
            'version': '1.0.0',
            'endpoints': {
                'products': '/api/products',
                'cart': '/api/cart',
                'orders': '/api/orders',
                'health': '/api/health'
            }
        })
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    # Get configuration from environment variable
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(config_name)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
