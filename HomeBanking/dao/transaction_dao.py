from db.tables.account import Account as AccountTable
from db.database import get_db
from util.messages import *
from pojo.transaction import Transaction as TransactionPOJO
from db.tables.transaction import Transaction as TransactionTable


def transfer(transaction: TransactionPOJO):
    """
    Transfers money from an account to another
    :param transaction: contains the source and destination account numbers as well as the amount in EURO to transfer
    :raises BankingException: the amount to transfer is negative or the account numbers are unknown
    """

    session = get_db()
    try:
        if transaction.amount < 0:
            raise BankingException(NEGATIVE_AMOUNT)

        acc1 = session.query(AccountTable).filter(AccountTable.number == transaction.from_acc).first()
        if acc1 is None:  # checks the source account existence
            raise BankingException(UNKNOWN_FROM_ACCOUNT)
        if acc1.balance < transaction.amount:  # checks that the amount to transfer is positive
            raise BankingException(NOT_ENOUGH_MONEY)

        acc2 = session.query(AccountTable).filter(AccountTable.number == transaction.to_acc).first()
        if acc2 is None:  # checks the destination account existence
            raise BankingException(UNKNOWN_TO_ACCOUNT)

        try:

            acc1.balance = acc1.balance - transaction.amount
            acc2.balance = acc2.balance + transaction.amount
            session.add(__convert_to_sql(transaction))
            # Validates the transaction
            session.commit()

        except Exception as e:
            # In case of error, the transaction is cancelled
            session.rollback()
    finally:
        session.close()


def __convert_to_sql(tr: TransactionPOJO) -> TransactionTable:
    """
    Converts a model transaction to a SQLAlchemy transaction
    :param tr:
    :return:
    """
    return TransactionTable(from_acc=tr.from_acc, to_acc=tr.to_acc, amount=tr.amount)
