import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Timetable(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'timetable'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    doc_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("persons.id"))
    mon = sqlalchemy.Column(sqlalchemy.String)
    tue = sqlalchemy.Column(sqlalchemy.String)
    wed = sqlalchemy.Column(sqlalchemy.String)
    thu = sqlalchemy.Column(sqlalchemy.String)
    fri = sqlalchemy.Column(sqlalchemy.String)
    sat = sqlalchemy.Column(sqlalchemy.String)
    sun = sqlalchemy.Column(sqlalchemy.String)

    professions = orm.relation('Doctor')
