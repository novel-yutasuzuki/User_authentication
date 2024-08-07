from app import main

class User (main.dbModel):
    __tablename__ = 'users'
    id = main.db.Column(main.db.Integer, primary_key=True, autoincrement=True)
    name = main.db.Column(main.db.String(), nullable=False)
    email = main.db.Column(main.db.String(), nullable=False, unique=True)
    password = main.db.Column(main.db.String(25))