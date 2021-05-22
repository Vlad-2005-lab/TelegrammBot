import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Boss(SqlAlchemyBase, UserMixin):
    __tablename__ = 'boss'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    salary = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    name_vacancy = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    trebovanija = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    timetable = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    liked = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    tags = sqlalchemy.Column(sqlalchemy.String, default="")
