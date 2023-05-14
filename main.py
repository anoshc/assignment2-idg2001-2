# Import modules
from flask import Flask, render_template, request, jsonify, send_file, make_response
import json
# import html
import os
import pymongo
from flask_cors import CORS
# import bson
# import vobject

# Import files
import database
# import vcard_to_json_parser
# import json_to_vcard_parser
# import json_to_vcard_id_parser

# Imported functions from files
from database import db
from database import collection
from bson.objectid import ObjectId
from vcard_to_json_parser import vcard_parser
from json_to_vcard_parser import json_parser
from json_to_vcard_id_parser import json_id_parser

# Set the flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


# * HOME route – Render the HTML form to the page
@app.route('/')
def render_form():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def render_test():
    # Get the request data
    data = request.json
    name = data.get('name')

    # Push the data to the collection
    result = collection.insert_one({'name': name})
    return jsonify({'message': f'Data added with id {result.inserted_id}'})


# * POST route '/contacts' endpoint - Get the parsed to json file from the cacheAPI, and then insert it to the mainAPI database.
@app.route('/contacts', methods=['POST'])
def new_contact():
    # Security key
    key = request.headers.get('X-API-Key')
    #print(key)

    # Check if the key matches the hardcoded key from cacheAPI
    if key != 'post-key':
        return {'message': 'Wrong security key, try again!'}, 401
    else:
        return {'message': 'Correct security key!'}, 200

    # Load the JSON data from the request body
    file_data = request.json
    print(file_data)

    # Push the data to the mainAPI database
    if isinstance(file_data, list):
        collection.insert_many(file_data)
    else:
        collection.insert_one(file_data)

    # Return a success message
    return {'message': 'Data uploaded successfully'}


# * GET route '/contacts/vcard' (vcard) – Parses the contacts in json back to vcf, and shows all contacts in vcf.
@app.route('/contacts/vcard', methods=['GET'])
def getVCard():
    # Security key
    key = request.headers.get('X-API-Key')
    #print(key)

    # Check if the key matches the hardcoded key from cacheAPI
    if key != 'get-key':
        return {'message': 'Wrong security key, try again!'}, 401
    else:
        return {'message': 'Correct security key!'}, 200

    # Find all in the database, and parses it from json back to vcard format.
    json_parser()  # Runs when we type in the route in Postman
    # Saves the output
    vcards_json = json_parser()
    # Return the output
    return jsonify(vcards_json)  # Pushes the json to the Postman output


# * GET route '/contacts' endpoint - Show all contacts (json)
@app.route('/contacts', methods=['GET'])
def getAllContacts():
    result = collection.find()
    return f' {(list(result))}'


# * GET route '/contacts/<id>' - Shows one contact based on id (json)
@app.route('/contacts/<id>', methods=['GET'])
def getContacts(id):
    result = collection.find_one({"_id": ObjectId(id)})
    return f'{result}'



# * GET route '/contacts/id/vcard' (vcard) – Parses one contact (based on id) in json back to vcf, and shows that one contact in vcf.
@app.route('/contacts/<id>/vcard', methods=['GET'])
def getVCardId(id):
    json_id_parser(id)
    vcards_id_json = json_id_parser(id)
    return jsonify(vcards_id_json)


# Run the app on port 3000
app.run(port=3000)
