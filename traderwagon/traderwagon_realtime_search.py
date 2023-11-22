import requests
import time
from pymongo import MongoClient
from datetime import datetime
from fake_useragent import UserAgent
import random
from tqdm import tqdm

ua = UserAgent()
#database connection
client = MongoClient('mongodb://localhost:27017/')
db = client['exchanges']
collection = db['traderwagonPositions']

def extractReadltimeData(portfolioId):
    response = requests.get(f'https://www.traderwagon.com/v1/friendly/social-trading/lead-portfolio/get-position-info/{portfolioId}',
                headers={'user-agent':ua.random})
    data=response.json()['data']
    for each_data in data:
        each_data['updateAt']=datetime.utcnow()
        each_data['portfolioId']=portfolioId
        collection.update_one({"portfolioId":portfolioId,'symbol':each_data['symbol']}, {'$set': each_data}, upsert=True)
        print(each_data)

# Calculate the time threshold for the last 24 hours
current_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
# Query MongoDB to find documents with 'updatedAt' within the last 24 hours
query = {
    'updateAt': {
        '$gte': current_time
    }
}

while True:
    # Fetch documents and extract portfolioId values
    portfolio_ids = collection.distinct('portfolioId', query)
    #loop through and extract data
    for portfolioId in tqdm(portfolio_ids):
        try:
            extractReadltimeData(portfolioId)
        except Exception as e:
            print(e)
        time.sleep(5)
    time.sleep(random.uniform(60,180))
