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
collection = db['binanceUsers']

headers = {
    'authority': 'www.binance.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'clienttype': 'web',
    'content-type': 'application/json',
    'lang': 'en',
    'origin': 'https://www.binance.com',
    'referer': 'https://www.binance.com/en/copy-trading',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-passthrough-token': '',
}

json_data = {
    'pageNumber': 2,
    'pageSize': 18,
    'timeRange': '90D',
    'dataType': 'ROI',
    'favoriteOnly': False,
    'hideFull': False,
    'nickname': '',
    'order': 'DESC',
}

def extractdata(page):
    headers['user-agent']=ua.random
    json_data['pageNumber']=page
    response = requests.post('https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/home-page/query-list',headers=headers,json=json_data, verify=False)
    response=response.json()
    for each_data in response['data']['list']:
        each_data['updateAt']=datetime.utcnow()
        collection.update_one({"leadPortfolioId":each_data['leadPortfolioId']}, {'$set': each_data}, upsert=True)
        print(each_data)


for i in tqdm(range(1,90)):
    try:
        extractdata(i)
    except Exception as e:
        print(e)
    time.sleep(random.uniform(10,20))
