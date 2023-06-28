import pytest
import datetime

from tests.conftest import client, app, db_session
from dao.account_dao import get_accounts, get_account, create_account
from dao.user_dao import create_user
from pojo.user import BaseUser
from pojo.account import Account
from util.messages import BankingException
from dao.transaction_dao import transfer
from pojo.transaction import Transaction

@pytest.fixture(autouse=True)
def init(app, client, db_session):
    """
    Required to initialize the SQLite test database
    """
    pass


def create_user_with_accounts():
    # test user creation
    user = BaseUser(firstname="Loup",
                    lastname="Meurice",
                    address="rue Comte Jacques de Meeus, 13, 1428 Lillois, Belgique")

    # user creation
    user_id = create_user(user)
    account1 = Account(number="FR7630006000011234567890189", balance=100, user_id=user_id)
    account2 = Account(number="DE91100000000123456789", user_id=user_id)
    create_account(account1)
    create_account(account2)

    return user_id, account1, account2


def test_transfer():
    """
    Tests the money transfer between two accounts
    """

    user_id, account1, account2 = create_user_with_accounts()
    transaction = Transaction(from_acc=account1.number, to_acc=account2.number, amount=25.0)
    transfer(transaction)

    acc1 = get_account(account1.number)
    acc2 = get_account(account2.number)

    assert acc1.balance == account1.balance - transaction.amount
    assert acc2.balance == account2.balance + transaction.amount


def test_transfer_not_enough_money():
    with pytest.raises(BankingException):
        """
        Tests the money transfer when not enough money
        """

        user_id, account1, account2 = create_user_with_accounts()
        transaction = Transaction(from_acc=account2.number, to_acc=account1.number, amount=25.0)
        transfer(transaction)


def test_transfer_invalid_source():
    with pytest.raises(BankingException):
        """
        Tests the money transfer when the source account is unknown
        """

        user_id, account1, account2 = create_user_with_accounts()
        transaction = Transaction(from_acc="unknown", to_acc=account2.number, amount=25.0)
        transfer(transaction)


def test_transfer_invalid_destination():
    with pytest.raises(BankingException):
        """
        Tests the money transfer when the destination account is unknown
        """

        user_id, account1, account2 = create_user_with_accounts()
        transaction = Transaction(from_acc=account1.number, to_acc="unknown", amount=25.0)
        transfer(transaction)



