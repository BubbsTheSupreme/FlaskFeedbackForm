from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32), index=True)
    email = db.Column(db.String(150), index=True, unique=True)
    feedback = db.Column(db.String(1024))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        # generates a hash out of the string passed through the password parameter
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        # compares the passwords by hashing the input and comparing that hash

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))