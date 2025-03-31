from config import db_path

from bank_core import Bank
from UI import console


def main():
    bank = Bank(db_path)
    console.start_cli(bank)

if __name__ == "__main__":
    main()