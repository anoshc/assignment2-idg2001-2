# Import modules
from flask import Flask, render_template, request, jsonify, send_file, make_response
import json
# import html
import os
# import bson
# import vobject

# Import files
# import database
# import vcard_to_json_parser
# import json_to_vcard_parser
# import json_to_vcard_id_parser

# Imported functions from files
# from database import db
from database import collection
from bson.objectid import ObjectId
from vcard_to_json_parser import vcard_parser
from json_to_vcard_parser import json_parser
from json_to_vcard_id_parser import json_id_parser

# Set the flask app
app = Flask(__name__)


# * HOME route – Render the HTML form to the page
@app.route('/')
def render_form():
    return render_template('index.html')


# * POST route '/contacts' endpoint - Get the uploaded vcf-file, parses it to JSON, and pushes it to the database.
@app.route('/contacts', methods=['POST'])
def new_contact():
    # Retrive the uploaded file from the html form
    if request.method == 'POST':
        uploaded_file = request.files['file']
        # If the file is NOT empty, do this:
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)  # Saves the file
            vcard_parser(uploaded_file.filename)  # Parsing the file to JSON
            os.remove(uploaded_file.filename)  # Remove the vcf file locally
            return 'File read successfully and uploaded to database!'
        else:
            return 'Could not read file, try again.'  # In case of error

    # Push the file to the database
    with open('data.json') as data:
        file_data = json.load(data)
        if isinstance(file_data, list):
            collection.insert_many(file_data)
        else:
            collection.insert_one(file_data)
        return jsonify(file_data)


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


# * GET route '/contacts/vcard' (vcard) – Parses the contacts in json back to vcf, and shows all contacts in vcf.
@app.route('/contacts/vcard', methods=['GET'])
def getVCard():
    # Find all in the database, and parses it from json back to vcard format.
    json_parser()  # Runs when we type in the route in Postman
    # Saves the output
    vcards_json = json_parser()
    # Return the output
    return jsonify(vcards_json)  # Pushes the json to the Postman output


# * GET route '/contacts/id/vcard' (vcard) – Parses one contact (based on id) in json back to vcf, and shows that one contact in vcf.
@app.route('/contacts/<id>/vcard', methods=['GET'])
def getVCardId(id):
    json_id_parser(id)
    vcards_id_json = json_id_parser(id)
    return jsonify(vcards_id_json)


# Run the app on port 3000
app.run(port=3000)
