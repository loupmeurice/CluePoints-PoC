import pytest

from tests.conftest import client, app, db_session
from dao.user_dao import create_user, get_user, get_users, modify_user
from pojo.user import BaseUser
from util.messages import BankingException


@pytest.fixture(autouse=True)
def init(app, client, db_session):
    """
    Required to initialize the SQLite test database
    """
    pass


def test_create_and_read_user():
    """
    Tests the user creation and the retrieval of his/her information once created.
    It also checks if the geographical location is correctly calculated
    """
    user = BaseUser(firstname="Loup",
                    lastname="Meurice",
                    address="rue Comte Jacques de Meeus, 13, 1428 Lillois, Belgique")

    # user creation
    user_id = create_user(user)
    assert user_id >= 0

    # user reading
    user2 = get_user(user_id)
    assert user.firstname == user2.firstname
    assert user.lastname == user2.lastname
    assert user.address == user2.address
    # checks the dynamic calculation of the geographical location
    assert user2.coordinates.latitude == 50.64842575 \
           and user2.coordinates.longitude == 4.372272362912566


def test_create_and_read_user_with_malformed_address():
    """
    Checks that malformed address is properly handled (no coordinates)
    """

    user = BaseUser(firstname="Loup",
                    lastname="Meurice",
                    address="malformed address")

    # user creation
    user_id = create_user(user)
    assert user_id >= 0

    # user reading
    user2 = get_user(user_id)
    assert user.firstname == user2.firstname
    assert user.lastname == user2.lastname
    assert user.address == user2.address
    # checks the dynamic calculation of the geographical location
    assert user2.coordinates is None


def test_get_all_users():
    """
    Tests the retrieval of all users information
    """

    users = get_users()
    assert len(users) == 0  # empty db

    user = BaseUser(firstname="Loup",
                    lastname="Meurice",
                    address="malformed address")

    counter = 5
    # user creations
    for i in range(counter):
        create_user(user)

    users = get_users()
    assert len(users) == counter


def test_get_all_users_when_empy():
    """
    Tests user information retrieval when the database is empty
    :return:
    """

    users = get_users()
    assert len(users) == 0  # empty db


def test_get_unknown_user():
    with pytest.raises(BankingException):
        """
        Tests user information retrieval when an unknown ID is provided
        :raises BankingException
        """
        get_user(-1)


def test_modify_user():
    """
    Tests the modification of user information
    """

    user = BaseUser(firstname="Loup",
                    lastname="Meurice",
                    address="rue Comte Jacques de Meeus, 15, 1428 Lillois, Belgique")

    # user creation
    user_id = create_user(user)

    user.firstname = "X"
    user.lastname = "Y"
    user.address = "rue Comte Jacques de Meeus, 13, 1428 Lillois, Belgique"
    modify_user(user_id, user)

    user2 = get_user(user_id)
    assert user2.firstname == user.firstname
    assert user2.lastname == user.lastname
    assert user2.address == user2.address


def test_modify_unknown_user():
    with pytest.raises(BankingException):
        """
        Tests user information modification when an unknown ID is provided
        :raises BankingException
        """

        user = BaseUser(firstname="Loup",
                        lastname="Meurice",
                        address="rue Comte Jacques de Meeus, 15, 1428 Lillois, Belgique")
        modify_user(-1, user)