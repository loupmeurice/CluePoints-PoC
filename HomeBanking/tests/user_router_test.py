import json

from schwifty.common import Base

import routers.user
from pojo.user import BaseUser, User
from tests.conftest import client
from datetime import datetime as d
import datetime


def create_user(user: BaseUser) -> int:
    return routers.user.create_user(user)


def read_user(user_id: int) -> User:
    return routers.user.get_user(user_id)


def test_get_all_users(client):
    """
    Tests the retrieval of all users information
    """

    counter = 5
    for i in range(counter):  # creates 5 users
        user = BaseUser(firstname=f"f{i + 1}",
                        lastname=f"l{i + 1}",
                        address=f"rue Léopold {i}, 5500 Dinant, Belgique")
        user_id = create_user(user)  # create test user

    # Endpoint call
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == counter

    # checks user information
    for i in range(counter):
        assert users[i]["firstname"] == f"f{i + 1}"
        assert users[i]["lastname"] == f"l{i + 1}"
        assert users[i]["address"] == f"rue Léopold {i}, 5500 Dinant, Belgique"


def test_get_all_users_when_nobody(client):
    """
    Tests the retrieval of all users information when the database is empty
    """

    # Endpoint call
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 0


def test_get_user(client):
    """
    Tests the retrieval of a user's information
    """
    # creates test user
    user = BaseUser(firstname="Loup",
                    lastname="Meurice",
                    address="rue Léopold 11, 5500 Dinant, Belgique")
    user_id = create_user(user)  # create test user

    # Endpoint call
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200

    user2 = response.json()
    assert user_id == user2["id"]
    assert user.firstname == user2["firstname"]
    assert user.lastname == user2["lastname"]
    assert user.address == user2["address"]


def test_get_nonexistent_user(client):
    """
    Tests the retrieval of a nonexistent user's information
    """

    # Endpoint call
    user_id = -1
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 422


def test_create_user_with_right_address(client):
    """
    Checks (1) the user creation,
    (2) the calculation of the geographical location based on a well-formed address,
    (3) the retrieval of the freshly created user
    """

    # user information
    data = {"firstname": "Loup", "lastname": "Meurice",
            "address": "rue Comte Jacques de Meeus, 13, 1428 Lillois, Belgique"}

    # Endpoint call
    response = client.post("/create_user/", params=data,)

    assert response.status_code == 200
    user_id = response.json()["user_id"]
    assert user_id >= 0

    user = read_user(user_id)
    assert user.id == user_id
    assert user.firstname == data["firstname"]
    assert user.lastname == data["lastname"]
    assert user.address == data["address"]

    # checks the dynamic calculation of the geographical location
    assert user.coordinates.latitude == 50.64842575 \
           and user.coordinates.longitude == 4.372272362912566


def test_create_user_with_wrong_address(client):
    """
    Checks (1) the user creation,
    (2) that a malformed address does not provoke errors,
    (3) the retrieval of the freshly created user
    """

    # user information
    data = {"firstname": "Loup", "lastname": "Meurice",
            "address": "wrong address"}

    # Endpoint call
    response = client.post("/create_user/", params=data, )

    assert response.status_code == 200
    user_id = response.json()["user_id"]
    assert user_id >= 0

    user = read_user(user_id)
    assert user.id == user_id
    assert user.firstname == data["firstname"]
    assert user.lastname == data["lastname"]
    assert user.address == data["address"]

    # the geographical location cannot be calculated
    assert user.coordinates is None


def test_update_user(client):
    """
    Tests the update of user's information
    """

    user = BaseUser(firstname="Loup_",
                    lastname="Meurice_",
                    address="rue Léopold 11, 5500 Dinant, Belgique")
    user_id = create_user(user)  # creates test user

    # updated info
    data = {"firstname": "Loup",
            "lastname": "Meurice",
            "address": "rue Comte Jacques de Meeus, 13, 1428 Lillois, Belgique"}

    # Endpoint call
    response = client.put(f"/update_user/{user_id}", params=data, )
    assert response.status_code == 200
    assert response.json()["ok"] is True

    # Checks the update
    user2 = read_user(user_id)
    assert user2.firstname == data["firstname"]
    assert user2.lastname == data["lastname"]
    assert user2.address == data["address"]


def test_update_nonexistent_user(client):
    """
    Tests the update of a nonexistent user's information
    """

    user_id = -1  # nonexistent
    # updated info
    data = {"firstname": "Loup",
            "lastname": "Meurice",
            "address": "rue Comte Jacques de Meeus, 13, 1428 Lillois, Belgique"}

    # Endpoint call
    response = client.put(f"/update_user/{user_id}", params=data, )
    assert response.status_code == 422


