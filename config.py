"""
Configuration file for Restaurant Billing & POS System
SQLite Database Configuration
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # SQLite Database Configuration
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'restaurant_pos.db'
    DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)
    
    # Build SQLAlchemy connection string for SQLite
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False},  # SQLite requires this for multithreading
        'echo': False  # Set to True for SQL query logging
    }
    
    # Application Settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # OTP Configuration
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    
    # SMS Gateway Configuration (Optional)
    # Set these environment variables to enable SMS:
    # TWILIO_ACCOUNT_SID=your_account_sid
    # TWILIO_AUTH_TOKEN=your_auth_token
    # TWILIO_PHONE_NUMBER=your_twilio_phone_number
    # If not set, OTP will be displayed on screen (development mode)
    
    # Business Rules
    DEFAULT_GST_PERCENTAGE = 5.00
    DEFAULT_TABLE_CAPACITY = 4
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # QR Code Settings
    QR_CODE_SIZE = 10
    QR_CODE_BORDER = 4

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_ECHO = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

