from flask import Flask, request, jsonify, make_response, Response
from models.user import User
from db import SessionLocal, session
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, set_access_cookies)
from werkzeug.security import check_password_hash
from typing import Optional, Any, Tuple
import os



app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
print("JWT_SECRET_KEY:", os.getenv('JWT_SECRET_KEY'))

jwt = JWTManager(app)

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
    # app.logger.info('login started')
    req_data: Any = request.get_json()
    print("req_data:", req_data)
    user_name_to_auth: Optional[str] = req_data.get('name')
    email_to_auth: Optional[str] = req_data.get('email')
    password_to_auth: Optional[str] = str(req_data.get('password'))
    print("出力:", user_name_to_auth, email_to_auth, password_to_auth)

    user = session.query(User).filter(User.name == user_name_to_auth)\
        .filter(User.email == email_to_auth).one_or_none()
    # 問題点↑↑↑？

    print("User Name:", user.name)
    print("User Email:", user.email)
    print("password_to_auth:", password_to_auth)
    print("password_hash:", user.password_hash)
    if user and check_password_hash(user.password_hash, password_to_auth):
        # app.logger.info('login succeeded')
        access_token = create_access_token(
            identity={'name': user.name, 'email': user.email})
        response = make_response("成功")
        set_access_cookies(response, access_token)
        print("成功")
        print("access_token:", access_token)
        print("set_access_cookies:", response.headers.get('Set-Cookie'))
        print("response:", response)
        return response, 200
    else:
        print("失敗")
        # app.logger.info('login failed')
        return jsonify({'msg': 'Wrong login id or password.'}), 401

if __name__ == "__main__":
    app.run(debug=True)