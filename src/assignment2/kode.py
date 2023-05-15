import pytest

from assignment2.json_to_vcard_id_parser import serialize_data

# def data_test(x):
#     return 3 * x


def serialize_data():
    # Mock the data and collection
    mock_data = [
        {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'telefon': '1234567890',
        },
        {
            'name': 'Jane Smith',
            'email': 'janesmith@example.com',
            'telefon': '0987654321',
        }
    ]
    # Mock the collection find method to return the mock data
    collection.find = lambda: mock_data


