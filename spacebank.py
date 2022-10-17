import path
import datetime

class Account:
    # balances are stored in the smallest denomination possible (read: cents)
    def __init__(self, accountholder: str, balance: int, last_updated: datetime.datetime, pos_or_neg_since: datetime.datetime = 'None'):


class AccountStore:
    _accounts = {}
    def __init__(self, filename="spacebank.accounts"):
        if not path.exists(filename):
            raise FileNotFoundError(f"Account storage '{filename}' does not exist")
        
        linenumber = 1
        with open(filename) as f_accounts:

        
