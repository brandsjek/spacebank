from spacebank import product
import pytest
import random
import datetime
# only works on linux because of writing stuff to /tmp
# don't care for now, I (and most other people who may be interested in helping) run linux
# TODO make this work on other stuff
def test_standard_product_file():
    productfile = """5449000014535   0.70    Sprite
5449000000996   0.70    Coca-Cola
1337133713371   2.40    Voorbeeldproduct hmmm heel lekker"""
    randomnumber = str(random.randint(10000,50000))
    randomfilename = f"/tmp/spacebanktest{randomnumber}"
    with open(randomfilename, 'w') as samplefileoutput:
        samplefileoutput.write(productfile)
    prodstor = product.ProductStore(store_filename=randomfilename)
    blikjesprite = prodstor['5449000014535']
    assert type(blikjesprite) == product.Product
    assert blikjesprite.price == 70
    assert blikjesprite.description == "Sprite"
    
    voorbeeldproduct = prodstor['1337133713371']
    assert voorbeeldproduct.price == 240
    assert voorbeeldproduct.description == "Voorbeeldproduct hmmm heel lekker"

