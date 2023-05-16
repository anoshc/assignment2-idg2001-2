# Denne parseren er inspirert fra IDG2001 Cloud Technologies Lab 3

def value_split(value):
    return value.split(';')[2:7]


def create_vcard_object(street, city, region, code, country):
    import vobject

    address = vobject.vcard.Address(
        street=street or '',
        city=city or '',
        region=region or '',
        code=code or '',
        country=country or ''
    )
    return address


# * This function finds all collections objects, and parses it from json to vcard
def json_parser():

    import vobject
    import json
    from database import collection

    # Load the JSON object from the MongoDB collection
    data = list(collection.find())

    # Create a vCard object
    vcard = vobject.vCard()

    # Create empty vcard object list
    vcards = []

    # Set the properties that need to be mapped between MongoDB and vCard formats
    properties = {
        'birthday': 'birthday',
        'version': 'version',
        'name': 'name',
        'first name': 'fn',
        'organisation': 'org',
        'telefon': 'tel',
        'email': 'email',
        'address': 'adr',
    }

    # Loop through the items in data
    for item in data:
        # Create a vCard object
        vcard = vobject.vCard()

        # Set the properties from the MongoDB data
        for mongo_property, vcard_property in properties.items():
            value = item.get(mongo_property, f'No {vcard_property.capitalize()}')
            if mongo_property == 'address' and value:
                street, city, region, code, country = value_split(value)
                address = create_vcard_object(street, city, region, code, country)
                vcard.add(vcard_property).value = address
            else:
                vcard.add(vcard_property).value = value

        # Add the vCard to the list
        vcards.append(vcard)

    # Serialize the vCards to a list of strings in
    vcard_str_list = [vcard.serialize() for vcard in vcards]

    # Combine the vCard strings into a single JSON string
    # Source: https://docs.python.org/3/library/json.html
    vcards_json = json.dumps(vcard_str_list, indent=2)

    # Return the output so we can access it in the API
    return {"message" : vcards_json}
