from fastapi import APIRouter
from dao.transaction_dao import *
from routers.util import *
from pojo.transaction import Transaction

router = APIRouter()


@router.post("/transfer/")
def transfer_money(from_acc: str, to_acc: str, amount: float):
    """
    Endpoint to transfer money from a source account to a destination account
    :param from_acc: source account number
    :param to_acc: destination account number
    :param amount: money to transfer
    :return: ok if the transfer is successful
    :raises HTTPException (code 422) if the amount to transfer is negative or if the account numbers are unknown
    :raises HTTPException (code 500): unexpected internal server error
    """

    try:
        transfer(Transaction(from_acc=from_acc, to_acc=to_acc, amount=amount))
        return {'ok': True}
    except BankingException as e:
        return wrap_error_msg(e)
    except Exception as e:
        print_error(e)

