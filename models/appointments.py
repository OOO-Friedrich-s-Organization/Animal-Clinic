import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Appointment(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'appointments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    dep_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("departments.id"))
    doc_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("persons.id"))
    p_date = sqlalchemy.Column(sqlalchemy.String)
    p_time = sqlalchemy.Column(sqlalchemy.String)

    professions = orm.relation('Department')
    doctors = orm.relation('Doctor')