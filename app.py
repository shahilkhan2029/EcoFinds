import os
from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Message
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import json
import logging
from logging.handlers import RotatingFileHandler
from config import db as db_config, email, app as app_config, upload, api, logging as logging_config, messages, features
from extensions import db, mail, jwt, cors
from models import User, Property, Agent, ContactMessage
from app.routes.auth import auth_bp
from app.routes.property import property_bp
from app.routes.contact import contact_bp
from app.routes.agent import agent_bp
from app.config.settings import config

def create_app():
    app = Flask(__name__, static_folder='public')
    os.makedirs(upload['uploadDir'], exist_ok=True)
    os.makedirs(os.path.dirname(logging_config['file']), exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_config['database']}.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = app_config['jwtSecret']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['MAX_CONTENT_LENGTH'] = upload['maxSize']
    
    app.config['MAIL_SERVER'] = email['host']
    app.config['MAIL_PORT'] = email['port']
    app.config['MAIL_USE_TLS'] = not email['secure']
    app.config['MAIL_USERNAME'] = email['auth']['user']
    app.config['MAIL_PASSWORD'] = email['auth']['pass']
    app.config['MAIL_DEFAULT_SENDER'] = email['from']
    
    handler = RotatingFileHandler(
        logging_config['file'],
        maxBytes=10000000,
        backupCount=5
    )
    handler.setFormatter(logging.Formatter(logging_config['format']))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging_config['level'])
    
    db.init_app(app)
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
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(property_bp, url_prefix='/api')
    app.register_blueprint(contact_bp, url_prefix='/api')
    app.register_blueprint(agent_bp, url_prefix='/api')
    
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Error creating database tables: {str(e)}")
            raise
    
    @app.route('/')
    def index():
        return send_from_directory('public', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('public', path)
    
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        if not features['enableRegistration']:
            return jsonify({'error': messages['errors']['unauthorized']}), 403
    
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': messages['errors']['emailExists']}), 400
        
        user = User(
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='user'
        )
        
        db.session.add(user)
        db.session.commit()
        
        msg = Message(
            'Welcome to PrimeHomes',
            recipients=[user.email]
        )
        msg.body = f"Welcome to PrimeHomes! We're excited to have you on board."
        mail.send(msg)
        
        return jsonify({'message': messages['success']['registration']}), 201
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        
        return jsonify({'error': messages['errors']['invalidCredentials']}), 401
    
    @app.route('/api/properties', methods=['GET'])
    def get_properties():
        filters = request.args.to_dict()
        properties = Property.query.filter_by(**filters).all()
        return jsonify([p.to_dict() for p in properties])
    
    @app.route('/api/properties/<int:id>', methods=['GET'])
    def get_property(id):
        property = Property.query.get_or_404(id)
        return jsonify(property.to_dict())
    
    @app.route('/api/properties', methods=['POST'])
    @jwt_required()
    def create_property():
        if not features['enableFileUpload']:
            return jsonify({'error': messages['errors']['unauthorized']}), 403
    
        data = request.form.to_dict()
        images = request.files.getlist('images')
        
        image_paths = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(upload['uploadDir'], filename)
                image.save(image_path)
                image_paths.append(image_path)
        
        property = Property(
            title=data['title'],
            type=data['type'],
            price=float(data['price']),
            location=data['location'],
            description=data['description'],
            bedrooms=int(data['bedrooms']),
            bathrooms=int(data['bathrooms']),
            area=float(data['area']),
            images=json.dumps(image_paths),
            agent_id=get_jwt_identity()
        )
        
        db.session.add(property)
        db.session.commit()
        
        return jsonify(property.to_dict()), 201
    
    @app.route('/api/properties/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_property(id):
        property = Property.query.get_or_404(id)
        if property.agent_id != get_jwt_identity():
            return jsonify({'error': messages['errors']['unauthorized']}), 403
        
        data = request.get_json()
        for key, value in data.items():
            setattr(property, key, value)
        
        db.session.commit()
        return jsonify(property.to_dict())
    
    @app.route('/api/properties/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_property(id):
        property = Property.query.get_or_404(id)
        if property.agent_id != get_jwt_identity():
            return jsonify({'error': messages['errors']['unauthorized']}), 403
        
        for image_path in json.loads(property.images):
            try:
                os.remove(image_path)
            except:
                pass
        
        db.session.delete(property)
        db.session.commit()
        return '', 204
    
    @app.route('/api/agents', methods=['GET'])
    def get_agents():
        agents = Agent.query.all()
        return jsonify([a.to_dict() for a in agents])
    
    @app.route('/api/agents/<int:id>', methods=['GET'])
    def get_agent(id):
        agent = Agent.query.get_or_404(id)
        return jsonify(agent.to_dict())
    
    @app.route('/api/agents', methods=['POST'])
    @jwt_required()
    def create_agent():
        data = request.form.to_dict()
        profile_image = request.files.get('profile_image')
        
        if profile_image and allowed_file(profile_image.filename):
            filename = secure_filename(profile_image.filename)
            image_path = os.path.join(upload['uploadDir'], filename)
            profile_image.save(image_path)
        else:
            image_path = None
        
        agent = Agent(
            user_id=get_jwt_identity(),
            full_name=data['full_name'],
            title=data['title'],
            phone=data['phone'],
            bio=data['bio'],
            specialization=data['specialization'],
            languages=data['languages'],
            profile_image=image_path
        )
        
        db.session.add(agent)
        db.session.commit()
        
        return jsonify(agent.to_dict()), 201
    
    @app.route('/api/contact', methods=['POST'])
    def submit_contact():
        data = request.get_json()
        
        message = ContactMessage(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            subject=data['subject'],
            message=data['message']
        )
        
        db.session.add(message)
        db.session.commit()
        
        msg = Message(
            'New Contact Form Submission',
            recipients=[email['from']]
        )
        msg.body = f"""
        New contact form submission:
        Name: {data['name']}
        Email: {data['email']}
        Phone: {data['phone']}
        Subject: {data['subject']}
        Message: {data['message']}
        """
        mail.send(msg)
        
        return jsonify({'message': messages['success']['emailSent']}), 201
    
    @app.route('/api/search/properties', methods=['GET'])
    def search_properties():
        if not features['enableSearch']:
            return jsonify({'error': messages['errors']['unauthorized']}), 403
    
        query = request.args.get('q', '')
        properties = Property.query.filter(
            (Property.title.ilike(f'%{query}%')) |
            (Property.location.ilike(f'%{query}%')) |
            (Property.description.ilike(f'%{query}%'))
        ).all()
        return jsonify([p.to_dict() for p in properties])
    
    @app.route('/api/search/agents', methods=['GET'])
    def search_agents():
        if not features['enableSearch']:
            return jsonify({'error': messages['errors']['unauthorized']}), 403
    
        query = request.args.get('q', '')
        agents = Agent.query.filter(
            (Agent.full_name.ilike(f'%{query}%')) |
            (Agent.specialization.ilike(f'%{query}%'))
        ).all()
        return jsonify([a.to_dict() for a in agents])
    
    @app.route('/api/upload', methods=['POST'])
    @jwt_required()
    def upload_file():
        if not features['enableFileUpload']:
            return jsonify({'error': messages['errors']['unauthorized']}), 403
    
        if 'file' not in request.files:
            return jsonify({'error': messages['errors']['uploadFailed']}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': messages['errors']['uploadFailed']}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload['uploadDir'], filename)
            file.save(file_path)
            return jsonify({'file_path': file_path}), 201
        
        return jsonify({'error': messages['errors']['invalidFileType']}), 400
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in upload['allowedExtensions']
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=app_config['debug'],
        port=app_config['port']
    ) 