from __future__ import absolute_import, unicode_literals
import ccxt
from datetime import datetime, timedelta
from celery import task
from coinsapp.models import Coin, Value, Coinproperties

#connect to an exchange
exchange = ccxt.binance  ({ 'verbose': True })
exchange.load_markets()
# Get all currencies vs BTC
list=exchange.symbols
markers=set(list)

symbols=[]
for symbol in markers:
    symbols.append(symbol.split('/')[0])

@task()
def remove_old_values():
    t=datetime.now()-timedelta(hours=5)
    c=Value.objects.filter(reqtime__lt=t)
    c.delete()


@task()
def update_markers():
    for ticker in symbols:
    c=Coin.objects.update_or_create(coin_name=ticker)

@task()
def get_coin_data():
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
    market=r.json()
    for ticker in market:
        if ticker['symbol'] in symbols:

            price = ticker['price_usd']
            price_change = ticker['percent_change_1h']
            basevolume = ticker['market_cap_usd']

            d=datetime.now()
            d=d.replace(tzinfo=None)
            c=Coin.objects.get(coin_name=ticker)
            v=Value.objects.create(coin=c, coin_value=price, reqtime=datetime.now(),coin_basevolume=basevolume)

        p=Coinproperties.objects.update_or_create (coin=c, defaults={'coin_perchange':price_change,'coin_change':price_change})
