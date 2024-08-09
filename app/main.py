from flask import Flask, request, jsonify, make_response, Response
from models.user import User
from db import SessionLocal
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, set_access_cookies,unset_access_cookies, verify_jwt_in_request)
from werkzeug.security import check_password_hash
from typing import Optional, Any, Tuple



app = Flask(__name__)

jwt = JWTManager()

@app.route('/create', methods=['POST'])
def create_user():
    session = SessionLocal()
    try:
        new_user = User()
        new_user.name = request.json['name']
        new_user.email = request.json['email']
        new_user.password = request.json['password']
        session.add(new_user)
        session.commit()
        return jsonify({'message': 'User created successfully!'}), 201
    finally:
        session.close()

@app.route('/login', methods=['POST'])
def authenticate() -> Tuple[Response, int]:
    app.logger.info('login started')

    req_data: Any = request.get_json()

    user_name_to_auth: Optional[str] = req_data['name']
    email_to_auth: Optional[str] = req_data['email']
    password_to_auth: Optional[str] = req_data['password']

    user = User.query.filter(User.name == user_name_to_auth)\
        .filter(User.email == email_to_auth)\
        .filter(User.password == password_to_auth).one_or_none()

    if user and check_password_hash(user.password_hash, password_to_auth):
        app.logger.info('login succeeded')
        access_token = create_access_token(
            identity={'name': user.name, 'email': user.email})
        response = make_response()
        set_access_cookies(response, access_token)
        return response, 200
    else:
        app.logger.info('login failed')
        return jsonify({'msg': 'Wrong login id or password.'}), 401

if __name__ == "__main__":
    app.run(debug=True)