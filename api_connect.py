import requests

#Function getTicks for multiple exchanges (Currently only BITTREX available)
def getTicks(exchange,market,interval):
    if exchange == 'BITTREX':
        return bittrex(market,interval)
    elif exchange == 'BINANCE':
        return null
    elif exchange == 'BITFINEX':
        return null
    elif exchange == 'BITSTAMP':
        return null
    elif exchange == 'POLONIEX':
        return null
    else:
        return null


def bittrex(market,interval):
    #if interval==24: interval = 'day' else: interval = 'hour'
    #tickInterval: ['oneMin','fiveMin','thirtyMin','hour,'day']
    request = requests.get('https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName='+market+'&tickInterval=hour')
    data = request.json()
    return data['result']
