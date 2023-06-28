from fastapi import HTTPException
from util.messages import BankingException


def wrap_error_msg(e: BankingException):
    raise HTTPException(status_code=422, detail=str(e))


def print_error(e: Exception):
    print("Unexpected error: ", str(e))
    raise HTTPException(status_code=500, detail=UNEXPECTED_ERROR)
