from .db_session import SqlAlchemyBase
from flask_login import UserMixin
import sqlalchemy
import datetime
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, default="N")
    contacts = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_activate = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    uuid = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    news = orm.relation("News", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)