import json

from assignment2.kode import data_test
from assignment2.json_to_vcard_parser import *




def test_data_test():
    setup_data = 4
    result = data_test(setup_data)
    expected = 12
    assert result == expected