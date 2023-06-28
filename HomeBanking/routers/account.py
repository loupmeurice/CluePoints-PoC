from fastapi import APIRouter
from dao.account_dao import *
from routers.util import *
from pojo.account import Account as AccountPOJO
from typing import Optional

router = APIRouter()


@router.get("/accounts/{user_id}")
def get_user_accounts(user_id: int):
    """
    Endpoint to retrieve the accounts information based on a provided user ID

    :param user_id: the user ID to whom the accounts belong
    :return: the user accounts
    :rtype: List[Account]
    :raises HTTPException (code 500): unexpected internal server error
    """

    try:
        return get_accounts(user_id)
    except Exception as e:
        print_error(e)


@router.get("/accounts/")
def get_all_accounts():
    """
    Endpoint to retrieve the information of all the accounts
    :return: a list of accounts
    :rtype: List[Account]
    :raises HTTPException (code 500): unexpected internal server error
    """

    try:
        return get_accounts(None)
    except Exception as e:
        print_error(e)


@router.post("/create_account/")
def create_new_account(number: str, user_id: int, balance: Optional[float] = 0.0):
    """
    Endpoint to create an account and attach it to an existing user
    :param number: account number to create (IBAN)
    :param balance: amount of money on this account
    :param user_id: user owning this account
    :return: true if the creation is successful
    :raises HTTPException (code 422) if the user ID is unknown or if the account number format is invalid
    :raises HTTPException (code 500): unexpected internal server error
    """

    try:
        create_account(AccountPOJO(number=number, balance=balance, user_id=user_id))
        return {'ok': True}
    except BankingException as e:
        return wrap_error_msg(e)
    except Exception as e:
        print_error(e)
