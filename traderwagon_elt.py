from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import pandas as pd

client = MongoClient('mongodb://myUserAdmin:%24C0NTaB0vps8765%25%25%24%23@161.97.97.183:27017/?authMechanism=DEFAULT')
db = client['exchanges']
collection = db['traderwagonSearch']

start = datetime.now()
end = start- timedelta(days = 1)

traderwagonPositions = db['traderwagonPositions'].find({"created_at": {"$gte": start, "$lt": end}})
traderwagonPositions=[data for data in db['traderwagonPositions'].find()]
traderwagonSearch = db['traderwagonSearch'].find({"created_at": {"$gte": start, "$lt": end}})
traderwagonSearch=[data for data in db['traderwagonSearch'].find()]

for item in a + b:
    d[item['id']].update(item)
list(d.values())