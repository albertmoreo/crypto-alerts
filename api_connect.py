import requests

#Function getTicks for multiple exchanges (Currently only BITTREX available)
def getTicks(exchange,market):
    if exchange == 'BITTREX':
        return bittrex(market)
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


def bittrex(market):
    request = requests.get('https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName='+market+'&tickInterval=hour')
    data = request.json()
    return data['result']
