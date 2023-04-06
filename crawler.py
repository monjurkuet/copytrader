import time,re,random
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import mysql.connector
import json

def tor_browser():
   options = uc.ChromeOptions() 
   options.add_argument(f'--proxy-server=socks5://127.0.0.1:9050')
   #options.user_data_dir = "/home/chromeprofileforbots"  
   #return uc.Chrome(user_data_dir="/home/chromeprofileforbots",options=options,version_main=109)  
   return uc.Chrome(user_data_dir="/home/copytraderscrapingprofile",browser_executable_path='/usr/bin/brave-browser',headless=False,version_main=111,options=options)      

def insert_details(company,rating,category,phone,website,claim_status,latitude,longitude,gmaps_url):
    connection = mysql.connector.connect(
                                host='localhost', 
                                #host='161.97.97.183',
                                database='google_maps',
                                user='root', 
                                password='$C0NTaB0vps8765%%$#', 
                                port=3306
                                ,auth_plugin='caching_sha2_password')
    cursor = connection.cursor()  
    sql_insert_with_param = """INSERT IGNORE INTO gmaps_details
                            (company,rating,category,phone,website,claim_status,latitude,longitude,gmaps_url) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    val = (company,rating,category,phone,website,claim_status,latitude,longitude,gmaps_url)
    cursor.execute(sql_insert_with_param , val)
    connection.commit() 
    print(val)

def update_gmaps_links(gmaps_url):
    connection = mysql.connector.connect(
                                host='localhost', 
                                #host='161.97.97.183',
                                database='google_maps',
                                user='root', 
                                password='$C0NTaB0vps8765%%$#', 
                                port=3306
                                ,auth_plugin='caching_sha2_password')
    cursor = connection.cursor()  
    sql = "UPDATE gmaps_links SET processed=1 WHERE gmaps_url = %s"
    val = (gmaps_url,)
    cursor.execute(sql, val)
    connection.commit() 
    print(val)



if __name__ == "__main__":
    gmaps_urls=geturls()
    extract_gmaps_details(gmaps_urls)       