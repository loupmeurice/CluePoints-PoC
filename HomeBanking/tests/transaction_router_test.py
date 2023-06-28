import json
from tests.conftest import client
from tests.account_router_test import create_test_users_and_accounts, read_account


def test_transfer(client):
    """
    Tests money transfer between two accounts
    """

    # Creates test users and accounts
    user_id1, user1, user_id2, user2, account1, account2 = create_test_users_and_accounts()

    data = {"from_acc": account1.number, "to_acc": account2.number, "amount": 20.00}
    response = client.post("/transfer/", params=data)
    assert response.status_code == 200
    assert response.json()["ok"]

    acc1 = read_account(account1.number)
    acc2 = read_account(account2.number)
    assert acc1.balance == account1.balance - data["amount"]
    assert acc2.balance == account2.balance + data["amount"]


def test_transfer_with_insufficient_money(client):
    """
    Tests money transfer between two accounts with insufficient balance
    """

    # Creates test users and accounts
    user_id1, user1, user_id2, user2, account1, account2 = create_test_users_and_accounts()

    data = {"from_acc": account2.number, "to_acc": account1.number, "amount": 20.00}
    response = client.post("/transfer/", params=data)
    assert response.status_code == 422


def test_transfer_with_nonexistent_source_account(client):
    """
    Tests money transfer from nonexistent account
    """

    # Creates test users and accounts
    user_id1, user1, user_id2, user2, account1, account2 = create_test_users_and_accounts()

    data = {"from_acc": "KO", "to_acc": account2.number, "amount": 20.00}
    response = client.post("/transfer/", params=data)
    assert response.status_code == 422


def test_transfer_with_nonexistent_destination_account(client):
    """
    Tests money transfer to nonexistent account
    """

    # Creates test users and accounts
    user_id1, user1, user_id2, user2, account1, account2 = create_test_users_and_accounts()

    data = {"from_acc": account1.number, "to_acc": "KO", "amount": 20.00}
    response = client.post("/transfer/", params=data)
    assert response.status_code == 422

