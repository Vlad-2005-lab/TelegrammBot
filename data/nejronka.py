import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Data(SqlAlchemyBase, UserMixin):
    __tablename__ = 'data'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id_boss = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    arg1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    arg2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    arg3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tg_id_people = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
