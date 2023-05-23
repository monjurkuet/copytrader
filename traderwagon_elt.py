from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import pandas as pd
from collections import defaultdict

client = MongoClient('mongodb://myUserAdmin:%24C0NTaB0vps8765%25%25%24%23@161.97.97.183:27017/?authMechanism=DEFAULT')
db = client['exchanges']
collection = db['traderwagonSearch']

start = datetime.now()
end = start- timedelta(days = 1)

traderwagonPositions = db['traderwagonPositions'].find({"created_at": {"$gte": start, "$lt": end}})
traderwagonPositions=[data for data in db['traderwagonPositions'].find()]
for i in traderwagonPositions:
    i['positiondata'] = i.pop('data')
traderwagonSearch = db['traderwagonSearch'].find({"created_at": {"$gte": start, "$lt": end}})
traderwagonSearch=[data for data in db['traderwagonSearch'].find()]
for i in traderwagonSearch:
    i['performancedata'] = i.pop('data')

d = defaultdict(dict)
for item in traderwagonSearch + traderwagonPositions:
    d[item['portfolioId']].update(item)

dd=[i for i in list(d.values()) if i!={}]
final=[]
for item in dd:
    try:
        if item['positiondata']!=[]:
            print(item['positiondata'])
            final.append(item)
    except:
        pass