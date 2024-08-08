from flask import Flask, request, jsonify
from models import user
from db import SessionLocal

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create_user():
    session = SessionLocal()
    try:
        new_user = user.User()
        new_user.name = request.form['name']
        new_user.email = request.form['email']
        new_user.password = request.form['password']
        session.add(new_user)
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)