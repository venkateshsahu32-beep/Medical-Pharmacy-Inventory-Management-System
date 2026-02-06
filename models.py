"""
Database Models for Smart Pharmacy Inventory Management System
Author: Senior Full Stack Python Developer
Purpose: SQLAlchemy ORM models for Medicine, Supplier, and Sales tables
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class Medicine(db.Model):
    """
    Medicine Model - Stores all medicine inventory information
    This is the core table for the pharmacy inventory system
    """
    __tablename__ = 'medicines'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Medicine Details
    name = db.Column(db.String(200), nullable=False, index=True)  # Indexed for faster search
    manufacturer = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)  # For seasonal filtering
    
    # Pricing and Stock
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    
    # Expiry Management
    expiry_date = db.Column(db.Date, nullable=False)
    
    # Seasonal Tag (Winter, Summer, Monsoon, Spring)
    seasonal_tag = db.Column(db.String(50), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with Sales
    sales = db.relationship('Sales', backref='medicine', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Medicine {self.name} - Stock: {self.stock_quantity}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'category': self.category,
            'price': self.price,
            'stock_quantity': self.stock_quantity,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d'),
            'seasonal_tag': self.seasonal_tag,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def days_until_expiry(self):
        """Calculate days remaining until expiry"""
        from datetime import date
        delta = self.expiry_date - date.today()
        return delta.days
    
    def is_low_stock(self, threshold=10):
        """Check if medicine is low on stock"""
        return self.stock_quantity < threshold
    
    def is_expiring_soon(self, days=30):
        """Check if medicine is expiring within specified days"""
        return 0 <= self.days_until_expiry() <= days


class Supplier(db.Model):
    """
    Supplier Model - Stores supplier/vendor information
    For future enhancement: linking medicines to suppliers
    """
    __tablename__ = 'suppliers'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Supplier Details
    name = db.Column(db.String(200), nullable=False, unique=True)
    contact = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'email': self.email,
            'address': self.address
        }


class Sales(db.Model):
    """
    Sales Model - Records all sales transactions
    Automatically deducts stock from Medicine table
    """
    __tablename__ = 'sales'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key to Medicine
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    
    # Sale Details
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Sale Date
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Sale #{self.id} - Medicine ID: {self.medicine_id} - Qty: {self.quantity_sold}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'medicine_name': self.medicine.name if self.medicine else 'Unknown',
            'quantity_sold': self.quantity_sold,
            'total_amount': self.total_amount,
            'sale_date': self.sale_date.strftime('%Y-%m-%d %H:%M:%S')
        }


def init_db(app):
    """
    Initialize database with Flask app
    Creates all tables if they don't exist
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("[OK] Database initialized successfully!")
