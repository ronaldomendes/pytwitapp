import sys

from flask import request, Response, json, make_response
from werkzeug.datastructures import Headers

from app import app, db, bcrypt
from app.model.tables import User


@app.route('/')
def index():
    headers = Headers()
    headers.add('Content-Type', 'application/json')
    return Response(status=403, headers=headers)


@app.route('/register', methods=['POST'])
def register():
    headers = Headers()
    headers.add('Content-Type', 'application/json')
    login_obj = request.json

    isrequestvalid = validateuserdata(login_obj, 'register')

    if isrequestvalid is False:
        return Response(response=json.dumps({"msg": "Invalid request"}), status=400, headers=headers)

    name_req = login_obj['name']
    username_req = login_obj['username']
    password_req = login_obj['password']
    email_req = login_obj['email']
    try:
        new_user = User(username=username_req, password=password_req, name=name_req, email=email_req)
        headers = Headers()
        headers.add('Content-Type', 'application/json')
        response_json = {"username": new_user.username, "email": new_user.email, "name": new_user.name}
        db.session.add(new_user)
        db.session.commit()
        return Response(response=json.dumps(response_json), status=201, headers=headers)
    except:
        print('Erro inesperado: ', sys.exc_info[0])
        return Response(status=500)


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method is "OPTIONS":  # CORS treatment
        return _build_cors_prelight_response()
    headers = Headers()
    headers.add('Content-Type', 'application/json')
    login_obj = request.json
    print('will validate request')
    if login_obj is None:
        print("Empty request")
        print(request.json)
        return Response(response=json.dumps({"msg": "Invalid request"}), status=400, headers=headers)
    isrequestvalid = validateuserdata(login_obj, 'login')
    username_req = login_obj['username'] if "username" in login_obj else login_obj['email']
    password_req = login_obj['password']

    if isrequestvalid is False:
        return Response(response=json.dumps({"msg": "Invalid request"}), status=400, headers=headers)

    user = User.query.filter_by(username=username_req).first() if "username" in login_obj else User.query.filter_by(
        email=username_req).first()

    if user is None:
        return Response(response=json.dumps({"msg": "Not Found"}), status=404, headers=headers)

    ispasswordcorrect = bcrypt.check_password_hash(user.password, password_req)

    if ispasswordcorrect is False:
        return Response(response=json.dumps({"msg": "Forbidden"}), status=403, headers=headers)
    response_json = {"username": user.username, "email": user.email, "name": user.name}

    return Response(response=json.dumps(response_json), status=200, headers=headers)


def validateuserdata(userData: dict, endpoint: str):
    if endpoint is 'register':
        try:
            username_req = userData['username']
            password_req = userData['password']
            name_req = userData['name']
            email_req = userData['email']
            if username_req is None or password_req is None or name_req is None or email_req is None:
                return False
            return True
        except KeyError:
            return False
    elif endpoint is 'login':
        try:
            if "email" in userData and "password" in userData:
                print("Checking object...")
                password_req = userData['password']
                print("Checking object keys filling...")
                if password_req is None or userData['email'] is None:
                    return False
                return True
            elif "username" in userData and "password" in userData:
                username_req = userData['username']
                password_req = userData['password']
                if password_req is None or username_req is None:
                    return False
                return True
        except KeyError:
            return False


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = "*"
    return response


def _build_cors_prelight_response():
    print('Returning CORS response')
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
