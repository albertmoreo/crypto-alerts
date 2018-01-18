import time
import config as cfg
import api_connect as api
import pandas as pd
from stockstats import StockDataFrame as Sdf
from datetime import datetime, timedelta

#Load config
EXCHANGE = cfg._EXCHANGE()
MARKET   = cfg._MARKET()
INTERVAL = cfg._CANDLE_INTERVAL()

#Obtain data from Exchange API
DATA_TICKS = api.getTicks(EXCHANGE,MARKET,INTERVAL)

#Load and struct raw data
CANDLES = []
count = len(DATA_TICKS)
while count > 0:
    print(DATA_TICKS[count-1])
    CANDLES.append(DATA_TICKS[count-1])
    count = count-INTERVAL
print(CANDLES)

#Generate historical data file (stockstats format)
ts = str(int(time.time()))
file = open(ts+'.csv','w')
file.write('date,amount,close,high,low,open,volume\n')
count = len(CANDLES)
while count > 0:
    file.write(CANDLES[count-1]['T']+','+str(CANDLES[count-1]['BV'])+',')
    file.write(str(CANDLES[count-1]['C'])+','+str(CANDLES[count-1]['H'])+','+str(CANDLES[count-1]['L'])+','+str(CANDLES[count-1]['O'])+',')
    file.write(str(CANDLES[count-1]['V'])+'\n')
    count = count-1
file.close()

#Load historical data file
stock = Sdf.retype(pd.read_csv(ts+'.csv'))

#Calculate MACD, MACD-signal and MACD-histogram
MACD =  stock['macd']
MACDS = stock['macds']
MACDH = stock['macdh']
print(MACD)
print(MACDS)
print(MACDH)

def BUY():
    file.write('BUY')
    LAST_ACTION = 'BUY'

def SELL():
    file.write('SELL')
    LAST_ACTION = 'SELL'

def REBUY():
    file.write('REBUY')
    LAST_ACTION = 'BUY'

def NO_ACTION():
    file.write('')


#Save MACD-histogram results and actions in MACDH file
#TODO ACTIONS
LAST_ACTION = ''
file = open('MACDH_'+ts+'.csv','w')
file.write('time;macdh;close;action\n')
count = len(CANDLES)-1
countM = 0
for key in MACDH.keys():
    file.write(key+';'+str(MACDH[key]).replace('.',',')+';'+str(CANDLES[count]['C']).replace('.',',')+';')
    if MACDH[key]>0:
        if MACDH[countM-1]<0:
            BUY()
        if MACDH[countM]<MACDH[countM-1] and LAST_ACTION=='BUY':
            SELL()
        if MACDH[countM]>MACDH[countM-1] and LAST_ACTION=='SELL':
            REBUY()
    else:
        if LAST_ACTION=='BUY':
            SELL()
        else:
            NO_ACTION()
    file.write('\n')
    count = count - 1
    countM = countM + 1
file.close()
