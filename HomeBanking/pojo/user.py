from typing import Optional
from datetime import date
from pydantic import BaseModel


class BaseUser(BaseModel):
    """
    This class serves as interface for the endpoints allowing user creation/modification.
    The user id is not useful (auto-generated) and the geographic location is dynamically calculated.

    Attributes:
        firstname: user's firstname
        lastname: user's lastname
        address: user's address
    """

    firstname: str
    lastname: str
    address: str


class Coordinates(BaseModel):
    """
    Class used to calculate the user's geographical position

    Attributes:
        latitude: user's latitude
        longitude: user's longitude
    """
    latitude: float
    longitude: float


class User(BaseUser):
    """
    This class aims to manipulate user's id and position

    Attributes:
        id: user ID
        coordinates: geographical location dynamically calculated from the address
    """
    id: Optional[int] = None
    coordinates: Optional[Coordinates] = None


