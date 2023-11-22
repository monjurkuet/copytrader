from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import pandas as pd
from collections import defaultdict
import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder

# myql ssh tunnel
ssh_host = '161.97.97.183'
ssh_username = 'root'
ssh_password = '$C0NTaB0vps8765%%$#'
database_username = 'root'
database_password = '$C0NTaB0vps8765%%$#'
database_name = 'exchangetrading'
localhost = '127.0.0.1'

def open_ssh_tunnel(verbose=False):
    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    global tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username = ssh_username,
        ssh_password = ssh_password,
        remote_bind_address = ('127.0.0.1', 3306)
    )
    tunnel.start()

def mysql_connect():
    global connection
    connection = pymysql.connect(
        host='127.0.0.1',
        user=database_username,
        passwd=database_password,
        db=database_name,
        port=tunnel.local_bind_port
    )

open_ssh_tunnel()
mysql_connect()

client = MongoClient('mongodb://myUserAdmin:%24C0NTaB0vps8765%25%25%24%23@161.97.97.183:27017/?authMechanism=DEFAULT')
db = client['exchanges']
collection = db['traderwagonSearch']

end = datetime.now()
start = end- timedelta(days = 1)

traderwagonPositions = db['traderwagonPositions'].find({"created_at": {"$gte": start, "$lt": end}})
traderwagonPositions=[data for data in db['traderwagonPositions'].find()]
for i in traderwagonPositions:
    i['positiondata'] = i.pop('data')
traderwagonSearch = db['traderwagonSearch'].find({"created_at": {"$gte": start, "$lt": end}})
traderwagonSearch=[data for data in db['traderwagonSearch'].find()]
for i in traderwagonSearch:
    i['performancedata'] = i.pop('data')

d = defaultdict(dict)
for item in traderwagonSearch + traderwagonPositions:
    d[item['portfolioId']].update(item)

dd=[i for i in list(d.values()) if i!={}]
final=[]
for item in dd:
    try:
        if item['positiondata']!=[]:
            print(item['positiondata'])
            final.append(item)
    except:
        pass

for each_item in final:
    portfolioId=each_item['portfolioId']
    last7DRoi=each_item['performancedata']['last7DRoi']
    last30DRoi=each_item['performancedata']['last30DRoi']
    last90DRoi=each_item['performancedata']['last90DRoi']
    for each_position in each_item['positiondata']:
        symbol=each_position['symbol']
        entryPrice=each_position['entryPrice']
        positionAmount=each_position['positionAmount']
        positionSide=each_position['positionSide']
        cursor = connection.cursor() 
        sql_insert_with_param = """REPLACE INTO traderwagon
                            (portfolioId,symbol,entryPrice,positionAmount,positionSide,last7DRoi,last30DRoi,last90DRoi) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""" 
        data_tuple = (portfolioId,symbol,entryPrice,positionAmount,positionSide,last7DRoi,last30DRoi,last90DRoi)
        cursor.execute(sql_insert_with_param, data_tuple)
        connection.commit() 
        print(data_tuple)
        

