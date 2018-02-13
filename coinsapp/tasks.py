from __future__ import absolute_import, unicode_literals
import ccxt
from datetime import datetime, timedelta
from celery import task
from coinsapp.models import Coin, Value, Coinproperties
import requests

#connect to an exchange
exchange = ccxt.binance  ({ 'verbose': True })
exchange.load_markets()

binance_symbols=exchange.symbols
binance_symbols.remove('123/456')
binance_symbols.remove('CHAT/BTC')
binance_symbols.remove('CHAT/ETH')
binance_symbols.remove('BCD/BTC')
binance_symbols.remove('BCD/ETH')

binance_symbols_clean=[]
for ticker in binance_symbols:
     binance_symbols_clean.append(ticker.split('/')[0])

r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
coinmarketcap_data=r.json()
coinmarkectcap_symbols=[]
coinmarkectcap_symbols=[c['symbol'] for c in coinmarketcap_data]

my_symbols=[]
my_symbols=[s for s in binance_symbols_clean if s in coinmarkectcap_symbols]



@task()
def remove_old_values():
    t=datetime.now()-timedelta(hours=5)
    c=Value.objects.filter(reqtime__lt=t)
    c.delete()


@task()
def update_markers():
    coins=Coin.objects.all().values('coin_name')
    coins_to_delete = [c['coin_name'] for c in coins if c['coin_name'] not in my_symbols]
    print(my_symbols)
    print(coins_to_delete)

    for ticker in coins_to_delete:
        coin=Coin.objects.get(coin_name=ticker)
        coin.delete()
        print(ticker)

    for ticker in  my_symbols:
        c=Coin.objects.update_or_create(coin_name=ticker)


@task()
def get_coin_data():
    t=datetime.now()-timedelta(hours=3)
    for ticker in coinmarketcap_data:
        if ticker['symbol'] in my_symbols:

            c=Coin.objects.get(coin_name=ticker['symbol'])
            price = ticker['price_usd']
            price_change = ticker['percent_change_1h']
            basevolume = ticker['market_cap_usd']

            volume=c.value_set.filter(reqtime__gt=t).order_by('reqtime')
            Last=volume.last().coin_basevolume
            First=volume.first().coin_basevolume
            volume_change=(Last-First)/First*100

            if (price is not None) and (price_change is not None) and (basevolume is not None):

                d=datetime.now()
                d=d.replace(tzinfo=None)
                v=Value.objects.create(coin=c, coin_value=price, reqtime=datetime.now(),coin_basevolume=basevolume)

                p=Coinproperties.objects.update_or_create (coin=c, defaults={'coin_perchange':price_change,'volume_change':volume_change})
            else: pass
