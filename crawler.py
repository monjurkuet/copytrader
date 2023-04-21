import platform
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import mysql.connector
import json
import time

#detect platform
SYSTEM_OS=platform.system()
#global variables
LEADERBOARD_URL='https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank'
POSITION_URL='https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getPositionStatus'
PROXY=False
LEADERBOARD_TIME_OPTIONS=['Daily','Weekly','Monthly','Total']

# xpath
LEADERBOARD_TIME_XPATH='//div[text()="Time"]/following::*//input'
LEADERBOARD_NEXT_PAGE_XPATH='//button[@aria-label="Next page"]'

def jsclick(xpth):
    try: 
        element=driver.find_element('xpath',xpth)
        driver.execute_script("arguments[0].click();", element)
    except:
        pass  

def tor_browser():
    options = uc.ChromeOptions() 
    if PROXY==True:
        options.add_argument(f'--proxy-server=socks5://127.0.0.1:9050')
    caps = options.to_capabilities()
    caps['goog:loggingPrefs'] = {'performance': 'ALL'} 
    if SYSTEM_OS=='Linux':
        return uc.Chrome(user_data_dir="/home/copytraderscrapingprofile",browser_executable_path='/usr/bin/brave-browser',headless=False,version_main=111,options=options,desired_capabilities=caps) 
    elif SYSTEM_OS=='Windows':
        return uc.Chrome(user_data_dir="G:\\copytraderscrapingprofile",browser_executable_path='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',headless=False,version_main=111,options=options,use_subprocess=True,desired_capabilities=caps)      

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

def extract_json_from_log(log,driver):
    request_id = log["params"]["requestId"]
    resp_url = log["params"]["response"]["url"]
    response_body=driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
    response_json=json.loads(response_body['body'])
    return response_json

def extract_baseinfo(leaderboard_data):
    #mysql connection
    connection = mysql.connector.connect(#host='localhost', 
                                host='161.97.97.183',
                                database='exchangetrading',
                                user='root', 
                                password='$C0NTaB0vps8765%%$#', 
                                port=3306
                                ,auth_plugin='caching_sha2_password')
    cursor = connection.cursor() 
    #iterate each item in loop
    for each_baseinfo in leaderboard_data:
        encryptedUid=each_baseinfo['encryptedUid']
        followerCount=each_baseinfo['followerCount']
        nickName=each_baseinfo['nickName']
        twitterUrl=each_baseinfo['twitterUrl']
        userPhotoUrl=each_baseinfo['userPhotoUrl']
        # mysql data insert
        sql_insert_with_param = """REPLACE INTO BaseInfo
                            (encryptedUid,followerCount,nickName,twitterUrl,userPhotoUrl) 
                            VALUES (%s,%s,%s,%s,%s);""" 
        data_tuple = (encryptedUid,followerCount,nickName,twitterUrl,userPhotoUrl)
        cursor.execute(sql_insert_with_param, data_tuple)
        connection.commit() 
        print(data_tuple)
    connection.close()

if __name__ == "__main__":
    driver=tor_browser()
    # crawl leaderboard
    driver.get('https://www.binance.com/en/futures-activity/leaderboard/futures')
    encryptedUid_list=[]
    for each_option in LEADERBOARD_TIME_OPTIONS:
        # click time dropdown filter
        jsclick(LEADERBOARD_TIME_XPATH)
        time.sleep(5)
        button_xpath=f'//div[text()="{each_option}"]'
        jsclick(button_xpath)
        time.sleep(10)
        # fetch data from api response
        logs_raw = driver.get_log("performance")     
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        LEADERBOARD_log=clean_logs(logs,LEADERBOARD_URL)
        if LEADERBOARD_log is not None:
            response_body=extract_json_from_log(LEADERBOARD_log,driver)
            leaderboard_data=response_body['data']
            extract_baseinfo(leaderboard_data)
        # check position data
        while True:
            POSITION_log=clean_logs(logs,POSITION_URL)
            if POSITION_log is not None:
                response_body=extract_json_from_log(POSITION_log,driver)
                position_data=response_body['data']
                for each_postion in position_data:
                    if each_postion['hasPosition']==True:
                        encryptedUid=each_postion['encryptedUid']
                        encryptedUid_list.append(encryptedUid)
                        print(encryptedUid)
            jsclick(LEADERBOARD_NEXT_PAGE_XPATH)
            time.sleep(10)
            logs_raw = driver.get_log("performance")   
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
            POSITION_log=clean_logs(logs,POSITION_URL)
            if POSITION_log is None:
                break

    