from typing import List
from pojo.account import Account as AccountPOJO
from dao.user_dao import get_user
from db.database import get_db
from db.tables.account import Account as AccountTable
from util.messages import *
from util.util import validate_account_number


def get_accounts(user_id) -> List[AccountPOJO]:
    """
    Returns the accounts information based on a given user ID
    :param user_id: the user ID to whom the accounts belong.
    :return: the list of accounts
    """

    accounts = []
    session = get_db()
    try:
        query = session.query(AccountTable)
        if user_id is not None:  # if user_id is not specified, it retrieves everybody's accounts
            query = query.filter(AccountTable.user_id == user_id)
        for account in query.all():
            accounts.append(_convert_to_pojo(account))
    finally:
        session.close()
    return accounts


def create_account(account: AccountPOJO) -> int:
    """
    Creates a new account
    :param account: information of the account to create and the owner (user) ID
    :raises: BankingException: the user ID is unknown or the account number to create is already used
    """

    session = get_db()
    try:
        if validate_account_number(account.number) is False:
            raise BankingException(INVALID_ACCOUNT_NUMBER)

        user = get_user(account.user_id)
        if user is None:
            raise BankingException(UNKNOWN_USER_ID)

        a = get_account(account.number)
        if a is not None:
            raise BankingException(ALREADY_USED_ACCOUNT_NUMBER)

        session.add(_convert_to_sql(account))
        session.commit()
    finally:
        session.close()


def get_account(number: str):
    """
    Retrieves information of a given account number
    :param number: the account number
    :return: the account information or None if the account number does not exist
    """

    session = get_db()
    try:
        account = session.query(AccountTable).filter(AccountTable.number == number).first()
        return account
    finally:
        session.close()


def _convert_to_pojo(account: AccountTable) -> AccountPOJO:
    """
    Convert POJO account object to SQLAlchemy account object.
    Required before a database write
    :param account: POJO object to convert
    :return: the converted SQLAlchemy object
    """

    if account is None:
        return None

    return AccountPOJO(number=account.number, balance=account.balance, user_id=account.user_id)


def _convert_to_sql(acc: AccountPOJO) -> AccountTable:
    """
    Converts a SQLAlchemy account object to a POJO account object.
    Required after a database read
    :param acc:
    :return:
    """

    if acc is None:
        return None
    res = AccountTable()
    res.number = acc.number
    res.balance = acc.balance
    res.user_id = acc.user_id
    return res
