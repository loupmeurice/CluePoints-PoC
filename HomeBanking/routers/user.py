from fastapi import APIRouter
from dao.user_dao import *
from pojo.user import BaseUser
from routers.util import *
from util.messages import BankingException
router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello world"}


@router.get("/users")
def list_users():
    """
    Endpoint to retrieve the list of users

    :return: list of users
    :rtype: List[User]
    :raises HTTPException (code 500): unexpected internal server error
    """

    try:
        return get_users()
    except Exception as e:
        print_error(e)


@router.get("/user/{user_id}")
def get_user_by_id(user_id: int):
    """
    Endpoint to retrieve user information based on the provided user ID

    :param user_id: the ID of the user
    :return: User information
    :rtype: User
    :raises HTTPException (code 422): when an unknown user ID is provided
    :raises HTTPException (code 500): unexpected internal server error
    """

    try:
        user = get_user(user_id)
        return user
    except BankingException as e:
        return wrap_error_msg(e)
    except Exception as e:
        print_error(e)


@router.post("/create_user/")
def create_new_user(firstname: str, lastname: str, address: str):
    """
    Endpoint to create a new user and calculates his/her geographical location based on his/her provided address

    :param address: new user address
    :param lastname: new user lastname
    :param firstname: new user firstname
    :return: the generated ID of the new user
    :raises HTTPException (code 500): unexpected internal server error
    """

    try:
        user_id = create_user(BaseUser(firstname=firstname, lastname=lastname, address=address))
        return {"user_id": user_id}
    except Exception as e:
        print_error(e)


@router.put("/update_user/{user_id}")
def update_user(user_id: int, firstname: str, lastname: str, address: str):
    """
    Endpoint to update user information based on a provided user ID

    :param address: new address
    :param lastname: new lastname
    :param firstname: new firstname
    :param user_id: the ID of the user to modify
    :return: true if the user is modified with success
    :raises HTTPException (code 500): unexpected internal server error
    :raises HTTPException (code 422): the user ID is unknown
    """

    try:
        modify_user(user_id, BaseUser(firstname=firstname, lastname=lastname, address=address))
        return {'ok': True}
    except BankingException as e:
        return wrap_error_msg(e)
    except Exception as e:
        print_error(e)
