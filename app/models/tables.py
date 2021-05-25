from datetime import datetime

from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, name, email, username, password):
        self.name = name.title()
        self.email = email.lower()
        self.username = username.lower()
        self.password = self.hashpassword(password)

    def hashpassword(self, password):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return password_hash


class Post(db.Model):
    __tablename__ = 'tb_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False)

    def __init__(self, content, user_id):
        self.content = content
        self.creation_date = datetime.now()
        self.user_id = user_id


class Follower(db.Model):
    __tablename__ = 'tb_follower'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False)

    def __init__(self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id
