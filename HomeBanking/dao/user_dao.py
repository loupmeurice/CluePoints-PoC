from typing import List
from pojo.user import User as UserPOJO, Coordinates
from pojo.user import BaseUser
from db.database import get_db
from db.tables.user import User as UserTable
from util import util
from util.messages import *


def get_users() -> List[UserPOJO]:
    """
    Returns the list of users
    :return: List[User]
    """

    users = []
    session = get_db()
    try:
        for user in session.query(UserTable).all():
            users.append(_convert_to_pojo(user))
    finally:
        session.close();

    return users


def get_user(user_id: int) -> UserPOJO:
    """
    Returns the user information based on a given user ID
    :param user_id: ID of the user
    :return: the user information
    :rtype: User
    :raises BankingException: the provided user ID is unknown
    """

    session = get_db()
    try:
        user = session.query(UserTable).get(user_id)
        res = _convert_to_pojo(user)
        if res is None:
            raise BankingException(UNKNOWN_USER_ID)
        return res
    finally:
        session.close()


def create_user(user: BaseUser) -> int:
    """
    Creates a new user and calculates the geographical location based on the provided address
    :param user: the user information
    :return: the auto-generated user ID
    """

    session = get_db()

    try:
        latitude, longitude = util.get_coordinates(user.address) # Calculates the geographical location

        if latitude is None or longitude is None:
            coordinates = None
        else:
            coordinates = Coordinates(latitude=latitude, longitude=longitude)

        x = UserPOJO(
            coordinates=coordinates,
            **user.dict()
        )
        u = _convert_to_sql(x)
        session.add(u)
        session.flush()  # Required to retrieve the auto-generated ID
        new_user_id = u.id  # Retrieves the user ID
        session.commit()
        return new_user_id
    finally:
        session.close()


def modify_user(user_id: int, user: BaseUser):
    """
    Updates an existing user and re-calculates the geographical position if the address has changed
    :param user_id: the ID of the user to modify
    :param user: the new user information
    :raises BankingException: the provided user ID is unknown
    """

    session = get_db()

    try:
        old_user = session.query(UserTable).filter(UserTable.id == user_id).first()

        if old_user:
            if user.firstname:
                old_user.firstname = user.firstname
            if user.lastname:
                old_user.lastname = user.lastname
            if user.address and old_user.address != user.address:
                old_user.address = user.address
                latitude, longitude = util.get_coordinates(user.address)
                old_user.coordinates = None if latitude is None and longitude is None else f"{latitude} {longitude}"
            session.commit()
        else:
            raise BankingException(UNKNOWN_USER_ID)
    finally:
        session.close()


def _convert_to_pojo(user: UserTable) -> UserPOJO:
    """
    Converts a UserTable object to a UserPOJO object (SQL to Model).
    This conversion is required after a database read
    :param user: the UserTable object to convert
    :return: the converted UserPOJO
    """

    if user is None:
        return None

    if user.coordinates is None:
        coordinates = None
    else:
        latitude_str, longitude_str = user.coordinates.split()
        latitude = float(latitude_str)
        longitude = float(longitude_str)
        coordinates = Coordinates(latitude=latitude, longitude=longitude)

    return UserPOJO(id=user.id, firstname=user.firstname,
                    lastname=user.lastname,
                    address=user.address, coordinates=coordinates)


def _convert_to_sql(user: UserPOJO) -> UserTable:
    """
    Converts a UserPOJO object to a UserTable object (Model to SQL).
    This conversion is required before a database write
    :param user: the UserPOJO object to convert
    :return: the converted UserTable
    """
    if user is None:
        return None
    res = UserTable()
    res.id = user.id
    res.firstname = user.firstname
    res.lastname = user.lastname
    res.address = user.address
    if user.coordinates is None:
        res.coordinates = None
    else:
        res.coordinates = f"{user.coordinates.latitude} {user.coordinates.longitude}" #required to respect the MySQL POINT data type format

    return res
