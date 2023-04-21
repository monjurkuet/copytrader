import platform
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import mysql.connector
import json

#detect platform
SYSTEM_OS=platform.system()
LEADERBOARD_URL='https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank'

def tor_browser():
    options = uc.ChromeOptions() 
    options.add_argument(f'--proxy-server=socks5://127.0.0.1:9050')
    caps = options.to_capabilities()
    caps['goog:loggingPrefs'] = {'performance': 'ALL'} 
    if SYSTEM_OS=='Linux':
        return uc.Chrome(user_data_dir="/home/copytraderscrapingprofile",browser_executable_path='/usr/bin/brave-browser',headless=False,version_main=111,options=options,desired_capabilities=caps) 
    elif SYSTEM_OS=='Windows':
        return uc.Chrome(user_data_dir="G:\\copytraderscrapingprofile",browser_executable_path='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',headless=False,version_main=111,options=options,use_subprocess=True,desired_capabilities=caps)      

def extract_position_data(log,driver):
    request_id = log["params"]["requestId"]
    resp_url = log["params"]["response"]["url"]
    response_body=driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
    response_body=json.loads(response_body['body'])
    return response_body

def clean_logs(logs,target_url):
    cleaned_log=None
    for log in logs:
        try:
            resp_url = log["params"]["response"]["url"]
            if resp_url==target_url:
                cleaned_log=log
                return cleaned_log
        except:
            pass   

def extract_leaderboard_data(log,driver):
     request_id = log["params"]["requestId"]
     resp_url = log["params"]["response"]["url"]
     response_body=driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
     response_body=json.loads(response_body['body'])
     return response_body

if __name__ == "__main__":
    driver=tor_browser()
    driver.get('https://www.binance.com/en/futures-activity/leaderboard/futures')
    logs_raw = driver.get_log("performance")     
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    logs=clean_logs(logs,LEADERBOARD_URL)
    if logs is not None:
        response_body=extract_leaderboard_data(logs,driver)
        data=response_body['data']
    