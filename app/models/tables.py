from app import db


class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('tb_post', backref='tb_user', lazy=True)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password


class Post(db.Model):
    __tablename__ = 'tb_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id
