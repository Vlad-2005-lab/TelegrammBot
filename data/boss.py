import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Boss(SqlAlchemyBase, UserMixin):
    __tablename__ = 'boss'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    name_of_company = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    name_of_vacancy = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    trebovanija = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    zadachi_funkcii = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    salary = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    about_company = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    name_of_rab = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    job_of_rab = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    phone = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default="")
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    spratan = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True, default=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    tags = sqlalchemy.Column(sqlalchemy.Text, default='')
    timetable = sqlalchemy.Column(sqlalchemy.Text, default='')
