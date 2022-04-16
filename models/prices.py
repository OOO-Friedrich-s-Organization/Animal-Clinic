import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Price(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'price'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    dep_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("departments.id"))

    professions = orm.relation('Department')