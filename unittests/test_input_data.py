from datetime import datetime
import string

def valid_date(trx_date):
    try:
        d = datetime.strptime(trx_date, '%m%d%Y')
    except ValueError:
        return False
    else:
        return True

def valid_name(name):
    name = name.replace(" ","")
    strip_name = "".join((char for char in name if char not in string.punctuation))
    n = strip_name.isalpha()
    return n

class TestInput(object):
    def test_invalid_date(self):
        assert valid_date("2017") == False

    def test_valid_date(self):
        assert valid_date("01122018") == True

    def test_invalid_name(self):
        s = "273e327290"
        assert valid_name(s) == False

    def test_valid_name(self):
        s = "ABBOTT, JOSEPH"
        assert valid_name(s) == True
