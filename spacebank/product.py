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
        Initializes the Product object.

        Parameters:
            product_name (str): The unique identifier of the product (i.e. EAN code)
            price (int): The price of the product, in cents (optionally a string, will be parsed to cents)
            description (str): HUman-friendly description of the product
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