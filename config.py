import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
db = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'primehomes')
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
    'from': os.getenv('EMAIL_FROM', 'noreply@primehomes.com')
}

# Application configuration
app = {
    'name': 'PrimeHomes',
    'version': '1.0.0',
    'debug': os.getenv('NODE_ENV', 'development') == 'development',
    'port': int(os.getenv('PORT', 3000)),
    'baseUrl': os.getenv('BASE_URL', 'http://localhost:3000'),
    'jwtSecret': os.getenv('JWT_SECRET', 'your-secret-key'),
    'jwtExpiration': os.getenv('JWT_EXPIRATION', '24h')
}

# File upload configuration
upload = {
    'uploadDir': os.path.join(os.path.dirname(__file__), 'public', 'uploads'),
    'maxSize': 5 * 1024 * 1024,  # 5MB
    'allowedExtensions': {'png', 'jpg', 'jpeg', 'gif'},
    'imageQuality': 85,
    'thumbnailSize': (300, 300)
}

# API configuration
api = {
    'rateLimit': {
        'enabled': True,
        'requests': 100,
        'window': 3600  # 1 hour
    },
    'cors': {
        'origins': ['*'],
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization']
    },
    'pagination': {
        'defaultLimit': 10,
        'maxLimit': 100
    }
}

# Create upload directory if it doesn't exist
os.makedirs(upload['uploadDir'], exist_ok=True)

# Logging configuration
logging = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.path.join(os.path.dirname(__file__), 'logs', 'app.log')
}

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(logging['file']), exist_ok=True)

# Cache configuration
cache = {
    'type': 'simple',  # simple, redis, or memcached
    'defaultTimeout': 300,  # 5 minutes
    'redis': {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': int(os.getenv('REDIS_PORT', 6379)),
        'password': os.getenv('REDIS_PASSWORD', None),
        'db': int(os.getenv('REDIS_DB', 0))
    }
}

# Security configuration
security = {
    'passwordMinLength': 8,
    'passwordMaxLength': 128,
    'passwordRequirements': {
        'uppercase': True,
        'lowercase': True,
        'numbers': True,
        'special': True
    },
    'sessionTimeout': 3600,  # 1 hour
    'maxLoginAttempts': 5,
    'lockoutDuration': 900  # 15 minutes
}

# Feature flags
features = {
    'enableRegistration': True,
    'enableSocialLogin': False,
    'enableTwoFactor': False,
    'enableEmailVerification': True,
    'enablePasswordReset': True,
    'enableFileUpload': True,
    'enableSearch': True,
    'enableNotifications': True
}

# Error messages
messages = {
    'errors': {
        'invalidCredentials': 'Invalid email or password',
        'emailExists': 'Email already registered',
        'invalidToken': 'Invalid or expired token',
        'unauthorized': 'Unauthorized access',
        'notFound': 'Resource not found',
        'serverError': 'Internal server error',
        'validationError': 'Validation error',
        'fileTooLarge': 'File size exceeds limit',
        'invalidFileType': 'Invalid file type',
        'uploadFailed': 'File upload failed'
    },
    'success': {
        'registration': 'Registration successful',
        'login': 'Login successful',
        'logout': 'Logout successful',
        'passwordReset': 'Password reset successful',
        'emailSent': 'Email sent successfully',
        'fileUploaded': 'File uploaded successfully',
        'profileUpdated': 'Profile updated successfully',
        'propertyAdded': 'Property added successfully',
        'propertyUpdated': 'Property updated successfully',
        'propertyDeleted': 'Property deleted successfully'
    }
} 