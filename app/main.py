from flask import Flask, request, jsonify, make_response, Response
from models.user import User
from db import SessionLocal, session
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
# /loginにPOSTメソッドでアクセスした場合のエンドポイント
def authenticate() -> Tuple[Response, int]:
# ログインの状況に応じて、レスポンスとHTTPステータスコード(整数)を返す
    # app.logger.info('login started')
    # ログインスタートというログを残す
    req_data: Any = request.get_json()
    print()
    # json形式のデータをキー(req_data)のバリューとしてAnyに代入する
    user_name_to_auth: Optional[str] = req_data.get('name')
    email_to_auth: Optional[str] = req_data.get('email')
    password_to_auth: Optional[str] = str(req_data.get('password'))
    # 上記のカラムのデータをとりだして各変数に代入する
    email_to_auth: Optional[str] = req_data.get('email')
    print(user_name_to_auth, email_to_auth, password_to_auth)

    user = session.query(User).filter(User.name == user_name_to_auth)\
        .filter(User.email == email_to_auth)\
        .filter(User.password_hash == password_to_auth).one_or_none()
    # Userテーブルに入力された各カラムの入力値と一致するデータがあるか比較し、あればuser変数に代入しなければnoneを返す
    print(user)
    if user and check_password_hash(user.password_hash, password_to_auth):
        # userが存在し、入力されたパスワードがデータベースに保存されているパスワードのハッシュと一致した場合はTrue
        # app.logger.info('login succeeded')
        # ログインが成功というメッセージをログに残す
        access_token = create_access_token(
            identity={'name': user.name, 'email': user.email})
        response = make_response()
        # nameとemailを含むトークンを作成する
        set_access_cookies(response, access_token)
        # クッキーに、レスポンス変数とトークンを設定する
        return response, 200
        # レスポンス変数とコードを返す
    else:
        # app.logger.info('login failed')
        # userが存在せず、入力されたパスワードがデータベースに保存されているパスワードのハッシュと不一致の場合
        return jsonify({'msg': 'Wrong login id or password.'}), 401
        # json形式でメッセージとコードを返す

if __name__ == "__main__":
    app.run(debug=True)