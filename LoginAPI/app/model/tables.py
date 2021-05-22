from app import db
from app import bcrypt

class User(db.Model):
    __tablename__ = "tbusers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)

    def __init__(self, username: str, password: str, name: str, email: str):
        self.username = username.lower()
        self.password = self.hashPassword(password)
        capitalized_names = name.title()
        self.name = capitalized_names
        self.email = email.lower()

    def hashPassword(self, password):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return password_hash