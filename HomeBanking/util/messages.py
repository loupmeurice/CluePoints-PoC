UNKNOWN_USER_ID = "Unknown user id"
ALREADY_USED_ACCOUNT_NUMBER = "This account number is already used"
INVALID_ACCOUNT_NUMBER = "This account number is invalid"
UNKNOWN_FROM_ACCOUNT = "The sender account is unknown"
UNKNOWN_TO_ACCOUNT = "The recipient account is unknown"
NOT_ENOUGH_MONEY = "The sender account balance is insufficient"
NEGATIVE_AMOUNT = "The amount to transfer has to be a positive number"

UNEXPECTED_ERROR = "Error processing request"


class BankingException(Exception):
    pass
