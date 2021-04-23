import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    can_access_closed = sqlalchemy.Column(sqlalchemy.Boolean)
    is_closed = sqlalchemy.Column(sqlalchemy.Boolean)

    bdate = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    domain = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    sex = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    date_of_beginnig = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
