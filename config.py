import pymongo
import certifi


mongo_url = "mongodb+srv://FSDI:tecGithub18@cluster0.lqyon.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url, tlsCAFile=certifi.where())

db = client.get_database("neopil")