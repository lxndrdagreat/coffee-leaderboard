# database.py
from pymongo import MongoClient

from coffee_leaderboard import app

db_client = MongoClient()
db = db_client.coffee

# handle database authentication
if 'DATABASE_USERNAME' in app.config and len(app.config['DATABASE_USERNAME']) > 0:
    db.authenticate(app.config['DATABASE_USERNAME'], app.config['DATABASE_PASSWORD'])
