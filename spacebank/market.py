import os.path
import datetime
import re
from . import utils, store, account
import logging

class MarketProduct:
    seller = None
    product_name = None
    price_seller = None
    price_fee = None
    description = None
    total_price = None
    def __init__(self, seller: account.Account, product_name: str, price_seller: int, price_fee: int, description: str = None):
        """
        Initializes the MarketProduct object.

        Parameters:
            seller (account.Account): The seller (who will recieve the amount as defined in price_seller)
            product_name (str): The unique identifier of the product (i.e. EAN code)
            price_seller (int): The amount of money that the seller will receive, in cents (optionally a string, will be parsed to cents)
            price_fee (int): A fee that will be added to price_seller that will not go to the seller, maybe for the benefit of the spacebank operator.
            description (str): Human-friendly description of the product
        """
        
        self.seller = seller
        self.product_name = product_name 
        if type(price_seller) == int:
            self.price_seller = price_seller
        else:
            # convert balance to integer
            self.price_seller = utils.balance_str_to_int(price_seller)
        
        if type(price_fee) == int:
            self.price_fee = price_fee
        else:
            # convert balance to integer
            self.price_fee = utils.balance_str_to_int(price_fee)
        
        self.total_price = self.price_fee + self.price_seller

        self.description = description
        
    
    def __str__(self):
        return f"<MarketProduct '{self.product_name}' ({self.total_price})>"
    
    def _to_line(self):
        price_seller = utils.cents_to_decimal_string(self.price_seller)
        price_fee = utils.cents_to_decimal_string(self.price_fee)
        return f"{self.seller} {self.product_name} {price_seller} {price_fee} {self.description}"



class MarketProductStore(store.BaseStore):    
    def _read_store(self):
        linenumber = 1
        with open(self.store_filename) as f_products:
            logging.info(f"Opening market product store @ '{self.store_filename}'")
            f_products_lines = f_products.readlines()
            for product_line in f_products_lines:
                product_line_split_raw = product_line.rstrip().split(' ')
                product_line_split = []
                # parse out a bunch of spaces, see the parser in account.py
                for value in product_line_split_raw:
                    value = value.rstrip()
                    if value != '':
                        product_line_split.append(value)
                    
                price_seller = utils.balance_str_to_int(product_line_split[2])
                price_fee = utils.balance_str_to_int(product_line_split[3])
                if len(product_line_split) > 5:
                    # the description MAY contain spaces which have been split, so if there are more than 3 words in the list,
                    # combine them
                    product_description = ' '.join(product_line_split[4:])
                else:
                    product_description = product_line_split[4]
                new_product = MarketProduct(product_line_split[0], product_line_split[1], price_seller, price_fee, product_description)
                self._store[product_line_split[1]] = new_product
            linenumber += 1
    
    def __repr__(self):
        return f"<MarketProductStore containing {len(self._store)} products>"