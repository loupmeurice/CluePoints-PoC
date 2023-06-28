import json

import dao.account_dao
import routers.account
from pojo.account import Account
from tests.conftest import client
from pojo.user import BaseUser, User
from tests.user_router_test import read_user, create_user


def create_account(account: Account) -> int:
    return dao.account_dao.create_account(account)


def read_account(account_id: int) -> Account:
    return dao.account_dao.get_account(account_id)


def create_test_users_and_accounts():
    # creates 2 test users
    user1 = BaseUser(firstname="Loup_",
                     lastname="Meurice_",
                     address="rue Léopold 11, 5500 Dinant, Belgique")
    user_id1 = create_user(user1)

    user2 = BaseUser(firstname="Loup",
                     lastname="Meurice",
                     address="rue Léopold 11, 5500 Dinant, Belgique")
    user_id2 = create_user(user2)

    account1 = Account(number="FR7630006000011234567890189", balance=100, user_id=user_id1)
    account2 = Account(number="DE91100000000123456789", user_id=user_id2)

    create_account(account1)
    create_account(account2)
    return user_id1, user1, user_id2, user2, account1, account2


def test_get_accounts(client):
    """
    Tests the retrieval of all user accounts
    """

    # creates 2 test users
    user_id1, user1, user_id2, user2, account1, account2 = create_test_users_and_accounts()

    # Endpoint calls
    response = client.get("/accounts/")
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts) == 2

    assert accounts[0]["number"] == account1.number
    assert accounts[0]["balance"] == account1.balance
    assert accounts[0]["user_id"] == user_id1
    assert accounts[1]["number"] == account2.number
    assert accounts[1]["balance"] == 0.0
    assert accounts[1]["user_id"] == user_id2


def test_get_all_accounts_when_empty(client):
    """
    Tests the retrieval of all the accounts when the database is empty
    """
    # Endpoint calls
    response = client.get("/accounts/")
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts) == 0


def test_get_user_account(client):
    """
    Tests the retrieval of the accounts of a given user
    """

    # creates 2 test users
    user_id1, user1, user_id2, user2, account1, account2 = create_test_users_and_accounts()

    # Endpoint calls for first user
    response = client.get(f"/accounts/{user_id1}")
    response.status_code == 200
    accounts = response.json()
    assert len(accounts) == 1
    assert accounts[0]["number"] == account1.number
    assert accounts[0]["balance"] == account1.balance
    assert accounts[0]["user_id"] == user_id1

    # Endpoint calls for snd user
    response = client.get(f"/accounts/{user_id2}")
    response.status_code == 200
    accounts = response.json()
    assert len(accounts) == 1
    assert accounts[0]["number"] == account2.number
    assert accounts[0]["balance"] == 0
    assert accounts[0]["user_id"] == user_id2


def test_get_nonexistent_user_account(client):
    """
    Tests the account retrieval for a nonexistent user
    """

    user_id = -1 # nonexistent
    # Endpoint calls for
    response = client.get(f"/accounts/{user_id}")
    response.status_code == 422


def test_create_account(client):
    """
    Tests the creation of a new account
    """

    # Create test user
    user = BaseUser(firstname="Loup",
                     lastname="Meurice",
                     address="rue Léopold 11, 5500 Dinant, Belgique")
    user_id = create_user(user)

    # Account information
    number = "FR7630006000011234567890189"
    data = {"number": number, "balance": 100, "user_id": user_id}

    # Endpoint call
    response = client.post("/create_account/", params=data, )
    assert response.status_code == 200

    account = read_account(number)
    assert account.number == data["number"]
    assert account.balance == data["balance"]
    assert account.user_id == user_id


def test_create_account_with_option_balance(client):
    """
    Tests the creation of a new account without specifying balance
    """

    # Create test user
    user = BaseUser(firstname="Loup",
                     lastname="Meurice",
                     address="rue Léopold 11, 5500 Dinant, Belgique")
    user_id = create_user(user)

    # Account information
    number = "FR7630006000011234567890189"
    data = {"number": number, "user_id": user_id}

    # Endpoint call
    response = client.post("/create_account/", params=data, )
    assert response.status_code == 200

    account = read_account(number)
    assert account.number == data["number"]
    assert account.balance == 0.0  # default balance value
    assert account.user_id == user_id


def test_create_account_to_non_existent_user(client):
    """
    Tests the creation of a new account attached to a nonexitent user
    """

    # Account information
    number = "FR7630006000011234567890189"
    data = {"number": number, "balance": 100, "user_id": -1}  # nonexistent user

    # Endpoint call
    response = client.post("/create_account/", params=data, )
    assert response.status_code == 422


def test_create_account_with_invalid_iban(client):
    """
    Tests the account creation with invalid iban
    """

    # Create test user
    user = BaseUser(firstname="Loup",
                     lastname="Meurice",
                     address="rue Léopold 11, 5500 Dinant, Belgique")
    user_id = create_user(user)

    # Account information
    number = "INVALID"  # invalid iban
    data = {"number": number, "balance": 100, "user_id": user_id}

    # Endpoint call
    response = client.post("/create_account/", params=data, )
    assert response.status_code == 422

