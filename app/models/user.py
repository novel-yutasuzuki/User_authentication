from app import main
from werkzeug.security import generate_password_hash, check_password_hash

class User (main.db.Model):
    __tablename__ = 'users'
    id = main.db.Column(main.db.Integer, primary_key=True, autoincrement=True)
    name = main.db.Column(main.db.String(255), nullable=False)
    email = main.db.Column(main.db.String(120), nullable=False, unique=True)
    password_hash = main.db.Column(main.db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)