from abc import ABC, ABCMeta

from sqlalchemy import Column, Integer, String, Date
from db.database import Base
from sqlalchemy import func
from sqlalchemy.types import UserDefinedType
from sqlalchemy.dialects import sqlite


def get_col_spec():
    return 'GEOMETRY'


class Geometry(UserDefinedType):
    """"
    Class used to deal with MySQL POINT data type
    """

    def bind_expression(self, bindvalue):  # function used when a INSERT SQL statement is executed (str to POINT)
        return func.ST_GeomFromText(func.CONCAT("POINT(", bindvalue, ")"), type_=self)

    def column_expression(self, col):  # function used when a SELECT SQL statement is executed (POINT to str)
        return func.REPLACE(func.REPLACE(func.ST_AsText(col, type_=self), 'POINT(', ''), ')', '')


class User(Base):
    """
    SQL interface to table users
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    address = Column(String, nullable=False)
    coordinates = Column(Geometry().with_variant(String, 'sqlite'), nullable=True)  # String type if test sqlite db
