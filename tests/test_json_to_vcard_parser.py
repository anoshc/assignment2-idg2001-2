# Import functions that are going to be tested
from assignment2.json_to_vcard_parser import value_split, create_vcard_object


# Testing the function 'value_split' and check if it splits the string value into a list of substrings.
def test_value_split():
    value = "something;something;One;Two;Three;Four;Five;Six;Seven"

    result = value_split(value)

    # Assert the correctness of the split
    expected_result = ["One", "Two", "Three", "Four", "Five"]
    assert result == expected_result


# Testing the function 'create_address_vobject' and check if the address matches the result.
def test_create_address_vobject():
    import vobject
    from vobject.vcard import Address

    expected_address = vobject.vcard.Address(
        street = "One Microsoft Way",
        city = "Redmond",
        region = "WA",
        code = "98052-6399",
        country = "USA"
    )

    expected_result = create_vcard_object("One Microsoft Way", "Redmond", "WA", "98052-6399", "USA")

    assert expected_address == expected_result


