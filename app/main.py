from flask import Flask, request, jsonify, make_response, Response
from models.user import User
from models.todo import Todo
from db import SessionLocal, session
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, set_access_cookies
from werkzeug.security import check_password_hash
from typing import Optional, Any, Tuple
import os

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)

@app.route('/registration', methods=['POST'])
def registration_user():
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
    user_name_to_auth: Optional[str] = req_data.get('name')
    email_to_auth: Optional[str] = req_data.get('email')
    password_to_auth: Optional[str] = str(req_data.get('password'))

    user = session.query(User).filter(User.name == user_name_to_auth)\
        .filter(User.email == email_to_auth).one_or_none()

    if user and check_password_hash(user.password_hash, password_to_auth):
        # app.logger.info('login succeeded')
        access_token = create_access_token(
            identity={'id': user.id, 'name': user.name, 'email': user.email})
        response = make_response("Login Success")
        set_access_cookies(response, access_token)
        return response, 200
    else:
        # app.logger.info('login failed')
        return jsonify({'msg': 'Wrong login id or password.'}), 401
    
@app.route('/')
def todo_list():
    user_id = current_user.id

# current_userでは無く、トークンから取得

    todo_list = Todo.query.filter_by(user_id = user_id).all()

    def todo_to_dict(todo):
        return {
            'id': todo.id,
            'title': todo.title
        }
    
    todo_list_dict = [todo_to_dict(todo) for todo in todos]

    return jsonify(todo_list_dict)

@app.route('/create', methods=['POST'])
def create_todo():
    new_todo = Todo()
    new_todo.title = request.json['title']
    session.add(new_todo)
    session.commit()
    return jsonify({'msg': 'New creation succeeded'})

if __name__ == "__main__":
    app.run(debug=True)