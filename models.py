from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(128))
    fname = db.Column(db.String(50))
    mname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    dob = db.Column(db.Date)
    phone = db.Column(db.BigInteger)
    email = db.Column(db.String(50))
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return (self.username)
    
    def get_personal_details(self):
         return {
            'fname': self.fname,
            'mname': self.mname,
            'lname': self.lname,
            'dob': self.dob,
            'phone': self.phone,
            'email': self.email,
            'username':self.username
        }
        
            
        
        


