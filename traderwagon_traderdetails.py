import seleniumwire.undetected_chromedriver as uc
from seleniumwire.utils import decode
import time,random,os,platform,os
from pymongo import MongoClient
from datetime import datetime

def jsclick(xpth):
    try: 
        element=driver.find_element('xpath',xpth)
        driver.execute_script("arguments[0].click();", element)
    except:
        pass  

def newBrowser():
    if SYSTEM_OS=='Windows':
        user_data_dir="G:\\copytraderscrapingprofile2"
        browser_executable_path='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    if SYSTEM_OS=='Linux':
        user_data_dir=f"/home/{CURRENTUSER}/copytraderscrapingprofile2"
        browser_executable_path='/usr/bin/brave-browser'
    driver=uc.Chrome(user_data_dir=user_data_dir,
                     browser_executable_path=browser_executable_path,
                     headless=False,seleniumwire_options={
        'proxy': {
            'http': "http://45.85.147.136:24003",
            'https': "http://45.85.147.136:24003"
                }
            })
    return driver

def extractReadltimeData(driver,portfolioId):
    # Access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            if POSITIONS_API in request.url and request.response.status_code==200:
                #request_payload=eval(request.body)
                response_content=eval(decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8'))
                break
    data=response_content['data']
    each_data={'data':data,'updateAt':datetime.now()}
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
SYSTEM_OS=platform.system()
CURRENTUSER=os.environ['USER']
client = MongoClient('mongodb://myUserAdmin:%24C0NTaB0vps8765%25%25%24%23@161.97.97.183:27017/?authMechanism=DEFAULT')
db = client['exchanges']
collection = db['traderwagonPositions']

portfolioId_List=[]
for data in db['traderwagonSearch'].find():
    portfolioId_List.append(data['portfolioId'])
print(f'Total : {len(portfolioId_List)} Accounts to crawl')

driver=newBrowser()
driver.get('https://www.traderwagon.com/en')
for portfolioId in portfolioId_List:
    try:
        driver.get(f'https://www.traderwagon.com/en/portfolio/{portfolioId}')
        time.sleep(2)
        extractReadltimeData(driver,portfolioId)
    except Exception as e:
        print(e)
    del driver.requests

driver.close()
driver.quit()