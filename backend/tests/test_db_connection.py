from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')

# Add these options to the connection string
client = MongoClient(
    mongodb_uri,
    server_api=ServerApi('1'),
    socketTimeoutMS=10000,
    connectTimeoutMS=10000,
    serverSelectionTimeoutMS=10000,
    retryWrites=True,
    tls=True,
    tlsAllowInvalidCertificates=False
)

try:
    # Use a shorter timeout for the initial connection test
    client.admin.command('ping', serverSelectionTimeoutMS=5000)
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # Print the actual URI (with password hidden)
    uri_parts = mongodb_uri.split('@')
    if len(uri_parts) > 1:
        print(f"URI format: mongodb+srv://<username>:<password>@{uri_parts[1]}")