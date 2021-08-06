# -*- coding: utf-8 -*-
"""
Created on Sat May  8 23:55:36 2021

@author: tooru

https://www.binance.com/en/my/settings/api-management
https://algotrading101.com/learn/binance-python-api-guide/


##### Total Crypto: 111 - Some failed to export (interval = 1d)
######### Total run time (first) ###########
0:02:34.187878

##### Total Crypto: 111 - Some failed to export (interval = 1h)
######### Total run time (first) ###########
0:25:15.880044


"""

import os
from binance.client import Client
from datetime import datetime
import pandas as pd

startTime = datetime.now()
print('######### Start of Script ###########')
print(datetime.now() - startTime)

os.chdir('Working directory path')
download_folder = r'Download folder path'

'''
    1. Credentials API - BINANCE
'''
api_key='Insert API KEY'
api_secret='Insert API Secret'

api_key, api_secret

client = Client(api_key, api_secret)

'''
    2. Get Historical Crypto Data in csv
'''

# Crypto list to retrieve data
crypto_list = pd.read_csv('crypto_list.csv')
crypto_list = crypto_list['crypto_list'].tolist()

# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
interval = '1h'

a = 0
for crypto in crypto_list:
    a = a + 1
    print('##### Crypto sec: ' + str(a))  
    
    try:
        # get timestamp of earliest date data is available
        timestamp = client._get_earliest_valid_timestamp(crypto, interval)
        
        # request historical data
        bars = client.get_historical_klines(crypto, interval, timestamp, limit=1000)
        
        # keep date, open, high, low, close
        for line in bars:
            del line[5:]
        
        # create a Pandas DataFrame and export to CSV
        df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
        df.date = df.date.apply(int)
        
        df['timestamp'] = pd.to_datetime(df['date']/1000, unit='s')
        df['crypto_name'] = crypto
                
        # export DataFrame to csv
        file_csv = download_folder + 'historical_' + str(interval) + "_" + str(crypto) + '.csv'
        df.to_csv(file_csv)
        
        print('Success: ' + str(crypto))
        print(datetime.now() - startTime)
        
    except:
        print('Failed: ' + str(crypto))
        print(datetime.now() - startTime)

print('######### End of Script ###########')
print(datetime.now() - startTime)