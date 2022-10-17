from spacebank import utils
import pytest
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