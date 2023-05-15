from assignment2.json_to_vcard_id_parser import get_address_fields

# def test_data_test():
#     setup_data = 4
#     result = data_test(setup_data)
#     expected = 12
#     assert result == expected


def test_get_address_fields():
    address = ";;One Microsoft Way;Redmond;WA;98052-6399;USA"

    result = get_address_fields(address)

    # Assert the correctness of the serialization
    expected_result = ["One Microsoft Way", "Redmond", "WA", "98052-6399", "USA"]
    assert result == expected_result
