import seleniumwire.undetected_chromedriver as uc
from seleniumwire.utils import decode
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
from tqdm import tqdm

def jsclick(xpth):
    try: 
        element=driver.find_element('xpath',xpth)
        driver.execute_script("arguments[0].click();", element)
    except:
        pass  

def extractReadltimeData(driver,portfolioId):
    # Access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            if POSITIONS_API in request.url and request.response.status_code==200:
                #request_payload=eval(request.body)
                response_content=eval(decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8'))
                break
    data=response_content['data']
    for each_data in data:
        each_data['updateAt']=datetime.utcnow()
        each_data['portfolioId']=portfolioId
        collection.update_one({"portfolioId":portfolioId}, {'$set': each_data}, upsert=True)
        print(portfolioId)

# xpath
POSTFOLIO_LIST='//div[text()="Portfolio List"]'
NEXTBUTTON='//button[@aria-label="Next page"]'
# URLS
POSITIONS_API='https://www.traderwagon.com/v1/friendly/social-trading/lead-portfolio/get-position-info/'
# global variables
null=None
true=True
false=False

client = MongoClient('mongodb://localhost:27017/') 
db = client['exchanges']
collection = db['traderwagonPositions']

# Calculate the time threshold for the last 24 hours
current_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

# Query MongoDB to find documents with 'updatedAt' within the last 24 hours
query = {
    'updateAt': {
        '$gte': current_time
    }
}

# Fetch documents and extract portfolioId values
cursor = db['traderwagonSearch'].find(query)
portfolio_ids = [doc['portfolioId'] for doc in cursor if float(doc['data']['allRoi'])>0]

driver=uc.Chrome()
driver.get('https://www.traderwagon.com/en')

for portfolioId in tqdm(portfolio_ids):
    try:
        driver.get(f'https://www.traderwagon.com/en/portfolio/{portfolioId}')
        time.sleep(5)
        extractReadltimeData(driver,portfolioId)
    except Exception as e:
        print(e)
    del driver.requests

driver.close()
driver.quit()