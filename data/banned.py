import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Ban(SqlAlchemyBase, UserMixin):
    __tablename__ = 'ban'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    ban = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=0)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    arg1 = sqlalchemy.Column(sqlalchemy.String)
    arg2 = sqlalchemy.Column(sqlalchemy.String)
    arg3 = sqlalchemy.Column(sqlalchemy.Integer)
