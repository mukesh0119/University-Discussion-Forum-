# application/models.py
from . import db
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(255), unique=False, nullable=True)
    uni_number = db.Column(db.String(255), unique=False, nullable=True)
    user_role = db.Column(db.String(255), unique=False, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def encode_api_key(self):
        self.api_key = sha256_crypt.hash(self.email + str(datetime.utcnow))

    def encode_password(self):
        self.password = sha256_crypt.hash(self.password)
        
    def __repr__(self):
        return '<User %r>' % (self.id)

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': str(self.first_name + ' ' +self.last_name),
            'email': self.email,
            'phone_number': self.phone_number,
            'uni_number': self.uni_number,
            'user_role': self.user_role,
            'id': self.id,
            'image_url':self.image_url,
            'api_key': self.api_key,
            'is_active': True
        }
