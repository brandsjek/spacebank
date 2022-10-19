from spacebank import market
import pytest
import random
import datetime
# only works on linux because of writing stuff to /tmp
# don't care for now, I (and most other people who may be interested in helping) run linux
# TODO make this work on other stuff
def test_standard_market_file():
    accountfile = """Juerd      sku81873           6.00    2.00  Cijfertjes/ledjes/knopjes-module
testuser      13371337           4.00    1.30  Sampleproduct met spaties, spannend hoor!"""
    randomnumber = str(random.randint(10000,50000))
    randomfilename = f"/tmp/spacebanktest{randomnumber}"
    with open(randomfilename, 'w') as samplefileoutput:
        samplefileoutput.write(accountfile)
    marketstor = market.MarketProductStore(store_filename=randomfilename)

    sampleproduct = marketstor['sku81873']
    assert type(sampleproduct) == market.MarketProduct
    assert sampleproduct.seller == "Juerd"
    assert sampleproduct.product_name == 'sku81873'
    assert sampleproduct.price_seller == 600
    assert sampleproduct.price_fee == 200
    assert sampleproduct.total_price == 800
    assert sampleproduct.description == "Cijfertjes/ledjes/knopjes-module"


def test_market_export():
    marketproduct = market.MarketProduct('Voorbeeld', '13371337', 300, 200, 'voorbeeldproductje')
    assert marketproduct._to_line() == "Voorbeeld 13371337 3.00 2.00 voorbeeldproductje"