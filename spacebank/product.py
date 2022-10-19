import os.path
import datetime
import re
from . import utils, store
import logging

class Product:
    product_name = None
    price = None
    description = None
    def __init__(self, product_name: str, price: int, description: str = None):
        """
        Initializes the Account object.

        Parameters:
            accountholder (str): The name of the account. Must not start with [-+*], contain whitespace or be 'too numeric' (see utils.py, parse_amount)
            balance (int): The balance of the account, in cents.
            last_updated (datetime.datetime): The time when the account was last updated (i.e. when a tx was made), or created.
            pos_or_neg_since (datetime.datetime): The time when the account last went in the red or the green. Used to warn users for long-standing debts (if enabled)
        """
        self.product_name = product_name
        if type(price) == int:
            self.price = price
        else:
            # convert balance to integer
            self.price = utils.balance_str_to_int(price)
        self.description = description
    
    def __str__(self):
        return f"<Product '{self.product_name}' ({self.price})>"
    
    def _to_line(self):
        return f"{self.product_name} {self.price} {self.description}"



class ProductStore(store.BaseStore):    
    def _read_store(self):
        linenumber = 1
        with open(self.store_filename) as f_products:
            logging.info(f"Opening product store @ '{self.store_filename}'")
            f_products_lines = f_products.readlines()
            for product_line in f_products_lines:
                product_line_split_raw = product_line.rstrip().split(' ')
                product_line_split = []
                # parse out a bunch of spaces, see the parser in account.py
                for value in product_line_split_raw:
                    value = value.rstrip()
                    if value != '':
                        product_line_split.append(value)
                    
                product_price = utils.balance_str_to_int(product_line_split[1])
                if len(product_line_split) > 3:
                    # the description MAY contain spaces which have been split, so if there are more than 3 words in the list,
                    # combine them
                    product_description = ' '.join(product_line_split[2:])
                else:
                    product_description = product_line_split[2]
                new_product = Product(product_line_split[0], product_price, product_description)
                self._store[product_line_split[0]] = new_product
            linenumber += 1
    
    def __repr__(self):
        return f"<ProductStore containing {len(self._store)} products>"