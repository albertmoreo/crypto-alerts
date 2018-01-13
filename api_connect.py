import requests

def getBittrex(pair):
    request = requests.get('https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName='+pair+'&tickInterval=hour')
    data = request.json()
    #candles = data['result']
    return data['result']
