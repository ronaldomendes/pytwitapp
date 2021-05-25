from flask import render_template, request

from app import app, db
from app.models.tables import Post


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home", methods=['POST'])
def home():
    result = db.engine.execute('SELECT id FROM tb_user WHERE username = :user;', {'user': request.form['username']})
    user = [x[0] for x in result][0]
    new_post = Post(request.form['content'], user)
    db.session.add(new_post)
    db.session.commit()
    return render_template("home.html")


@app.route("/home", methods=['GET'])
def show_all_posts():
    # TODO falta corrigir o bug apos inserir um novo post, nao esta carregando direto
    result = db.engine.execute(
        """SELECT p.*, u.* FROM tb_post p JOIN tb_user u ON p.user_id = u.id ORDER BY p.creation_date DESC; """)
    return render_template("home.html", result=result)


@app.route("/profile/<string:username>")
def profile(username):
    result = db.engine.execute(
        'SELECT p.*, u.* FROM tb_post p JOIN tb_user u ON p.user_id = u.id and u.username = :username;',
        {'username': username})
    user_data = db.engine.execute('SELECT * FROM tb_user WHERE username = :username;', {'username': username})
    return render_template("perfil.html", result=result, userdata=user_data)


@app.route("/followers/<string:username>")
def followers(username):
    return render_template("seguidores.html")
