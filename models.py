from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginLogoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(10), nullable=False)  # 'login' or 'logout'
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(10), nullable=False)  # 'success' or 'failure'
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
