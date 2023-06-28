from sqlalchemy import Column, String, Float, Integer, DateTime
from db.database import Base


class Transaction(Base):
    """
    SQL interface to table transfer (money transactions)
    """

    __tablename__ = "transfer"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    from_acc = Column(String, nullable=False)
    to_acc = Column(String, nullable=False)
