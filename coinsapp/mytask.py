from __future__ import unicode_literals
import ccxt

def my_scheduled_job():
    exchange = ccxt.bxinth ({ 'verbose': True })
    print(exchange.fetch_ticker('ETH/BTC').get('last'))

    # with open('file_to_write', 'w') as f:
    # f.write(exchange.fetch_ticker('ETH/BTC').get('last'))
