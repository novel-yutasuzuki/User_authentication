from flask_login import UserMixin
from app import main


class User (UserMixin, main.dbModel):
    id = main.db.Column(main.db.Integer, primary_key=True, autoincrement=True)
    username = main.dc.Column(main.db.String(), nullable=False)
    email = main.dc.Column(main.db.String(), nullable=False, unique=True)
    password = main.db.Column(main.db.String(25))