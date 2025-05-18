from datetime import datetime
from app.extensions import db

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.Text)
    specialization = db.Column(db.String(100))
    languages = db.Column(db.String(200))
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'title': self.title,
            'phone': self.phone,
            'bio': self.bio,
            'specialization': self.specialization,
            'languages': self.languages,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 