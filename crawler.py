import platform
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import mysql.connector
import json
import time
import random

<<<<<<< HEAD
proxies = {
   'http': 'http://127.0.0.1:16379',
   'https': 'http://127.0.0.1:16379',
}

=======
#detect platform
SYSTEM_OS=platform.system()
#global variables
LEADERBOARD_URL='https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank'
POSITION_URL='https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getPositionStatus'
POSITION_DETAILS_URL='https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition'
PERFORMANCE_URL='https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherPerformance'
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

>>>>>>> abf7a5659227d9e8898f440caa4e7aff0f910ca7
def tor_browser():
<<<<<<< HEAD
   options = uc.ChromeOptions() 
   options.add_argument(f'--proxy-server=http://127.0.0.1:16379')
   #options.user_data_dir = "/home/chromeprofileforbots"  
   #return uc.Chrome(user_data_dir="/home/chromeprofileforbots",options=options,version_main=109)  
   return uc.Chrome(user_data_dir="/home/copytraderscrapingprofile",browser_executable_path='/usr/bin/brave-browser',headless=False,version_main=111,options=options)      
=======
    options = uc.ChromeOptions() 
    if PROXY==True:
        options.add_argument(f'--proxy-server=socks5://127.0.0.1:9050')
    caps = options.to_capabilities()
    caps['goog:loggingPrefs'] = {'performance': 'ALL'} 
    if SYSTEM_OS=='Linux':
        return uc.Chrome(user_data_dir="/home/copytraderscrapingprofile",browser_executable_path='/usr/bin/brave-browser',headless=False,version_main=111,options=options,desired_capabilities=caps) 
    elif SYSTEM_OS=='Windows':
        return uc.Chrome(user_data_dir="G:\\copytraderscrapingprofile",browser_executable_path='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',headless=False,version_main=111,options=options,use_subprocess=True,desired_capabilities=caps)      
>>>>>>> abf7a5659227d9e8898f440caa4e7aff0f910ca7

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

def extract_position_data(encryptedUid_list):
    for encryptedUid in encryptedUid_list:
        url='https://www.binance.com/en/futures-activity/leaderboard/user/um?encryptedUid='+ encryptedUid
        driver.get(url)   
        time.sleep(10)
        logs_raw = driver.get_log("performance")  
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        POSTION_DETAILS_log=clean_logs(logs,POSITION_DETAILS_URL)
        if POSTION_DETAILS_log is not None:
            connection = mysql.connector.connect(#host='localhost', 
                                    host='161.97.97.183',
                                    database='exchangetrading',
                                    user='root', 
                                    password='$C0NTaB0vps8765%%$#', 
                                    port=3306
                                    ,auth_plugin='caching_sha2_password')
            cursor = connection.cursor() 
            response_body=extract_json_from_log(POSTION_DETAILS_log,driver)
            data=response_body['data']
            if data['otherPositionRetList'] is not None:
                for each_position in data['otherPositionRetList']:
                    amount=each_position['amount']
                    entryPrice=each_position['entryPrice']
                    leverage=each_position['leverage']
                    markPrice=each_position['markPrice']
                    pnl=each_position['pnl']
                    roe=each_position['roe']
                    symbol=each_position['symbol']
                    updateTimeStamp=each_position['updateTimeStamp']
                    sql_insert_with_param = """REPLACE INTO binance_positions
                          (amount,entryPrice,leverage,markPrice,pnl,roe,symbol,updateTimeStamp,encryptedUid) 
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);""" 
                    data_tuple = (amount,entryPrice,leverage,markPrice,pnl,roe,symbol,updateTimeStamp,encryptedUid)
                    cursor.execute(sql_insert_with_param, data_tuple)
                    connection.commit() 
                    print(data_tuple)
            connection.close()
        PERFORMANCE_DETAILS_log=clean_logs(logs,PERFORMANCE_URL)
        if PERFORMANCE_DETAILS_log is not None:
            response_body=extract_json_from_log(PERFORMANCE_DETAILS_log,driver)
            performance_dictionary=response_body['data']
            extract_performancedata(performance_dictionary,encryptedUid)    

def extract_performancedata(performance_dictionary,encryptedUid):
    lastTradeTime=performance_dictionary['lastTradeTime']
    connection = mysql.connector.connect(#host='localhost', 
                                host='161.97.97.183',
                                database='exchangetrading',
                                user='root', 
                                password='$C0NTaB0vps8765%%$#', 
                                port=3306
                                ,auth_plugin='caching_sha2_password')
    cursor = connection.cursor() 
    YEARLY_ROI =0
    YEARLY_PNL=0
    for each_period in performance_dictionary['performanceRetList']:
        if each_period['periodType']=='DAILY' and each_period['statisticsType']=='ROI':
            DAILY_ROI= each_period['value']
        if each_period['periodType']=='DAILY' and each_period['statisticsType']=='PNL':
            DAILY_PNL= each_period['value']
        if each_period['periodType']=='WEEKLY' and each_period['statisticsType']=='ROI':
            WEEKLY_ROI= each_period['value']
        if each_period['periodType']=='WEEKLY' and each_period['statisticsType']=='PNL':
            WEEKLY_PNL= each_period['value']
        if each_period['periodType']=='MONTHLY' and each_period['statisticsType']=='ROI':
            MONTHLY_ROI = each_period['value']
        if each_period['periodType']=='MONTHLY' and each_period['statisticsType']=='PNL':
            MONTHLY_PNL = each_period['value']
        if each_period['periodType']=='YEARLY' and each_period['statisticsType']=='ROI':
            YEARLY_ROI = each_period['value']
        if each_period['periodType']=='YEARLY' and each_period['statisticsType']=='PNL':
            YEARLY_PNL = each_period['value']        
        if each_period['periodType']=='ALL' and each_period['statisticsType']=='ROI':
            ALL_ROI = each_period['value']
        if each_period['periodType']=='ALL' and each_period['statisticsType']=='PNL':
            ALL_PNL = each_period['value']     
    # mysql insert  
    sql_insert_with_param = """REPLACE INTO binance_performance
                        (DAILY_ROI,DAILY_PNL,WEEKLY_ROI,WEEKLY_PNL,MONTHLY_ROI,MONTHLY_PNL,YEARLY_ROI,YEARLY_PNL,ALL_ROI,ALL_PNL,encryptedUid,lastTradeTime) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""" 
    data_tuple = (DAILY_ROI,DAILY_PNL,WEEKLY_ROI,WEEKLY_PNL,MONTHLY_ROI,MONTHLY_PNL,YEARLY_ROI,YEARLY_PNL,ALL_ROI,ALL_PNL,encryptedUid,lastTradeTime)
    cursor.execute(sql_insert_with_param, data_tuple)
    connection.commit() 
    print(data_tuple)

