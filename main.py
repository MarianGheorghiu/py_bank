from config import db_path

from bank_core import Bank, Transactions
from UI import console


def main():
    bank = Bank(db_path)
    transactions = Transactions(bank)
    console.start_cli(bank, transactions)

if __name__ == "__main__":
    main()