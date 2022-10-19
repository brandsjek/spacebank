from spacebank import utils
import pytest
import datetime
def test_balance_string_to_int():
    assert utils.balance_str_to_int('-42.42') == -4242
    assert utils.balance_str_to_int('+42.42') == 4242
    assert utils.balance_str_to_int('13.37') == 1337
    assert utils.balance_str_to_int('1.37') == 137
    assert utils.balance_str_to_int('0') == 0
    assert utils.balance_str_to_int('-0') == 0
    assert utils.balance_str_to_int('+0') == 0
    assert utils.balance_str_to_int('14') == 1400
    assert utils.balance_str_to_int('-1.37') == -137
    with pytest.raises(ValueError):
        utils.balance_str_to_int('1,1,1')
    with pytest.raises(ValueError):
        utils.balance_str_to_int('abcdefg')
    with pytest.raises(ValueError):
        utils.balance_str_to_int('2,3.1')

def test_timestring_datetime_conversion():
    sample_dt = datetime.datetime(2022, 10, 9, 12, 13, 37)
    sample_timestring = '2022-10-09_12:13:37'
    assert utils.datetime_to_store_timestring(sample_dt) == sample_timestring
    assert utils.store_timestring_to_datetime(sample_timestring) == sample_dt

def test_cents_int_to_decimal_string():
    assert utils.cents_to_decimal_string(1337) == "13.37"
    assert utils.cents_to_decimal_string(13337) == "133.37"
    assert utils.cents_to_decimal_string(100000) == "1000.00"
    assert utils.cents_to_decimal_string(1) == "0.01"
    assert utils.cents_to_decimal_string(10) == "0.10"

    assert utils.cents_to_decimal_string(-100, False) == "-1.00"
    assert utils.cents_to_decimal_string(-1337, False) == "-13.37"
    
    # negative digits, with absolute=True
    assert utils.cents_to_decimal_string(-100) == "1.00"
    assert utils.cents_to_decimal_string(-1337) == "13.37"