if __name__ == "__main__":
<<<<<<< HEAD
    gmaps_urls=geturls()
    a=driver.execute_script("""
    fetch('https://www.traderwagon.com/v1/friendly/social-trading/lead/list-active-portfolio', {
  method: 'POST',
  headers: {
    'authority': 'www.traderwagon.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
    'bnc-uuid': '4d6d58b8-1c2c-45d0-aec8-20be7a30ed5b',
    'clienttype': 'web',
    'content-type': 'application/json',
    'cookie': 'bnc-uuid=4d6d58b8-1c2c-45d0-aec8-20be7a30ed5b; _ga=GA1.2.515105667.1680811157; _gid=GA1.2.631361189.1680811157; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221875826f1b428d-0ff714940d342f-76574611-1049088-1875826f1b5500%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.binance.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3NTgyNmYxYjQyOGQtMGZmNzE0OTQwZDM0MmYtNzY1NzQ2MTEtMTA0OTA4OC0xODc1ODI2ZjFiNTUwMCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221875826f1b428d-0ff714940d342f-76574611-1049088-1875826f1b5500%22%7D; _gat=1',
    'csrftoken': 'd41d8cd98f00b204e9800998ecf8427e',
    'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6Ijc2OCwxMzY2IiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiNjc0LDEzNjYiLCJzeXN0ZW1fdmVyc2lvbiI6IkxpbnV4IHg4Nl82NCIsImJyYW5kX21vZGVsIjoidW5rbm93biIsInN5c3RlbV9sYW5nIjoiZW4tR0IiLCJ0aW1lem9uZSI6IkdNVCs2IiwidGltZXpvbmVPZmZzZXQiOi0zNjAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTMuMC4wLjAgU2FmYXJpLzUzNy4zNiBFZGcvMTEzLjAuMC4wIiwibGlzdF9wbHVnaW4iOiJQREYgVmlld2VyLENocm9tZSBQREYgVmlld2VyLENocm9taXVtIFBERiBWaWV3ZXIsTWljcm9zb2Z0IEVkZ2UgUERGIFZpZXdlcixXZWJLaXQgYnVpbHQtaW4gUERGIiwiY2FudmFzX2NvZGUiOiI1YzYzYWM3MCIsIndlYmdsX3ZlbmRvciI6Ikdvb2dsZSBJbmMuIChJbnRlbCkiLCJ3ZWJnbF9yZW5kZXJlciI6IkFOR0xFIChJbnRlbCwgTWVzYSBJbnRlbChSKSBIRCBHcmFwaGljcyA1MjAgKFNLTCBHVDIpLCBPcGVuR0wgNC42KSIsImF1ZGlvIjoiMTI0LjA0MzQ3NTI3NTE2MDc0IiwicGxhdGZvcm0iOiJMaW51eCB4ODZfNjQiLCJ3ZWJfdGltZXpvbmUiOiJBc2lhL0RoYWthIiwiZGV2aWNlX25hbWUiOiJFZGdlIFYxMTMuMC4wLjAgKExpbnV4KSIsImZpbmdlcnByaW50IjoiOTM5OWYwZDMxNDU1YzliY2VmZGE0OWJiYjNmNDBjYjEiLCJkZXZpY2VfaWQiOiIiLCJyZWxhdGVkX2RldmljZV9pZHMiOiIifQ==',
    'dnt': '1',
    'fvideo-id': 'null',
    'lang': 'en',
    'origin': 'https://www.traderwagon.com',
    'referer': 'https://www.traderwagon.com/en',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.0.0',
    'x-trace-id': 'd3ab6031-0636-432e-940a-be410a809501',
    'x-ui-request-trace': 'd3ab6031-0636-432e-940a-be410a809501'
  },
  body: JSON.stringify({
    'portfolioType': 'NORMAL',
    'available': 0,
    'battleTag': 0,
    'latestTag': 0,
    'isApi': 0,
    'isFavorite': 0,
    'page': 1,
    'rows': 10,
    'sort': 'stLast30DOrders'
  })
});
""")  
=======
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
    encryptedUid_list=list(set(encryptedUid_list))
    extract_position_data(encryptedUid_list)
>>>>>>> abf7a5659227d9e8898f440caa4e7aff0f910ca7