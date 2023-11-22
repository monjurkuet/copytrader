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
collection = db['binancePositions']

headers = {
    'authority': 'www.binance.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'clienttype': 'web',
    'content-type': 'application/json',
    'lang': 'en',
    'referer': 'https://www.binance.com/en/copy-trading/lead-details',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

params = {
    'portfolioId': '3674713871828527105',
}

def extractdata(leadPortfolioId):
    headers['user-agent']=ua.random
    params['portfolioId']=leadPortfolioId
    response = requests.get('https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-data/positions',params=params,headers=headers)
    response=response.json()
    for each_data in response['data']:
        if float(each_data['entryPrice'])>0:
            each_data['updateAt']=datetime.utcnow()
            collection.update_one({"leadPortfolioId":leadPortfolioId,"symbol":each_data['symbol']}, {'$set': each_data}, upsert=True)
            print(each_data)

# Calculate the time threshold for the last 24 hours
current_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
# Query MongoDB to find documents with 'updatedAt' within the last 24 hours
query = {
    'updateAt': {
        '$gte': current_time
    },
    'roi': {'$gt': 5}
}

while True:
    # Fetch documents and extract portfolioId values
    portfolio_ids = db['binanceUsers'].distinct('leadPortfolioId', query)
    #loop through and extract data
    for leadPortfolioId in tqdm(portfolio_ids):
        try:
            extractdata(leadPortfolioId)
        except Exception as e:
            print(e)
        time.sleep(5)
    time.sleep(random.uniform(60,180))
