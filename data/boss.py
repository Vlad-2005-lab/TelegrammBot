import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Boss(SqlAlchemyBase, UserMixin):
    __tablename__ = 'boss'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pozizninij_ban = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
