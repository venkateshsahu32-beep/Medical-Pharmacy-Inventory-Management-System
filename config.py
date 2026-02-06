"""
Configuration settings for the Smart Pharmacy Inventory Management System
Author: Senior Full Stack Python Developer
Purpose: Centralized configuration for database, app settings, and constants
"""

import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Main configuration class for Flask application"""
    
    # Flask secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pharmacy-secret-key-2026'
    
    # SQLite database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'pharmacy.db')
    
    # Disable SQLAlchemy modification tracking (saves resources)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CSV dataset path for seeding
    CSV_DATASET_PATH = os.path.join(BASE_DIR, 'medicines_dataset.csv')
    
    # Business logic constants
    LOW_STOCK_THRESHOLD = 10  # Alert when stock falls below this
    EXPIRY_WARNING_DAYS = 30  # Alert when medicine expires within this many days
    
    # Seasonal mapping for intelligent recommendations
    # Maps medicine categories to seasons when they're most needed
    SEASONAL_CATEGORIES = {
        'Winter': ['Cough Syrup', 'Cold Relief', 'Throat Lozenges', 'Decongestant', 'Vitamin C'],
        'Monsoon': ['Antifungal', 'Antibiotic', 'Antiseptic', 'Anti-diarrheal', 'Mosquito Repellent'],
        'Summer': ['Antacid', 'Oral Rehydration', 'Sunscreen', 'Antihistamine', 'Heat Rash Cream'],
        'Spring': ['Antihistamine', 'Allergy Relief', 'Eye Drops', 'Nasal Spray']
    }
    
    # Month to season mapping (for India - adjust based on region)
    MONTH_TO_SEASON = {
        1: 'Winter',   # January
        2: 'Winter',   # February
        3: 'Spring',   # March
        4: 'Spring',   # April
        5: 'Summer',   # May
        6: 'Summer',   # June
        7: 'Monsoon',  # July
        8: 'Monsoon',  # August
        9: 'Monsoon',  # September
        10: 'Spring',  # October
        11: 'Winter',  # November
        12: 'Winter'   # December
    }
