import json

from assignment2.kode import data_test




def test_data_test():
    setup_data = 4
    result = data_test(setup_data)
    expected = 12
    assert result == expected