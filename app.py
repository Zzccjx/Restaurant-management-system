"""
Flask Application Entry Point
Restaurant Billing & POS System
"""
from flask import Flask
from flask_session import Session
from config import config
from models import db
# Import all models to ensure they're registered with SQLAlchemy
# Note: Bill model exists in database but we use Order as single source of truth
from models import (
    Membership, User, Admin, RestaurantTable, TableReservation,
    MenuItem, MenuPhoto, Order, OrderItem,
    Offer, OrderOffer, Feedback
)
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass

# Initialize Flask extensions
session = Session()

def create_app(config_name=None):
    """
    Application factory pattern
    Creates and configures Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    session.init_app(app)
    
    # Initialize database - create all tables if they don't exist
    with app.app_context():
        try:
            # Import all models to ensure they're registered
            # Note: Bill model exists in database but we use Order as single source of truth
            from models import (
                Membership, User, Admin, Restaurant, RestaurantTable, TableReservation,
                MenuItem, MenuPhoto, Order, OrderItem,
                Offer, OrderOffer, Feedback, CustomerFeedback, HomeSlide
            )
            db.create_all()
            print("[OK] Database tables initialized successfully")
        except Exception as e:
            print(f"[WARNING] Could not initialize database tables: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'photos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'qr_codes'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'feedback'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'restaurants'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'foods'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'slider'), exist_ok=True)
    
    # Create static directories for web access
    static_upload = os.path.join('static', 'photos')
    os.makedirs(static_upload, exist_ok=True)
    static_upload = os.path.join('static', 'qr_codes')
    os.makedirs(static_upload, exist_ok=True)
    static_upload = os.path.join('static', 'feedback')
    os.makedirs(static_upload, exist_ok=True)
    static_upload = os.path.join('static', 'restaurants')
    os.makedirs(static_upload, exist_ok=True)
    static_upload = os.path.join('static', 'foods')
    os.makedirs(static_upload, exist_ok=True)
    static_upload = os.path.join('static', 'slider')
    os.makedirs(static_upload, exist_ok=True)
    
    # Route to serve uploaded files
    from flask import send_from_directory
    @app.route('/static/<path:folder>/<path:filename>')
    def serve_uploaded_file(folder, filename):
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], folder)
        return send_from_directory(upload_folder, filename)
    
    # Register blueprints
    from routes.main import main_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

