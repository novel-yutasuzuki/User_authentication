import os
from flask import Flask, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import user

app = Flask(__name__)

username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}/{database}")

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.route('/new')
def user_registration():
    return render_template('new.html')

@app.route('/create', methods=['POST'])
def create_user():
    session = SessionLocal()
    try:
        user = user.User()
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        session.add(user)
        session.commit()
    finally:
        session.close()

    return render_template('show.html', user = user)

if __name__ == "__main__":
    app.run(debug=True)