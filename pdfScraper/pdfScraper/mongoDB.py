from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
if __name__ == "__main__":
    uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0aws.ev9ut.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0AWS"
    client = MongoClient(uri)
    db = client['testDB']
    collection = db['pdfScraper']
    document = {"name": "John", "age": 30}
    result = collection.insert_one(document)
    print(result.inserted_id)
    
    

