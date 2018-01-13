
import json
import array
import time
import config
import globalvars
import api_connect as api
import pandas as pd
from stockstats import StockDataFrame as Sdf
from datetime import datetime, timedelta

#Global vars
NUMBER_OF_PERIODS = 50
CANDLE_4H = 4

#Obtain data from Bittrex
candles = api.getBittrex("BTC-XRP")

#Read and struct data
DATA = []
count = len(candles)
while count > 0:
    print(candles[count-1])
    DATA.append(candles[count-1])
    count = count-CANDLE_4H
print(DATA)

#Generate CSV - stockstats format
ts = str(int(time.time()))
file = open(ts+'.csv','w')
file.write('date,amount,close,high,low,open,volume\n')
count = len(DATA)
while count > 0:
    file.write(DATA[count-1]['T']+','+str(DATA[count-1]['BV'])+',')
    file.write(str(DATA[count-1]['C'])+','+str(DATA[count-1]['H'])+','+str(DATA[count-1]['L'])+','+str(DATA[count-1]['O'])+',')
    file.write(str(DATA[count-1]['V'])+'\n')
    count = count-1
file.close()

#Read CSV
stock = Sdf.retype(pd.read_csv(ts+'.csv'))

#Calculate MACD, MACDsignal and Histogram
MACD =  stock['macd']
MACDS = stock['macds']
MACDH = stock['macdh']
print(MACD)
print(MACDS)
print(MACDH)

#Save Histogram results
file = open('MACDH_'+ts+'.csv','w')
file.write('time,macdh\n')
for key in MACDH.keys():
    file.write(key+','+str(MACDH[key])+'\n')
file.close()
