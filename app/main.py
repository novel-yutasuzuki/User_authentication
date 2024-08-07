import os
from flask import Flask
from flask_login import LoginManager
from sqlalchemy import SQLAlchemy

app = Flask(__name__)

username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_HOST')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app)