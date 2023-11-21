import seleniumwire.undetected_chromedriver as uc
from seleniumwire.utils import decode
import time,getpass,os,platform,os
from pymongo import MongoClient
from datetime import datetime

# xpath
POSTFOLIO_LIST='//div[text()="Portfolio List"]'
NEXTBUTTON='//button[@aria-label="Next page"]'
# URLS
SEARCH_API='https://www.traderwagon.com/v1/friendly/social-trading/lead/list-active-portfolio'
# global variables
null=None
true=True
false=False
SYSTEM_OS=platform.system()
CURRENTUSER=getpass.getuser()
client = MongoClient('mongodb://localhost:27017/')
db = client['exchanges']
collection = db['traderwagonSearch']


def jsclick(xpth):
    try: 
        element=driver.find_element('xpath',xpth)
        driver.execute_script("arguments[0].click();", element)
    except:
        pass  

def newBrowser():
    driver=uc.Chrome(
                     headless=False,seleniumwire_options={
        'proxy': {
            'http': "http://45.85.147.136:24003",
            'https': "http://45.85.147.136:24003"
                }
            })
    return driver

def extractReadltimeData(driver):
    # Access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            if request.url==SEARCH_API and request.response.status_code==200:
                #request_payload=eval(request.body)
                response_content=eval(decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8'))
                break
    data=response_content['data']
    for each_data in data:
        try:
            portfolioId=each_data['portfolioId']
            each_data={'data':each_data,'updateAt':datetime.now()}
            collection.update_one({"portfolioId":portfolioId}, {'$set': each_data}, upsert=True)
            print(each_data)
        except Exception as e:
            print(e)


driver=newBrowser()

driver.get('https://www.traderwagon.com/en')
time.sleep(5)
jsclick('//button[text()="Skip"]')
time.sleep(5)
jsclick(POSTFOLIO_LIST)
while True:
    try:
        time.sleep(10)
        extractReadltimeData(driver)
        del driver.requests
        jsclick(NEXTBUTTON)
    except Exception as e:
        print(e)
        break

driver.close()
driver.quit()