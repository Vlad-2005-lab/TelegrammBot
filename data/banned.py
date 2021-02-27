import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Ban(SqlAlchemyBase, UserMixin):
    __tablename__ = 'ban'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    ban = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
