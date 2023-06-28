import pytest
import datetime

from tests.conftest import client, app, db_session
from dao.account_dao import get_accounts, get_account, create_account
from dao.user_dao import create_user
from pojo.user import BaseUser
from pojo.account import Account
from util.messages import BankingException


@pytest.fixture(autouse=True)
def init(app, client, db_session):
    """
    Required to initialize the SQLite test database
    """
    pass


def create_test_user() -> int:
    user = BaseUser(firstname="Loup",
                    lastname="Meurice",
                    birthdate=datetime.datetime(1990, 6, 22),
                    address="rue Comte Jacques de Meeus, 13, 1428 Lillois, Belgique")

    # user creation
    user_id = create_user(user)
    return user_id


def test_get_accounts():
    """
    Tests the account retrieval for a user with existing accounts
    """

    # test user creation
    user_id = create_test_user()
    account1 = Account(number="FR7630006000011234567890189", balance=100, user_id=user_id)
    account2 = Account(number="DE91100000000123456789", user_id=user_id)
    create_account(account1)
    create_account(account2)

    accounts = get_accounts(user_id)
    assert len(accounts) == 2


def test_get_accounts_for_user_without_accounts():
    """"
    Tests the account retrieval of a given user when this user does not have any accounts
    """

    # test user creation
    user_id = create_test_user()

    accounts = get_accounts(user_id)
    assert len(accounts) == 0


def test_create_account():
    """
    Tests the creation of a new account with a specified balance
    """

    # test user creation
    user_id = create_test_user()
    account = Account(number="FR7630006000011234567890189", balance=100, user_id=user_id)

    # account creation
    create_account(account)

    # account retrieval
    accounts = get_accounts(user_id)

    assert len(accounts) == 1
    assert accounts[0].number == account.number
    assert accounts[0].balance == account.balance
    assert accounts[0].user_id == account.user_id


def test_create_account():
    """
    Tests the creation of a new account without any specified balance
    """

    # test user creation
    user_id = create_test_user()
    account = Account(number="FR7630006000011234567890189", user_id=user_id)

    # account creation
    create_account(account)

    # account retrieval
    accounts = get_accounts(user_id)

    assert len(accounts) == 1
    assert accounts[0].number == account.number
    assert accounts[0].balance == 0
    assert accounts[0].user_id == account.user_id


def test_create_account_with_invalid_iban():
    with pytest.raises(BankingException):
        """
        Tests the creation of a new account with an invalid iban
        """

        # test user creation
        user_id = create_test_user()
        account = Account(number="INVALID IBAN", balance=100, user_id=user_id)

        # account creation
        create_account(account)


def test_get_account():
    """
    Test the information retrieval of a given account number
    """

    # test user creation
    user_id = create_test_user()
    account = Account(number="FR7630006000011234567890189", user_id=user_id)

    # account creation
    create_account(account)

    account2 = get_account(account.number)

    assert account.number == account2.number
    assert account.balance == account2.balance
    assert account.user_id == account2.user_id


def test_get_unknown_account():
    """
    Test the information retrieval of an unknown account number
    """

    assert get_account("unknown") is None
