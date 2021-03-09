import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class People(SqlAlchemyBase, UserMixin):
    __tablename__ = 'people'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    birth_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    mail = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    salary = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    schedule = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    employment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    experience = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    achievements = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about_me = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    education = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
