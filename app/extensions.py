from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()
cors = CORS() 