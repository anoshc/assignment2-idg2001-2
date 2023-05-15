import json

from assignment2.kode import serialize_data




# def test_data_test():
#     setup_data = 4
#     result = data_test(setup_data)
#     expected = 12
#     assert result == expected


def test_serialize_data():
    # Call the function to serialize vcards
    result = serialize_data()
    # Assert the correctness of the generated JSON string
    expected_json = '''[
      "BEGIN:VCARD\\nVERSION:3.0\\nN:Doe;John;;;\\nFN:John Doe\\nEMAIL:johndoe@example.com\\nTEL:1234567890\\nEND:VCARD",
      "BEGIN:VCARD\\nVERSION:3.0\\nN:Smith;Jane;;;\\nFN:Jane Smith\\nEMAIL:janesmith@example.com\\nTEL:0987654321\\nEND:VCARD"
    ]'''
    
    assert result == expected_json