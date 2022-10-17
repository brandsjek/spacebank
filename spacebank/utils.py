import re

# generic functions, primarily for validating/parsing input

def validate_account_name(account_name: str, raise_exception_on_error: bool = True):
    """
    Validates a account name.

    Parameters:
        account_name (str): The account name to be validated
        raise_exception_on_error (bool): Raise a ValueError if the name is invalid, otherwise return False
    Returns:
        validity (bool): Whether the account name is valid.
    """
    # see revbank/plugins/adduser, checking if a account already exists is done in AccountStore, however
    validity = True
    if re.match('/\s/', account_name):
        validity = False
        if raise_exception_on_error:
            raise ValueError("Whitespace is not allowed in account names")
    if re.match('/^[-+*]/', account_name):
        # 'reserved' characters that collide with other functions in the accountstore
        validity = False
        if raise_exception_on_error:
            raise ValueError("First character is not allowed")
    # TODO implement a check of parse_amount here (when that's implemented), to disallow usernames that look too much like barcodes or amounts

    return validity

def balance_str_to_int(balance_value: str):
    """
    Converts a string representing a human-friendly balance (i.e. '133.70' or '-42.42' to a integer)

    Parameters:
        balance_value (str): The balance to be converted to a integer
    Returns:
        balance_int (int): The balance represented as a integer
    """
    positive = True
    
    # check if the amount is explicitly positive or negative
    if balance_value[0] == '-':
        positive = False
        balance_value = balance_value[1:]
    if balance_value[0] == '+':
        positive = True
        balance_value = balance_value[1:]
    
    # determine what decimal separator is used
    balance_comma_split = balance_value.split(",")
    balance_is_comma_split = False
    if len(balance_comma_split) > 2:
        raise ValueError("Couldn't parse balance to integer: too many commas")
    elif len(balance_comma_split) == 2:
        balance_is_comma_split = True
    
    balance_period_split = balance_value.split(".")
    balance_is_period_split = False
    if len(balance_period_split) > 2:
        raise ValueError("Couldn't parse balance to integer: too many periods")
    elif len(balance_period_split) == 2:
        balance_is_period_split = True

    if(len(balance_comma_split) > 1 and len(balance_period_split) > 1):
        raise ValueError("Balance appears to contain both periods and commas")
    elif balance_is_comma_split:
        balance_split = balance_comma_split
    elif balance_is_period_split:
        balance_split = balance_period_split
    else:
        balance_split = [balance_value, '0']
    if(balance_split[0].isnumeric()):
        hundreds = int(balance_split[0]) * 100
    else:
        raise ValueError("Balance is not numeric")
    if(balance_split[1].isnumeric()):
        cents = balance_split[1]


    absolute_value = int(hundreds) + int(cents)
    if not positive:
        return -absolute_value
    else:
        return absolute_value

