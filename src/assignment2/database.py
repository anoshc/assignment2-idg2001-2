from pymongo import MongoClient
from dotenv import dotenv_values


# Set the mongo uri
config = dotenv_values('.env')
mongo_uri = config['MONGO_URI']
client = MongoClient(mongo_uri)

# Find the database and collection
db = client['vCardDB-1']
collection = db['vCard1']

# Find all documents in collection
documents = collection.find({})
for document in documents:
    print(document)

# test
