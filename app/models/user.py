from sqlalchemy import Column, Integer, String
from db import Base, engine
from werkzeug.security import generate_password_hash, check_password_hash

class User (Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128))

    # 読み取り不可にする
    @property
    def password(self):
        raise AttributeError('password is not a readable!')

    # ハッシュ化して保存する
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 入力されたパスワードが保存されているハッシュ化したパスワードと一致するか比較する
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    Base.metadata.create_all(engine)