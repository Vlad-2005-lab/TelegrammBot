import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Boss(SqlAlchemyBase, UserMixin):
    __tablename__ = 'boss'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    liked = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
