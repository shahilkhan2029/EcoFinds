import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db = {
    'database': os.getenv('DB_NAME', 'ecofinds')
}

# Email configuration
email = {
    'host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
    'port': int(os.getenv('SMTP_PORT', 587)),
    'secure': os.getenv('SMTP_SECURE', 'false').lower() == 'true',
    'auth': {
        'user': os.getenv('SMTP_USER', ''),
        'pass': os.getenv('SMTP_PASS', '')
    },
    'from': os.getenv('EMAIL_FROM', 'noreply@ecofinds.com')
}

# Application configuration
app = {
    'debug': os.getenv('FLASK_ENV', 'development') == 'development',
    'port': int(os.getenv('PORT', 3000)),
    'baseUrl': os.getenv('BASE_URL', 'http://localhost:3000'),
    'jwtSecret': os.getenv('JWT_SECRET', 'your-secret-key'),
    'jwtExpiration': os.getenv('JWT_EXPIRATION', '24h')
}

# Upload configuration
upload = {
    'uploadDir': 'uploads',
    'maxSize': 16 * 1024 * 1024,
    'allowedExtensions': {'png', 'jpg', 'jpeg', 'gif'}
}

# API configuration
api = {
    'cors': {
        'origins': ['*'],
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization']
    }
}

# Logging configuration
logging = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/app.log'
}

# Feature flags
features = {
    'enableRegistration': True,
    'enableFileUpload': True,
    'enableSearch': True,
    'enablePropertyCreation': True,
    'enableAgentRegistration': True,
    'enableContactForm': True,
    'enableContactViewing': True
}

# Messages
messages = {
    'success': {
        'registration': 'Registration successful! Welcome to EcoFinds.',
        'emailSent': 'Your message has been sent successfully.',
        'deletion': 'Item deleted successfully.'
    },
    'errors': {
        'unauthorized': 'You are not authorized to perform this action.',
        'emailExists': 'An account with this email already exists.',
        'invalidCredentials': 'Invalid email or password.',
        'uploadFailed': 'File upload failed.',
        'invalidFileType': 'Invalid file type. Allowed types: PNG, JPG, JPEG, GIF.'
    }
}

# Create necessary directories
os.makedirs(upload['uploadDir'], exist_ok=True)
os.makedirs(os.path.dirname(logging['file']), exist_ok=True)

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db['database']}.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = app['jwtSecret']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(app['jwtExpiration'].split('h')[0]))
    
    # Mail
    MAIL_SERVER = email['host']
    MAIL_PORT = email['port']
    MAIL_USE_TLS = email['secure']
    MAIL_USERNAME = email['auth']['user']
    MAIL_PASSWORD = email['auth']['pass']
    MAIL_DEFAULT_SENDER = email['from']
    
    # Upload
    UPLOAD_FOLDER = upload['uploadDir']
    MAX_CONTENT_LENGTH = upload['maxSize']
    ALLOWED_EXTENSIONS = upload['allowedExtensions']
    
    # Features
    FEATURES = features
    
    # Messages
    MESSAGES = messages
    
    # CORS
    CORS = api['cors']

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}[os.getenv('FLASK_ENV', 'development')] 