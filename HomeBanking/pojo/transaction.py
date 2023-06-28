from typing import Optional
from datetime import date
from pydantic import BaseModel


class Transaction(BaseModel):
    """
    Represents a money transfer performed from an account to another.

    Attributes:
        id: transfer ID (auto-generated)
        amount: amount in EURO that was transferred
        from_acc: source account number
        to_acc: destination account number
    """

    id: Optional[int] = None
    amount: float
    from_acc: str
    to_acc: str
