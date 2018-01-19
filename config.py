#CUSTOMIZE CONFIGURATION
##########################
#EXCHANGE (currently only BITTREX allowed)
EXCHANGE = 'BITTREX'
#MARKET
MARKET = 'BTC-XRP'
#CANDLE INTERVAL (currently only 'day' or 'hour' allowed)
CANDLE_INTERVAL_HOURS = 'hour'
##########################
#FIN CUSTOMIZE CONFIGURATION


def _EXCHANGE():
    return EXCHANGE

def _MARKET():
    return MARKET

def _CANDLE_INTERVAL():
        return 12
