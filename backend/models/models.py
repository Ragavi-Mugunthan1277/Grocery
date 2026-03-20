"""
Database models for Grocery Store Application
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cart_items = relationship('Cart', back_populates='user', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='user')
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Category(db.Model):
    """Category model"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    products = relationship('Product', back_populates='category')
    
    def to_dict(self):
        """Convert category object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    """Product model"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    stock_quantity = Column(Integer, default=0)
    image_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship('Category', back_populates='products')
    cart_items = relationship('Cart', back_populates='product', cascade='all, delete-orphan')
    order_items = relationship('OrderItem', back_populates='product', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert product object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'stock_quantity': self.stock_quantity,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Cart(db.Model):
    """Cart model"""
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(String(255))
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='cart_items')
    product = relationship('Product', back_populates='cart_items')
    
    def to_dict(self):
        """Convert cart object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(String(255))
    order_number = Column(String(50), unique=True, nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), default='pending')
    shipping_address = Column(Text)
    payment_method = Column(String(50))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert order object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'order_number': self.order_number,
            'total_amount': float(self.total_amount),
            'status': self.status,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'order_items': [item.to_dict() for item in self.order_items]
        }

class OrderItem(db.Model):
    """Order item model"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items')
    
    def to_dict(self):
        """Convert order item object to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'price_per_unit': float(self.price_per_unit),
            'total_price': float(self.total_price)
        }
