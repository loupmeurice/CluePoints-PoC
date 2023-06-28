from geopy.geocoders import Nominatim
from schwifty import IBAN

geolocator = Nominatim(user_agent="my_geocoder")


def get_coordinates(address: str):
    location = geolocator.geocode(address)
    if location is None:
        return None, None

    coordinates = f"POINT({location.latitude} {location.longitude})"
    return location.latitude, location.longitude


def validate_account_number(account_number):
    try:
        IBAN(account_number)
        return True
    except Exception as e:
        return False
