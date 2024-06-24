import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

URI = ("mongodb+srv://vladislavputintsev:7%23%237fF%2ANACDPv6W@cluster0.yqxzmo3.mongodb.net/?retryWrites=true&w"
       "=majority&appName=Cluster0")
CLIENT = MongoClient(URI, server_api=ServerApi('1'))
DB = CLIENT.quotes
collection_authors = DB.authors
collection_quotes = DB.quotes

with open('authors.json') as file:
    data_authors = json.load(file)

if isinstance(data_authors, list):
    collection_authors.insert_many(data_authors)  # For a list of documents
else:
    collection_authors.insert_one(data_authors)   # For a single document

with open('quotes.json') as file:
    data_quotes = json.load(file)

if isinstance(data_quotes, list):
    collection_quotes.insert_many(data_quotes)  # For a list of documents
else:
    collection_quotes.insert_one(data_quotes)   # For a single document

