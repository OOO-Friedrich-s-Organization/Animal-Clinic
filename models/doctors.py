import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Doctor(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'persons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    sec_name = sqlalchemy.Column(sqlalchemy.String)
    profession = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("departments.id"))
    experience = sqlalchemy.Column(sqlalchemy.Integer)
    quote = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)

    professions = orm.relation('Department')
