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

global LAST_ACTION
LAST_ACTION = 'R'

def BUY():
    file.write('BUY')
    LAST_ACTION = 'BUY'
    return LAST_ACTION

def SELL():
    file.write('SELL')
    LAST_ACTION = 'SELL'
    return LAST_ACTION

def REBUY():
    file.write('REBUY')
    LAST_ACTION = 'BUY'
    return LAST_ACTION

def NO_ACTION():
    file.write('')
    return LAST_ACTION

#Save MACD-histogram results and actions in MACDH file
#TODO ACTIONS

file = open('MACDH_'+ts+'.csv','w')
file.write('time;macdh;close;action\n')
count = len(CANDLES)-1
countM = 0
for key in MACDH.keys():
    print(LAST_ACTION)
    file.write(key+';'+str(MACDH[key]).replace('.',',')+';'+str(CANDLES[count]['C']).replace('.',',')+';')
    #si histograma es positivo
    if MACDH[countM]>0:
        #histograma anterior es negativo
        if (MACDH[countM-1]<0) and (LAST_ACTION!='BUY'):
            #BUY()
            file.write('BUY')
            LAST_ACTION='BUY'
        #histograma es menor que el anterior y ha comprado
        elif (MACDH[countM]<MACDH[countM-1]) and (LAST_ACTION=='BUY'):
            #SELL()
            file.write('SELL')
            LAST_ACTION = 'SELL'
        #Los 2 ultimos histogramas han subido y ha vendido
        elif (MACDH[countM]>MACDH[countM-1]) and (MACDH[countM-1]>MACDH[countM-2]) and (LAST_ACTION=='SELL'):
            #REBUY()
            file.write('REBUY')
            LAST_ACTION = 'BUY'
        else:
            #NO_ACTION()
            file.write('')
    #si histograma es negativo
    else:
        #los 3 ultimos histogramas han subido y ha vendido
        if (MACDH[countM]>MACDH[countM-1]) and (MACDH[countM-1]>MACDH[countM-2]) and (LAST_ACTION=='SELL'):
            #BUY()
            file.write('BUY')
            LAST_ACTION='BUY'
        else:
            file.write('')
    file.write('\n')
    count = count - 1
    countM = countM + 1
file.close()









'''
INITIAL ALGORITHM CON CANDLES DE 24H Y X16 EN 2017 BTC-XRP
file = open('MACDH_'+ts+'.csv','w')
file.write('time;macdh;close;action\n')
count = len(CANDLES)-1
countM = 0
for key in MACDH.keys():
    print(LAST_ACTION)
    file.write(key+';'+str(MACDH[key]).replace('.',',')+';'+str(CANDLES[count]['C']).replace('.',',')+';')
    if MACDH[key]>0:
        if MACDH[countM-1]<0:
            #BUY()
            file.write('BUY')
            LAST_ACTION='BUY'
        elif (MACDH[countM]<MACDH[countM-1]) and (LAST_ACTION=='BUY'):
            #SELL()
            file.write('SELL')
            LAST_ACTION = 'SELL'
        elif (MACDH[countM]>MACDH[countM-1]) and (LAST_ACTION=='SELL'):
            #REBUY()
            file.write('REBUY')
            LAST_ACTION = 'BUY'
        else:
            #NO_ACTION()
            file.write('')
    else:
        if LAST_ACTION=='BUY':
            #SELL()
            file.write('SELL')
            LAST_ACTION = 'SELL'
        else:
            #NO_ACTION()
            file.write('')
    file.write('\n')
    count = count - 1
    countM = countM + 1
file.close()
'''
