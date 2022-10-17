from spacebank import account
import pytest
import random
import datetime
# only works on linux because of writing stuff to /tmp
# don't care for now, I (and most other people who may be interested in helping) run linux
# TODO make this work on other stuff
def test_standard_account_file():
    accountfile = """voorbeelduser              +163.48 2022-06-04_02:19:56 +@2021-12-03_18:27:54
bla                 -36.00 2022-01-19_17:11:25 -@2022-01-19_17:00:43"""
    randomnumber = str(random.randint(10000,50000))
    randomfilename = f"/tmp/spacebanktest{randomnumber}"
    with open(randomfilename, 'w') as samplefileoutput:
        samplefileoutput.write(accountfile)
    actstor = account.AccountStore(filename=randomfilename)
    voorbeelduser_account = actstor['voorbeelduser']
    assert type(voorbeelduser_account) == account.Account
    assert voorbeelduser_account.balance == 16348
    assert type(voorbeelduser_account.last_updated) == datetime.datetime
    assert type(voorbeelduser_account.pos_or_neg_since) == datetime.datetime

