from flask import request, Response, json, render_template
from werkzeug.datastructures import Headers

from app import app, db, bcrypt
from app.models.tables import User

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/profile/<string:username>")
def profile(username):
    return render_template("perfil.html")

@app.route("/followers/<string:username>")
def followers(username):
    return render_template("seguidores.html")