from flask import Flask
from app.extensions import db, mail, jwt, cors
from app.config.settings import Config, db as db_config, email, app as app_config, upload, api, logging as logging_config, messages, features
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='public')
    
    # Load configuration
    app.config.from_object(Config)
    
    # Create necessary directories
    os.makedirs(upload['uploadDir'], exist_ok=True)
    os.makedirs(os.path.dirname(logging_config['file']), exist_ok=True)
    
    # Configure logging
    handler = RotatingFileHandler(
        logging_config['file'],
        maxBytes=10000000,
        backupCount=5
    )
    handler.setFormatter(logging.Formatter(logging_config['format']))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging_config['level'])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": api['cors']['origins'],
            "methods": api['cors']['methods'],
            "allow_headers": api['cors']['allow_headers']
        }
    })
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.product import product_bp
    from app.routes.cart import cart_bp
    from app.routes.order import order_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Error creating database tables: {str(e)}")
            raise
    
    return app 