# Atribute (număr de cont, nume titular cont, sold, data deschiderii, istoric tranzacții),
# Metode (depunere, retragere, transfer, verificare sold, obținere informații cont). 
# Aceasta reprezintă entitatea centrală în sistemul bancar.
# Această clasă va fi esențială pentru aplicație, conținând toate informațiile și 
# funcționalitățile necesare pentru un cont bancar.

class BankAccount:
    def __init__(self, first_name, last_name, account_number, account_id, balance):
        self.first_name = first_name
        self.last_name = last_name
        self.account_number = account_number
        self.account_id = account_id
        self.balance = balance

    def __str__(self):
        return f"BankAccount({self.first_name} {self.last_name}, Account Number: {self.account_number}, Balance: {self.balance})"
