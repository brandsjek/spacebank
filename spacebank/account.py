import os.path
import datetime
import re
from . import utils
import logging

class Account:
    # balances are stored in the smallest denomination possible (read: cents)
    # only when they are presented to the user, they will be decimalised.
    
    account_name = None
    balance = None
    last_updated = None
    pos_or_neg_since = None
    def __init__(self, account_name: str, balance: int = None, last_updated: datetime.datetime = datetime.datetime.now(), pos_or_neg_since: datetime.datetime = None):
        """
        Initializes the Account object.

        Parameters:
            accountholder (str): The name of the account. Must not start with [-+*], contain whitespace or be 'too numeric' (see utils.py, parse_amount)
            balance (int): The balance of the account, in cents.
            last_updated (datetime.datetime): The time when the account was last updated (i.e. when a tx was made), or created.
            pos_or_neg_since (datetime.datetime): The time when the account last went in the red or the green. Used to warn users for long-standing debts (if enabled)
        """
        utils.validate_account_name(account_name)
        self.account_name = account_name
        if type(balance) == int:
            self.balance = balance
        else:
            # convert balance to integer
            self.balance = utils.balance_str_to_int(balance)
        self.last_updated = last_updated
        self.pos_or_neg_since = pos_or_neg_since
    
    def __str__(self):
        return f"<Account '{self.account_name}' ({self.balance})>"



class AccountStore:
    _accounts = {}
    store_filename = None
    def __init__(self, filename="spacebank.accounts"):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Account storage '{filename}' does not exist")
        self.store_filename = filename
        self.read_account_store()
    
    def read_account_store(self):
        linenumber = 1
        with open(self.store_filename) as f_accounts:
            logging.info(f"Opening account store @ '{self.store_filename}'")
            f_accounts_lines = f_accounts.readlines()
            for account_line in f_accounts_lines:
                account_line_split_raw = account_line.rstrip().split(' ')
                account_line_split = []
                # sometimes accounts are defined a bit weird, below is a line from revbank/revbank.accounts (the sample account file):
                # juerd              +163.48 2022-06-04_02:19:56 +@2021-12-03_18:27:54
                # this will result in a bunch of empty list items, filter them out and put them into account_line_split
                for value in account_line_split_raw:
                    value = value.rstrip()
                    if value != '':
                        account_line_split.append(value)                
                new_account = Account(account_line_split[0], account_line_split[1], account_line_split)
                self._accounts[account_line_split[0]] = new_account
            linenumber += 1
    
    def __repr__(self):
        return f"<AccountStore containing {len(self._accounts)} accounts>"
    
    def __getitem__(self, val):
        if type(val) != str:
            raise ValueError("Invalid slice")
        if val not in self._accounts:
            raise KeyError(val)
        return self._accounts[val]