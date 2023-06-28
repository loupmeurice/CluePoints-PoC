from sqlalchemy import Column, String, Float, Integer
from db.database import Base


class Account(Base):
    """"
    SQL interface to the table account (user accounts)
    """

    __tablename__ = "account"

    number = Column(String, primary_key=True, index=True)
    balance = Column(Float, nullable=False)
    user_id = Column(Integer, nullable=False)
