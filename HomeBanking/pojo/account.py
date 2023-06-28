from typing import Optional
from pydantic import BaseModel


class Account(BaseModel):
    """
    Model class representing the user accounts

    Attributes:
        number: account number
        balance: current balance in EURO
        user_id: owner ID
    """

    number: str
    balance: Optional[float] = 0.0
    user_id: int
