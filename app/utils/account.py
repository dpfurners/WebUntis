
from cryptography.fernet import Fernet


class AccountManager:
    pass


def create_key():
    key = Fernet.generate_key()
    with open("webuntis.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return Fernet(open("webuntis.key", "rb").read())


def load_account_file(file: str = "accounts.wu"):
    with open(file, "rb") as acc_file:
        acc_file.write()


def store_new_account(username: str, password: str, file: str = "accounts.wu"):
    pass
