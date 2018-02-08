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
btc_list=filter(lambda k: '/BTC' in k, list)


@task()
def remove_old_values():
    t=datetime.now()-timedelta(hours=5)
    c=Value.objects.filter(reqtime__lt=t)
    c.delete()


@task()

def update_markers():
    for market in btc_list:
        c=Coin.objects.update_or_create(coin_name=market)

@task()
def get_coin_data():
    market_data=exchange.fetch_tickers()
    for ticker in btc_list:
        price = market_data[ticker]['info']['lastPrice']
        price_change = market_data[ticker]['info']['priceChange']
        percent_change = market_data[ticker]['change']
        basevolume = market_data[ticker]['baseVolume']

        d=datetime.now()
        d=d.replace(tzinfo=None)
        c=Coin.objects.get(coin_name=ticker)
        v=Value.objects.create(coin=c, coin_value=price, reqtime=datetime.now(),
        coin_basevolume=basevolume)
        t=datetime.now()-timedelta(hours=1)


        #v=Coinproperties.objects.update_or_create (coin=c, defaults={'coin_perchange':percent_change,'coin_change':price_change})
