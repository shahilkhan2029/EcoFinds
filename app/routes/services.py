from flask import Blueprint, jsonify, request, render_template
from app.models.property import Property
from app.extensions import db
from app.config.settings import messages
from datetime import datetime

services_bp = Blueprint('services', __name__)

@services_bp.route('/services')
def services():
    return render_template('services/index.html')

@services_bp.route('/services/property-valuation', methods=['GET', 'POST'])
def property_valuation():
    if request.method == 'POST':
        data = request.get_json()
        
        # Calculate property value based on various factors
        base_value = float(data.get('area', 0)) * 1000  # Base value per square foot
        location_multiplier = {
            'urban': 1.5,
            'suburban': 1.2,
            'rural': 0.8
        }.get(data.get('location_type', 'suburban'), 1.0)
        
        condition_multiplier = {
            'excellent': 1.3,
            'good': 1.1,
            'fair': 0.9,
            'poor': 0.7
        }.get(data.get('condition', 'good'), 1.0)
        
        amenities_bonus = sum([
            50000 if amenity in data.get('amenities', []) else 0
            for amenity in ['pool', 'garden', 'garage', 'security']
        ])
        
        estimated_value = (base_value * location_multiplier * condition_multiplier) + amenities_bonus
        
        return jsonify({
            'estimated_value': estimated_value,
            'valuation_date': datetime.utcnow().isoformat(),
            'factors_considered': {
                'base_value': base_value,
                'location_multiplier': location_multiplier,
                'condition_multiplier': condition_multiplier,
                'amenities_bonus': amenities_bonus
            }
        })
    
    return render_template('services/property-valuation.html')

@services_bp.route('/services/rent-property', methods=['GET', 'POST'])
def rent_property():
    if request.method == 'POST':
        data = request.form.to_dict()
        images = request.files.getlist('images')
        
        # Handle image uploads
        image_paths = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_paths.append(image_path)
        
        # Create new property listing
        property = Property(
            title=data['title'],
            type='rent',
            price=float(data['price']),
            location=data['location'],
            description=data['description'],
            bedrooms=int(data['bedrooms']),
            bathrooms=int(data['bathrooms']),
            area=float(data['area']),
            images=json.dumps(image_paths),
            user_id=get_jwt_identity()
        )
        
        db.session.add(property)
        db.session.commit()
        
        return jsonify(property.to_dict()), 201
    
    return render_template('services/rent-property.html')

@services_bp.route('/services/sell-property', methods=['GET', 'POST'])
def sell_property():
    if request.method == 'POST':
        data = request.form.to_dict()
        images = request.files.getlist('images')
        
        # Handle image uploads
        image_paths = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_paths.append(image_path)
        
        # Create new property listing
        property = Property(
            title=data['title'],
            type='sale',
            price=float(data['price']),
            location=data['location'],
            description=data['description'],
            bedrooms=int(data['bedrooms']),
            bathrooms=int(data['bathrooms']),
            area=float(data['area']),
            images=json.dumps(image_paths),
            user_id=get_jwt_identity()
        )
        
        db.session.add(property)
        db.session.commit()
        
        return jsonify(property.to_dict()), 201
    
    return render_template('services/sell-property.html')

@services_bp.route('/services/home-loans', methods=['GET', 'POST'])
def home_loans():
    if request.method == 'POST':
        data = request.get_json()
        
        # Calculate loan details
        loan_amount = float(data.get('property_value', 0)) - float(data.get('down_payment', 0))
        interest_rate = float(data.get('interest_rate', 5.0)) / 100
        loan_term = int(data.get('loan_term', 30))
        
        # Calculate monthly payment using the formula: P = L[c(1 + c)^n]/[(1 + c)^n - 1]
        monthly_rate = interest_rate / 12
        num_payments = loan_term * 12
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        
        return jsonify({
            'loan_amount': loan_amount,
            'monthly_payment': monthly_payment,
            'total_payment': monthly_payment * num_payments,
            'total_interest': (monthly_payment * num_payments) - loan_amount,
            'amortization_schedule': generate_amortization_schedule(loan_amount, interest_rate, loan_term)
        })
    
    return render_template('services/home-loans.html')

@services_bp.route('/services/legal-services', methods=['GET', 'POST'])
def legal_services():
    if request.method == 'POST':
        data = request.get_json()
        
        # Process legal service request
        service_type = data.get('service_type')
        property_id = data.get('property_id')
        
        # Create legal service record
        legal_service = LegalService(
            service_type=service_type,
            property_id=property_id,
            user_id=get_jwt_identity(),
            status='pending',
            details=data.get('details', '')
        )
        
        db.session.add(legal_service)
        db.session.commit()
        
        # Send notification email
        msg = Message(
            'New Legal Service Request',
            recipients=[current_app.config['MAIL_DEFAULT_SENDER']]
        )
        msg.body = f"""
        New legal service request:
        Service Type: {service_type}
        Property ID: {property_id}
        User ID: {get_jwt_identity()}
        Details: {data.get('details', '')}
        """
        mail.send(msg)
        
        return jsonify(legal_service.to_dict()), 201
    
    return render_template('services/legal-services.html')

def generate_amortization_schedule(loan_amount, interest_rate, loan_term):
    monthly_rate = interest_rate / 12
    num_payments = loan_term * 12
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    
    schedule = []
    balance = loan_amount
    
    for payment in range(1, num_payments + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        
        schedule.append({
            'payment_number': payment,
            'payment_amount': monthly_payment,
            'principal_payment': principal_payment,
            'interest_payment': interest_payment,
            'remaining_balance': balance
        })
    
    return schedule 