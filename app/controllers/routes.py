from flask import render_template

from app import app


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
