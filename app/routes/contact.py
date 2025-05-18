from flask import Blueprint, request, jsonify
from app.models.contact import ContactMessage
from app.extensions import db, mail
from flask_mail import Message
from app.config.settings import messages, features

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['POST'])
def create_contact():
    if not features['enableContactForm']:
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    data = request.get_json()
    contact = ContactMessage(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        subject=data['subject'],
        message=data['message']
    )
    
    db.session.add(contact)
    db.session.commit()
    
    # Send notification email
    msg = Message(
        'New Contact Message',
        recipients=[features['adminEmail']]
    )
    msg.body = f"""
    New contact message received:
    
    From: {contact.name}
    Email: {contact.email}
    Phone: {contact.phone}
    Subject: {contact.subject}
    Message: {contact.message}
    """
    mail.send(msg)
    
    return jsonify(contact.to_dict()), 201

@contact_bp.route('/contact', methods=['GET'])
def get_contacts():
    if not features['enableContactViewing']:
        return jsonify({'error': messages['errors']['unauthorized']}), 403

    contacts = ContactMessage.query.all()
    return jsonify([c.to_dict() for c in contacts]), 200 