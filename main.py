# Imports
import json
import os
import pymongo
import database

from flask import Flask, render_template, request, jsonify, send_file, make_response
from bson.objectid import ObjectId
from flask_cors import CORS

# Database
from database import db
from database import collection

# Parse functions
from json_to_vcard_parser import json_parser
from json_to_vcard_id_parser import json_id_parser

# Set the flask app
app = Flask(__name__)

# Make the app accept all requests
CORS(app, resources={r"/*": {"origins": "*"}})


# * POST route '/contacts' endpoint - Get the parsed file from the cacheAPI, and then insert it to the mainAPI database.
@app.route('/contacts', methods=['POST'])
def new_contact():
    # Security key
    key = request.headers.get('X-API-Key')
    #print(key)

    # Check if the key matches the hardcoded key from cacheAPI
    if key != 'post-key':
        return {'message': 'Wrong security key, try again!'}, 401

    # Load the JSON data from the request body
    file_data = request.json
    # print(file_data)

    # Push the data to the mainAPI database
    if isinstance(file_data, list):
        collection.insert_many(file_data)
    else:
        collection.insert_one(file_data)

    # Return a success message
    return {'message': 'Correct security key: Data uploaded successfully!'}, 200


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
        # Find all in the database, and parses it from json back to vcard format.
        json_parser()  # Runs when we type in the route in Postman
        
        # Saves the output
        vcards_json = json_parser()

        # Return the output
        return jsonify(vcards_json), 200


# * GET route '/contacts' endpoint - Show all contacts (json)
@app.route('/contacts', methods=['GET'])
def getAllContacts():
    # Security key
    key = request.headers.get('X-API-Key')
    #print(key)

    # Check if the key matches the hardcoded key from cacheAPI
    if key != 'get-key':
        return {'message': 'Wrong security key, try again!'}, 401
    else:
        result = collection.find()
        return f' {(list(result))}'


# * GET route '/contacts/<id>' - Shows one contact based on id (json)
@app.route('/contacts/<id>', methods=['GET'])
def getContacts(id):
    # Security key
    key = request.headers.get('X-API-Key')
    
    # Check if the key matches the hardcoded key from cacheAPI
    if key != 'get-id-key':
        return {'message': 'Wrong security key, try again!'}, 401
    else:
        result = collection.find_one({"_id": ObjectId(id)})
        return f'{result}'


# * GET route '/contacts/id/vcard' (vcard) – Parses one contact (based on id) in json back to vcf, and returns the parsed output.
@app.route('/contacts/<id>/vcard', methods=['GET'])
def getVCardId(id):
    # Security key
    key = request.headers.get('X-API-Key')
    
    # Check if the key matches the hardcoded key from cacheAPI
    if key != 'get-id-key':
        return {'message': 'Wrong security key, try again!'}, 401
    else:
        json_id_parser(id)
        vcards_id_json = json_id_parser(id)
        return jsonify(vcards_id_json)


# Run the mainAPI app on port 3000
app.run(port=3000)
