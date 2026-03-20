"""
Run script for Grocery Store Flask Application
"""
import os
from app import create_app

# Set environment
config_name = os.environ.get('FLASK_ENV', 'development')

# Create app
app = create_app(config_name)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
