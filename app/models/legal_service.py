from datetime import datetime
from app.extensions import db

class LegalService(db.Model):
    __tablename__ = 'legal_services'
    
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property', backref='legal_services')
    user = db.relationship('User', backref='legal_services')
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_type': self.service_type,
            'property_id': self.property_id,
            'user_id': self.user_id,
            'status': self.status,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 