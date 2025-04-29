from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r'/*': {'origins': '*'}})

mongodb_client = PyMongo(app, uri="mongodb+srv://hyu:3257@cluster-test.2rqcp.mongodb.net/?retryWrites=true&w=majority")
db = mongodb_client.db

from app import routes
